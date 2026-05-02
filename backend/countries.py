import json
import os
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COUNTRIES_FILE = os.path.join(BASE_DIR, "countries.json")


INVALID_OCR_CODES = {
    "", "-", "0", "TEST", "TES", "ART", "XXX", "AAA"
}

INVALID_NAME_PATTERNS = [
    r"TEST",
    r"TSET",
    r"اختبار",
    r"ADIROLF",
    r"TTTTSET",
]


EXTRA_ALIASES = {
    "DEU": ["المانيا", "ألمانيا", "الماني", "ألماني", "germany", "german", "deu"],
    "JOR": ["الاردن", "الأردن", "اردني", "أردني", "jordan", "jordanian", "jor"],
    "EGY": ["مصر", "مصري", "مصرية", "egypt", "egyptian", "egy"],
    "ESP": ["اسبانيا", "إسبانيا", "اسباني", "إسباني", "spain", "spanish", "esp"],
    "LBN": ["لبنان", "لبناني", "لبنانية", "lebanon", "lebanese", "lbn"],
    "SAU": ["السعودية", "سعودي", "سعودية", "saudi", "saudi arabia", "sau"],
    "BHR": ["البحرين", "بحريني", "bahrain", "bahraini", "bhr"],
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
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ى", "ي").replace("ة", "ه")
    return text


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
            pattern = re.compile(rf"(?<!\w){re.escape(alias_norm)}(?!\w)", re.IGNORECASE)
            if pattern.search(normalized):
                return country

    return None


def list_countries():
    return COUNTRIES
