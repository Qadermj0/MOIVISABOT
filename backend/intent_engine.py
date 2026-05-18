import re

from .countries import (
    COUNTRIES,
    country_alias_variants,
    is_negated_country_reference,
    resolve_country,
)


ARABIC_DIACRITICS = re.compile(r"[\u064b-\u065f\u0670]")

VISA_WORDS = [
    "فيزا",
    "فيزه",
    "فيز",
    "تاشيرة",
    "تأشيرة",
    "تاشيرات",
    "تأشيرات",
    "التاشيرات",
    "التأشيرات",
    "سمة",
    "سمه",
    "الكويت",
    "visa",
]

VISA_QUERY_WORDS = [
    "فيزا",
    "فيزه",
    "فيز",
    "تاشيرة",
    "تأشيرة",
    "تاشيرات",
    "تأشيرات",
    "التاشيرات",
    "التأشيرات",
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
    "شنو التاشيرات",
    "شنو التأشيرات",
    "شو التاشيرات",
    "شو التأشيرات",
    "ايش التاشيرات",
    "ايش التأشيرات",
    "وش التاشيرات",
    "وش التأشيرات",
    "ما هي التاشيرات",
    "ما هي التأشيرات",
    "انواع التاشيرات",
    "أنواع التأشيرات",
    "التاشيرات المتاحة",
    "التأشيرات المتاحة",
    "الفيز المسموح",
    "المسموحه",
    "المسموحة",
    "المتاحة",
    "المتاحه",
    "المتوفره",
    "المتوفرة",
    "متوفر",
    "متوفره",
    "متوفرة",
    "شو متوفر",
    "شنو متوفر",
    "ايش متوفر",
    "وش متوفر",
    "شو عندهم",
    "شنو عندهم",
    "ايش عندهم",
    "وش عندهم",
    "شو عند",
    "شنو عند",
    "ايش عند",
    "وش عند",
    "what do they have",
    "what visas do they have",
    "اطلع الكويت",
    "ادخل الكويت",
    "للتقديم",
    "available visas",
    "visa types",
    "all visas",
]

OCCUPATION_QUERY_WORDS = [
    "المهن",
    "مهن",
    "المهنة",
    "مهنة",
    "وظائف",
    "الوظائف",
    "occupation",
    "occupations",
    "profession",
    "professions",
    "jobs",
]

RELATIONSHIP_QUERY_WORDS = [
    "العلاقات",
    "علاقات",
    "العلاقة",
    "علاقة",
    "صلة",
    "الصلات",
    "صلة القرابة",
    "قرابة",
    "القرايب",
    "المرافق",
    "مرافق",
    "المرافقين",
    "اصطحاب",
    "اصطحب",
    "relationship",
    "relationships",
    "relation",
    "relations",
    "companion",
    "companions",
    "dependent",
    "dependents",
]

COMPARISON_WORDS = [
    "أيهما",
    "ايهما",
    "ايهم",
    "أسهل",
    "اسهل",
    "الأفضل",
    "افضل",
    "أفضل",
    "الفرق",
    "فرق",
    "مقارنة",
    "قارن",
    "ولا",
    "which is easier",
    "which one is easier",
    "compare",
    "comparison",
    "difference",
    "versus",
    " vs ",
]

AGE_QUERY_WORDS = [
    "العمر",
    "عمر",
    "السن",
    "سن",
    "الاعمار",
    "الأعمار",
    "age",
    "ages",
    "age requirement",
    "age requirements",
    "what age",
    "age allowed",
]

OCCUPATION_CONFIRMATION_WORDS = [
    "فقط",
    "بس",
    "يعني",
    "بس اساتذه",
    "بس أساتذة",
    "محصور",
    "محصورة",
    "حصرا",
    "حصراً",
    "only",
    "just",
    "only professor",
    "only professors",
]

RELATIONSHIP_DECLINE_WORDS = [
    "لا ما",
    "لا اريد",
    "لا أريد",
    "ما اريد",
    "ما أريد",
    "ما ابغى",
    "ما أبغى",
    "ما ابي",
    "ما أبي",
    "ما بدي",
    "بدون",
    "من غير",
    "ما رح اجيب",
    "ما راح اجيب",
    "ما رح اصطحب",
    "ما راح اصطحب",
    "لا تجيب",
    "لا اصطحاب",
    "no companion",
    "no wife",
    "without",
    "not with",
    "not bringing",
    "do not want to bring",
    "don't want to bring",
    "i do not want to bring",
    "i don't want to bring",
    "i will not bring",
]

RELATIONSHIP_SWITCH_QUESTION_WORDS = [
    "هل",
    "بقدر",
    "اقدر",
    "أقدر",
    "يمكنني",
    "ممكن",
    "خلص",
    "بطلت",
    "بدل",
    "instead",
    "can i",
    "could i",
    "is it possible",
]

DEPENDENT_RESIDENCY_WORDS = [
    "التحاق بعائل",
    "التحاق عائل",
    "الالتحاق بعائل",
    "إلتحاق بعائل",
    "اقامة التحاق",
    "إقامة التحاق",
    "اقامه التحاق",
    "اقامة عائلية",
    "إقامة عائلية",
    "اقامه عائليه",
    "كفالة عائلية",
    "كفاله عائليه",
    "زوجتي وابنائي",
    "زوجتي وأبنائي",
    "زوجتي تعيش معي",
    "زوجتي تعيش معاي",
    "اجيب زوجتي",
    "أجيب زوجتي",
    "بدي اجيب زوجتي",
    "بدي أجيب زوجتي",
    "ابغى اجيب زوجتي",
    "ابي اجيب زوجتي",
    "تعيش معي",
    "تعيش معاي",
    "ابنائي",
    "أبنائي",
    "زوجتي واولادي",
    "زوجتي وأولادي",
    "wife live with me",
    "bring my wife",
    "bring my wife to live",
    "my wife to live with me",
    "dependent residency",
    "family residency",
    "family joining",
    "joining family",
]

DEPENDENT_RESIDENCY_STRONG_WORDS = [
    "التحاق",
    "إلتحاق",
    "اقامة",
    "إقامة",
    "اقامه",
    "كفالة",
    "كفاله",
    "تعيش معي",
    "تعيش معاي",
    "تعيش وياي",
    "تسكن معي",
    "تسكن معاي",
    "زوجتي وابنائي",
    "زوجتي وأبنائي",
    "زوجتي واولادي",
    "زوجتي وأولادي",
    "ابنائي",
    "أبنائي",
    "اولادي",
    "أولادي",
    "راتب",
    "شرط الراتب",
    "dependent residency",
    "family residency",
    "family joining",
    "joining family",
    "live with me",
    "residency",
    "salary",
]

FAMILY_VISIT_APPLICATION_WORDS = [
    "اجيب زوجتي",
    "أجيب زوجتي",
    "اجلب زوجتي",
    "أجلب زوجتي",
    "اجسب زوجتي",
    "أجسب زوجتي",
    "اصطحب زوجتي",
    "أصطحب زوجتي",
    "اقدم لزوجتي",
    "أقدم لزوجتي",
    "اسجل لزوجتي",
    "أسجل لزوجتي",
    "ابغى اجيب زوجتي",
    "ابغى أجيب زوجتي",
    "ابي اجيب زوجتي",
    "بدي اجيب زوجتي",
    "بدي أجيب زوجتي",
    "زوجتي على الكويت",
    "زوجتي للكويت",
    "زوجتي الى الكويت",
    "زوجتي إلى الكويت",
    "bring my wife",
    "bring wife",
    "apply for my wife",
    "register my wife",
    "wife to kuwait",
]

RESIDENCY_ADMIN_WORDS = [
    "تحويل الزيارة",
    "تحويل هذه الزيارة",
    "تحويل سمة",
    "تحويل فيزا",
    "تحويلها إلى إقامة",
    "تحويلها الى اقامة",
    "تحويلها لإقامة",
    "اقامة عمل",
    "إقامة عمل",
    "اقامه عمل",
    "مادة 18",
    "ماده 18",
    "مادة (18)",
    "ماده (18)",
    "المادة 18",
    "الماده 18",
    "انتهت صلاحية",
    "انتهاء صلاحية",
    "منتهية",
    "منتهيه",
    "تجاوزت الزيارة",
    "غرامات",
    "غرامة",
    "غرامه",
    "التأخير",
    "التاخير",
    "دفعها إلكترونياً",
    "دفعها الكترونيا",
    "دفع الغرامات",
    "دفع مخالفات",
    "مغادرة البلاد",
    "مغادره البلاد",
    "بدون مغادرة",
    "دون الحاجة لمغادرة",
    "شؤون الاقامة",
    "شؤون الإقامة",
    "الاقامة",
    "الإقامة",
    "residency affairs",
    "work residency",
    "article 18",
    "article (18)",
    "convert visit",
    "convert visa",
    "overstay",
    "expired visit",
    "expired visa",
    "fine",
    "fines",
    "penalty",
    "leave the country",
    "without leaving",
    "pay online",
    "salary requirement",
]

INSIDE_KUWAIT_VISA_WORDS = [
    "من داخل الكويت",
    "داخل الكويت",
    "وانا داخل الكويت",
    "وأنا داخل الكويت",
    "واني داخل الكويت",
    "موجود في الكويت",
    "موجوده في الكويت",
    "موجودة في الكويت",
    "متواجد في الكويت",
    "متواجدة في الكويت",
    "متواجده في الكويت",
    "انا في الكويت",
    "أنا في الكويت",
    "بفيزا زيارة سابقة",
    "فيزا زيارة سابقة",
    "زيارة سابقة",
    "داخل بفيزا زيارة",
    "دخلت بفيزا زيارة",
    "currently in kuwait",
    "inside kuwait",
    "from inside kuwait",
    "in kuwait on a visit visa",
    "in kuwait on visit visa",
    "previous visit visa",
]

SYSTEM_SUPPORT_WORDS = [
    "رفع صورة جواز",
    "رفع صوره جواز",
    "صورة جواز",
    "صوره جواز",
    "جواز سفري",
    "جواز السفر",
    "رفع الجواز",
    "مشكلة بالنظام",
    "مشكله بالنظام",
    "مشاكل النظام",
    "خطأ بالنظام",
    "خطا بالنظام",
    "اخطاء النظام",
    "أخطاء النظام",
    "upload passport",
    "passport upload",
    "passport image",
    "passport photo",
    "system error",
    "technical error",
    "الموقع شغال",
    "الموقع يعمل",
    "هل الموقع شغال",
    "هل الموقع يعمل",
    "يوم السبت",
    "السبت",
    "اوقات العمل",
    "أوقات العمل",
    "ساعات العمل",
    "دوام",
    "working hours",
    "site working",
    "website working",
    "open on saturday",
    "saturday",
]

DETAILS_WORDS = [
    "تفاصيل",
    "شروط",
    "الشرط",
    "مطلوب",
    "المطلوب",
    "متطلبات",
    "المتطلبات",
    "الأوراق",
    "الاوراق",
    "المستندات",
    "الوثائق",
    "documents",
    "papers",
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
    "مسموحة",
    "اقدم",
    "أقدم",
    "بدي اقدم",
    "بدي أقدم",
    "ابغى اقدم",
    "ابغى أقدم",
    "ابي اقدم",
    "ابي أقدم",
    "اسجل",
    "أسجل",
    "ابغى اسجل",
    "ابي اسجل",
    "بدي اسجل",
    "ابغى اروح",
    "ابغى أروح",
    "ابي اروح",
    "ابي أروح",
    "بدي اروح",
    "بدي أروح",
    "ابغى اطلع",
    "ابغى أطلع",
    "ابي اطلع",
    "ابي أطلع",
    "بدي اطلع",
    "بدي أطلع",
    "التقديم",
    "يمكنني التقديم",
    "هل يمكنني التقديم",
    "مؤهل",
    "مؤهلة",
    "apply",
    "eligible",
    "can i",
    "allowed",
]

STRONG_CHECK_WORDS = [
    "بقدر",
    "اقدر",
    "أقدر",
    "ينفع",
    "مسموح",
    "مسموحة",
    "مؤهل",
    "مؤهلة",
    "هل اقدر",
    "هل أقدر",
    "بدي اقدم",
    "بدي أقدم",
    "ابغى اقدم",
    "ابغى أقدم",
    "ابي اقدم",
    "ابي أقدم",
    "اسجل",
    "أسجل",
    "ابغى اسجل",
    "ابي اسجل",
    "بدي اسجل",
    "ابغى اروح",
    "ابغى أروح",
    "ابي اروح",
    "ابي أروح",
    "بدي اروح",
    "بدي أروح",
    "ابغى اطلع",
    "ابغى أطلع",
    "ابي اطلع",
    "ابي أطلع",
    "بدي اطلع",
    "بدي أطلع",
    "يمكنني التقديم",
    "هل يمكنني التقديم",
    "can i",
    "eligible",
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
    "مدير مبيعات",
    "مديرة مبيعات",
    "قاضي",
    "قاضية",
    "قضاة",
    "القضاة",
    "القضاه",
    "مهندس برمجيات",
    "مهندسة برمجيات",
    "مطور برمجيات",
    "مبرمج برمجيات",
    "فل ستاك",
    "فول ستاك",
    "ديف اوبس",
    "ديف أوبس",
    "عالم بيانات",
    "محلل بيانات",
    "نظم معلومات",
    "اخصائي نظم معلومات",
    "أخصائي نظم معلومات",
    "خبير امن سيبراني",
    "خبير أمن سيبراني",
    "مدير شركة",
    "صاحب شركة",
    "راعي أعمال",
    "راعي اعمال",
    "رائد أعمال",
    "رائد اعمال",
    "صيدلي",
    "صيدلية",
    "صيدلاني",
    "صيدلانية",
    "صيادلة",
    "الصيادلة",
    "استاذ",
    "أستاذ",
    "أستاذة",
    "استاذة",
    "ستاذ",
    "ستاد",
    "ستاذة",
    "اساتذة",
    "اساتذه",
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
    "طيار",
    "طيارة",
    "جيولوجي",
    "جيولوجية",
    "رجل اعمال",
    "سيدة اعمال",
    "موظف",
    "موظفة",
    "engineer",
    "doctor",
    "lawyer",
    "nurse",
    "teacher",
    "software engineer",
    "full stack developer",
    "full-stack developer",
    "frontend developer",
    "front end developer",
    "backend developer",
    "back end developer",
    "software developer",
    "software eng",
    "software programmer",
    "devops engineer",
    "dev ops engineer",
    "data scientist",
    "data analyst",
    "systems analyst",
    "information systems",
    "it specialist",
    "it professional",
    "developer",
    "cyber security expert",
    "ceo",
    "chief executive officer",
    "hr specialist",
    "human resources specialist",
    "pr manager",
    "public relations manager",
    "pharmacist",
    "pharmacists",
    "programmer",
    "accountant",
    "manager",
    "student",
    "pilot",
    "professor",
    "president",
    "presidents",
    "member of council",
    "member of councils",
    "members of council",
    "members of councils",
    "council member",
    "council members",
    "real estate owner",
    "real estate owners",
    "real estate",
    "real state",
    "property owner",
    "property owners",
    "property investor",
]

VISA_TYPE_NAME_ALIASES = {
    1: ["government work", "work government", "عمل حكومة", "عمل حكومي"],
    2: ["private sector work", "private work", "عمل اهلي", "عمل أهلي", "عمل خاص"],
    6: ["study visa", "student visa", "دراسة", "طالب"],
    7: ["medical treatment", "treatment visa", "علاج"],
    8: ["commercial visit", "business visit", "زيارة تجارية", "تجارية"],
    9: ["government visit", "زيارة حكومية", "حكومية"],
    10: ["family visit", "family visa", "family visit visa", "family entry visa", "زيارة عائلية", "عائلية"],
    11: ["embassy visit", "زيارة سفارة", "سفارة"],
    14: ["multiple return", "عودة عدة سفرات", "عدة سفرات"],
    16: ["tourist visa", "tourism visa", "tourism entry visa", "tourism", "tourist", "vacation", "holiday", "leisure trip", "فيزا سياحية", "تأشيرة سياحية", "سمة دخول للسياحة", "سياحة", "سياحي", "سياحية", "السياحة", "اجازة", "إجازة", "رحلة سياحية"],
    19: ["return visa", "عودة"],
    20: ["special entry", "special visa", "سمة دخول خاصة", "دخول خاصة", "خاصه", "خاصة"],
}


def normalize_text(value: str) -> str:
    text = str(value or "").strip().lower()
    text = ARABIC_DIACRITICS.sub("", text)
    text = text.replace("لل ", "لل").replace("ل ", "ل")
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


def is_occupation_details_question(text: str) -> bool:
    return has_any(text, OCCUPATION_QUERY_WORDS)


def is_relationship_details_question(text: str) -> bool:
    return has_any(text, RELATIONSHIP_QUERY_WORDS)


def is_age_details_question(text: str) -> bool:
    return has_any(text, AGE_QUERY_WORDS)


def is_occupation_confirmation_question(text: str, context: dict) -> bool:
    has_confirmation = has_any(text, OCCUPATION_CONFIRMATION_WORDS)
    has_occupation_reference = (
        bool(extract_occupation(text))
        or is_occupation_details_question(text)
        or has_any(text, ["اساتذه", "أساتذة", "استاذ", "أستاذ", "professor", "professors"])
    )
    follows_occupation_answer = context.get("last_intent") == "occupation_details"

    return has_confirmation and (has_occupation_reference or follows_occupation_answer)


def is_relationship_decline(text: str, relationship, context: dict) -> bool:
    has_relationship_context = bool(relationship) or bool(context.get("relationship"))
    follows_relationship_answer = context.get("last_intent") == "relationship_check"
    if (
        is_family_visit_application_question(text)
        and has_any(text, RELATIONSHIP_SWITCH_QUESTION_WORDS)
    ):
        return False
    return (has_relationship_context or follows_relationship_answer) and has_any(text, RELATIONSHIP_DECLINE_WORDS)


def has_explicit_age_cue(text: str) -> bool:
    normalized = normalize_text(text)
    cue_words = [
        "عمري",
        "العمر",
        "سني",
        "سنّي",
        "عندي",
        "age",
        "years old",
        "year old",
    ]
    return has_any(text, cue_words) or bool(
        re.search(r"\b\d{1,3}\s*(?:سنه|سنة|عام|years?\s+old)\b", normalized, re.IGNORECASE)
    )


def has_explicit_occupation_cue(text: str) -> bool:
    cue_words = [
        "مهنتي",
        "المهنة",
        "مهنة",
        "وظيفتي",
        "الوظيفة",
        "وظيفة",
        "شغلي",
        "عملي",
        "اشتغل",
        "أشتغل",
        "اعمل",
        "أعمل",
        "job",
        "occupation",
        "profession",
        "work as",
        "my work",
        "real estate",
        "real state",
        "property owner",
        "own property",
        "own real estate",
        "have property",
        "have real estate",
    ]
    return has_any(text, cue_words)


def is_kuwait_current_location_reference(text: str) -> bool:
    normalized = normalize_text(text)
    if not normalized:
        return False

    kuwait_terms = ["الكويت", "kuwait"]
    location_cues = [
        "داخل",
        "من داخل",
        "في",
        "موجود",
        "موجوده",
        "موجودة",
        "متواجد",
        "متواجده",
        "متواجدة",
        "مقيم",
        "مقيمه",
        "مقيمة",
        "زيارة سابقة",
        "فيزا زيارة سابقة",
        "inside",
        "currently in",
        "in kuwait",
        "from inside",
        "visit visa",
        "previous visit",
    ]

    return any(term in normalized for term in kuwait_terms) and any(
        normalize_text(cue) in normalized for cue in location_cues
    )


def is_residence_location_context(before_text: str) -> bool:
    before = normalize_text(before_text)
    residence_endings = [
        "مقيم في",
        "مقيمه في",
        "مقيمة في",
        "ساكن في",
        "ساكنه في",
        "ساكنة في",
        "اعيش في",
        "أعيش في",
        "موجود في",
        "موجوده في",
        "موجودة في",
        "متواجد في",
        "resident in",
        "residing in",
        "living in",
        "based in",
        "located in",
        "currently in",
    ]
    work_endings = [
        "شغال في",
        "شغاله في",
        "شغالة في",
        "شغالين في",
        "اشتغل في",
        "أشتغل في",
        "اعمل في",
        "أعمل في",
        "وظيفتي في",
        "عملي في",
        "work in",
        "works in",
        "working in",
        "employed in",
    ]
    if any(before.endswith(normalize_text(ending)) for ending in residence_endings + work_endings):
        return True

    location_tail = before[-70:]
    work_markers = [
        "شغال",
        "شغاله",
        "شغالة",
        "اشتغل",
        "اعمل",
        "أعمل",
        "وظيفتي",
        "عملي",
        "work",
        "works",
        "working",
        "employed",
    ]
    return (
        (location_tail.endswith("في") or location_tail.endswith("in"))
        and any(normalize_text(marker) in location_tail for marker in work_markers)
    )


def _country_alias_pattern(country: dict):
    aliases = [
        country.get("country_name_ar"),
        country.get("country_name_en"),
        *(country.get("aliases") or []),
    ]
    variants = set()
    ocr_norm = normalize_text(country.get("ocr_code"))
    for alias in aliases:
        alias_norm = normalize_text(alias)
        if not alias_norm or alias_norm == ocr_norm:
            continue
        variants.update(country_alias_variants(alias))

    if not variants:
        return None

    return re.compile(
        rf"(?<!\w)(?:{'|'.join(re.escape(variant) for variant in sorted(variants, key=len, reverse=True))})(?!\w)",
        re.IGNORECASE,
    )


def _has_country_origin_context(before_text: str):
    before = normalize_text(before_text)
    origin_pattern = re.compile(
        r"(?:انا|اني|احنا|نحن|جنسيتي|الجنسية|مواطن|مواطنة|مواطنه|from|nationality|citizen)\s*(?:من|is|:)?\s*$",
        re.IGNORECASE,
    )
    return bool(origin_pattern.search(before)) or before.endswith("من ")


def is_non_applicant_country_reference(text: str, country: dict | None):
    if not country:
        return False

    normalized = normalize_text(text)
    pattern = _country_alias_pattern(country)
    if not normalized or not pattern:
        return False

    has_location_reference = False
    has_origin_reference = False
    for match in pattern.finditer(normalized):
        before = normalized[max(0, match.start() - 80):match.start()]
        if is_negated_country_reference(before):
            continue
        if _has_country_origin_context(before):
            has_origin_reference = True
        if is_residence_location_context(before):
            has_location_reference = True

    return has_location_reference and not has_origin_reference


def is_negated_applicant_country_reference(text: str, country_or_ocr):
    if isinstance(country_or_ocr, dict):
        country = country_or_ocr
    else:
        country = next(
            (item for item in COUNTRIES if str(item.get("ocr_code") or "").upper() == str(country_or_ocr or "").upper()),
            None,
        )

    if not country:
        return False

    normalized = normalize_text(text)
    pattern = _country_alias_pattern(country)
    if not normalized or not pattern:
        return False

    for match in pattern.finditer(normalized):
        before = normalized[max(0, match.start() - 24):match.start()]
        if is_negated_country_reference(before):
            return True

    return False


def is_inside_kuwait_visa_question(text: str) -> bool:
    return has_any(text, INSIDE_KUWAIT_VISA_WORDS) and has_any(text, VISA_WORDS + CHECK_WORDS + DETAILS_WORDS)


def is_visa_comparison_question(text: str) -> bool:
    return has_any(text, COMPARISON_WORDS) and (
        has_any(text, VISA_WORDS)
        or sum(1 for aliases in VISA_TYPE_NAME_ALIASES.values() if any(has_any(text, [alias]) for alias in aliases)) >= 2
    )


def is_family_visit_application_question(text: str) -> bool:
    return has_any(text, FAMILY_VISIT_APPLICATION_WORDS)


def has_explicit_gender_cue(text: str) -> bool:
    cue_words = [
        "ذكر",
        "انثى",
        "أنثى",
        "رجل",
        "امرأة",
        "امراة",
        "الجنس",
        "gender",
        "male",
        "female",
    ]
    return has_any(text, cue_words)


def resolve_applicant_country(text: str):
    raw_text = str(text or "").strip()
    normalized = normalize_text(text)
    if not normalized:
        return None

    origin_pattern = re.compile(
        r"(?:انا|اني|احنا|نحن|جنسيتي|الجنسية|مواطن|مواطنة|مواطنه|from|nationality|citizen)\s*(?:من|is|:)?\s*$",
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
            has_origin_context = _has_country_origin_context(before)
            if is_residence_location_context(before):
                continue
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

            alias_variants = country_alias_variants(alias)

            variant_pattern = "|".join(
                re.escape(variant)
                for variant in sorted(alias_variants, key=len, reverse=True)
            )
            pattern = re.compile(rf"(?<!\w)(?:{variant_pattern})(?!\w)", re.IGNORECASE)

            for match in pattern.finditer(normalized):
                before = normalized[max(0, match.start() - 45):match.start()]
                after = normalized[match.end():match.end() + 35]
                if is_negated_country_reference(before):
                    continue
                if is_residence_location_context(before):
                    continue

                has_origin_context = _has_country_origin_context(before)
                has_destination_context = any(
                    normalize_text(word) in before[-22:] or normalize_text(word) in after[:22]
                    for word in destination_words
                )

                if country.get("ocr_code") == "KWT" and (is_kuwait_current_location_reference(text) or not has_origin_context):
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
        r"(?:فيزا|فيزه|تأشيرة|تاشيرة|سمة|سمه|visa(?:\s*no\.?)?)\s*(?:رقم\s*)?[:#\-]?\s*[\(\[]?\s*(\d{1,4})\s*[\)\]]?",
        r"(?:رقم|نوع)\s*[:#\-]?\s*[\(\[]?\s*(\d{1,4})\s*[\)\]]?",
        r"\bvisa\s*(?:no\.?)?\s*[:#\-]?\s*(\d{1,4})\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    if has_any(text, VISA_WORDS + ["زيارة", "الزيارة", "visit"]):
        typo_match = re.search(
            r"(?:^|\s)قم\s*[:#\-]?\s*[\(\[]?\s*(\d{1,4})\s*[\)\]]?",
            text,
            re.IGNORECASE,
        )
        if typo_match:
            return int(typo_match.group(1))

    return None


def extract_visa_type_by_name(text: str):
    normalized = normalize_text(text)
    if not normalized:
        return None

    for visa_type, aliases in VISA_TYPE_NAME_ALIASES.items():
        for alias in aliases:
            alias_norm = normalize_text(alias)
            if alias_norm and re.search(rf"(?<!\w){re.escape(alias_norm)}(?!\w)", normalized, re.IGNORECASE):
                return visa_type

    return None


def extract_generic_visit_visa_type(text: str):
    normalized = normalize_text(text)
    if not normalized:
        return None

    has_visit = has_any(text, ["زيارة", "زياره", "ازور", "أزور", "visit"])
    has_kuwait = has_any(text, ["الكويت", "kuwait"])
    has_request = has_any(
        text,
        [
            "ابغى",
            "ابي",
            "بدي",
            "اريد",
            "أريد",
            "اروح",
            "أروح",
            "اطلع",
            "أطلع",
            "اسافر",
            "هل بقدر",
            "هل اقدر",
            "هل أقدر",
            "can i",
            "want to",
            "need to",
        ],
    )
    specific_visit_words = [
        "زيارة تجارية",
        "زياره تجاريه",
        "تجارية",
        "تجاريه",
        "business",
        "commercial",
        "زيارة عائلية",
        "زياره عائليه",
        "عائلية",
        "عائليه",
        "family",
        "زيارة حكومية",
        "زياره حكوميه",
        "حكومية",
        "حكوميه",
        "government",
        "زيارة لسفارة",
        "زياره لسفاره",
        "سفارة",
        "سفاره",
        "embassy",
        "علاج",
        "medical",
        "دراسة",
        "study",
        "سابقة",
        "سابقه",
        "previous",
    ]

    if has_visit and has_kuwait and has_request and not has_any(text, specific_visit_words):
        return 16

    return None


def extract_contextual_visa_type(text: str, context: dict):
    normalized = normalize_text(text)
    if not normalized:
        return None

    if context.get("visa_type"):
        return None

    if context.get("last_intent") not in {"list_visa_types", "provide_country", "general_question", "eligibility_check", "relationship_check", "dependent_residency_inquiry", "residency_admin_inquiry"} and not context.get("available_visa_types_pending"):
        return None

    match = re.fullmatch(r"(?:فيزا\s*)?(\d{1,4})", normalized, re.IGNORECASE)
    if not match:
        return None

    return int(match.group(1))


def extract_age(text: str):
    if (
        has_any(text, ["اعمارهم", "أعمارهم", "اعمار الاطفال", "أعمار الأطفال", "ابنائي", "أبنائي", "اطفالي", "أطفالي"])
        and not has_any(text, ["عمري", "العمر", "سني", "سنّي", "my age", "i am"])
    ):
        return None

    patterns = [
        r"(?:عمري|عمرى|العمر|سنّي|سني)\s*(\d{1,3})",
        r"\b(?:i\s+am|i'm)\s+(?:a\s+)?(\d{1,3})\s*(?:year|years)[\s-]*old\b",
        r"(?:my\s+age\s+is|age\s+is|age|i am)\s*(\d{1,3})",
        r"\b(\d{1,3})\s*(?:سنه|سنة|عام|year old|years old)\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None


def extract_contextual_age(text: str, context: dict):
    if not context.get("ocr_code") or not context.get("visa_type"):
        return None

    if extract_visa_type(text) or has_any(text, VISA_WORDS):
        return None

    numbers = re.findall(r"(?<!\d)(\d{1,3})(?!\d)", normalize_text(text))
    if len(numbers) != 1:
        return None

    age = int(numbers[0])
    return age if 0 <= age <= 120 else None


def extract_gender(text: str):
    normalized = normalize_text(text)

    if any(word in normalized for word in ["ذكر", "رجل", "ولد"]) or re.search(r"(?<!\w)مواطن(?!\w)", normalized) or re.search(r"\b(?:male|man)\b", normalized, re.IGNORECASE):
        return "male"

    if any(word in normalized for word in ["انثي", "انثى", "امرأه", "امراه", "بنت"]) or re.search(r"(?<!\w)مواطنه(?!\w)", normalized) or re.search(r"\b(?:female|woman)\b", normalized, re.IGNORECASE):
        return "female"

    return None


def extract_occupation(text: str):
    normalized = normalize_text(text)

    if re.search(
        r"\b(?:i\s+)?(?:have|own|hold|invest\s+in)\s+(?:real\s+estate|real\s+state|property|properties)\b",
        normalized,
        re.IGNORECASE,
    ):
        return "real estate owner"

    if re.search(r"\b(?:real\s+estate|real\s+state|property)\s+owner\b", normalized, re.IGNORECASE):
        return "real estate owner"

    professor_match = re.search(r"(?:أستاذ|استاذ|ستاذ|ستاد)\s+([^\d،,.!?]{2,40})", text, re.IGNORECASE)
    if professor_match:
        specialty = clean_occupation_candidate(professor_match.group(1))
        if specialty:
            return normalize_text(f"استاذ {specialty}")

    for occupation in sorted(KNOWN_OCCUPATIONS, key=lambda item: len(normalize_text(item)), reverse=True):
        if normalize_text(occupation) in normalized:
            if normalize_text(occupation) == "presidents":
                return "president"
            return occupation

    # Words that should never be treated as occupations when extracted via
    # the generic "i am ..." pattern.  These are common eligibility/check
    # words that appear after "i am" in visa-related questions.
    NON_OCCUPATION_WORDS = {
        "allowed",
        "eligible",
        "interested",
        "able",
        "ready",
        "qualified",
        "approved",
        "looking",
        "trying",
        "planning",
        "going",
        "asking",
        "wondering",
        "checking",
        "applying",
        "want",
        "wanting",
        "hoping",
        "living",
        "staying",
        "traveling",
        "travelling",
        "visiting",
        "coming",
        "based",
        "located",
        "currently",
        "from",
        "not",
    }

    patterns = [
        r"(?:مهنتي|وظيفتي|اعمل ك|أعمل ك|انا اعمل ك|انا أعمل ك|اعمل بمهنة|أعمل بمهنة|بمهنة|مهنة)\s*[\(:：]?\s*([^\d،,.!?)]{2,40})",
        r"(?:اشتغل|أشتغل|انا اشتغل|انا أشتغل|اعمل|أعمل|شغلي|عملي)\s+([^\d،,.!?]{2,40})",
        r"(?:لو مهنتي|اذا مهنتي|إذا مهنتي|مهنتي|لو كنت|اذا كنت|إذا كنت|كنت)\s+([^\d،,.!?]{2,40})",
        r"\bas\s+([a-zA-Z][a-zA-Z\s-]{1,40})",
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
        if resolve_country(candidate_norm):
            continue
        # Reject candidates whose first word is a non-occupation word
        first_word = candidate_norm.split()[0] if candidate_norm else ""
        if first_word in NON_OCCUPATION_WORDS:
            continue
        if (
            not candidate_norm.startswith("من ")
            and not candidate_norm.startswith("from ")
            and not has_any(candidate, VISA_WORDS + LIST_WORDS)
        ):
            return candidate_norm or candidate

    return None


def clean_occupation_candidate(candidate: str):
    text = str(candidate or "").strip()
    text = re.split(
        r"\b(?:and|with|my age|age is|age|visa|for|from|country|nationality)\b|\s+(?:عمري|العمر|سني|سنّي|هل|هل يمكنني|مسموح|مسموحة|اقدر|أقدر|يمكنني|على|لفيزا|للتقديم|من|في)\s+|[,،.!?;]",
        text,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    text = re.sub(r"^(?:a|an|the)\s+", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_relationship(text: str):
    normalized = normalize_text(text)

    if re.search(r"(?:مع|اجيب|اجلب|اصطحب|أجيب|أجلب|أصطحب)\s+(?:ابي|أبي)\b", text, re.IGNORECASE):
        return "الأب"

    relation_patterns = {
        "الزوجة": ["زوجتي", "مرتي", "زوجة", "wife"],
        "الزوج": ["زوجي", "زوج", "husband"],
        "الابن": ["ابني", "إبني", "ابن", "ولدي", "son"],
        "الابنة": ["بنتي", "ابنتي", "إبنتي", "daughter"],
        "الأم": ["امي", "أمي", "والدتي", "mother"],
        "الأب": ["ابوي", "أبوي", "ابويا", "أبويا", "والدي", "الأب", "الاب", "father"],
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


def is_dependent_residency_question(text: str) -> bool:
    if is_family_visit_application_question(text) and not has_any(text, DEPENDENT_RESIDENCY_STRONG_WORDS):
        return False
    return has_any(text, DEPENDENT_RESIDENCY_WORDS)


def is_residency_admin_question(text: str) -> bool:
    return has_any(text, RESIDENCY_ADMIN_WORDS)


def is_system_support_question(text: str) -> bool:
    return has_any(text, SYSTEM_SUPPORT_WORDS)


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
    context_has_applicant_data = any(context.get(key) is not None for key in ("age", "occupation", "gender"))

    if is_context_country_question(text):
        return "context_question"

    if is_dependent_residency_question(text):
        return "dependent_residency_inquiry"

    if is_residency_admin_question(text):
        return "residency_admin_inquiry"

    if is_inside_kuwait_visa_question(text):
        return "inside_kuwait_visa_inquiry"

    if is_visa_comparison_question(text):
        return "visa_comparison_inquiry"

    if is_system_support_question(text) and not (visa_type or age is not None or occupation or gender or relationship):
        return "system_support_inquiry"

    if is_chitchat(text, country):
        return "chitchat"

    if is_relationship_decline(text, relationship, context):
        return "relationship_reset"

    if is_family_visit_application_question(text):
        return "eligibility_check"

    if relationship:
        return "relationship_check"

    if effective_visa_type and (age is not None or occupation or gender):
        return "eligibility_check"

    if (
        effective_visa_type
        and has_country
        and context_has_applicant_data
        and has_any(text, CHECK_WORDS)
        and not has_any(text, DETAILS_WORDS + LIST_WORDS + OCCUPATION_QUERY_WORDS + RELATIONSHIP_QUERY_WORDS + AGE_QUERY_WORDS)
    ):
        return "eligibility_check"

    if effective_visa_type and is_relationship_details_question(text):
        return "relationship_details"

    if effective_visa_type and is_age_details_question(text):
        return "age_details"

    if effective_visa_type and is_occupation_confirmation_question(text, context):
        return "occupation_confirmation"

    if effective_visa_type and is_occupation_details_question(text):
        return "occupation_details"

    if not has_country and (age or occupation or gender) and has_any(text, CHECK_WORDS):
        return "eligibility_check"

    if has_any(text, LIST_WORDS):
        return "list_visa_types"

    if effective_visa_type and has_any(text, STRONG_CHECK_WORDS):
        return "eligibility_check"

    if not effective_visa_type and has_country and (age or occupation or gender) and has_any(text, CHECK_WORDS + DETAILS_WORDS):
        return "eligibility_check"

    if (
        message_has_country
        and context_visa_type
        and not visa_type
        and age is None
        and not occupation
        and not gender
        and not relationship
        and not has_any(text, CHECK_WORDS + DETAILS_WORDS + LIST_WORDS)
    ):
        return "provide_country"

    if (
        effective_visa_type
        and has_country
        and context.get("last_intent") == "eligibility_check"
        and not has_any(text, DETAILS_WORDS + LIST_WORDS + OCCUPATION_QUERY_WORDS + RELATIONSHIP_QUERY_WORDS + AGE_QUERY_WORDS)
    ):
        return "eligibility_check"

    if effective_visa_type and has_any(text, DETAILS_WORDS):
        return "visa_details"

    if effective_visa_type and has_any(text, CHECK_WORDS):
        return "eligibility_check"

    if message_has_country and not visa_type and not context_visa_type:
        if has_any(text, VISA_QUERY_WORDS) or context.get("last_intent") == "list_visa_types":
            return "list_visa_types"
        return "provide_country"

    if message_has_country and context_visa_type and not visa_type and not has_any(text, CHECK_WORDS + DETAILS_WORDS + LIST_WORDS):
        return "provide_country"

    if message_has_country and context_visa_type:
        if context.get("last_intent") in {"age_details", "occupation_details", "relationship_details", "visa_details"}:
            return context.get("last_intent")
        return "visa_details"

    if effective_visa_type and has_country:
        return "visa_details"

    if (age or occupation or gender) and context_has_country and context_visa_type:
        return "eligibility_check"

    return "general_question"


def should_consult_gemini(intent: str, text: str, occupation, gender) -> bool:
    if intent in {
        "chitchat",
        "context_question",
        "list_visa_types",
        "visa_details",
        "age_details",
        "occupation_details",
        "relationship_details",
        "relationship_reset",
        "occupation_confirmation",
        "provide_country",
        "dependent_residency_inquiry",
        "residency_admin_inquiry",
        "inside_kuwait_visa_inquiry",
        "visa_comparison_inquiry",
        "system_support_inquiry",
    }:
        return False
    if occupation or gender:
        return False
    return has_any(text, CHECK_WORDS) and has_any(text, VISA_WORDS)


def analyze_message(user_message: str, context: dict, gemini_service):
    local_country = resolve_applicant_country(user_message)
    local_visa_type = (
        extract_visa_type(user_message)
        or extract_visa_type_by_name(user_message)
        or extract_generic_visit_visa_type(user_message)
        or (10 if is_family_visit_application_question(user_message) else None)
        or extract_contextual_visa_type(user_message, context)
    )
    local_age = extract_age(user_message)
    if local_age is None:
        local_age = extract_contextual_age(user_message, context)
    local_relationship = extract_relationship(user_message)
    local_occupation = extract_occupation(user_message)
    local_gender = extract_gender(user_message)
    allow_gemini_age = has_explicit_age_cue(user_message)
    allow_gemini_occupation = bool(local_occupation) or has_explicit_occupation_cue(user_message)
    allow_gemini_gender = bool(local_gender) or has_explicit_gender_cue(user_message)

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
    if gemini_service and should_consult_gemini(intent, user_message, local_occupation, local_gender):
        gemini_data = gemini_service.extract_query(user_message, context)

    country = local_country or resolve_country(gemini_data.get("country_text", ""))
    if country and country.get("ocr_code") == "KWT" and is_kuwait_current_location_reference(user_message):
        country = None
    if country and is_non_applicant_country_reference(user_message, country):
        country = None
    visa_type = local_visa_type or gemini_data.get("visa_type")
    age = local_age if local_age is not None else (gemini_data.get("age") if allow_gemini_age else None)
    occupation = local_occupation or (gemini_data.get("occupation") if allow_gemini_occupation else None)
    gender = local_gender or (gemini_data.get("gender") if allow_gemini_gender else None)

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
