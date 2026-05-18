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
    "wish you",
    "safe trip",
    "رحلة موفقة",
    "نتمنى",
)

AGENT_MODEL_ENV = {
    "query_understanding_agent": "GEMINI_QUERY_UNDERSTANDING_MODEL",
    "intent_router_agent": "GEMINI_INTENT_ROUTER_MODEL",
    "occupation_matching_agent": "GEMINI_OCCUPATION_MATCHING_MODEL",
    "inquiry_answer_agent": "GEMINI_INQUIRY_MODEL",
    "eligibility_answer_agent": "GEMINI_ELIGIBILITY_MODEL",
    "chitchat_answer_agent": "GEMINI_CHITCHAT_MODEL",
}

ANSWER_AGENT_INSTRUCTIONS = {
    "inquiry_answer_agent": """
You are the inquiry answer agent.
Your job is to answer information requests only: available visa types, visa details, allowed occupations,
allowed relationships, and allowed age ranges.
Do not turn an inquiry into an eligibility check.
Do not ask for missing applicant data unless the requested information cannot be retrieved without it.
Make the answer explanatory and conversational, but stay inside the visible rule data.
""",
    "eligibility_answer_agent": """
You are the eligibility answer agent.
Your job is to explain an eligibility decision from the rule engine.
The rule engine status, checks, failed checks, and missing fields are mandatory and cannot be changed.
If more information is needed, say that clearly and ask only for the missing fields.
If a check passed, never describe it as failed. If a check failed, never describe it as passed.
""",
    "chitchat_answer_agent": """
You are the chitchat answer agent.
Keep the answer short, warm, and useful.
Do not list visa rules unless the user asks for visa information.
Gently guide the user to provide a country/nationality, visa type, or eligibility details when relevant.
""",
}


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
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
        final_answer_enabled = os.getenv("GEMINI_FINAL_ANSWER_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
        final_answer_intents = self._parse_intents(
            os.getenv("GEMINI_FINAL_ANSWER_INTENTS", "")
        )
        timeout_ms = self._env_int("GEMINI_TIMEOUT_MS", 12000)
        max_output_tokens = self._env_int("GEMINI_MAX_OUTPUT_TOKENS", 2500)
        extract_max_output_tokens = self._env_int("GEMINI_EXTRACT_MAX_OUTPUT_TOKENS", 7500)
        thinking_budget = self._env_int("GEMINI_THINKING_BUDGET", 1000)
        temperature = self._env_float("GEMINI_TEMPERATURE", 0.3)

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

    def _response_language(self, user_message: str, preferred_language: str | None = None) -> str:
        normalized = str(preferred_language or "").strip().lower()
        if normalized in {"ar", "ar-kw", "ar-sa", "arabic", "العربية"}:
            return "Arabic"
        if normalized in {"en", "en-us", "en-gb", "english"}:
            return "English"
        if normalized in {"fr", "fr-fr", "french", "français", "francais"}:
            return "French"
        if normalized in {"de", "de-de", "german", "deutsch"}:
            return "German"
        if normalized in {"es", "es-es", "spanish", "español", "espanol"}:
            return "Spanish"

        if ARABIC_RE.search(user_message or ""):
            return "Arabic"

        if re.search(r"[A-Za-z]", user_message or ""):
            return "English"
        return "English"

    def _has_wrong_language(self, response_language: str, answer: str) -> bool:
        if response_language == "English":
            return bool(ARABIC_RE.search(answer or ""))
        if response_language == "Arabic":
            return not bool(ARABIC_RE.search(answer or ""))
        return False

    def _has_unsupported_note(self, answer: str) -> bool:
        text = str(answer or "").lower()
        return any(marker in text for marker in UNSUPPORTED_NOTE_MARKERS)

    def _misses_relationship_specific_missing_fields(self, answer: str, decision: dict) -> bool:
        status = str((decision or {}).get("status") or "").upper()
        if status != "NEED_MORE_INFO":
            return False

        relationship = str(((decision or {}).get("applicant_data") or {}).get("relationship") or "").lower()
        if "زوج" not in relationship and "wife" not in relationship:
            return False

        missing = set((decision or {}).get("missing_fields") or [])
        if not (missing & {"age", "occupation"}):
            return False

        text = str(answer or "").lower()
        age_ok = not ("age" in missing) or any(
            marker in text
            for marker in (
                "عمر الزوجة",
                "عمر زوجتك",
                "سن الزوجة",
                "wife's age",
                "wife age",
                "age of your wife",
            )
        )
        occupation_ok = not ("occupation" in missing) or any(
            marker in text
            for marker in (
                "مهنة الزوجة",
                "مهنة زوجتك",
                "وظيفة الزوجة",
                "wife's occupation",
                "wife occupation",
                "occupation of your wife",
            )
        )
        return not (age_ok and occupation_ok)

    def _misses_alternative_visas(self, answer: str, decision: dict) -> bool:
        alternatives = (decision or {}).get("alternative_visas") or []
        if not alternatives:
            return False

        text = str(answer or "").lower()
        for item in alternatives:
            visa_type = item.get("visa_type")
            visa_name = str(item.get("visa_name") or item.get("visa_name_en") or "").strip().lower()
            if visa_type and (
                f"فيزا رقم {visa_type}" in text
                or f"visa no. {visa_type}" in text
                or f"visa number {visa_type}" in text
                or f"visa {visa_type}" in text
            ):
                return False
            if visa_name and visa_name in text:
                return False

        return True

    def _contradicts_decision(self, answer: str, decision: dict) -> bool:
        text = str(answer or "").lower()
        status = str((decision or {}).get("status") or "").upper()
        checks = (decision or {}).get("checks") or []

        if status == "NEED_MORE_INFO" and ("not approved" in text or "approved" in text):
            return True

        if status == "APPROVED" and "not approved" in text:
            return True

        if status == "NOT_APPROVED" and (
            "status: approved" in text
            or "currently approved" in text
            or "application is approved" in text
            or "you are approved" in text
        ):
            return True

        for check in checks:
            if check.get("field") != "occupation":
                continue

            if check.get("passed") is True and (
                "occupation is not listed" in text
                or "occupation is not allowed" in text
                or "not listed as an allowed occupation" in text
            ):
                return True

            if check.get("passed") is False and (
                "occupation is allowed" in text
                or "your occupation as" in text and "is allowed" in text
            ):
                return True

        return False

    def _model_for_agent(self, agent_name: str | None):
        env_name = AGENT_MODEL_ENV.get(str(agent_name or "").strip())
        if env_name:
            return os.getenv(env_name) or self.model
        return self.model

    def _generate_content_with_retry(self, prompt: str, config=None, model: str | None = None):
        last_exc = None
        selected_model = model or self.model

        for attempt in range(2):
            try:
                response = self.client.models.generate_content(
                    model=selected_model,
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
        status = str((decision or {}).get("status") or "").upper()
        if status == "API_ERROR" or intent in {"dependent_residency_inquiry", "residency_admin_inquiry", "system_support_inquiry"}:
            return False

        if any(
            check.get("field") == "age_occupation_consistency" and check.get("passed") is False
            for check in ((decision or {}).get("checks") or [])
        ):
            return False

        return not self.final_answer_intents or intent in self.final_answer_intents

    def _compact_decision_for_prompt(self, decision: dict):
        compact = dict(decision or {})
        compact.pop("raw_visa_details", None)
        compact.pop("raw", None)
        return compact

    def extract_query(self, user_message: str, context: dict):
        self.refresh_settings()

        if not self.enabled or not self.client:
            return self._empty_extract()

        prompt = f"""
You are a strict query parser for a Kuwait visa assistant.
Return ONLY valid JSON. Do not answer the user.

Rules:
- Extract Arabic or English country/nationality, visa number, age, occupation, gender, and explicit relationship.
- For age, occupation, and gender, return a value only when the user explicitly stated that field.
- Do not treat a visa number as an age, and do not guess an occupation from the visa type or country.
- Do not treat "inside Kuwait", "from inside Kuwait", "currently in Kuwait", "داخل الكويت", or "موجود في الكويت" as applicant nationality. Kuwait is the destination/current location unless the user explicitly says Kuwaiti nationality.
- Do not treat workplace or residence location as applicant nationality. For example "شغال في البحرين", "أعمل في البحرين", "مقيم في دبي", "working in Bahrain", or "based in Dubai" means location only; ask for nationality unless the user explicitly says "بحريني", "من البحرين", "جنسية البحرين", etc.
- If the user says vacation, holiday, leisure trip, tourist trip, or Arabic equivalents like tourism/vacation wording, map the visa type to 16.
- If the user says a generic personal visit to Kuwait like "زيارة على الكويت", "أطلع زيارة على الكويت", or "visit Kuwait" without family/business/government/medical/study wording, treat it as Tourism Entry Visa / Visa No. 16.
- Treat "I want to register/apply", "ابغى اسجل", "ابي اسجل", or "بدي اقدم" with a visa type/country as an eligibility check, not a generic details request.
- If the user wants to bring/apply/register for their wife to Kuwait without residency/live-with-me wording, map it to Family Visit Entry Visa / Visa No. 10 and keep wife as the explicit relationship.
- Treat shortened job wording as occupation when explicit, for example "software eng" means software engineer, and "president" / "member of council" are occupations.
- Treat modern and abbreviated job wording as occupation when explicit, for example "full stack developer", "DevOps engineer", "data scientist", "CEO", "HR specialist", and "PR manager".
- Treat ownership wording as occupation when explicit: "I have real estate", "I own property", or "real state" means real estate owner.
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
            response = self._generate_content_with_retry(
                prompt,
                config=self.extract_config,
                model=self._model_for_agent("query_understanding_agent"),
            )
            return json.loads(self._clean_json(response.text))
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            return self._empty_extract()

    def rewrite_query(self, user_message: str, context: dict):
        self.refresh_settings()

        if not self.enabled or not self.client:
            return {}

        prompt = f"""
You are the query rewrite agent for a Kuwait visa assistant.
Return ONLY valid JSON. Do not answer the user.

Rewrite the user's message into a clearer query that the visa rules system can understand.

Core job:
- Convert nationality/demonym wording into a country name.
- Do not convert current-location wording into nationality. "داخل الكويت", "موجود في الكويت", "from inside Kuwait", or "currently in Kuwait" means current location, not applicant country.
- Do not convert workplace or residence wording into nationality. "شغال في البحرين", "أعمل في البحرين", "مقيم في دبي", "working in Bahrain", or "based in Dubai" means location only; the rewritten query must say nationality is not mentioned.
- Convert travel-purpose wording such as vacation, holiday, leisure trip, tourism, or Arabic vacation/tourism wording into Tourism Entry Visa / Visa No. 16 when the user is asking what to apply for or whether they can apply.
- Convert generic personal visit wording such as "زيارة على الكويت", "أطلع زيارة على الكويت", or "visit Kuwait" into Tourism Entry Visa / Visa No. 16 unless family, business, government, medical, or study wording is present.
- Convert "ابغى اسجل / ابي اسجل / بدي اقدم" with a visa type into an eligibility/register intent, not visa details.
- Convert "أجيب زوجتي / اقدم لزوجتي / زوجتي على الكويت" into Family Visit Entry Visa / Visa No. 10 unless the user clearly says residency, dependent residency, or "تعيش معي".
- Preserve the user's intent: visa list, visa details, occupations, relationships, age, eligibility check, or chitchat.
- Keep applicant facts if present: age, occupation, gender, visa type, relationship.
- Do not invent facts.
- Kuwait is always the destination. The country in the query is the applicant's nationality/country.

Examples:
- "شنو الفيز المتوفرة للبحرينيين" -> "ما أنواع الفيزا المتوفرة لدولة البحرين؟"
- "انا كوري شو متوفر لي فيز" -> "ما أنواع الفيزا المتوفرة لمواطني كوريا؟"
- "انا شغال في البحرين مهندس هل بقدر اطلع الكويت؟" -> "مقدم الطلب يعمل في البحرين بمهنة مهندس ويريد معرفة إمكانية دخول الكويت؛ جنسية مقدم الطلب غير مذكورة."
- "الصينيين" after a visa-list context -> "ما أنواع الفيزا المتوفرة لمواطني الصين؟"
- "الهنديين شو عندهم" -> "ما أنواع الفيزا المتوفرة لمواطني الهند؟"
- "i am a lawyer from germany can i apply to tourist visa" -> "Applicant from Germany, occupation lawyer, asks eligibility for tourist visa."
- "i need a vacation what type of visa i must apply for" -> "The user wants a vacation to Kuwait; the relevant visa type is Tourism Entry Visa, Visa No. 16."
- "i am 26 years old as software eng" -> "Applicant age 26, occupation software engineer."
- "I have real estate can I apply for visa 8" -> "Applicant occupation real estate owner asks eligibility for Visa No. 8."
- "هل يمكنني التقديم على فيزا سياحية من داخل الكويت وأنا داخل بفيزا زيارة سابقة؟" -> "يسأل عن فيزا سياحية رقم 16 من داخل الكويت أثناء وجوده بزيارة سابقة؛ الجنسية غير مذكورة."
- "انا من الاردن و ابغى اسجل على فيزا 8" -> "مقدم طلب من الأردن يريد فحص/تسجيل أهلية فيزا رقم 8."
- "هل بقدر اجيب زوجتي على الكويت" -> "يريد التقديم للزوجة لزيارة الكويت؛ الفيزا المناسبة زيارة عائلية رقم 10، والعلاقة زوجة."

Return country_text as the normalized country/nationality text when a country is present.
Return rewritten_query in the same language as the user when possible.

User message:
{user_message}

Current context:
{json.dumps(context, ensure_ascii=False)}

Return JSON:
{{
  "rewritten_query": "",
  "country_text": "",
  "intent_hint": "",
  "confidence": 0.0
}}
"""

        try:
            response = self._generate_content_with_retry(
                prompt,
                config=self.extract_config,
                model=self._model_for_agent("query_understanding_agent"),
            )
            data = json.loads(self._clean_json(response.text))
            if not isinstance(data, dict):
                return {}
            return data
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            return {}

    def route_task(self, user_message: str, context: dict, extracted: dict):
        self.refresh_settings()

        if not self.enabled or not self.client:
            return {}

        prompt = f"""
You are the intent router agent for a Kuwait visa assistant.
Return ONLY valid JSON. Do not answer the user.

Choose exactly one task_type:
- inquiry: the user asks for available visa types, visa details, allowed occupations, allowed relationships, or allowed age ranges.
- inquiry: also use this for comparing two visa types, asking about in-country application while already inside Kuwait, dependent/family residency procedure, or website/support hours.
- eligibility: the user asks whether they can apply / are eligible, or provides applicant details for a check.
- chitchat: greetings, thanks, or conversational messages that do not request visa rules.

Rules:
- A message that only changes nationality/country after a visa-list question is inquiry.
- A follow-up like "okay I need to check if I can apply" is eligibility when the context already has a selected or recommended visa type.
- A vacation / holiday purpose points to Tourism Entry Visa (Visa No. 16); keep that context for follow-up eligibility checks.
- A message like "what do Russians have", "الروسيين", "الباكستانيين", or "الهنود" after a visa-list context is inquiry.
- Do not use old context country if the current message names a different nationality.
- Do not route "inside Kuwait / currently in Kuwait / داخل الكويت" questions as a normal eligibility check unless the user also provides applicant nationality and asks to check rules.
- If the user switches from tourism to bringing a wife to live with them, route as inquiry about dependent/family residency, not tourism.
- If the user says they want to bring/apply for their wife to Kuwait without residency/live-with-me wording, route as eligibility for Family Visit Visa No. 10, not as a companion reset for the previous visa.
- If the user asks "which is easier" between tourism and commercial visit, route as inquiry/comparison, not a single visa check.
- Do not infer eligibility unless the user asks to check/apply/allowed/eligible or gives applicant details.

User message:
{user_message}

Current context:
{json.dumps(context, ensure_ascii=False)}

Deterministic extraction:
{json.dumps(extracted, ensure_ascii=False, separators=(",", ":"))}

Return JSON:
{{
  "task_type": "inquiry",
  "confidence": 0.0,
  "reason": ""
}}
"""

        try:
            response = self._generate_content_with_retry(
                prompt,
                config=self.extract_config,
                model=self._model_for_agent("intent_router_agent"),
            )
            data = json.loads(self._clean_json(response.text))
            task_type = str(data.get("task_type") or "").strip().lower()
            if task_type not in {"inquiry", "eligibility", "chitchat"}:
                return {}
            return data
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            return {}

    def match_occupation(self, user_occupation: str, allowed_occupations: list[str], context: dict | None = None):
        self.refresh_settings()

        occupation_text = str(user_occupation or "").strip()
        options = [str(item or "").strip() for item in (allowed_occupations or []) if str(item or "").strip()]

        if not self.enabled or not self.client or not occupation_text or not options:
            return {}

        prompt = f"""
You are the occupation matching agent for a Kuwait visa rules system.
Return ONLY valid JSON. Do not answer the user.

Task:
Decide whether the user's stated occupation semantically matches ONE of the allowed occupation categories.

Strict rules:
- Match only against the provided allowed occupation list.
- Do not invent a new allowed occupation.
- Accept clear synonyms, job families, typos, and ownership phrasing when they belong to an allowed category.
- Examples:
  - "software programmer" can match an information systems / networks / computers / websites category.
  - "full stack developer", "DevOps engineer", "data scientist", "systems analyst", or "نظم معلومات" can match an information systems / networks / computers / websites category.
  - "CEO" can match presidents / chief executives / general managers categories when those are visible.
  - "HR specialist" can match a specialist category only when a specialist/professional category is visible.
  - "راعي أعمال" can match business owner / owners-managers-representatives categories when visible.
  - "دكتور" can match doctors/physicians categories when visible.
  - "I have real estate", "real state", "property owner", or "I own property" can match "Real estate Owners".
  - "president" can match a presidents/deputies/assistants category.
  - "member of council" can match a members of councils category.
- If the user wording is too vague or not semantically equivalent to any allowed category, return matched=false.
- Keep confidence conservative. Use 0.85 or higher only for strong matches.

User occupation:
{occupation_text}

Allowed occupations:
{json.dumps(options[:120], ensure_ascii=False, indent=2)}

Context:
{json.dumps(context or {}, ensure_ascii=False)}

Return JSON:
{{
  "matched": false,
  "matched_value": "",
  "normalized_occupation": "",
  "confidence": 0.0,
  "reason": ""
}}
"""

        try:
            response = self._generate_content_with_retry(
                prompt,
                config=self.extract_config,
                model=self._model_for_agent("occupation_matching_agent"),
            )
            data = json.loads(self._clean_json(response.text))
            if not isinstance(data, dict):
                return {}

            matched_value = str(data.get("matched_value") or "").strip()
            if matched_value and matched_value not in options:
                option_lookup = {option.lower(): option for option in options}
                matched_value = option_lookup.get(matched_value.lower(), matched_value)
                data["matched_value"] = matched_value

            return data
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            return {}

    def generate_final_answer(
        self,
        user_message: str,
        decision: dict,
        fallback_answer: str | None = None,
        preferred_language: str | None = None,
    ):
        if not self.should_generate_final_answer(decision):
            return None

        response_language = self._response_language(user_message, preferred_language)
        decision = {
            **(decision or {}),
            "response_language": response_language,
        }
        answer_agent = decision.get("answer_agent") or "inquiry_answer_agent"
        agent_instructions = ANSWER_AGENT_INSTRUCTIONS.get(answer_agent, ANSWER_AGENT_INSTRUCTIONS["inquiry_answer_agent"])
        answer_model = self._model_for_agent(answer_agent)
        prompt_decision = self._compact_decision_for_prompt(decision)

        prompt = f"""
You are a professional Kuwait Visa Smart Assistant.
You are currently operating as: {answer_agent}.

The system is ONLY for Kuwait entry visas.
Kuwait is the fixed destination. The country in the decision data means the applicant's country/nationality,
not the destination.

Required response language: {response_language}.
This language requirement is mandatory and higher priority than the language of the decision data.
Use a polished, human, official-service tone.
Answer like a helpful conversational assistant, not like a copied template.

Role-specific instructions:
{agent_instructions}

Absolute rules:
- If Required response language is English, every visible label, bullet, heading, visa name, country name, rule name, field name, and sentence in your answer must be English.
- If Required response language is English, do not output Arabic characters at all. Translate Arabic data into English.
- Follow Required response language even if the user's latest message uses another language.
- If Required response language is Arabic, answer in Arabic.
- If Required response language is French, answer entirely in French.
- If Required response language is German, answer entirely in German.
- If Required response language is Spanish, answer entirely in Spanish.
- For English answers, translate Arabic country names, visa names, rule names, and field names into natural English. Do not leave Arabic text in the final answer unless there is no usable English equivalent.
- For French, German, or Spanish answers, translate Arabic and English labels, country names, visa names, rule names, and field names into the required response language when possible.
- Use ONLY the compact decision data and the fallback answer facts.
- The fallback answer is the authoritative fact source for user-visible rule details. Preserve its facts and level of detail, but do not copy its wording rigidly unless the structured format is genuinely clearer.
- You may make the answer more natural and responsive to the exact user question, but you must not add examples, countries, age ranges, gender notes, documents, or requirements that are not already visible in the fallback answer or compact decision data.
- The rule engine decision is authoritative. Never change status, passed checks, failed checks, missing fields, visa number, visa name, or applicant country.
- Do not invent documents, fees, processing time, final approvals, or extra requirements.
- If the user asks about passport image upload, scanned passport files, or technical system upload issues, do not confirm that there is or is not a problem unless the fallback answer explicitly does. Say that this is outside the available eligibility rule data.
- Do not add generic notes about standard procedures, documentation, approvals, or other visa options unless they are present in the decision data.
- Do not add closing service phrases such as "contact us", "further assistance", "additional questions", or "do not hesitate".
- Do not add greetings, congratulations, approval-like encouragement, or travel wishes unless the user explicitly greeted you and the answer is chitchat.
- If no detailed rule conditions are visible, say only that no detailed rule conditions are visible in the current data.
- For visa type lists, include every visa number. Use English visa names for English answers and Arabic visa names for Arabic answers.
- For requirements, explain only the visible rules already present in the fallback answer or compact decision data.
- Preserve the fallback answer facts and level of detail. Do not expand long arrays beyond the fallback answer unless the user explicitly asks for the full list.
- For eligibility checks, clearly explain Approved / Not Approved / Need More Information based on decision.status.
- If decision.intent is visa_details, answer as an informational rule summary only. Do not describe it as an eligibility check, do not mention missing fields, and do not ask the user to provide age, occupation, gender, or relationship.
- For visa_details, summarize relationship lists briefly and do not list more than 12 relationships unless the user explicitly asks about relationships.
- If decision.intent is age_details, answer only with the age rule for the selected country and visa. Do not ask for age, occupation, gender, or relationship.
- If decision.intent is occupation_details, answer only with the allowed occupations or professional categories for the selected country and visa. Do not list visa types and do not ask the user to provide their occupation.
- If decision.intent is occupation_confirmation, directly confirm or correct the user's understanding using the visible occupation rules. Do not ask for age or occupation.
- If decision.intent is relationship_details, answer only with the allowed relationships/companions. If none are listed, clearly say that no relationships or companions are allowed in the current data. Do not list visa types.
- If decision.intent is relationship_check, answer only whether the mentioned relationship is allowed or not allowed. Do not ask for age, occupation, or gender.
- If decision.intent is relationship_reset, acknowledge that the companion/relationship was removed from the check, then give the updated result if the compact decision contains one.
- If decision.status is NEED_MORE_INFO, never call it Approved or Not Approved. Say that more information is needed and ask only for missing_fields.
- If the check is for the wife as the applicant and missing_fields includes age or occupation, ask specifically for the wife's age and/or wife's occupation. Do not ask for generic age or occupation.
- If decision.status is NOT_APPROVED because occupation failed, do not ask for age just because it is absent. The failed occupation already determines the current visa result.
- If decision.alternative_visas is present, mention those alternative visa numbers as options the user may check instead. Do not invent alternatives.
- If occupation is failed, do not say it is allowed. If occupation is passed, do not say it is failed.
- Gender rules are a blacklist. A listed gender is restricted; any other explicitly provided gender passes. If gender is not provided, do not ask for gender; mention the visible allowed-gender note from decision.details.gender_policy.
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
{json.dumps(prompt_decision, ensure_ascii=False, separators=(",", ":"))}

Fallback answer with authoritative facts:
{fallback_answer or ""}
"""

        try:
            response = self._generate_content_with_retry(
                prompt,
                config=self.answer_config,
                model=answer_model,
            )
            answer = response.text

            if (
                self._contradicts_decision(answer, decision)
                or self._misses_relationship_specific_missing_fields(answer, decision)
                or self._misses_alternative_visas(answer, decision)
            ):
                return None

            if self._has_wrong_language(response_language, answer) or self._has_unsupported_note(answer):
                repair_prompt = f"""
Rewrite the assistant answer below entirely in {response_language}.
Do not add new facts. Remove unsupported generic notes, closing service phrases, referrals, standard procedure/documentation statements, and anything not directly supported by the compact decision data or fallback answer.
Do not remove visa numbers, status, country, missing fields, passed checks, or failed checks.
If the target language is English, do not output Arabic characters.

Compact decision data:
{json.dumps(prompt_decision, ensure_ascii=False, separators=(",", ":"))}

Fallback answer:
{fallback_answer or ""}

Assistant answer to rewrite:
{answer}
"""
                repair_response = self._generate_content_with_retry(
                    repair_prompt,
                    config=self.answer_config,
                    model=answer_model,
                )
                repaired_answer = repair_response.text
                if (
                    self._contradicts_decision(repaired_answer, decision)
                    or self._misses_relationship_specific_missing_fields(repaired_answer, decision)
                    or self._misses_alternative_visas(repaired_answer, decision)
                ):
                    return None
                return repaired_answer

            return answer
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            return None


gemini_service = GeminiService()
