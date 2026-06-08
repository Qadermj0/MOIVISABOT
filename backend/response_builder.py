import re

from .rules_engine import (
    first_rule_list,
    gender_policy,
    gender_rule_values,
    get_age_rule,
    get_occupation_rules,
    occupation_display_name,
)


VISA_TYPE_NAMES = {
    1: "سمة دخول عمل بالحكومة",
    2: "سمة دخول عمل أهلي",
    3: "سمة دخول عامل منزلي",
    6: "سمة دخول دراسة",
    7: "سمة دخول علاج",
    8: "سمة دخول زيارة تجارية",
    9: "سمة دخول زيارة حكومية",
    10: "سمة دخول زيارة عائلية",
    11: "سمة دخول زيارة لسفارة",
    14: "سمة عودة عدة سفرات",
    16: "سمة دخول للسياحة",
    19: "سمة عودة",
    20: "سمة دخول خاصة",
}

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

AR_FIELD_NAMES = {
    "country": "الدولة / الجنسية",
    "visa_type": "رقم الفيزا",
    "age": "العمر",
    "valid_age": "عمر صحيح",
    "occupation": "المهنة",
    "age_occupation_consistency": "منطق العمر والمهنة",
    "gender": "الجنس",
    "relationship": "العلاقة / المرافق",
}

EN_FIELD_NAMES = {
    "country": "country / nationality",
    "visa_type": "visa number",
    "age": "age",
    "valid_age": "valid age",
    "occupation": "occupation",
    "age_occupation_consistency": "age and occupation consistency",
    "gender": "gender",
    "relationship": "relationship / companion",
}

RELATIONSHIP_NAMES_EN = {
    "الزوجة": "wife",
    "الزوج": "husband",
    "الابن": "son",
    "الابنة": "daughter",
    "الأم": "mother",
    "الأب": "father",
    "الأخ": "brother",
    "الأخت": "sister",
    "مرافق": "companion",
}


def is_arabic(text: str, session: dict | None = None) -> bool:
    if re.search(r"[\u0600-\u06ff]", text or ""):
        return True

    language = str((session or {}).get("language") or "").strip().lower()
    return language in {"ar", "ar-kw", "ar-sa", "arabic", "العربية"}


def normalize_chat_text(text: str) -> str:
    normalized = str(text or "").strip().lower()
    normalized = re.sub(r"[\u064b-\u065f\u0670]", "", normalized)
    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ى": "ي",
        "ة": "ه",
        "ؤ": "و",
        "ئ": "ي",
        "ـ": "",
    }
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    normalized = re.sub(r"[^\w\s\u0600-\u06ff]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def asks_about_passport_upload(text: str) -> bool:
    normalized = str(text or "").lower()
    normalized = (
        normalized
        .replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
        .replace("ة", "ه")
    )
    phrases = (
        "رفع صوره جواز",
        "صوره جواز",
        "جواز سفري",
        "جواز السفر",
        "رفع الجواز",
        "passport upload",
        "upload passport",
        "passport image",
        "passport photo",
    )
    return any(phrase in normalized for phrase in phrases)


def visa_name_for(visa_type):
    try:
        return VISA_TYPE_NAMES.get(int(visa_type))
    except (TypeError, ValueError):
        return None


def visa_name_en_for(visa_type):
    try:
        return VISA_TYPE_NAMES_EN.get(int(visa_type))
    except (TypeError, ValueError):
        return None


def field_name(field, arabic: bool):
    names = AR_FIELD_NAMES if arabic else EN_FIELD_NAMES
    return names.get(str(field), str(field).replace("_", " "))


def relationship_name(value, arabic: bool):
    if not value:
        return "العلاقة المذكورة" if arabic else "the mentioned relationship"
    if arabic:
        return str(value)
    return RELATIONSHIP_NAMES_EN.get(str(value), str(value))


def gender_policy_note(policy: dict | None, arabic: bool):
    policy = policy or {}
    allowed = set(policy.get("allowed") or [])
    restricted = set(policy.get("restricted") or [])

    if "male" in allowed and "female" in restricted:
        return (
            "ملاحظة: هذه الفيزا متاحة للذكور فقط حسب قيود الجنس الظاهرة في البيانات."
            if arabic
            else "Note: this visa is available to male applicants only according to the visible gender restriction."
        )

    if "female" in allowed and "male" in restricted:
        return (
            "ملاحظة: هذه الفيزا متاحة للإناث فقط حسب قيود الجنس الظاهرة في البيانات."
            if arabic
            else "Note: this visa is available to female applicants only according to the visible gender restriction."
        )

    if restricted:
        restricted_label = "، ".join(sorted(restricted)) if arabic else ", ".join(sorted(restricted))
        return (
            f"ملاحظة: توجد قيود جنس ظاهرة في البيانات: {restricted_label}."
            if arabic
            else f"Note: visible gender restrictions apply: {restricted_label}."
        )

    return ""


def status_text(status, arabic: bool):
    normalized = str(status or "").upper()
    if arabic:
        return {
            "APPROVED": "مبدئياً مطابق",
            "NOT_APPROVED": "غير مطابق",
            "NEED_MORE_INFO": "تحتاج معلومات إضافية",
            "INFO": "معلومات",
        }.get(normalized, "تحتاج معلومات إضافية")

    return {
        "APPROVED": "Approved",
        "NOT_APPROVED": "Not Approved",
        "NEED_MORE_INFO": "Need More Information",
        "INFO": "Information",
    }.get(normalized, "Need More Information")


def country_display(session: dict, decision: dict | None = None, arabic: bool = True):
    decision = decision or {}
    if arabic:
        country = decision.get("country_ar") or decision.get("country") or session.get("country") or session.get("country_en")
    else:
        country = decision.get("country_en") or session.get("country_en") or decision.get("country") or session.get("country")
        if isinstance(country, str) and country.isupper():
            country = country.title()
    ocr_code = decision.get("ocr_code") or decision.get("country_ocr_code") or session.get("ocr_code")

    if country and ocr_code:
        return f"{country} ({ocr_code})"
    return country or ocr_code


def format_visa_label(visa_type, visa_name=None, arabic: bool = True, with_check: bool = False):
    name = visa_name or visa_name_for(visa_type)
    prefix = "✓ " if with_check else ""

    if arabic:
        if visa_type and name:
            return f"{prefix}فيزا رقم {visa_type} - {name}"
        if visa_type:
            return f"{prefix}فيزا رقم {visa_type}"
        return f"{prefix}{name or 'اسم الفيزا غير متوفر في البيانات'}"

    english_name = visa_name_en_for(visa_type) or name
    if visa_type and english_name:
        return f"{prefix}Visa No. {visa_type} - {english_name}"
    if visa_type:
        return f"{prefix}Visa No. {visa_type}"
    return f"{prefix}{english_name or 'Name not available in the data'}"


def clean_items(items):
    result = []
    seen = set()

    for item in items or []:
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)

    return result


def allowed_names(items, keys, limit=10):
    names = []
    occupation_keys = {
        "occupationNameAr",
        "ArabicDescription",
        "occupationNameEn",
        "DescriptionEn",
        "EnglishDescription",
    }
    is_occupation_list = any(key in occupation_keys for key in keys)
    arabic_preferred = bool(keys and keys[0] in {"occupationNameAr", "ArabicDescription"})

    for item in items or []:
        if not isinstance(item, dict):
            continue
        if item.get("allowed", True) is False:
            continue
        if is_occupation_list:
            value = occupation_display_name(item, arabic=arabic_preferred)
            if value:
                names.append(str(value).strip())
                continue
        for key in keys:
            value = item.get(key)
            if value:
                names.append(str(value).strip())
                break

    return clean_items(names)[:limit]


def allowed_values(items, keys):
    values = []

    for item in items or []:
        if not isinstance(item, dict):
            continue
        if item.get("allowed", True) is False:
            continue
        for key in keys:
            value = item.get(key)
            if value:
                values.append(str(value).strip())

    return clean_items(values)


def compact_text(value: str):
    text = str(value or "").strip().lower()
    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ى": "ي",
        "ة": "ه",
        "ؤ": "و",
        "ئ": "ي",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^\w\s\u0600-\u06ff]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def occupation_item_is_professor(item: dict):
    values = allowed_values([item], ["occupationNameEn", "DescriptionEn", "EnglishDescription", "occupationNameAr", "ArabicDescription"])
    return any("professor" in compact_text(value) or "استاذ" in compact_text(value) for value in values)


def all_allowed_occupations_are_professors(occupations):
    allowed_items = [
        item for item in occupations or []
        if isinstance(item, dict) and item.get("allowed", True) is not False
    ]
    return bool(allowed_items) and all(occupation_item_is_professor(item) for item in allowed_items)


def extract_rule_summary(raw_visa_details: dict):
    if not raw_visa_details:
        return {
            "age_rule": (None, None),
            "occupations": [],
            "relationships": [],
            "gender": [],
        }

    country_rule = raw_visa_details.get("countryRule") or {}
    rules = country_rule.get("rules") or {}
    general_rules = raw_visa_details.get("generalRules") or {}

    min_age, max_age = get_age_rule(rules)
    if not min_age and not max_age:
        min_age, max_age = get_age_rule(general_rules)

    occupations = get_occupation_rules(raw_visa_details)

    relationships = first_rule_list(
        rules.get("relationship"),
        general_rules.get("relationship"),
    )

    gender = first_rule_list(
        rules.get("gender"),
        general_rules.get("gender"),
    )
    gender_restrictions = gender_rule_values(gender)

    return {
        "age_rule": (min_age, max_age),
        "occupations": occupations,
        "relationships": relationships,
        "gender": gender,
        "gender_policy": gender_policy(gender_restrictions),
    }


def build_chitchat_answer(user_message: str):
    normalized = normalize_chat_text(user_message)
    arabic = is_arabic(user_message)
    thanks_markers = ["شكرا", "يعطيك العافيه", "مشكور", "thanks", "thank you"]
    farewell_markers = ["مع السلامه", "سلام", "وداعا", "باي", "bye", "goodbye", "see you"]

    if any(marker in normalized for marker in thanks_markers):
        return (
            "العفو، حاضر. إذا احتجت أي استفسار ثاني عن التأشيرات أنا موجود."
            if arabic
            else "You're welcome. I am here if you need anything else about Kuwait visas."
        )

    if any(marker in normalized for marker in farewell_markers):
        return (
            "مع السلامة، بالتوفيق."
            if arabic
            else "Goodbye, and best of luck."
        )

    if arabic:
        return "هلا فيك، أنا بخير. أنا مساعد التأشيرات الذكي، اسألني عن الفيز المتاحة للكويت أو شروط أي فيزا حسب دولتك."
    return "Hello. I am ready to help with Kuwait visa types and requirements based on your country."


def build_context_answer(user_message: str, session: dict):
    arabic = is_arabic(user_message, session)
    country = country_display(session, arabic=arabic)

    if country:
        return f"أنت مسجل عندي أنك من {country}." if arabic else f"I have your country as {country}."

    return (
        "لسا ما عندي دولتك في هذه المحادثة. اذكر دولتك أو جنسيتك حتى أقدر أبحث لك بدقة."
        if arabic
        else "I do not have your country in this conversation yet. Please provide your country or nationality."
    )


def build_country_ack(user_message: str, session: dict):
    arabic = is_arabic(user_message, session)
    country = country_display(session, arabic=arabic)
    visa_type = session.get("visa_type")
    visa_name = visa_name_for(visa_type) if visa_type else None
    visa_label = format_visa_label(visa_type, visa_name, arabic) if visa_type else None

    if visa_label:
        if arabic:
            return (
                f"تم، سجلت أن مقدم الطلب من {country}. ما زال عندي في سياق المحادثة {visa_label}. "
                "هل تريد نكمل فحص الأهلية على هذه الفيزا، أم تريد اختيار نوع فيزا آخر؟"
            )
        return (
            f"Got it. I have the applicant country as {country}. I still have {visa_label} in this conversation. "
            "Do you want to continue checking this visa, or choose a different visa type?"
        )

    if arabic:
        return f"تم، سجلت أنك من {country}. تقدر تسألني الآن عن الفيز المتاحة أو تذكر رقم فيزا معين لمعرفة الشروط."
    return f"Got it. I have your country as {country}. You can ask for available visa types or a specific visa number."


def build_missing_country_answer(user_message: str, decision: dict):
    arabic = is_arabic(user_message)
    visa_type = decision.get("visa_type")
    visa_name = decision.get("visa_name") or visa_name_for(visa_type)
    visa_label = format_visa_label(visa_type, visa_name, arabic)

    if arabic:
        if visa_type:
            return f"{visa_label}. حتى أجيب الشروط بدقة من قواعد التأشيرات، من أي دولة أو جنسية أنت؟"
        return "حتى أقدر أبحث لك بدقة، اذكر الدولة أو الجنسية أولاً."

    if visa_type:
        return f"{visa_label}. To retrieve the exact requirements, please tell me your country or nationality."
    return "Please provide your country or nationality first so I can check the visa rules accurately."


def build_visa_list_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    visa_types = decision.get("visa_types") or decision.get("available_visa_types") or []
    country = country_display(session, decision, arabic)

    if not visa_types:
        return (
            f"لم أجد فيز متاحة في البيانات الحالية لـ {country}."
            if arabic
            else f"I could not find available visa types in the current data for {country}."
        )

    lines = []
    if arabic:
        lines.append(f"الفيز المتاحة في البيانات الحالية لـ {country}:")
        lines.extend(format_visa_label(v.get("visa_type"), v.get("visa_name"), arabic, True) for v in visa_types)
    else:
        lines.append(f"Available visa types in the current data for {country}:")
        lines.extend(format_visa_label(v.get("visa_type"), v.get("visa_name_en"), arabic, True) for v in visa_types)

    return "\n".join(lines)


def build_visa_details_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    raw = decision.get("raw_visa_details") or {}
    summary = extract_rule_summary(raw)
    visa_label = format_visa_label(decision.get("visa_type"), decision.get("visa_name"), arabic)
    country = country_display(session, decision, arabic)
    min_age, max_age = summary["age_rule"]
    occupation_names = allowed_names(
        summary["occupations"],
        ["occupationNameAr", "ArabicDescription", "occupationNameEn", "DescriptionEn", "EnglishDescription"] if arabic else ["occupationNameEn", "DescriptionEn", "EnglishDescription", "occupationNameAr", "ArabicDescription"],
        limit=8,
    )
    relationship_names = allowed_names(
        summary["relationships"],
        ["relationNameAr", "arabicDescription", "relationNameEn"] if arabic else ["relationNameEn", "relationNameAr", "arabicDescription"],
        limit=12,
    )
    gender_note = gender_policy_note(summary.get("gender_policy"), arabic)

    lines = []

    if arabic:
        lines.append("هذه المعلومات المتاحة من قواعد التأشيرات:")
        lines.append(f"البلد: {country}")
        lines.append(f"الفيزا: {visa_label}")
        lines.append("")
        lines.append("الشروط والبيانات المطلوبة:")

        has_rule = False
        if min_age or max_age:
            has_rule = True
            lines.append(f"• العمر: من {min_age or 'غير محدد'} إلى {max_age or 'غير محدد'}.")

        if summary["occupations"]:
            has_rule = True
            if occupation_names:
                lines.append(f"• المهنة: توجد مهن أو فئات مهنية مسموحة، منها: {'، '.join(occupation_names)}.")
            else:
                lines.append("• المهنة: توجد قائمة مهن مسموحة في البيانات.")

        if not summary["relationships"]:
            has_rule = True
            lines.append("• العلاقة / المرافق: لا توجد علاقات أو مرافقون مسموحون في البيانات الحالية.")

        if summary["relationships"]:
            has_rule = True
            if relationship_names:
                lines.append(f"• العلاقة / المرافق: العلاقات الظاهرة ضمن البيانات تشمل: {'، '.join(relationship_names)}.")
            else:
                lines.append("• العلاقة / المرافق: توجد قائمة علاقات مسموحة في البيانات.")

        if gender_note:
            has_rule = True
            lines.append(f"• {gender_note}")

        if not has_rule:
            lines.append("• لا تظهر شروط تفصيلية إضافية لهذه الفيزا في البيانات الحالية.")

        return "\n".join(lines)

    lines.append("Available visa rule information:")
    lines.append(f"Country: {country}")
    lines.append(f"Visa: {visa_label}")
    lines.append("")
    lines.append("Requirements and visible rule data:")

    has_rule = False
    if min_age or max_age:
        has_rule = True
        lines.append(f"- Age: from {min_age or 'not specified'} to {max_age or 'not specified'}.")

    if summary["occupations"]:
        has_rule = True
        if occupation_names:
            lines.append(f"- Occupation: allowed occupations or professional categories include: {', '.join(occupation_names)}.")
        else:
            lines.append("- Occupation: this visa has an allowed occupation list.")

    if not summary["relationships"]:
        has_rule = True
        lines.append("- Relationship / companion: no allowed relationships or companions are listed in the current data.")

    if summary["relationships"]:
        has_rule = True
        if relationship_names:
            lines.append(f"- Relationship / companion: allowed relationships include: {', '.join(relationship_names)}.")
        else:
            lines.append("- Relationship / companion: this visa has an allowed relationship list.")

    if gender_note:
        has_rule = True
        lines.append(f"- {gender_note}")

    if not has_rule:
        lines.append("- No additional detailed rule conditions are visible in the current data.")

    return "\n".join(lines)


def build_occupation_details_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    raw = decision.get("raw_visa_details") or {}
    summary = extract_rule_summary(raw)
    visa_label = format_visa_label(decision.get("visa_type"), decision.get("visa_name"), arabic)
    country = country_display(session, decision, arabic)
    occupation_names = allowed_names(
        summary["occupations"],
        ["occupationNameAr", "ArabicDescription", "occupationNameEn", "DescriptionEn", "EnglishDescription"] if arabic else ["occupationNameEn", "DescriptionEn", "EnglishDescription", "occupationNameAr", "ArabicDescription"],
        limit=80,
    )

    if not occupation_names:
        return (
            f"لا تظهر قائمة مهن محددة في البيانات الحالية لـ {visa_label} لمقدمي الطلب من {country}."
            if arabic
            else f"No specific occupation list is visible in the current data for {visa_label} for applicants from {country}."
        )

    if arabic:
        lines = [f"المهن أو الفئات المهنية المسموحة لـ {visa_label} لمقدمي الطلب من {country}:"]
        lines.extend(f"• {name}" for name in occupation_names)
        return "\n".join(lines)

    lines = [f"Allowed occupations or professional categories for {visa_label} for applicants from {country}:"]
    lines.extend(f"- {name}" for name in occupation_names)
    return "\n".join(lines)


def build_age_details_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    raw = decision.get("raw_visa_details") or {}
    summary = extract_rule_summary(raw)
    visa_label = format_visa_label(decision.get("visa_type"), decision.get("visa_name"), arabic)
    country = country_display(session, decision, arabic)
    min_age, max_age = summary["age_rule"]

    if min_age is None and max_age is None:
        return (
            f"لا يظهر شرط عمر محدد في البيانات الحالية لـ {visa_label} لمقدمي الطلب من {country}."
            if arabic
            else f"No specific age requirement is visible in the current data for {visa_label} for applicants from {country}."
        )

    if arabic:
        return (
            f"حسب القواعد الحالية لـ {visa_label} لمقدمي الطلب من {country}، "
            f"العمر المسموح هو من {min_age if min_age is not None else 'غير محدد'} إلى {max_age if max_age is not None else 'غير محدد'} سنة."
        )

    return (
        f"Based on the current rules for {visa_label} for applicants from {country}, "
        f"the allowed age range is from {min_age if min_age is not None else 'not specified'} to {max_age if max_age is not None else 'not specified'} years."
    )


def build_occupation_confirmation_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    raw = decision.get("raw_visa_details") or {}
    summary = extract_rule_summary(raw)
    visa_label = format_visa_label(decision.get("visa_type"), decision.get("visa_name"), arabic)
    country = country_display(session, decision, arabic)
    occupation_names = allowed_names(
        summary["occupations"],
        ["occupationNameAr", "ArabicDescription", "occupationNameEn", "DescriptionEn", "EnglishDescription"] if arabic else ["occupationNameEn", "DescriptionEn", "EnglishDescription", "occupationNameAr", "ArabicDescription"],
        limit=12,
    )

    if not occupation_names:
        return (
            f"لا تظهر قائمة مهن محددة في البيانات الحالية لـ {visa_label} لمقدمي الطلب من {country}."
            if arabic
            else f"No specific occupation list is visible in the current data for {visa_label} for applicants from {country}."
        )

    if all_allowed_occupations_are_professors(summary["occupations"]):
        if arabic:
            return (
                f"نعم، حسب البيانات الحالية لـ {visa_label} لمقدمي الطلب من {country}، "
                "المهن المسموحة محصورة بفئة الأساتذة / PROFESSOR. "
                "القائمة تظهر عدة تخصصات أستاذ، لكنها كلها ضمن نفس الفئة المهنية."
            )

        return (
            f"Yes. In the current data, {visa_label} for applicants from {country} is limited to the PROFESSOR occupation category. "
            "The list contains several professor specializations, but they all fall under the same professional category."
        )

    if arabic:
        return (
            f"لا، ليست محصورة بالأساتذة فقط حسب البيانات الحالية. "
            f"المهن المسموحة لـ {visa_label} من {country} تشمل: {', '.join(occupation_names)}."
        )

    return (
        f"No. The visible allowed occupations for {visa_label} from {country} are not limited to professors. "
        f"They include: {', '.join(occupation_names)}."
    )


def build_relationship_details_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    raw = decision.get("raw_visa_details") or {}
    summary = extract_rule_summary(raw)
    visa_label = format_visa_label(decision.get("visa_type"), decision.get("visa_name"), arabic)
    country = country_display(session, decision, arabic)
    relationship_names = allowed_names(
        summary["relationships"],
        ["relationNameAr", "arabicDescription", "ArabicDescription", "relationNameEn", "DescriptionEn"] if arabic else ["relationNameEn", "DescriptionEn", "relationNameAr", "arabicDescription", "ArabicDescription"],
        limit=80,
    )

    if not relationship_names:
        return (
            f"لا، {visa_label} لمقدمي الطلب من {country} لا تظهر لها أي علاقات أو مرافقين مسموحين في البيانات الحالية."
            if arabic
            else f"No. {visa_label} for applicants from {country} does not list any allowed relationships or companions in the current data."
        )

    if arabic:
        lines = [f"العلاقات / المرافقون المسموحون لـ {visa_label} لمقدمي الطلب من {country}:"]
        lines.extend(f"• {name}" for name in relationship_names)
        return "\n".join(lines)

    lines = [f"Allowed relationships / companions for {visa_label} for applicants from {country}:"]
    lines.extend(f"- {name}" for name in relationship_names)
    return "\n".join(lines)


def build_relationship_check_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    relationship_checks = [
        check for check in (decision.get("checks") or [])
        if check.get("field") == "relationship"
    ]

    if not relationship_checks:
        return build_relationship_details_answer(user_message, decision, session)

    visa_label = format_visa_label(decision.get("visa_type"), decision.get("visa_name"), arabic)
    country = country_display(session, decision, arabic)
    failed = [check for check in relationship_checks if check.get("passed") is False]
    passed = [check for check in relationship_checks if check.get("passed") is True]
    relation = relationship_name((decision.get("applicant_data") or {}).get("relationship"), arabic)

    if failed:
        if arabic:
            return f"لا، {relation} غير مسموحة كمرافق لـ {visa_label} لمقدمي الطلب من {country} حسب البيانات الحالية."
        return f"No. The {relation} is not allowed as a companion for {visa_label} for applicants from {country} according to the current data."

    if passed:
        if arabic:
            return f"نعم، {relation} مسموحة كمرافق لـ {visa_label} لمقدمي الطلب من {country} حسب البيانات الحالية."
        return f"Yes. The {relation} is allowed as a companion for {visa_label} for applicants from {country} according to the current data."

    return build_relationship_details_answer(user_message, decision, session)


def build_relationship_reset_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    has_recheck = decision.get("status") not in {None, "INFO"} and (
        decision.get("checks") or decision.get("missing_fields")
    )

    if has_recheck:
        eligibility_answer = build_eligibility_answer(user_message, decision, session)
        prefix = (
            "تمام، لن أحتسب الزوجة أو أي مرافق في هذا الفحص. النتيجة بعد التحديث:"
            if arabic
            else "Got it. I will not include the wife or any companion in this check. Updated result:"
        )
        return f"{prefix}\n\n{eligibility_answer}"

    return (
        "تمام، لن أحتسب الزوجة أو أي مرافق في الفحص. إذا بدك أفحص أهليتك الآن، اذكر العمر والمهنة."
        if arabic
        else "Got it. I will not include the wife or any companion in the check. To check your eligibility now, provide the age and occupation."
    )


def build_dependent_residency_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    country = country_display(session, decision, arabic)

    if arabic:
        lines = [
            "فهمت عليك: سؤالك عن التحاق بعائل / إقامة عائلية، وذكرت الزوجة والأبناء والراتب والمهنة.",
            "",
            "البيانات المتاحة داخل هذا المساعد تخص قواعد سمات دخول الكويت الموجودة في النظام الحالي، وليست مرجعاً كاملاً لقوانين الإقامة أو شرط الراتب أو الاستثناءات الإدارية لعام 2026.",
            "",
            "لذلك لا أقدر أؤكد لك من هذه البيانات أن مهنة مهندس برمجيات تمنح استثناء من شرط الراتب، ولا أقدر أؤكد القوانين المحدثة أو قرار المراجعة اليدوية للإدارة العامة لشؤون الإقامة.",
        ]

        if country:
            lines.append(f"الجنسية التي فهمتها من رسالتك: {country}.")

        lines.extend([
            "",
            "إذا كنت تريد فحص سمة دخول من البيانات المتاحة، أقدر أساعدك بتحديد فيزا مثل زيارة عائلية رقم 10 أو أي رقم فيزا آخر.",
            "أما موضوع التحاق بعائل/الإقامة العائلية وشرط الراتب فيحتاج الرجوع للجهة المختصة أو القنوات الرسمية لشؤون الإقامة."
        ])
        return "\n".join(lines)

    lines = [
        "I understand that your question is about dependent/family residency, including wife, children, salary, and occupation.",
        "",
        "The data available in this assistant covers Kuwait entry visa rules in the current system. It is not a complete source for residency law, salary exemptions, or administrative residency decisions for 2026.",
        "",
        "Because of that, I cannot confirm from this data whether a software engineer occupation gives a salary exemption, or whether a manual review by Residency Affairs is required.",
    ]

    if country:
        lines.append(f"Applicant nationality understood from your message: {country}.")

    lines.extend([
        "",
        "If you want to check an entry visa from the available data, I can help with a specific visa type such as Family Visit Visa No. 10 or another visa number.",
        "For dependent/family residency and salary conditions, please refer to the competent Residency Affairs authority or official channels.",
    ])
    return "\n".join(lines)


def build_residency_admin_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    country = country_display(session, decision, arabic)
    visa_type = decision.get("visa_type") or session.get("visa_type")
    visa_label = format_visa_label(visa_type, decision.get("visa_name") or visa_name_for(visa_type), arabic) if visa_type else None

    if arabic:
        lines = [
            "فهمت عليك: سؤالك عن إجراء إقامة أو وضع إداري، مثل تحويل زيارة إلى إقامة عمل مادة 18، انتهاء صلاحية الزيارة، الغرامات، أو الدفع الإلكتروني.",
            "",
            "البيانات المتاحة داخل هذا المساعد تخص قواعد سمات دخول الكويت الظاهرة في نظام التأشيرات الحالي. هذه البيانات لا تكفي لتأكيد إجراءات الإقامة، التحويل من زيارة إلى إقامة عمل، الغرامات، أو القوانين المحدثة لشهر مايو 2026.",
            "",
            "لذلك لا أقدر أؤكد من هذه البيانات هل يمكن تحويل الزيارة إلى إقامة عمل دون مغادرة البلاد، ولا أقدر أحدد قيمة الغرامات أو طريقة الدفع القانونية المعتمدة.",
        ]

        if country:
            lines.append(f"الجنسية التي فهمتها من رسالتك: {country}.")
        if visa_label:
            lines.append(f"الفيزا التي فهمتها من رسالتك: {visa_label}.")

        lines.append("")
        if visa_label:
            lines.append(f"أقدر أفحص لك فقط قواعد {visa_label} من ناحية العمر والمهنة والجنس والعلاقات المسموحة.")
        else:
            lines.append("أقدر أفحص لك فقط قواعد سمة دخول محددة من ناحية العمر والمهنة والجنس والعلاقات المسموحة.")
        lines.append("أما التحويل إلى إقامة عمل، انتهاء الصلاحية، والغرامات فيحتاج الرجوع إلى القنوات الرسمية لوزارة الداخلية أو الإدارة العامة لشؤون الإقامة.")
        return "\n".join(lines)

    lines = [
        "I understand that your question is about a residency or administrative procedure, such as converting a visit visa to Article 18 work residency, an expired visit, overstay fines, or online payment.",
        "",
        "The data available in this assistant covers Kuwait entry visa rules in the current visa-rules system. It is not enough to confirm residency conversion procedures, overstay fines, payment methods, or updated legal rules for May 2026.",
        "",
        "Because of that, I cannot confirm from this data whether the visit can be converted to work residency without leaving Kuwait, or what fines/payment process applies.",
    ]

    if country:
        lines.append(f"Applicant nationality understood from your message: {country}.")
    if visa_label:
        lines.append(f"Visa understood from your message: {visa_label}.")

    lines.append("")
    if visa_label:
        lines.append(f"I can still check the visible entry-visa rules for {visa_label}, including age, occupation, gender, and allowed relationships.")
    else:
        lines.append("I can still check the visible entry-visa rules for a specific visa, including age, occupation, gender, and allowed relationships.")
    lines.append("For residency conversion, expired stay, and fines, please refer to the official Ministry of Interior channels or the competent Residency Affairs authority.")
    return "\n".join(lines)


def build_inside_kuwait_visa_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    visa_type = decision.get("visa_type") or session.get("visa_type") or 16
    visa_label = format_visa_label(visa_type, decision.get("visa_name") or visa_name_for(visa_type), arabic)

    if arabic:
        return "\n".join([
            f"فهمت عليك: أنت تتكلم عن {visa_label} لكن من داخل الكويت، ومعك أو كان معك دخول زيارة سابق.",
            "",
            "وجودك داخل الكويت يعني أنك سبق ودخلت بنوع زيارة ما، لكنه لا يعني أن جنسيتك هي الكويت، ولا يؤكد تلقائياً أن شروط فيزا سياحية جديدة أو إجراء التقديم من داخل الكويت متاحة بنفس الطريقة.",
            "",
            "قواعد الأهلية المتاحة لدي تفحص شروط سمة الدخول حسب جنسية مقدم الطلب، العمر، المهنة، والجنس عند الحاجة. لذلك إذا تريد تأكيد الأهلية حسب القواعد الظاهرة، اذكر جنسيتك أولاً، ومعها العمر والمهنة.",
            "",
            "أما سؤال: هل يمكن تقديم/تجديد/تحويل الطلب من داخل الكويت وأنت على زيارة سابقة، فهذا جانب إجرائي تابع لشؤون الإقامة أو القنوات الرسمية، وليس كافياً أن أحسمه من قواعد الأهلية فقط."
        ])

    return "\n".join([
        f"I understand: you are asking about {visa_label} while you are already inside Kuwait on a previous visit entry.",
        "",
        "Being inside Kuwait means you previously entered on some visit basis, but it does not mean your applicant nationality is Kuwait, and it does not automatically confirm that a new tourist visa or an in-country application procedure is available the same way.",
        "",
        "The rule data I can check is based on the applicant nationality, age, occupation, and sometimes gender. If you want an eligibility confirmation from the visible rules, please provide your nationality first, plus age and occupation.",
        "",
        "Whether you can submit, renew, or change status from inside Kuwait is an administrative Residency Affairs procedure, so I cannot confirm it from eligibility rules alone."
    ])


def build_visa_comparison_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    country = country_display(session, decision, arabic)

    if arabic:
        lines = [
            "سؤالك فيه مقارنة بين أكثر من نوع فيزا، لذلك ما رح أفترض أنك ما زلت تقصد آخر فيزا في المحادثة.",
            "",
            "بشكل عام: فيزا السياحة تكون مناسبة لغرض السفر/الترفيه، أما الزيارة التجارية فتحتاج غرضاً تجارياً ومهنة أو فئة مهنية مسموحة حسب جنسية مقدم الطلب.",
        ]
        if country:
            lines.append(f"الجنسية/الدولة الموجودة عندي حالياً: {country}.")
        lines.extend([
            "",
            "حتى أقارن لك حسب القواعد الفعلية، أحتاج جنسية مقدم الطلب والهدف الأساسي من السفر. بعدها أقدر أوضح أيهما أنسب أو أطلب منك اختيار نوع واحد للفحص."
        ])
        return "\n".join(lines)

    lines = [
        "Your question compares more than one visa type, so I will not assume you still mean the previous visa in the conversation.",
        "",
        "In general: a tourism visa fits leisure travel, while a commercial visit visa needs a business purpose and an allowed occupation/professional category based on the applicant nationality.",
    ]
    if country:
        lines.append(f"Current applicant country/nationality in context: {country}.")
    lines.extend([
        "",
        "To compare them against the actual rules, I need the applicant nationality and the main purpose of travel. Then I can explain which path is more suitable or check one selected visa type."
    ])
    return "\n".join(lines)


def build_system_support_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    text = str(user_message or "").lower()
    asks_hours = any(marker in text for marker in ["سبت", "saturday", "اوقات", "أوقات", "ساعات", "دوام", "working hours"])

    if arabic:
        if asks_hours:
            return (
                "بالنسبة لساعات عمل الموقع أو توفره يوم السبت: قواعد التأشيرات المتاحة لدي لا تحتوي جدول تشغيل الموقع أو ساعات الدعم، لذلك لا أقدر أؤكد لك هل الخدمة تعمل يوم السبت من هذه البيانات.\n\n"
                "لكن ما زلت حافظ سياق الفحص السابق. إذا كنت كنت ستزودني بالمهنة أو العمر أو الجنسية، اكتبها وسأكمل فحص الأهلية من نفس النقطة."
            )

        return (
            "فهمت أن سؤالك عن مشكلة تقنية أو إجراء داخل النظام، مثل رفع صورة جواز السفر أو خطأ أثناء التقديم.\n\n"
            "هذا خارج نطاق قواعد أهلية سمات الدخول المتاحة لدي؛ لذلك لا أقدر أؤكد سبب خطأ تقني أو مشكلة رفع ملف من هذه البيانات.\n\n"
            "أقدر أساعدك بفحص شروط الفيزا نفسها إذا ذكرت الجنسية، رقم الفيزا، العمر، المهنة، والجنس عند الحاجة."
        )

    if asks_hours:
        return (
            "For website availability or Saturday working hours: the visa-rule data available to me does not include the website operating schedule or support hours, so I cannot confirm Saturday availability from this data.\n\n"
            "I still keep the previous eligibility context. If you were about to provide the missing age, occupation, or nationality, send it and I will continue the check from the same point."
        )

    return (
        "I understand that your question is about a technical or system-side issue, such as passport image upload or an application error.\n\n"
        "The data available to me covers entry-visa eligibility rules only, so I cannot confirm the cause of a technical upload or system issue from this data.\n\n"
        "I can help check the visa rules themselves if you provide the nationality, visa number, age, occupation, and gender when needed."
    )


def translate_check(check: dict, arabic: bool):
    message = check.get("message") or ""
    field = check.get("field")
    passed = check.get("passed")

    if not arabic:
        if field == "age_occupation_consistency":
            return message or "The provided age is not logically consistent with the stated occupation."
        if field == "occupation" and check.get("matched_value"):
            return f"Occupation is allowed ({check.get('matched_value')})." if passed else "Occupation is not listed as allowed."
        return message or field_name(field, False)

    if field == "age":
        return "العمر ضمن النطاق المسموح." if passed else "العمر خارج النطاق المسموح."
    if field == "age_occupation_consistency":
        return "العمر المذكور غير منطقي مع المهنة المذكورة؛ يرجى التأكد من عمر مقدم الطلب الحقيقي أو المهنة الصحيحة."
    if field == "occupation":
        if passed and check.get("matched_value"):
            return f"المهنة مسموحة ({check.get('matched_value')})."
        return "المهنة مسموحة حسب البيانات." if passed else "المهنة غير مدرجة ضمن المهن المسموحة."
    if field == "relationship":
        return "العلاقة مسموحة حسب البيانات." if passed else "العلاقة غير مسموحة حسب البيانات."
    if field == "gender":
        return "الجنس مطابق للشروط." if passed else "يوجد تقييد على الجنس لهذه الفيزا."

    return message or field_name(field, True)


def build_eligibility_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message, session)
    checks = decision.get("checks") or []
    passed = [check for check in checks if check.get("passed") is True]
    failed = [check for check in checks if check.get("passed") is False]
    missing = decision.get("missing_fields") or []
    alternatives = decision.get("alternative_visas") or []
    visa_label = format_visa_label(decision.get("visa_type"), decision.get("visa_name"), arabic)
    country = country_display(session, decision, arabic)
    gender_note = gender_policy_note((decision.get("details") or {}).get("gender_policy"), arabic)
    applicant_relationship = (decision.get("applicant_data") or {}).get("relationship")
    family_wife_check = decision.get("visa_type") == 10 and relationship_name(applicant_relationship, True) == "الزوجة"

    lines = []

    if arabic:
        lines.append("نتيجة الفحص المبدئي حسب قواعد التأشيرات المتاحة:")
        lines.append(f"الحالة: {status_text(decision.get('status'), True)}")
        lines.append(f"البلد: {country}")
        lines.append(f"الفيزا: {visa_label}")
        if gender_note:
            lines.append(gender_note)

        if passed:
            lines.append("")
            lines.append("الفحوصات المطابقة:")
            lines.extend(f"✅ {translate_check(check, True)}" for check in passed)

        if failed:
            lines.append("")
            lines.append("الفحوصات غير المطابقة:")
            lines.extend(f"❌ {translate_check(check, True)}" for check in failed)

        if missing:
            if family_wife_check:
                readable = "، ".join(
                    "عمر الزوجة" if field == "age" else "مهنة الزوجة" if field == "occupation" else field_name(field, True)
                    for field in missing
                )
            else:
                readable = "، ".join(field_name(field, True) for field in missing)
            lines.append("")
            lines.append(f"معلومات مطلوبة لإكمال الفحص: {readable}.")

        if alternatives:
            lines.append("")
            lines.append("بناءً على مهنتك، قد تكون هذه الأنواع أقرب للفحص بدل هذه الفيزا:")
            lines.extend(
                f"- {format_visa_label(item.get('visa_type'), item.get('visa_name'), True)}"
                for item in alternatives
            )

        if asks_about_passport_upload(user_message):
            lines.append("")
            lines.append("وبخصوص رفع صورة جواز السفر: هذه النقطة لا تظهر ضمن قواعد الأهلية المتاحة لدي، لذلك لا أقدر أؤكد وجود أو عدم وجود مشكلة تقنية أو إدارية في رفع الصورة من هذه البيانات.")

        return "\n".join(lines)

    lines.append("Preliminary eligibility result based on available visa rules:")
    lines.append(f"Status: {status_text(decision.get('status'), False)}")
    lines.append(f"Country: {country}")
    lines.append(f"Visa: {visa_label}")
    if gender_note:
        lines.append(gender_note)

    if passed:
        lines.append("")
        lines.append("Passed checks:")
        lines.extend(f"- {translate_check(check, False)}" for check in passed)

    if failed:
        lines.append("")
        lines.append("Failed checks:")
        lines.extend(f"- {translate_check(check, False)}" for check in failed)

    if missing:
        if family_wife_check:
            readable = ", ".join(
                "wife's age" if field == "age" else "wife's occupation" if field == "occupation" else field_name(field, False)
                for field in missing
            )
        else:
            readable = ", ".join(field_name(field, False) for field in missing)
        lines.append("")
        lines.append(f"Missing information: {readable}.")

    if alternatives:
        lines.append("")
        lines.append("Based on your occupation, these visa types may be more suitable to check instead:")
        lines.extend(
            f"- {format_visa_label(item.get('visa_type'), item.get('visa_name_en') or item.get('visa_name'), False)}"
            for item in alternatives
        )

    if asks_about_passport_upload(user_message):
        lines.append("")
        lines.append("Regarding passport image upload: this is not covered by the eligibility rule data available to me, so I cannot confirm whether a technical or administrative upload issue will occur.")

    return "\n".join(lines)


def build_api_error_answer(user_message: str):
    if is_arabic(user_message):
        return "حاولت جلب قواعد التأشيرات أكثر من مرة، لكن البيانات لم ترجع بشكل موثوق الآن. لا أريد أعطيك نتيجة غير مؤكدة؛ أعد المحاولة بعد لحظات أو اسألني بصيغة أبسط عن الدولة ورقم الفيزا."
    return "I tried to retrieve the visa rules more than once, but the data did not return reliably. I do not want to give an uncertain result; please try again shortly or ask with the country and visa number."


def build_chat_answer(user_message: str, decision: dict, session: dict, extracted: dict):
    intent = decision.get("intent") or extracted.get("intent")

    if intent == "chitchat":
        return build_chitchat_answer(user_message)

    if intent == "context_question":
        return build_context_answer(user_message, session)

    if intent == "provide_country":
        return build_country_ack(user_message, session)

    if decision.get("status") == "API_ERROR":
        return build_api_error_answer(user_message)

    if intent == "list_visa_types" or decision.get("visa_types"):
        return build_visa_list_answer(user_message, decision, session)

    if "country" in (decision.get("missing_fields") or []):
        return build_missing_country_answer(user_message, decision)

    if intent == "occupation_details":
        return build_occupation_details_answer(user_message, decision, session)

    if intent == "age_details":
        return build_age_details_answer(user_message, decision, session)

    if intent == "occupation_confirmation":
        return build_occupation_confirmation_answer(user_message, decision, session)

    if intent == "relationship_details":
        return build_relationship_details_answer(user_message, decision, session)

    if intent == "relationship_check":
        return build_relationship_check_answer(user_message, decision, session)

    if intent == "relationship_reset":
        return build_relationship_reset_answer(user_message, decision, session)

    if intent == "dependent_residency_inquiry":
        return build_dependent_residency_answer(user_message, decision, session)

    if intent == "residency_admin_inquiry":
        return build_residency_admin_answer(user_message, decision, session)

    if intent == "inside_kuwait_visa_inquiry":
        return build_inside_kuwait_visa_answer(user_message, decision, session)

    if intent == "visa_comparison_inquiry":
        return build_visa_comparison_answer(user_message, decision, session)

    if intent == "system_support_inquiry":
        return build_system_support_answer(user_message, decision, session)

    if intent == "visa_details":
        return build_visa_details_answer(user_message, decision, session)

    if intent == "eligibility_check":
        return build_eligibility_answer(user_message, decision, session)

    if decision.get("available_visa_types"):
        return build_visa_list_answer(user_message, decision, session)

    return build_missing_country_answer(user_message, decision)
