import re

from .rules_engine import first_rule_list, get_age_rule


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
    "gender": "الجنس",
    "relationship": "العلاقة / المرافق",
}

EN_FIELD_NAMES = {
    "country": "country / nationality",
    "visa_type": "visa number",
    "age": "age",
    "valid_age": "valid age",
    "occupation": "occupation",
    "gender": "gender",
    "relationship": "relationship / companion",
}


def is_arabic(text: str) -> bool:
    return bool(re.search(r"[\u0600-\u06ff]", text or ""))


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

    for item in items or []:
        if not isinstance(item, dict):
            continue
        if item.get("allowed", True) is False:
            continue
        for key in keys:
            value = item.get(key)
            if value:
                names.append(str(value).strip())
                break

    return clean_items(names)[:limit]


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

    occupations = first_rule_list(
        rules.get("occupations"),
        rules.get("occupation"),
        rules.get("newOccupation"),
        general_rules.get("occupations"),
        general_rules.get("occupation"),
        general_rules.get("newOccupation"),
    )

    relationships = first_rule_list(
        rules.get("relationship"),
        general_rules.get("relationship"),
    )

    gender = first_rule_list(
        rules.get("gender"),
        general_rules.get("gender"),
    )

    return {
        "age_rule": (min_age, max_age),
        "occupations": occupations,
        "relationships": relationships,
        "gender": gender,
    }


def build_chitchat_answer(user_message: str):
    if is_arabic(user_message):
        return "هلا فيك، أنا بخير. أنا مساعد التأشيرات الذكي، اسألني عن الفيز المتاحة للكويت أو شروط أي فيزا حسب دولتك."
    return "Hello. I am ready to help with Kuwait visa types and requirements based on your country."


def build_context_answer(user_message: str, session: dict):
    arabic = is_arabic(user_message)
    country = country_display(session, arabic=arabic)

    if country:
        return f"أنت مسجل عندي أنك من {country}." if arabic else f"I have your country as {country}."

    return (
        "لسا ما عندي دولتك في هذه المحادثة. اذكر دولتك أو جنسيتك حتى أقدر أبحث لك بدقة."
        if arabic
        else "I do not have your country in this conversation yet. Please provide your country or nationality."
    )


def build_country_ack(user_message: str, session: dict):
    arabic = is_arabic(user_message)
    country = country_display(session, arabic=arabic)

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
    arabic = is_arabic(user_message)
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
    arabic = is_arabic(user_message)
    raw = decision.get("raw_visa_details") or {}
    summary = extract_rule_summary(raw)
    visa_label = format_visa_label(decision.get("visa_type"), decision.get("visa_name"), arabic)
    country = country_display(session, decision, arabic)
    min_age, max_age = summary["age_rule"]
    occupation_names = allowed_names(
        summary["occupations"],
        ["occupationNameAr", "ArabicDescription", "occupationNameEn", "DescriptionEn"] if arabic else ["occupationNameEn", "DescriptionEn", "occupationNameAr", "ArabicDescription"],
        limit=8,
    )
    relationship_names = allowed_names(
        summary["relationships"],
        ["relationNameAr", "arabicDescription", "relationNameEn"] if arabic else ["relationNameEn", "relationNameAr", "arabicDescription"],
        limit=12,
    )

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
                lines.append(f"• المهنة: توجد مهن أو فئات مهنية مسموحة، منها: {', '.join(occupation_names)}.")
            else:
                lines.append("• المهنة: توجد قائمة مهن مسموحة في البيانات.")

        if summary["relationships"]:
            has_rule = True
            if relationship_names:
                lines.append(f"• العلاقة / المرافق: العلاقات الظاهرة ضمن البيانات تشمل: {', '.join(relationship_names)}.")
            else:
                lines.append("• العلاقة / المرافق: توجد قائمة علاقات مسموحة في البيانات.")

        if not has_rule:
            lines.append("• لا تظهر شروط تفصيلية إضافية لهذه الفيزا في البيانات الحالية.")

        missing = decision.get("missing_fields") or []
        if missing:
            readable = "، ".join(field_name(field, True) for field in missing)
            lines.append("")
            lines.append(f"لإكمال فحص الأهلية بشكل أدق أحتاج: {readable}.")

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
        lines.append("- Occupation: this visa has an allowed occupation list.")

    if summary["relationships"]:
        has_rule = True
        lines.append("- Relationship / companion: this visa has an allowed relationship list.")

    if not has_rule:
        lines.append("- No additional detailed rule conditions are visible in the current data.")

    missing = decision.get("missing_fields") or []
    if missing:
        readable = ", ".join(field_name(field, False) for field in missing)
        lines.append("")
        lines.append(f"To complete an eligibility check, I need: {readable}.")

    return "\n".join(lines)


def translate_check(check: dict, arabic: bool):
    message = check.get("message") or ""
    field = check.get("field")
    passed = check.get("passed")

    if not arabic:
        return message or field_name(field, False)

    if field == "age":
        return "العمر ضمن النطاق المسموح." if passed else "العمر خارج النطاق المسموح."
    if field == "occupation":
        return "المهنة مسموحة حسب البيانات." if passed else "المهنة غير مدرجة ضمن المهن المسموحة."
    if field == "relationship":
        return "العلاقة مسموحة حسب البيانات." if passed else "العلاقة غير مسموحة حسب البيانات."
    if field == "gender":
        return "الجنس مطابق للشروط." if passed else "يوجد تقييد على الجنس لهذه الفيزا."

    return message or field_name(field, True)


def build_eligibility_answer(user_message: str, decision: dict, session: dict):
    arabic = is_arabic(user_message)
    checks = decision.get("checks") or []
    passed = [check for check in checks if check.get("passed") is True]
    failed = [check for check in checks if check.get("passed") is False]
    missing = decision.get("missing_fields") or []
    visa_label = format_visa_label(decision.get("visa_type"), decision.get("visa_name"), arabic)
    country = country_display(session, decision, arabic)

    lines = []

    if arabic:
        lines.append("نتيجة الفحص المبدئي حسب قواعد التأشيرات المتاحة:")
        lines.append(f"الحالة: {status_text(decision.get('status'), True)}")
        lines.append(f"البلد: {country}")
        lines.append(f"الفيزا: {visa_label}")

        if passed:
            lines.append("")
            lines.append("الفحوصات المطابقة:")
            lines.extend(f"✅ {translate_check(check, True)}" for check in passed)

        if failed:
            lines.append("")
            lines.append("الفحوصات غير المطابقة:")
            lines.extend(f"❌ {translate_check(check, True)}" for check in failed)

        if missing:
            readable = "، ".join(field_name(field, True) for field in missing)
            lines.append("")
            lines.append(f"معلومات مطلوبة لإكمال الفحص: {readable}.")

        return "\n".join(lines)

    lines.append("Preliminary eligibility result based on available visa rules:")
    lines.append(f"Status: {status_text(decision.get('status'), False)}")
    lines.append(f"Country: {country}")
    lines.append(f"Visa: {visa_label}")

    if passed:
        lines.append("")
        lines.append("Passed checks:")
        lines.extend(f"- {translate_check(check, False)}" for check in passed)

    if failed:
        lines.append("")
        lines.append("Failed checks:")
        lines.extend(f"- {translate_check(check, False)}" for check in failed)

    if missing:
        readable = ", ".join(field_name(field, False) for field in missing)
        lines.append("")
        lines.append(f"Missing information: {readable}.")

    return "\n".join(lines)


def build_api_error_answer(user_message: str):
    if is_arabic(user_message):
        return "تعذر الاتصال بخدمة قواعد التأشيرات حالياً. حاول مرة ثانية بعد قليل."
    return "The visa rules service could not be reached right now. Please try again shortly."


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

    if intent in {"visa_details", "relationship_check"}:
        return build_visa_details_answer(user_message, decision, session)

    if intent == "eligibility_check":
        return build_eligibility_answer(user_message, decision, session)

    if decision.get("available_visa_types"):
        return build_visa_list_answer(user_message, decision, session)

    return build_missing_country_answer(user_message, decision)
