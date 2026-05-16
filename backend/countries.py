import json
import os
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COUNTRIES_FILE = os.path.join(BASE_DIR, "countries.json")


INVALID_OCR_CODES = {
    "", "-", "0", "TEST", "TES", "ART", "XXX"
}

INVALID_NAME_PATTERNS = [
    r"TEST",
    r"TSET",
    r"اختبار",
    r"ADIROLF",
    r"TTTTSET",
]


EXTRA_ALIASES = {
    "AAA": [
        "الشيشان",
        "شيشان",
        "شيشاني",
        "شيشانية",
        "شيشانيه",
        "الشيشاني",
        "الشيشانية",
        "الشيشانيه",
        "شيشانيين",
        "الشيشانيين",
        "chechenia",
        "chechnya",
        "chechen",
        "chechens",
        "aaa",
    ],
    "DEU": [
        "المانيا",
        "ألمانيا",
        "الماني",
        "ألماني",
        "المانية",
        "ألمانية",
        "المانيين",
        "ألمانيين",
        "الألمان",
        "الالمان",
        "germany",
        "german",
        "germans",
        "deu",
    ],
    "JOR": [
        "الاردن", "الأردن", "اردني", "أردني", "اردنية", "أردنية", "الاردنية", "الأردنية",
        "اردنيين", "أردنيين", "الاردنيين", "الأردنيين",
        "اردنيون", "أردنيون", "الاردنيون", "الأردنيون",
        "jordan", "jordanian", "jordanians", "jor",
    ],
    "EGY": [
        "مصر", "مصري", "مصرية", "مصريين", "المصريين", "مصريون", "المصريون",
        "egypt", "egyptian", "egyptians", "egy",
    ],
    "RUS": [
        "روسيا", "روسي", "روسية", "روسيين", "الروسيين", "روسيون", "الروسيون",
        "روس", "الروس", "russia", "russian", "russians", "rus",
    ],
    "IND": [
        "الهند", "هند", "هندي", "هندية", "هنديين", "الهنديين",
        "هنود", "الهنود", "الهندي", "الهندية",
        "india", "indian", "indians", "ind",
    ],
    "PAK": [
        "باكستان", "باكستاني", "باكستانية", "باكستانيين", "الباكستانيين",
        "باكستانيون", "الباكستانيون",
        "pakistan", "pakistani", "pakistanis", "pak",
    ],
    "ESP": ["اسبانيا", "إسبانيا", "اسباني", "إسباني", "spain", "spanish", "esp"],
    "LBN": ["لبنان", "لبناني", "لبنانية", "lebanon", "lebanese", "lbn"],
    "SAU": [
        "السعودية", "السعوديه", "سعودي", "سعودية", "سعوديه",
        "سعوديين", "السعوديين", "سعوديون", "السعوديون",
        "saudi", "saudis", "saudi arabia", "sau",
    ],
    "QAT": [
        "قطر", "قطري", "قطرية", "قطريه", "قطريين", "القطريين",
        "قطريون", "القطريون", "qatar", "qatari", "qataris", "qat",
    ],
    "CHN": [
        "الصين الشعبية", "الصين الشعبيه", "الصين", "صين", "صيني", "صينية", "صينيه",
        "صينيين", "الصينيين", "صينيون", "الصينيون",
        "china", "chinese", "chn",
    ],
    "SOM": [
        "الصومال", "صومال", "صومالي", "صومالية", "صوماليه",
        "صوماليين", "الصوماليين", "صوماليون", "الصوماليون",
        "somalia", "somali", "somalis", "som",
    ],
    "ROU": [
        "رومانيا", "روماني", "رومانية", "رومانيه", "رومانيين", "الرومانيين",
        "رومانيون", "الرومانيون", "romania", "romanian", "romanians", "rou",
    ],
    "KOR": [
        "كوريا", "كوريا الجنوبية", "كوريا الجنوبيه", "كوري", "كورية", "كوريه",
        "كوريين", "الكوريين", "كوريون", "الكوريون",
        "republic of korea", "south korea", "korea", "korean", "koreans", "kor",
    ],
    "PRK": [
        "كوريا الشمالية", "كوريا الشماليه", "كوريا الديمقراطية", "كوريا الديمقراطيه",
        "north korea", "democratic republic of korea", "prk",
    ],
    "BHR": [
        "البحرين", "بحرين", "بحريني", "بحرينية", "بحرينيه",
        "بحرينيين", "البحرينيين", "بحرينيون", "البحرينيون",
        "bahrain", "bahraini", "bahrainis", "bhr",
    ],
    "BRN": [
        "بوروني",
        "بروني",
        "بروناي",
        "بروناوي",
        "بروناوية",
        "بروناويه",
        "البرونيين",
        "البروناويين",
        "brunei",
        "bruneian",
        "bruneians",
        "brn",
    ],
    "GBR": ["بريطانيا", "المملكة المتحدة", "انجلترا", "إنجلترا", "uk", "united kingdom", "british", "gbr"],
    "NLD": ["هولندا", "الهولندي", "هولندي", "netherlands", "dutch", "nld"],
    "FRA": ["فرنسا", "فرنسي", "france", "french", "fra"],
    "ITA": ["ايطاليا", "إيطاليا", "italy", "italian", "ita"],
    "TUR": ["تركيا", "تركي", "turkey", "turkish", "tur"],
    "USA": ["امريكا", "أمريكا", "الولايات المتحدة", "usa", "united states", "american"],
    "CAN": ["كندا", "كندي", "canada", "canadian", "can"],
    "ARE": ["الامارات", "الإمارات", "اماراتي", "إماراتي","امارات","الامارات العربية المتحدة", "uae", "emirates", "are"],
}


def _is_invalid_country(item: dict) -> bool:
    ocr = str(item.get("ocr_code", "")).strip().upper()
    ar = str(item.get("country_name_ar", "") or "")
    en = str(item.get("country_name_en", "") or "")

    if ocr in INVALID_OCR_CODES:
        return True

    if not re.match(r"^[A-Z]{3}$", ocr):
        return True

    combined = f"{ar} {en}".upper()

    for pattern in INVALID_NAME_PATTERNS:
        if re.search(pattern, combined, re.IGNORECASE):
            return True

    return False


def load_countries():
    if not os.path.exists(COUNTRIES_FILE):
        return []

    with open(COUNTRIES_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    cleaned = []
    seen = set()

    for item in raw:
        if not isinstance(item, dict):
            continue

        if _is_invalid_country(item):
            continue

        ocr = str(item.get("ocr_code", "")).strip().upper()

        # Avoid duplicate OCR code
        if ocr in seen:
            continue

        seen.add(ocr)

        ar = str(item.get("country_name_ar", "") or "").strip()
        en = str(item.get("country_name_en", "") or "").strip()

        aliases = [
            ar,
            en,
            ar.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا"),
            en.lower(),
        ]

        aliases.extend(EXTRA_ALIASES.get(ocr, []))

        cleaned.append({
            "country_name_ar": ar,
            "country_name_en": en,
            "ocr_code": ocr,
            "country_code": item.get("country_code"),
            "aliases": list(set([a for a in aliases if a]))
        })

    return cleaned


COUNTRIES = load_countries()


def normalize_text(text: str) -> str:
    text = str(text or "").lower().strip()
    text = text.replace("لل ", "لل").replace("ل ", "ل")
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ى", "ي").replace("ة", "ه")
    return text


def country_alias_variants(alias: str):
    alias_norm = normalize_text(alias)
    if not alias_norm:
        return set()

    variants = {alias_norm, f"ل{alias_norm}", f"لل{alias_norm}"}

    if alias_norm.startswith("ال"):
        without_article = alias_norm[2:]
        variants.update({
            without_article,
            f"ل{without_article}",
            f"لل{without_article}",
        })

    return variants


def is_negated_country_reference(text_before_country: str):
    before = normalize_text(text_before_country)
    return bool(re.search(r"(?:^|\s)(?:مو|مش|ليس|ليست|غير|not|no)\s*$", before, re.IGNORECASE))


def resolve_country(text: str):
    if not text:
        return None

    normalized = normalize_text(text)

    # Direct OCR search
    for country in COUNTRIES:
        if country["ocr_code"].lower() == normalized:
            return country

    # Alias search
    for country in COUNTRIES:
        ocr_norm = country["ocr_code"].lower()
        for alias in country.get("aliases", []):
            alias_norm = normalize_text(alias)
            if not alias_norm or alias_norm == ocr_norm:
                continue
            alias_variants = country_alias_variants(alias)

            variant_pattern = "|".join(
                re.escape(variant)
                for variant in sorted(alias_variants, key=len, reverse=True)
            )
            pattern = re.compile(rf"(?<!\w)(?:{variant_pattern})(?!\w)", re.IGNORECASE)
            for match in pattern.finditer(normalized):
                before = normalized[max(0, match.start() - 18):match.start()]
                if is_negated_country_reference(before):
                    continue
                return country

    return None


def list_countries():
    return COUNTRIES
