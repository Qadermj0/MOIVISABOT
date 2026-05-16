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
    "real estate": ["real estate", "real state", "real estate owner", "real estate owners", "property owner", "property owners", "property investor", "property investors", "own real estate", "owns real estate", "have real estate", "has real estate", "own property", "owns property", "have property", "has property"],
    "real state": ["real state", "real estate", "real estate owner", "real estate owners", "property owner", "property owners", "own property", "have property"],
    "real estate owner": ["real estate owner", "real estate owners", "real estate", "real state", "property owner", "property owners", "property investor", "property investors", "own real estate", "have real estate", "own property", "have property"],
    "property owner": ["property owner", "property owners", "real estate owner", "real estate owners", "real estate", "real state", "own property", "have property"],
    "نائب": ["نائب", "نواب", "نائبه", "نائبة"],
    "عضو مجلس": ["عضو مجلس", "عضو مجالس", "اعضاء مجلس", "اعضاء مجالس", "مجالس"],
    "عضو المجالس": ["عضو مجلس", "عضو مجالس", "اعضاء مجلس", "اعضاء مجالس", "مجالس"],
    "رئيس": ["رئيس", "رؤساء", "رئيسه", "رئيسة"],
    "مساعد": ["مساعد", "مساعدين", "مساعديهم"],
    "president": ["president", "presidents", "chairman", "chairperson", "head", "heads", "رئيس", "رؤساء", "رئيسه", "رئيسة"],
    "member of council": ["member of council", "member of councils", "members of council", "members of councils", "council member", "council members", "عضو مجلس", "عضو مجالس", "اعضاء مجلس", "اعضاء مجالس", "مجالس"],
    "council member": ["council member", "council members", "member of council", "member of councils", "members of council", "members of councils", "عضو مجلس", "عضو مجالس", "اعضاء مجلس", "اعضاء مجالس", "مجالس"],
    "lawyer": ["lawyer", "lawyers", "attorney", "attorneys", "محامي", "محاميه", "محامية", "محامون", "المحامون"],
    "محامي": ["محامي", "محاميه", "محامية", "محامون", "المحامون", "lawyer", "lawyers", "attorney", "attorneys"],
    "judge": ["judge", "judges", "قاضي", "قاضيه", "قاضية", "قضاة", "قضاه", "القضاة", "القضاه", "اعضاء النيابه", "اعضاء النيابة"],
    "قاضي": ["قاضي", "قاضيه", "قاضية", "قضاة", "قضاه", "القضاة", "القضاه", "judge", "judges"],
    "software engineer": ["software engineer", "software eng", "software developer", "developer", "programmer", "مهندس برمجيات", "مهندسه برمجيات", "مهندسة برمجيات", "مطور برمجيات", "مبرمج", "نظم المعلومات", "الشبكات", "الحاسوب", "الحاسب", "المواقع الالكترونيه", "المواقع الإلكترونية", "information systems", "networks", "computers", "electronic websites"],
    "software eng": ["software eng", "software engineer", "software developer", "developer", "programmer", "مهندس برمجيات", "مهندسه برمجيات", "مهندسة برمجيات", "مطور برمجيات", "مبرمج", "نظم المعلومات", "الشبكات", "الحاسوب", "الحاسب", "المواقع الالكترونيه", "المواقع الإلكترونية", "information systems", "networks", "computers", "electronic websites"],
    "مهندس برمجيات": ["مهندس برمجيات", "مهندسه برمجيات", "مهندسة برمجيات", "مطور برمجيات", "مبرمج", "software engineer", "software eng", "software developer", "developer", "programmer", "نظم المعلومات", "الشبكات", "الحاسوب", "الحاسب", "المواقع الالكترونيه", "المواقع الإلكترونية", "information systems", "networks", "computers", "electronic websites"],
    "full stack developer": ["full stack developer", "full-stack developer", "frontend developer", "front end developer", "backend developer", "back end developer", "software developer", "software engineer", "developer", "programmer", "مهندس برمجيات", "مطور برمجيات", "مبرمج", "نظم المعلومات", "الشبكات", "الحاسوب", "المواقع الالكترونيه", "information systems", "networks", "computers", "electronic websites"],
    "devops engineer": ["devops engineer", "dev ops engineer", "cloud engineer", "site reliability engineer", "sre", "systems engineer", "software engineer", "engineer", "مهندس برمجيات", "مهندس نظم", "ديف اوبس", "ديف أوبس", "نظم المعلومات", "الشبكات", "الحاسوب", "information systems", "networks", "computers"],
    "data scientist": ["data scientist", "data analyst", "machine learning engineer", "ai engineer", "analytics engineer", "عالم بيانات", "محلل بيانات", "مهندس بيانات", "نظم المعلومات", "الحاسوب", "information systems", "computers"],
    "information systems": ["information systems", "it professional", "it specialist", "systems analyst", "نظم المعلومات", "اخصائي نظم معلومات", "أخصائي نظم معلومات", "الشبكات", "الحاسوب", "computers", "networks", "electronic websites"],
    "نظم معلومات": ["نظم معلومات", "نظم المعلومات", "اخصائي نظم معلومات", "أخصائي نظم معلومات", "information systems", "it professional", "it specialist", "systems analyst", "الشبكات", "الحاسوب", "computers", "networks", "electronic websites"],
    "programmer": ["programmer", "programmers", "software programmer", "software developer", "software engineer", "software eng", "developer", "مبرمج", "مبرمج برمجيات", "مطور برمجيات", "مهندس برمجيات", "نظم المعلومات", "الشبكات", "الحاسوب", "الحاسب", "المواقع الالكترونيه", "المواقع الإلكترونية", "information systems", "networks", "computers", "electronic websites"],
    "software programmer": ["software programmer", "programmer", "programmers", "software developer", "software engineer", "software eng", "developer", "مبرمج", "مبرمج برمجيات", "مطور برمجيات", "مهندس برمجيات", "نظم المعلومات", "الشبكات", "الحاسوب", "الحاسب", "المواقع الالكترونيه", "المواقع الإلكترونية", "information systems", "networks", "computers", "electronic websites"],
    "مبرمج": ["مبرمج", "مبرمج برمجيات", "مطور برمجيات", "مهندس برمجيات", "programmer", "programmers", "software programmer", "software developer", "software engineer", "software eng", "developer", "نظم المعلومات", "الشبكات", "الحاسوب", "الحاسب", "المواقع الالكترونيه", "المواقع الإلكترونية", "information systems", "networks", "computers", "electronic websites"],
    "cyber security": ["cyber security", "cybersecurity", "امن سيبراني", "الأمن السيبراني", "خبير امن سيبراني", "خبير أمن سيبراني", "نظم المعلومات", "الشبكات", "الحاسوب", "information systems", "networks", "computers"],
    "pharmacist": ["pharmacist", "pharmacists", "pharmacy", "صيدلي", "صيدليه", "صيدلية", "صيدلاني", "صيدلانيه", "صيدلانية", "صيادله", "صيادلة", "الصيادله", "الصيادلة"],
    "صيدلي": ["صيدلي", "صيدليه", "صيدلية", "صيدلاني", "صيدلانيه", "صيدلانية", "صيادله", "صيادلة", "الصيادله", "الصيادلة", "pharmacist", "pharmacists", "pharmacy"],
    "صيدلاني": ["صيدلي", "صيدليه", "صيدلية", "صيدلاني", "صيدلانيه", "صيدلانية", "صيادله", "صيادلة", "الصيادله", "الصيادلة", "pharmacist", "pharmacists", "pharmacy"],
    "professor": ["professor", "professors", "استاذ", "استاذه", "استاذة", "اساتذه", "اساتذة", "استاذ جامعي", "اساتذه جامعيون", "الاساتذة الجامعيون"],
    "استاذ": ["استاذ", "استاذه", "استاذة", "اساتذه", "اساتذة", "استاذ جامعي", "اساتذه جامعيون", "الاساتذة الجامعيون", "professor", "professors"],
    "doctor": ["doctor", "doctors", "physician", "physicians", "medical doctor", "دكتور", "دكتوره", "دكتورة", "طبيب", "طبيبه", "طبيبة", "الأطباء", "الاطباء"],
    "دكتور": ["دكتور", "دكتوره", "دكتورة", "طبيب", "طبيبه", "طبيبة", "doctor", "doctors", "physician", "physicians", "الأطباء", "الاطباء"],
    "pilot": ["pilot", "pilots", "طيار", "طياره", "طيارة", "طيارون", "الطيارون"],
    "طيار": ["طيار", "طياره", "طيارة", "طيارون", "الطيارون", "pilot", "pilots"],
    "ceo": ["ceo", "chief executive officer", "chief executive", "executive director", "president", "chairman", "general manager", "manager", "رئيس تنفيذي", "مدير تنفيذي", "رئيس", "مدير عام", "الرؤساء", "المدراء"],
    "hr specialist": ["hr specialist", "human resources specialist", "human resource specialist", "specialist", "اخصائي موارد بشرية", "أخصائي موارد بشرية", "اختصاصي موارد بشرية", "اختصاصي", "اخصائي", "أخصائي"],
    "pr manager": ["pr manager", "public relations manager", "relations manager", "manager", "مدير علاقات عامة", "مدير", "مدراء", "general manager"],
    "business owner": ["business owner", "business owners", "businessman", "businesswoman", "manager", "managers", "representative", "representatives", "رجل اعمال", "سيده اعمال", "سيدة اعمال", "صاحب شركه", "صاحب شركة", "مدير", "مدراء", "مندوب", "مندوبي", "اصحاب ومدراء ومندوبي الشركات والمؤسسات"],
    "رجل اعمال": ["رجل اعمال", "راعي اعمال", "راعي أعمال", "رائد اعمال", "رائد أعمال", "سيده اعمال", "سيدة اعمال", "صاحب شركه", "صاحب شركة", "مدير", "مدراء", "مندوب", "مندوبي", "اصحاب ومدراء ومندوبي الشركات والمؤسسات", "business owner", "business owners", "businessman", "businesswoman", "entrepreneur", "manager", "managers", "representative", "representatives"],
    "راعي اعمال": ["راعي اعمال", "راعي أعمال", "رائد اعمال", "رائد أعمال", "رجل اعمال", "صاحب شركة", "business owner", "businessman", "entrepreneur", "manager", "representative"],
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


ARABIC_OCCUPATION_TRANSLATIONS_EN = {
    "استاذ اصول التربيه": "Professor of Education Principles",
    "استاذ اصول تربيه": "Professor of Education Principles",
    "استاذ اداب": "Professor of Literature",
    "استاذ اصحاح مهني": "Professor of Vocational Rehabilitation",
    "استاذ اداره تربويه": "Professor of Educational Administration",
    "استاذ ارصاد": "Professor of Meteorology",
    "اخصائي توجيه مهني": "Vocational Guidance Specialist",
    "اخصائى توجيه مهني": "Vocational Guidance Specialist",
    "اخصايي توجيه مهني": "Vocational Guidance Specialist",
}

GENERIC_ENGLISH_OCCUPATION_NAMES = {
    "professor",
    "professors",
    "specialist",
    "specialists",
}


def translated_occupation_name_en(name_ar):
    normalized = normalize_text(name_ar)
    if not normalized:
        return ""

    if normalized in ARABIC_OCCUPATION_TRANSLATIONS_EN:
        return ARABIC_OCCUPATION_TRANSLATIONS_EN[normalized]

    if normalized.startswith("استاذ "):
        specialty = normalized.replace("استاذ ", "", 1).strip()
        specialty_translation = {
            "اصول التربيه": "Education Principles",
            "اصول تربيه": "Education Principles",
            "اداب": "Literature",
            "اصحاح مهني": "Vocational Rehabilitation",
            "اداره تربويه": "Educational Administration",
            "ارصاد": "Meteorology",
        }.get(specialty)
        if specialty_translation:
            return f"Professor of {specialty_translation}"

    if normalized.startswith(("اخصائي ", "اخصائى ")):
        specialty = normalized.split(" ", 1)[1].strip()
        specialty_translation = {
            "توجيه مهني": "Vocational Guidance",
        }.get(specialty)
        if specialty_translation:
            return f"{specialty_translation} Specialist"

    return ""


def is_generic_english_occupation_name(name_en):
    normalized = normalize_text(name_en)
    return normalized in GENERIC_ENGLISH_OCCUPATION_NAMES


def occupation_name_en_for(occupation):
    if not isinstance(occupation, dict):
        return ""

    name_ar = occupation.get("occupationNameAr") or occupation.get("ArabicDescription") or ""
    raw_name_en = (
        occupation.get("occupationNameEn")
        or occupation.get("DescriptionEn")
        or occupation.get("EnglishDescription")
        or ""
    )
    translated = translated_occupation_name_en(name_ar)

    if translated and (not raw_name_en or is_generic_english_occupation_name(raw_name_en)):
        return translated

    return str(raw_name_en or "").strip()


def occupation_name_ar_for(occupation):
    if not isinstance(occupation, dict):
        return ""
    return str(occupation.get("occupationNameAr") or occupation.get("ArabicDescription") or "").strip()


def occupation_display_name(occupation, arabic=False):
    name_ar = occupation_name_ar_for(occupation)
    name_en = occupation_name_en_for(occupation)

    if arabic:
        return name_ar or name_en

    return name_en or name_ar


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


NESTED_RULE_LIST_KEYS = (
    "children",
    "childrens",
    "subCategories",
    "subcategories",
    "subOccupations",
    "subOccupation",
    "occupations",
    "occupation",
    "newOccupation",
    "items",
    "data",
    "values",
    "list",
)


def flatten_rule_items(items):
    flattened = []

    def visit(value):
        if isinstance(value, list):
            for child in value:
                visit(child)
            return

        if not isinstance(value, dict):
            return

        flattened.append(value)
        for key in NESTED_RULE_LIST_KEYS:
            nested = value.get(key)
            if isinstance(nested, list):
                visit(nested)

    visit(items)
    return flattened


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

    return flatten_rule_items(country_occupations if country_occupations else general_occupations)


def build_occupation_list(visa_data):
    occupations = []
    seen = set()

    for occupation in get_occupation_rules(visa_data):
        if not isinstance(occupation, dict):
            continue

        if occupation.get("allowed", True) is False:
            continue

        name_ar = occupation_name_ar_for(occupation)
        name_en = occupation_name_en_for(occupation)
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

    direct_user_text = normalize_text(user_occupation)
    user_terms = occupation_search_terms(user_occupation)

    def candidate_names(occ):
        if not isinstance(occ, dict):
            return []

        if occ.get("allowed", True) is False:
            return []

        names = [
            occ.get("ArabicDescription"),
            occ.get("occupationNameAr"),
            occupation_name_en_for(occ),
        ]
        for raw_name in (occ.get("DescriptionEn"), occ.get("EnglishDescription"), occ.get("occupationNameEn")):
            if raw_name and not is_generic_english_occupation_name(raw_name):
                names.append(raw_name)
        return [name for name in names if name]

    for occ in occupations:
        for name in candidate_names(occ):
            name_norm = normalize_text(name)
            if direct_user_text and name_norm and (direct_user_text in name_norm or name_norm in direct_user_text):
                return True, name

    for occ in occupations:
        names = candidate_names(occ)
        if not names:
            continue

        for name in names:
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


def normalize_gender_value(value):
    text = normalize_text(value)
    if not text:
        return None

    if re.search(r"\bfemale\b", text, re.IGNORECASE) or text in {"f", "انثي", "انثى", "امراه", "امرأه", "بنت"}:
        return "female"

    if re.search(r"\bmale\b", text, re.IGNORECASE) or text in {"m", "ذكر", "رجل", "ولد"}:
        return "male"

    return text


def gender_rule_values(gender_rule):
    values = []

    if isinstance(gender_rule, dict):
        gender_rule = [gender_rule]
    elif not isinstance(gender_rule, list):
        gender_rule = [gender_rule] if gender_rule else []

    for item in gender_rule:
        if isinstance(item, dict):
            raw_values = [
                item.get("gender"),
                item.get("Gender"),
                item.get("value"),
                item.get("name"),
            ]
        else:
            raw_values = [item]

        for raw_value in raw_values:
            normalized = normalize_gender_value(raw_value)
            if normalized and normalized not in values:
                values.append(normalized)

    return values


def gender_policy(gender_restrictions):
    restricted = [value for value in gender_restrictions if value in {"male", "female"}]
    allowed = []

    if "female" in restricted and "male" not in restricted:
        allowed = ["male"]
    elif "male" in restricted and "female" not in restricted:
        allowed = ["female"]

    return {
        "restricted": restricted,
        "allowed": allowed,
    }


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


NON_WORK_OCCUPATION_TERMS = (
    "student",
    "pupil",
    "child",
    "minor",
    "\u0637\u0627\u0644\u0628",
    "\u0637\u0627\u0644\u0628\u0629",
    "\u062a\u0644\u0645\u064a\u0630",
    "\u062a\u0644\u0645\u064a\u0630\u0629",
    "\u0637\u0641\u0644",
    "\u0637\u0641\u0644\u0629",
    "\u0642\u0627\u0635\u0631",
)

PROFESSIONAL_OCCUPATION_TERMS = (
    "engineer",
    "software engineer",
    "software eng",
    "full stack developer",
    "devops engineer",
    "data scientist",
    "data analyst",
    "systems analyst",
    "information systems",
    "developer",
    "programmer",
    "ceo",
    "chief executive officer",
    "hr specialist",
    "pr manager",
    "president",
    "member of council",
    "council member",
    "lawyer",
    "attorney",
    "professor",
    "doctor",
    "physician",
    "nurse",
    "pilot",
    "manager",
    "consultant",
    "accountant",
    "teacher",
    "architect",
    "technician",
    "analyst",
    "business owner",
    "entrepreneur",
    "real estate owner",
    "real estate",
    "property owner",
    "property investor",
    "representative",
    "\u0645\u0647\u0646\u062f\u0633",
    "\u0645\u0647\u0646\u062f\u0633\u0629",
    "\u0645\u0647\u0646\u062f\u0633 \u0628\u0631\u0645\u062c\u064a\u0627\u062a",
    "\u0645\u0637\u0648\u0631",
    "\u0645\u0628\u0631\u0645\u062c",
    "\u0631\u0626\u064a\u0633",
    "\u0639\u0636\u0648 \u0645\u062c\u0644\u0633",
    "\u0645\u062d\u0627\u0645\u064a",
    "\u0645\u062d\u0627\u0645\u064a\u0629",
    "\u0627\u0633\u062a\u0627\u0630",
    "\u0623\u0633\u062a\u0627\u0630",
    "\u062f\u0643\u062a\u0648\u0631",
    "\u0637\u0628\u064a\u0628",
    "\u0645\u0645\u0631\u0636",
    "\u0637\u064a\u0627\u0631",
    "\u0645\u062f\u064a\u0631",
    "\u0627\u0633\u062a\u0634\u0627\u0631\u064a",
    "\u0645\u062d\u0627\u0633\u0628",
    "\u0645\u0639\u0644\u0645",
    "\u0645\u062f\u0631\u0633",
    "\u0645\u0639\u0645\u0627\u0631\u064a",
    "\u0641\u0646\u064a",
    "\u0645\u062d\u0644\u0644",
    "\u0645\u0646\u062f\u0648\u0628",
    "\u0635\u064a\u062f\u0644\u064a",
    "\u0635\u064a\u062f\u0644\u0627\u0646\u064a",
    "\u0635\u064a\u0627\u062f\u0644\u0629",
    "pharmacist",
)


def text_contains_any(value: str, terms: tuple[str, ...]) -> bool:
    normalized = normalize_text(value)
    return any(normalize_text(term) in normalized for term in terms if term)


def age_occupation_consistency_issue(age, occupation: str | None):
    if age is None or not occupation:
        return None

    try:
        age_int = int(age)
    except (TypeError, ValueError):
        return None

    normalized_occupation = normalize_text(occupation)
    if not normalized_occupation:
        return None

    if text_contains_any(normalized_occupation, NON_WORK_OCCUPATION_TERMS):
        return None

    if age_int < 16:
        return "Applicant age is not logically consistent with a working occupation."

    if age_int < 18 and text_contains_any(normalized_occupation, PROFESSIONAL_OCCUPATION_TERMS):
        return "Applicant age is not logically consistent with the stated professional occupation."

    return None


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
            "relationships_count": 0,
            "gender_restrictions": [],
            "gender_policy": {
                "restricted": [],
                "allowed": [],
            }
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
    gender_restrictions = gender_rule_values(gender_rule)
    result["details"]["gender_restrictions"] = gender_restrictions
    result["details"]["gender_policy"] = gender_policy(gender_restrictions)

    if gender_restrictions:
        normalized_gender = normalize_gender_value(gender)
        if normalized_gender in gender_restrictions:
            result["checks"].append({
                "passed": False,
                "field": "gender",
                "message": "Gender is restricted for this visa."
            })
        elif normalized_gender:
            result["checks"].append({
                "passed": True,
                "field": "gender",
                "message": "Gender is allowed."
            })

    occupation_rules = get_occupation_rules(visa_data)

    result["details"]["occupations"] = [
        occupation_display_name(o)
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

    consistency_issue = age_occupation_consistency_issue(age, occupation)
    if consistency_issue:
        result["checks"].append({
            "passed": False,
            "field": "age_occupation_consistency",
            "message": consistency_issue
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
    failed_fields = {c.get("field") for c in failed}

    if "occupation" in failed_fields:
        result["missing_fields"] = [
            field for field in result["missing_fields"]
            if field not in {"age", "valid_age"}
        ]

    if failed:
        result["status"] = "NOT_APPROVED"
    elif result["missing_fields"]:
        result["status"] = "NEED_MORE_INFO"
    else:
        result["status"] = "APPROVED"

    return result
