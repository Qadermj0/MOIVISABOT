import re

from .countries import COUNTRIES, resolve_country


ARABIC_DIACRITICS = re.compile(r"[\u064b-\u065f\u0670]")

VISA_WORDS = [
    "فيزا",
    "فيزه",
    "تاشيرة",
    "تأشيرة",
    "سمة",
    "سمه",
    "الكويت",
    "visa",
]

VISA_QUERY_WORDS = [
    "فيزا",
    "فيزه",
    "تاشيرة",
    "تأشيرة",
    "سمة",
    "سمه",
    "visa",
]

LIST_WORDS = [
    "شنو الفيز",
    "وش الفيز",
    "ايش الفيز",
    "ما هي الفيز",
    "انواع الفيز",
    "أنواع الفيز",
    "الفيز المسموح",
    "المسموحه",
    "المسموحة",
    "المتاحة",
    "المتاحه",
    "المتوفره",
    "المتوفرة",
    "اطلع الكويت",
    "ادخل الكويت",
    "للتقديم",
    "available visas",
    "visa types",
    "all visas",
]

DETAILS_WORDS = [
    "تفاصيل",
    "شروط",
    "الشرط",
    "مطلوب",
    "المطلوب",
    "متطلبات",
    "المتطلبات",
    "وش مطلوب",
    "شنو مطلوب",
    "كيف اقدم",
    "ابغى اسجل",
    "ابي اسجل",
    "أسجل",
    "اسجل",
    "التقديم",
    "requirements",
    "conditions",
    "details",
    "what is required",
]

CHECK_WORDS = [
    "بقدر",
    "اقدر",
    "أقدر",
    "ينفع",
    "مسموح",
    "اقدم",
    "أقدم",
    "مؤهل",
    "مؤهلة",
    "apply",
    "eligible",
    "can i",
    "allowed",
]

GREETING_WORDS = [
    "مرحبا",
    "هلا",
    "اهلا",
    "أهلا",
    "السلام عليكم",
    "صباح الخير",
    "مساء الخير",
    "شلونك",
    "كيفك",
    "hello",
    "hi",
    "hey",
]

THANKS_WORDS = [
    "شكرا",
    "يعطيك العافيه",
    "يعطيك العافية",
    "مشكور",
    "thanks",
    "thank you",
]

CONTEXT_COUNTRY_QUESTIONS = [
    "انا من وين",
    "أانا من وين",
    "من وين انا",
    "وش دولتي",
    "شنو دولتي",
    "ايش دولتي",
    "جنسيتي شنو",
    "شنو جنسيتي",
    "what country am i from",
    "my country",
    "my nationality",
]

KNOWN_OCCUPATIONS = [
    "استاذ",
    "أستاذ",
    "أستاذة",
    "استاذة",
    "نائب",
    "نائبة",
    "عضو مجلس",
    "عضو المجالس",
    "رئيس",
    "رئيسة",
    "مهندس",
    "مهندسة",
    "طبيب",
    "طبيبة",
    "دكتور",
    "دكتورة",
    "محامي",
    "محامية",
    "ممرض",
    "ممرضة",
    "مدرس",
    "مدرسة",
    "معلم",
    "معلمة",
    "مبرمج",
    "مبرمجة",
    "محاسب",
    "محاسبة",
    "مدير",
    "مديرة",
    "طالب",
    "طالبة",
    "رجل اعمال",
    "سيدة اعمال",
    "موظف",
    "موظفة",
    "engineer",
    "doctor",
    "lawyer",
    "nurse",
    "teacher",
    "programmer",
    "accountant",
    "manager",
    "student",
    "pilot",
]


def normalize_text(value: str) -> str:
    text = str(value or "").strip().lower()
    text = ARABIC_DIACRITICS.sub("", text)
    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ٱ": "ا",
        "ى": "ي",
        "ة": "ه",
        "ؤ": "و",
        "ئ": "ي",
        "ـ": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^\w\s\u0600-\u06ff]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def has_any(text: str, words: list[str]) -> bool:
    normalized = normalize_text(text)
    return any(normalize_text(word) in normalized for word in words)


def resolve_applicant_country(text: str):
    raw_text = str(text or "").strip()
    normalized = normalize_text(text)
    if not normalized:
        return None

    origin_pattern = re.compile(
        r"(?:انا|اني|احنا|نحن|جنسيتي|الجنسية|مواطن|مواطنة|مواطنه|مقيم|مقيمه|مقيمة|from|nationality|citizen)\s*(?:من|is|:)?\s*$",
        re.IGNORECASE,
    )
    destination_words = [
        "اطلع",
        "ادخل",
        "اروح",
        "ازور",
        "اسافر",
        "الى",
        "الي",
        "للكويت",
        "الكويت",
        "to",
        "visit",
        "enter",
        "travel",
    ]

    candidates = []

    for country in COUNTRIES:
        ocr_code = str(country.get("ocr_code") or "").upper()
        exact_code_pattern = re.compile(rf"(?<![A-Za-z]){re.escape(ocr_code)}(?![A-Za-z])")
        for match in exact_code_pattern.finditer(raw_text):
            before_raw = raw_text[max(0, match.start() - 45):match.start()]
            before = normalize_text(before_raw)
            is_only_code = raw_text.upper() == ocr_code
            has_origin_context = bool(origin_pattern.search(before)) or before.endswith("من ")
            if not is_only_code and not has_origin_context:
                continue

            score = 180 if has_origin_context else 120
            candidates.append((score, -match.start(), country))

        aliases = [
            country.get("country_name_ar"),
            country.get("country_name_en"),
            *(country.get("aliases") or []),
        ]
        ocr_norm = normalize_text(ocr_code)

        for alias in aliases:
            alias_norm = normalize_text(alias)
            if not alias_norm or len(alias_norm) < 2:
                continue
            if alias_norm == ocr_norm:
                continue

            alias_variants = {alias_norm}
            if alias_norm.startswith("ال"):
                alias_variants.add(f"لل{alias_norm[2:]}")
                alias_variants.add(f"ل{alias_norm[2:]}")
            alias_variants.add(f"ل{alias_norm}")

            variant_pattern = "|".join(
                re.escape(variant)
                for variant in sorted(alias_variants, key=len, reverse=True)
            )
            pattern = re.compile(rf"(?<!\w)(?:{variant_pattern})(?!\w)", re.IGNORECASE)

            for match in pattern.finditer(normalized):
                before = normalized[max(0, match.start() - 45):match.start()]
                after = normalized[match.end():match.end() + 35]
                has_origin_context = bool(origin_pattern.search(before)) or before.endswith("من ")
                has_destination_context = any(
                    normalize_text(word) in before[-22:] or normalize_text(word) in after[:22]
                    for word in destination_words
                )

                if country.get("ocr_code") == "KWT" and not has_origin_context:
                    continue

                score = len(alias_norm)
                if has_origin_context:
                    score += 140
                if country.get("ocr_code") != "KWT":
                    score += 25
                if country.get("ocr_code") == "KWT" and not has_origin_context:
                    score -= 50

                candidates.append((score, -match.start(), country))

    if not candidates:
        return None

    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    best_score, _, best_country = candidates[0]
    return best_country if best_score > 0 else None


def is_arabic(text: str) -> bool:
    return bool(re.search(r"[\u0600-\u06ff]", text or ""))


def extract_visa_type(text: str):
    patterns = [
        r"(?:فيزا|فيزه|تأشيرة|تاشيرة|سمة|سمه|visa(?:\s*no\.?)?)\s*(?:رقم\s*)?(\d{1,4})",
        r"(?:رقم|نوع)\s*(\d{1,4})",
        r"\bvisa\s*(\d{1,4})\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None


def extract_age(text: str):
    patterns = [
        r"(?:عمري|عمرى|العمر|سنّي|سني)\s*(\d{1,3})",
        r"(?:my\s+age\s+is|age\s+is|age|i am)\s*(\d{1,3})",
        r"\b(\d{1,3})\s*(?:سنه|سنة|عام|years old)\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None


def extract_gender(text: str):
    normalized = normalize_text(text)

    if any(word in normalized for word in ["ذكر", "رجل", "ولد", "male", "man"]):
        return "male"

    if any(word in normalized for word in ["انثي", "انثى", "امرأه", "امراه", "بنت", "female", "woman"]):
        return "female"

    return None


def extract_occupation(text: str):
    normalized = normalize_text(text)

    for occupation in KNOWN_OCCUPATIONS:
        if normalize_text(occupation) in normalized:
            return occupation

    patterns = [
        r"(?:مهنتي|وظيفتي|اعمل ك|أعمل ك|انا اعمل ك|انا أعمل ك)\s+([^\d،,.!?]{2,40})",
        r"(?:اشتغل|أشتغل|انا اشتغل|انا أشتغل|اعمل|أعمل|شغلي|عملي)\s+([^\d،,.!?]{2,40})",
        r"(?:لو مهنتي|اذا مهنتي|إذا مهنتي|مهنتي|لو كنت|اذا كنت|إذا كنت|كنت)\s+([^\d،,.!?]{2,40})",
        r"(?:i am|i'm|im)\s+(?:a|an)?\s*([a-zA-Z][a-zA-Z\s-]{1,40})",
        r"(?:my job is|i work as|occupation is)\s+([a-zA-Z\s]{2,40})",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            continue

        candidate = clean_occupation_candidate(match.group(1))
        candidate_norm = normalize_text(candidate)
        candidate_norm = re.sub(r"^(هي|هو|اني|انا)\s+", "", candidate_norm).strip()
        if not candidate_norm.startswith("من ") and not has_any(candidate, VISA_WORDS + LIST_WORDS):
            return candidate_norm or candidate

    return None


def clean_occupation_candidate(candidate: str):
    text = str(candidate or "").strip()
    text = re.split(
        r"\b(?:and|with|my age|age is|age|visa|for)\b|[,،.!?;]",
        text,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    text = re.sub(r"^(?:a|an|the)\s+", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_relationship(text: str):
    normalized = normalize_text(text)

    relation_patterns = {
        "الزوجة": ["زوجتي", "مرتي", "زوجة", "wife"],
        "الزوج": ["زوجي", "زوج", "husband"],
        "الابن": ["ابني", "إبني", "ابن", "ولدي", "son"],
        "الابنة": ["بنتي", "ابنتي", "إبنتي", "daughter"],
        "الأم": ["امي", "أمي", "والدتي", "mother"],
        "الأب": ["ابي", "أبي", "والدي", "father"],
        "الأخ": ["اخي", "أخي", "brother"],
        "الأخت": ["اختي", "أختي", "sister"],
        "مرافق": ["مرافق", "companion"],
    }

    for relation, words in relation_patterns.items():
        for word in words:
            if re.search(rf"(?<!\w){re.escape(normalize_text(word))}(?!\w)", normalized, re.IGNORECASE):
                return relation

    return None


def is_context_country_question(text: str) -> bool:
    return has_any(text, CONTEXT_COUNTRY_QUESTIONS)


def is_chitchat(text: str, country) -> bool:
    if country:
        return False

    if has_any(text, VISA_WORDS + LIST_WORDS + DETAILS_WORDS + CHECK_WORDS):
        return False

    if extract_visa_type(text) or extract_age(text) or extract_occupation(text):
        return False

    return has_any(text, GREETING_WORDS + THANKS_WORDS)


def detect_intent(
    text: str,
    country,
    visa_type,
    age,
    occupation,
    gender,
    relationship,
    context: dict,
):
    message_has_country = bool(country)
    context_has_country = bool(context.get("ocr_code"))
    has_country = message_has_country or context_has_country
    context_visa_type = context.get("visa_type")
    effective_visa_type = visa_type or context_visa_type

    if is_context_country_question(text):
        return "context_question"

    if is_chitchat(text, country):
        return "chitchat"

    if relationship:
        return "relationship_check"

    if has_any(text, LIST_WORDS):
        return "list_visa_types"

    if effective_visa_type and has_any(text, DETAILS_WORDS):
        return "visa_details"

    if effective_visa_type and (has_any(text, CHECK_WORDS) or age or occupation or gender):
        return "eligibility_check"

    if message_has_country and not visa_type and not context_visa_type:
        if has_any(text, VISA_QUERY_WORDS):
            return "list_visa_types"
        return "provide_country"

    if message_has_country and context_visa_type:
        return "visa_details"

    if effective_visa_type and has_country:
        return "visa_details"

    if (age or occupation or gender) and context_has_country and context_visa_type:
        return "eligibility_check"

    return "general_question"


def should_consult_gemini(intent: str, text: str, occupation, gender) -> bool:
    if intent in {"chitchat", "context_question", "list_visa_types", "visa_details", "provide_country"}:
        return False
    if occupation or gender:
        return False
    return has_any(text, CHECK_WORDS) and has_any(text, VISA_WORDS)


def analyze_message(user_message: str, context: dict, gemini_service):
    local_country = resolve_applicant_country(user_message)
    local_visa_type = extract_visa_type(user_message)
    local_age = extract_age(user_message)
    local_relationship = extract_relationship(user_message)
    local_occupation = extract_occupation(user_message)
    local_gender = extract_gender(user_message)

    intent = detect_intent(
        text=user_message,
        country=local_country,
        visa_type=local_visa_type,
        age=local_age,
        occupation=local_occupation,
        gender=local_gender,
        relationship=local_relationship,
        context=context,
    )

    gemini_data = {}
    if should_consult_gemini(intent, user_message, local_occupation, local_gender):
        gemini_data = gemini_service.extract_query(user_message, context)

    country = local_country or resolve_country(gemini_data.get("country_text", ""))
    visa_type = local_visa_type or gemini_data.get("visa_type")
    age = local_age or gemini_data.get("age")
    occupation = local_occupation or gemini_data.get("occupation")
    gender = local_gender or gemini_data.get("gender")

    # Relationship must only come from explicit local extraction to avoid inference.
    relationship = local_relationship

    intent = detect_intent(
        text=user_message,
        country=country,
        visa_type=visa_type,
        age=age,
        occupation=occupation,
        gender=gender,
        relationship=relationship,
        context=context,
    )

    return {
        "intent": intent,
        "country": country,
        "ocr_code": country["ocr_code"] if country else None,
        "country_name": country["country_name_ar"] if country else None,
        "country_name_en": country["country_name_en"] if country else None,
        "visa_type": visa_type,
        "age": age,
        "occupation": occupation,
        "gender": gender,
        "relationship": relationship,
        "is_follow_up": bool(context.get("ocr_code") or context.get("visa_type")),
    }
