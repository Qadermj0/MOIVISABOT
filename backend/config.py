import os
from dotenv import load_dotenv

load_dotenv()


def env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


def env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


GOOGLE_API_KEYS = os.getenv("GOOGLE_API_KEYS")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_ENABLED = env_bool("GEMINI_ENABLED", True)
GEMINI_FINAL_ANSWER_ENABLED = env_bool("GEMINI_FINAL_ANSWER_ENABLED", True)
GEMINI_FINAL_ANSWER_INTENTS = os.getenv(
    "GEMINI_FINAL_ANSWER_INTENTS",
    "",
)
GEMINI_TIMEOUT_MS = env_int("GEMINI_TIMEOUT_MS", 12000)
GEMINI_MAX_OUTPUT_TOKENS = env_int("GEMINI_MAX_OUTPUT_TOKENS", 512)
GEMINI_EXTRACT_MAX_OUTPUT_TOKENS = env_int("GEMINI_EXTRACT_MAX_OUTPUT_TOKENS", 256)
GEMINI_THINKING_BUDGET = env_int("GEMINI_THINKING_BUDGET", 0)
GEMINI_TEMPERATURE = env_float("GEMINI_TEMPERATURE", 0.2)
KUWAIT_VISA_API_BASE = os.getenv(
    "KUWAIT_VISA_API_BASE",
    "https://kuwaitvisatest.moi.gov.kw/kuwaitVisa/visaRules"
)
VISA_API_TIMEOUT_SECONDS = env_float("VISA_API_TIMEOUT_SECONDS", 15.0)
VISA_API_CACHE_TTL_SECONDS = env_int("VISA_API_CACHE_TTL_SECONDS", 3600)
