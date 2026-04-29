import json
import os
import time

from dotenv import load_dotenv
from google import genai


TRANSIENT_ERROR_MARKERS = ("503", "UNAVAILABLE", "high demand", "temporarily")


class GeminiService:
    def __init__(self):
        self.enabled = False
        self.api_key = None
        self.model = None
        self.client = None
        self.last_error = None
        self.refresh_settings()

    def refresh_settings(self):
        load_dotenv(override=True)

        enabled = os.getenv("GEMINI_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
        api_key = os.getenv("GOOGLE_API_KEYS") or os.getenv("GOOGLE_API_KEY")
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        if enabled == self.enabled and api_key == self.api_key and model == self.model:
            return

        self.enabled = enabled and bool(api_key)
        self.api_key = api_key
        self.model = model
        self.client = genai.Client(api_key=api_key) if self.enabled else None

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

    def _generate_content_with_retry(self, prompt: str):
        last_exc = None

        for attempt in range(2):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
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
            response = self._generate_content_with_retry(prompt)
            return json.loads(self._clean_json(response.text))
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            return self._empty_extract()

    def generate_final_answer(self, user_message: str, decision: dict, fallback_answer: str | None = None):
        self.refresh_settings()

        if not self.enabled or not self.client:
            return None

        prompt = f"""
You are a professional Kuwait Visa Smart Assistant.

The system is ONLY for Kuwait entry visas.
Kuwait is the fixed destination. The country in the decision data means the applicant's country/nationality,
not the destination.

Answer in the same language and dialect style as the user when possible.
Use a polished, human, official-service tone.

Absolute rules:
- Use ONLY the decision data and the fallback answer facts.
- The rule engine decision is authoritative. Never change status, passed checks, failed checks, missing fields, visa number, visa name, or applicant country.
- Do not invent documents, fees, processing time, final approvals, or extra requirements.
- For visa type lists, include every visa number and name from decision.visa_types exactly.
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
{json.dumps(decision, ensure_ascii=False, indent=2)}

Fallback answer to preserve facts and structure:
{fallback_answer or ""}
"""

        try:
            response = self._generate_content_with_retry(prompt)
            return response.text
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            return None


gemini_service = GeminiService()
