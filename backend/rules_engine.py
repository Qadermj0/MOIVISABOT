def normalize_text(value):
    text = str(value or "").strip().lower()
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ى", "ي").replace("ة", "ه")
    text = text.replace("ال", "")
    return text


def extract_first_visa_data(api_response):
    data = api_response.get("result", {}).get("data", [])
    if not data:
        return None
    return data[0]


def build_visa_types_list(api_response):
    data = api_response.get("result", {}).get("data", [])

    visa_types = []

    for item in data:
        visa_types.append({
            "visa_type": item.get("visaType"),
            "visa_name": item.get("typeOfVisa") or "الاسم غير متوفر في البيانات"
        })

    return visa_types


def get_age_rule(rules: dict):
    age = rules.get("age") or {}
    if isinstance(age, list) and age:
        age = age[0]
    if not isinstance(age, dict):
        return None, None

    return age.get("minAge"), age.get("maxAge")


def first_rule_list(*values):
    for value in values:
        if isinstance(value, list) and value:
            return value
    return []


def occupation_matches(user_occupation: str, occupations: list):
    if not user_occupation:
        return False, None

    user_text = normalize_text(user_occupation)

    for occ in occupations:
        if not isinstance(occ, dict):
            continue

        if occ.get("allowed", True) is False:
            continue

        names = [
            occ.get("ArabicDescription"),
            occ.get("occupationNameAr"),
            occ.get("DescriptionEn"),
            occ.get("occupationNameEn")
        ]

        for name in names:
            if not name:
                continue

            name_norm = normalize_text(name)

            if user_text in name_norm or name_norm in user_text:
                return True, name

            if user_text.rstrip("ونين") in name_norm:
                return True, name

    return False, None


def relationship_matches(user_relationship: str, relationships: list):
    if not user_relationship:
        return False, None

    user_text = normalize_text(user_relationship)

    for rel in relationships:
        if not isinstance(rel, dict):
            continue

        if rel.get("allowed", True) is False:
            continue

        names = [
            rel.get("relationNameAr"),
            rel.get("relationNameEn"),
            rel.get("arabicDescription")
        ]

        for name in names:
            if not name:
                continue

            name_norm = normalize_text(name)

            if user_text in name_norm or name_norm in user_text:
                return True, name

    return False, None


def check_eligibility(visa_data, user_data):
    if not visa_data:
        return {
            "status": "NOT_APPROVED",
            "reason": "Visa type is not available for this country.",
            "checks": [],
            "missing_fields": []
        }

    country_rule = visa_data.get("countryRule", {}) or {}
    general_rules = visa_data.get("generalRules", {}) or {}
    rules = country_rule.get("rules", {}) or {}

    result = {
        "status": "NEED_MORE_INFO",
        "visa_type": visa_data.get("visaType"),
        "visa_name": visa_data.get("typeOfVisa") or "الاسم غير متوفر في البيانات",
        "country": country_rule.get("ArabicDescription") or country_rule.get("LatinDescription"),
        "country_ocr_code": country_rule.get("OcrCode"),
        "checks": [],
        "missing_fields": [],
        "details": {
            "age_rule": None,
            "occupations": [],
            "relationships_count": 0
        }
    }

    age = user_data.get("age")
    occupation = user_data.get("occupation")
    gender = user_data.get("gender")
    relationship = user_data.get("relationship")

    min_age, max_age = get_age_rule(rules)
    if not min_age and not max_age:
        min_age, max_age = get_age_rule(general_rules)

    result["details"]["age_rule"] = {
        "min_age": min_age,
        "max_age": max_age
    }

    if min_age or max_age:
        if age is None:
            result["missing_fields"].append("age")
        else:
            try:
                age_int = int(age)

                if min_age and age_int < int(min_age):
                    result["checks"].append({
                        "passed": False,
                        "field": "age",
                        "message": f"Age {age_int} is below minimum age {min_age}."
                    })
                elif max_age and age_int > int(max_age):
                    result["checks"].append({
                        "passed": False,
                        "field": "age",
                        "message": f"Age {age_int} is above maximum age {max_age}."
                    })
                else:
                    result["checks"].append({
                        "passed": True,
                        "field": "age",
                        "message": f"Age {age_int} is within allowed range {min_age}-{max_age}."
                    })
            except Exception:
                result["missing_fields"].append("valid_age")

    gender_rule = rules.get("gender") or general_rules.get("gender") or []
    if gender and gender_rule:
        if normalize_text(gender) in normalize_text(gender_rule):
            result["checks"].append({
                "passed": False,
                "field": "gender",
                "message": "Gender is restricted for this visa."
            })

    country_occupations = first_rule_list(
        rules.get("occupations"),
        rules.get("occupation"),
        rules.get("newOccupation"),
    )
    general_occupations = first_rule_list(
        general_rules.get("occupations"),
        general_rules.get("occupation"),
        general_rules.get("newOccupation"),
    )

    occupation_rules = country_occupations if country_occupations else general_occupations

    result["details"]["occupations"] = [
        o.get("ArabicDescription") or o.get("occupationNameAr") or o.get("DescriptionEn") or o.get("occupationNameEn")
        for o in occupation_rules
        if isinstance(o, dict)
    ]

    if occupation_rules:
        if not occupation:
            result["missing_fields"].append("occupation")
        else:
            matched, matched_name = occupation_matches(occupation, occupation_rules)

            result["checks"].append({
                "passed": matched,
                "field": "occupation",
                "message": "Occupation is allowed." if matched else "Occupation is not listed as allowed.",
                "matched_value": matched_name
            })

    relationship_rules = rules.get("relationship") or general_rules.get("relationship") or []
    result["details"]["relationships_count"] = len(relationship_rules)

    if relationship:
        matched_rel, matched_rel_name = relationship_matches(relationship, relationship_rules)

        result["checks"].append({
            "passed": matched_rel,
            "field": "relationship",
            "message": "Relationship is allowed." if matched_rel else "Relationship is not allowed.",
            "matched_value": matched_rel_name
        })

    failed = [c for c in result["checks"] if c["passed"] is False]

    if failed:
        result["status"] = "NOT_APPROVED"
    elif result["missing_fields"]:
        result["status"] = "NEED_MORE_INFO"
    else:
        result["status"] = "APPROVED"

    return result
