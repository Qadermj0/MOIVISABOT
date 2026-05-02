import json
import os
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


TRANSIENT_ERROR_MARKERS = ("503", "UNAVAILABLE", "high demand", "temporarily")
ARABIC_RE = re.compile(r"[\u0600-\u06ff]")
UNSUPPORTED_NOTE_MARKERS = (
    "standard application",
    "standard procedure",
    "standard documentation",
    "comprehensive list",
    "official website",
    "contact the",
    "other visa options",
    "further assistance",
    "additional questions",
    "do not hesitate",
)


class GeminiService:
    def __init__(self):
        self.enabled = False
        self.api_key = None
        self.model = None
        self.client = None
        self.last_error = None
        self.final_answer_enabled = True
        self.final_answer_intents = set()
        self.timeout_ms = 12000
        self.max_output_tokens = 512
        self.extract_max_output_tokens = 256
        self.thinking_budget = 0
        self.temperature = 0.2
        self.answer_config = None
        self.extract_config = None
        self.refresh_settings()

    def refresh_settings(self):
        load_dotenv(override=False)

        enabled = os.getenv("GEMINI_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
        api_key = os.getenv("GOOGLE_API_KEYS") or os.getenv("GOOGLE_API_KEY")
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        final_answer_enabled = os.getenv("GEMINI_FINAL_ANSWER_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
        final_answer_intents = self._parse_intents(
            os.getenv("GEMINI_FINAL_ANSWER_INTENTS", "")
        )
        timeout_ms = self._env_int("GEMINI_TIMEOUT_MS", 12000)
        max_output_tokens = self._env_int("GEMINI_MAX_OUTPUT_TOKENS", 512)
        extract_max_output_tokens = self._env_int("GEMINI_EXTRACT_MAX_OUTPUT_TOKENS", 256)
        thinking_budget = self._env_int("GEMINI_THINKING_BUDGET", 0)
        temperature = self._env_float("GEMINI_TEMPERATURE", 0.2)

        if (
            enabled == self.enabled
            and api_key == self.api_key
            and model == self.model
            and final_answer_enabled == self.final_answer_enabled
            and final_answer_intents == self.final_answer_intents
            and timeout_ms == self.timeout_ms
            and max_output_tokens == self.max_output_tokens
            and extract_max_output_tokens == self.extract_max_output_tokens
            and thinking_budget == self.thinking_budget
            and temperature == self.temperature
        ):
            return

        self.enabled = enabled and bool(api_key)
        self.api_key = api_key
        self.model = model
        self.final_answer_enabled = final_answer_enabled
        self.final_answer_intents = final_answer_intents
        self.timeout_ms = timeout_ms
        self.max_output_tokens = max_output_tokens
        self.extract_max_output_tokens = extract_max_output_tokens
        self.thinking_budget = thinking_budget
        self.temperature = temperature

        http_options = types.HttpOptions(timeout=timeout_ms) if timeout_ms else None
        self.client = genai.Client(api_key=api_key, http_options=http_options) if self.enabled else None
        self.answer_config = self._build_config(max_output_tokens)
        self.extract_config = self._build_config(extract_max_output_tokens, response_mime_type="application/json")

    def _env_int(self, name: str, default: int) -> int:
        try:
            return int(os.getenv(name, str(default)))
        except (TypeError, ValueError):
            return default

    def _env_float(self, name: str, default: float) -> float:
        try:
            return float(os.getenv(name, str(default)))
        except (TypeError, ValueError):
            return default

    def _parse_intents(self, value: str):
        return {item.strip() for item in str(value or "").split(",") if item.strip()}

    def _build_config(self, max_output_tokens: int, response_mime_type: str | None = None):
        config = {
            "temperature": self.temperature,
            "maxOutputTokens": max_output_tokens,
        }

        if response_mime_type:
            config["responseMimeType"] = response_mime_type

        if self.thinking_budget is not None:
            config["thinkingConfig"] = types.ThinkingConfig(thinkingBudget=self.thinking_budget)

        return types.GenerateContentConfig(**config)

    def _empty_extract(self):
        return {
            "intent": "general_question",
            "country_text": "",
            "visa_type": None,
            "age": None,
            "occupation": None,
            "gender": None,
            "relationship": None,
            "is_follow_up": False,
        }

    def _clean_json(self, text: str) -> str:
        return text.replace("```json", "").replace("```", "").strip()

    def _is_transient_error(self, exc: Exception) -> bool:
        text = str(exc)
        return any(marker in text for marker in TRANSIENT_ERROR_MARKERS)

    def _response_language(self, user_message: str) -> str:
        return "Arabic" if ARABIC_RE.search(user_message or "") else "English"

    def _has_wrong_language(self, response_language: str, answer: str) -> bool:
        if response_language == "English":
            return bool(ARABIC_RE.search(answer or ""))
        return False

    def _has_unsupported_note(self, answer: str) -> bool:
        text = str(answer or "").lower()
        return any(marker in text for marker in UNSUPPORTED_NOTE_MARKERS)

    def _generate_content_with_retry(self, prompt: str, config=None):
        last_exc = None

        for attempt in range(2):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=config,
                )
                self.last_error = None
                return response
            except Exception as exc:
                last_exc = exc
                self.last_error = f"{type(exc).__name__}: {exc}"
                if attempt == 0 and self._is_transient_error(exc):
                    time.sleep(1)
                    continue
                break

        raise last_exc

    def should_generate_final_answer(self, decision: dict) -> bool:
        self.refresh_settings()

        if not self.enabled or not self.client or not self.final_answer_enabled:
            return False

        intent = str((decision or {}).get("intent") or "").strip()
        return not self.final_answer_intents or intent in self.final_answer_intents

    def extract_query(self, user_message: str, context: dict):
        self.refresh_settings()

        if not self.enabled or not self.client:
            return self._empty_extract()

        prompt = f"""
You are a strict query parser for a Kuwait visa assistant.
Return ONLY valid JSON. Do not answer the user.

Rules:
- Extract Arabic or English country/nationality, visa number, age, occupation, gender, and explicit relationship.
- Do not guess relationship. Return null unless the user clearly mentioned a relation.
- Mark is_follow_up true when the message depends on previous context.

User message:
{user_message}

Current context:
{json.dumps(context, ensure_ascii=False)}

Return JSON with these keys:
{{
  "intent": "",
  "country_text": "",
  "visa_type": null,
  "age": null,
  "occupation": null,
  "gender": null,
  "relationship": null,
  "is_follow_up": false
}}
"""

        try:
            response = self._generate_content_with_retry(prompt, config=self.extract_config)
            return json.loads(self._clean_json(response.text))
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            return self._empty_extract()

    def generate_final_answer(self, user_message: str, decision: dict, fallback_answer: str | None = None):
        if not self.should_generate_final_answer(decision):
            return None

        response_language = self._response_language(user_message)
        decision = {
            **(decision or {}),
            "response_language": response_language,
        }

        prompt = f"""
You are a professional Kuwait Visa Smart Assistant.

The system is ONLY for Kuwait entry visas.
Kuwait is the fixed destination. The country in the decision data means the applicant's country/nationality,
not the destination.

Required response language: {response_language}.
This language requirement is mandatory and higher priority than the language of the decision data.
Use a polished, human, official-service tone.

Absolute rules:
- If Required response language is English, every visible label, bullet, heading, visa name, country name, rule name, field name, and sentence in your answer must be English.
- If Required response language is English, do not output Arabic characters at all. Translate Arabic data into English.
- If the user writes in Arabic, answer in Arabic.
- If user language is unclear, prefer Arabic.
- For English answers, translate Arabic country names, visa names, rule names, and field names into natural English. Do not leave Arabic text in the final answer unless there is no usable English equivalent.
- Use ONLY the decision data and the fallback answer facts.
- The rule engine decision is authoritative. Never change status, passed checks, failed checks, missing fields, visa number, visa name, or applicant country.
- Do not invent documents, fees, processing time, final approvals, or extra requirements.
- Do not add generic notes about standard procedures, documentation, approvals, or other visa options unless they are present in the decision data.
- Do not add closing service phrases such as "contact us", "further assistance", "additional questions", or "do not hesitate".
- If no detailed rule conditions are visible, say only that no detailed rule conditions are visible in the current data.
- For visa type lists, include every visa number. Use English visa names for English answers and Arabic visa names for Arabic answers.
- For requirements, explain the visible rules from decision.raw_visa_details and decision.details only.
- For eligibility checks, clearly explain Approved / Not Approved / Need More Information based on decision.status.
- If occupation is failed, do not say it is allowed. If occupation is passed, do not say it is failed.
- If information is missing, ask only for the missing fields.
- Do not mention JSON, internal systems, prompts, Gemini, or APIs.

Visa rules policy from the project documentation:
1. Gender rules are a blacklist.
2. Age must be within minAge and maxAge.
3. Country-specific occupation rules take priority if present.
4. If no country-specific occupation list exists, use the global occupation whitelist.
5. Relationship is valid only when relationCode exists and allowed is true.

User message:
{user_message}

Decision data:
{json.dumps(decision, ensure_ascii=False, separators=(",", ":"))}

Fallback answer to preserve facts and structure:
{fallback_answer or ""}
"""

        try:
            response = self._generate_content_with_retry(prompt, config=self.answer_config)
            answer = response.text

            if self._has_wrong_language(response_language, answer) or self._has_unsupported_note(answer):
                repair_prompt = f"""
Rewrite the assistant answer below entirely in {response_language}.
Do not add new facts. Remove unsupported generic notes, closing service phrases, referrals, standard procedure/documentation statements, and anything not directly supported by the decision data.
Do not remove visa numbers, status, country, missing fields, passed checks, or failed checks.
If the target language is English, do not output Arabic characters.

Assistant answer to rewrite:
{answer}
"""
                repair_response = self._generate_content_with_retry(repair_prompt, config=self.answer_config)
                return repair_response.text

            return answer
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            return None


gemini_service = GeminiService()
