import re


VISA_TYPE_NAMES_EN = {
    1: "Government work entry visa",
    2: "Private sector work entry visa",
    3: "Domestic worker entry visa",
    6: "Study entry visa",
    7: "Medical treatment entry visa",
    8: "Commercial visit entry visa",
    9: "Government visit entry visa",
    10: "Family visit entry visa",
    11: "Embassy visit entry visa",
    14: "Multiple-return visa",
    16: "Tourism entry visa",
    19: "Return visa",
    20: "Special entry visa",
}

OCCUPATION_VARIANTS = {
    "نائب": ["نائب", "نواب", "نائبه", "نائبة"],
    "عضو مجلس": ["عضو مجلس", "عضو مجالس", "اعضاء مجلس", "اعضاء مجالس", "مجالس"],
    "عضو المجالس": ["عضو مجلس", "عضو مجالس", "اعضاء مجلس", "اعضاء مجالس", "مجالس"],
    "رئيس": ["رئيس", "رؤساء", "رئيسه", "رئيسة"],
    "مساعد": ["مساعد", "مساعدين", "مساعديهم"],
    "pilot": ["pilot", "طيار"],
    "طيار": ["طيار", "pilot"],
}


def normalize_text(value):
    text = str(value or "").strip().lower()
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ؤ", "و").replace("ئ", "ي")
    text = text.replace("ى", "ي").replace("ة", "ه")
    text = re.sub(r"[^\w\s\u0600-\u06ff]", " ", text)
    text = re.sub(r"\bال", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def occupation_search_terms(user_occupation: str):
    normalized = normalize_text(user_occupation)
    terms = {normalized}

    for source, variants in OCCUPATION_VARIANTS.items():
        source_norm = normalize_text(source)
        if source_norm and (source_norm in normalized or normalized in source_norm):
            terms.update(normalize_text(variant) for variant in variants)

    if "نائب" in normalized:
        terms.add("نواب")

    if "عضو" in normalized and "مجلس" in normalized:
        terms.update(["اعضاء مجالس", "اعضاء مجلس", "مجالس"])

    return [term for term in terms if term]


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
            "visa_name": item.get("typeOfVisa") or "الاسم غير متوفر في البيانات",
            "visa_name_en": VISA_TYPE_NAMES_EN.get(item.get("visaType"), "Name not available in the data"),
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


def get_occupation_rules(visa_data):
    if not visa_data:
        return []

    country_rule = visa_data.get("countryRule", {}) or {}
    general_rules = visa_data.get("generalRules", {}) or {}
    rules = country_rule.get("rules", {}) or {}

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

    return country_occupations if country_occupations else general_occupations


def build_occupation_list(visa_data):
    occupations = []
    seen = set()

    for occupation in get_occupation_rules(visa_data):
        if not isinstance(occupation, dict):
            continue

        if occupation.get("allowed", True) is False:
            continue

        name_ar = occupation.get("occupationNameAr") or occupation.get("ArabicDescription") or ""
        name_en = occupation.get("occupationNameEn") or occupation.get("DescriptionEn") or ""
        value = name_ar or name_en

        if not value:
            continue

        label = value
        if name_ar and name_en and normalize_text(name_ar) != normalize_text(name_en):
            label = f"{name_ar} - {name_en}"

        key = normalize_text(value)
        if key in seen:
            continue

        seen.add(key)
        occupations.append({
            "value": value,
            "label": label,
            "occupation_name_ar": name_ar,
            "occupation_name_en": name_en,
        })

    return occupations


def get_relationship_rules(visa_data):
    if not visa_data:
        return []

    country_rule = visa_data.get("countryRule", {}) or {}
    general_rules = visa_data.get("generalRules", {}) or {}
    rules = country_rule.get("rules", {}) or {}

    return first_rule_list(
        rules.get("relationship"),
        general_rules.get("relationship"),
    )


def build_relationship_list(visa_data):
    relationships = []
    seen = set()

    for relationship in get_relationship_rules(visa_data):
        if not isinstance(relationship, dict):
            continue

        if relationship.get("allowed", True) is False:
            continue

        name_ar = relationship.get("relationNameAr") or relationship.get("arabicDescription") or relationship.get("ArabicDescription") or ""
        name_en = relationship.get("relationNameEn") or relationship.get("DescriptionEn") or ""
        value = name_ar or name_en

        if not value:
            continue

        label = value
        if name_ar and name_en and normalize_text(name_ar) != normalize_text(name_en):
            label = f"{name_ar} - {name_en}"

        key = normalize_text(value)
        if key in seen:
            continue

        seen.add(key)
        relationships.append({
            "value": value,
            "label": label,
            "relation_code": relationship.get("relationCode"),
            "relation_name_ar": name_ar,
            "relation_name_en": name_en,
        })

    return relationships


def occupation_matches(user_occupation: str, occupations: list):
    if not user_occupation:
        return False, None

    user_terms = occupation_search_terms(user_occupation)

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

            for user_text in user_terms:
                if user_text in name_norm or name_norm in user_text:
                    return True, name

                if user_text.rstrip("ونين") in name_norm:
                    return True, name

    return False, None


def normalize_relationship_values(value):
    if value is None:
        return []

    if isinstance(value, (list, tuple, set)):
        values = value
    else:
        values = [value]

    normalized = []
    seen = set()

    for item in values:
        text = str(item or "").strip()
        if not text:
            continue

        key = normalize_text(text)
        if key in seen:
            continue

        seen.add(key)
        normalized.append(text)

    return normalized


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
        "visa_name_en": VISA_TYPE_NAMES_EN.get(visa_data.get("visaType"), "Name not available in the data"),
        "country": country_rule.get("ArabicDescription") or country_rule.get("LatinDescription"),
        "country_ar": country_rule.get("ArabicDescription"),
        "country_en": country_rule.get("LatinDescription"),
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

    occupation_rules = get_occupation_rules(visa_data)

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

    relationship_rules = get_relationship_rules(visa_data)
    result["details"]["relationships_count"] = len(relationship_rules)

    for relationship_value in normalize_relationship_values(relationship):
        matched_rel, matched_rel_name = relationship_matches(relationship_value, relationship_rules)

        result["checks"].append({
            "passed": matched_rel,
            "field": "relationship",
            "message": f"Relationship {relationship_value} is allowed." if matched_rel else f"Relationship {relationship_value} is not allowed.",
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
