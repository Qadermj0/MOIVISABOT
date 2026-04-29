import json
import os

from dotenv import load_dotenv
from google import genai


class GeminiService:
    def __init__(self):
        self.enabled = False
        self.api_key = None
        self.model = None
        self.client = None
        self.refresh_settings()

    def refresh_settings(self):
        load_dotenv(override=True)

        enabled = os.getenv("GEMINI_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
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
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return json.loads(self._clean_json(response.text))
        except Exception:
            return self._empty_extract()

    def generate_final_answer(self, user_message: str, decision: dict):
        self.refresh_settings()

        if not self.enabled or not self.client:
            return None

        prompt = f"""
You are a professional Kuwait visa assistant.
Answer in the same language as the user. Use only the decision data.
Do not invent rules. Do not mention internal JSON.

User message:
{user_message}

Decision data:
{json.dumps(decision, ensure_ascii=False, indent=2)}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text
        except Exception:
            return None


gemini_service = GeminiService()
