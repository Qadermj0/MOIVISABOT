import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEYS = os.getenv("GOOGLE_API_KEYS")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_ENABLED = os.getenv("GEMINI_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
KUWAIT_VISA_API_BASE = os.getenv(
    "KUWAIT_VISA_API_BASE",
    "https://kuwaitvisatest.moi.gov.kw/kuwaitVisa/visaRules"
)
