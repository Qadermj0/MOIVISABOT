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
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
GEMINI_QUERY_UNDERSTANDING_MODEL = os.getenv("GEMINI_QUERY_UNDERSTANDING_MODEL", GEMINI_MODEL)
GEMINI_INTENT_ROUTER_MODEL = os.getenv("GEMINI_INTENT_ROUTER_MODEL", GEMINI_MODEL)
GEMINI_INQUIRY_MODEL = os.getenv("GEMINI_INQUIRY_MODEL", GEMINI_MODEL)
GEMINI_ELIGIBILITY_MODEL = os.getenv("GEMINI_ELIGIBILITY_MODEL", GEMINI_MODEL)
GEMINI_CHITCHAT_MODEL = os.getenv("GEMINI_CHITCHAT_MODEL", GEMINI_MODEL)
GEMINI_ENABLED = env_bool("GEMINI_ENABLED", True)
GEMINI_FINAL_ANSWER_ENABLED = env_bool("GEMINI_FINAL_ANSWER_ENABLED", True)
GEMINI_FINAL_ANSWER_INTENTS = os.getenv(
    "GEMINI_FINAL_ANSWER_INTENTS",
    "",
)
GEMINI_TIMEOUT_MS = env_int("GEMINI_TIMEOUT_MS", 12000)
GEMINI_MAX_OUTPUT_TOKENS = env_int("GEMINI_MAX_OUTPUT_TOKENS", 2500)
GEMINI_EXTRACT_MAX_OUTPUT_TOKENS = env_int("GEMINI_EXTRACT_MAX_OUTPUT_TOKENS", 7500)
GEMINI_THINKING_BUDGET = env_int("GEMINI_THINKING_BUDGET", 1000)
GEMINI_TEMPERATURE = env_float("GEMINI_TEMPERATURE", 0.3)
KUWAIT_VISA_API_BASE = os.getenv(
    "KUWAIT_VISA_API_BASE",
    "https://kuwaitvisatest.moi.gov.kw/kuwaitVisa/visaRules"
)
VISA_API_TIMEOUT_SECONDS = env_float("VISA_API_TIMEOUT_SECONDS", 15.0)
VISA_API_CACHE_TTL_SECONDS = env_int("VISA_API_CACHE_TTL_SECONDS", 3600)
GOOGLE_SPEECH_API_KEY = (
    os.getenv("SPEECH_API_KEYS")
    or os.getenv("SPEECH_API_KEY")
    or os.getenv("GOOGLE_SPEECH_API_KEY")
    or os.getenv("GOOGLE_CLOUD_SPEECH_API_KEY")
    or os.getenv("SPEECH_TO_TEXT_API_KEY")
)
GOOGLE_SPEECH_ACCESS_TOKEN = os.getenv("GOOGLE_SPEECH_ACCESS_TOKEN")
GOOGLE_SPEECH_PROJECT_ID = (
    os.getenv("GOOGLE_SPEECH_PROJECT_ID")
    or os.getenv("GOOGLE_CLOUD_PROJECT")
)
GOOGLE_SPEECH_API_VERSION = os.getenv("GOOGLE_SPEECH_API_VERSION", "v1")
GOOGLE_SPEECH_LOCATION = os.getenv("GOOGLE_SPEECH_LOCATION", "us")
GOOGLE_SPEECH_MODEL = os.getenv("GOOGLE_SPEECH_MODEL", "latest_short")
GOOGLE_SPEECH_USE_ALTERNATIVE_LANGUAGES = env_bool("GOOGLE_SPEECH_USE_ALTERNATIVE_LANGUAGES", False)
GOOGLE_SPEECH_LANGUAGE_CODES = os.getenv(
    "GOOGLE_SPEECH_LANGUAGE_CODES",
    "ar-KW,en-US,fr-FR,de-DE,es-ES",
)
GOOGLE_SPEECH_TIMEOUT_SECONDS = env_float("GOOGLE_SPEECH_TIMEOUT_SECONDS", 25.0)
GOOGLE_SPEECH_MAX_AUDIO_MB = env_float("GOOGLE_SPEECH_MAX_AUDIO_MB", 8.0)
GOOGLE_SPEECH_API_ENDPOINT = os.getenv("GOOGLE_SPEECH_API_ENDPOINT", "")
GOOGLE_SPEECH_SAMPLE_RATE_HERTZ = env_int("GOOGLE_SPEECH_SAMPLE_RATE_HERTZ", 48000)
