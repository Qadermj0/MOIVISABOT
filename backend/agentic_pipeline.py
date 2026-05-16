from .intent_engine import (
    analyze_message,
    is_kuwait_current_location_reference,
    is_non_applicant_country_reference,
)


QUERY_UNDERSTANDING_AGENT = "query_understanding_agent"
INTENT_ROUTER_AGENT = "intent_router_agent"
INQUIRY_ANSWER_AGENT = "inquiry_answer_agent"
ELIGIBILITY_ANSWER_AGENT = "eligibility_answer_agent"
CHITCHAT_ANSWER_AGENT = "chitchat_answer_agent"


INQUIRY_INTENTS = {
    "list_visa_types",
    "visa_details",
    "age_details",
    "occupation_details",
    "occupation_confirmation",
    "relationship_details",
    "dependent_residency_inquiry",
    "residency_admin_inquiry",
    "inside_kuwait_visa_inquiry",
    "visa_comparison_inquiry",
}

ELIGIBILITY_INTENTS = {
    "eligibility_check",
    "relationship_check",
    "relationship_reset",
}

CHITCHAT_INTENTS = {
    "chitchat",
    "context_question",
    "provide_country",
    "system_support_inquiry",
}


PERSONAL_ELIGIBILITY_PHRASES = (
    "هل يمكنني",
    "يمكنني التقديم",
    "هل اقدر",
    "هل أقدر",
    "اقدر اقدم",
    "أقدر أقدم",
    "بقدر اقدم",
    "بقدر أقدم",
    "can i",
    "am i eligible",
    "can apply",
    "can i apply",
)

EXTRACTION_FIELDS = (
    "country",
    "ocr_code",
    "country_name",
    "country_name_en",
    "visa_type",
    "age",
    "occupation",
    "gender",
    "relationship",
)


def route_for_intent(intent: str | None):
    intent = str(intent or "").strip()

    if intent in ELIGIBILITY_INTENTS:
        return "eligibility"

    if intent in INQUIRY_INTENTS:
        return "inquiry"

    if intent in CHITCHAT_INTENTS:
        return "chitchat"

    return "inquiry"


def answer_agent_for_route(route: str | None):
    if route == "eligibility":
        return ELIGIBILITY_ANSWER_AGENT

    if route == "chitchat":
        return CHITCHAT_ANSWER_AGENT

    return INQUIRY_ANSWER_AGENT


def asks_personal_eligibility(message: str):
    text = str(message or "").lower()
    return any(phrase.lower() in text for phrase in PERSONAL_ELIGIBILITY_PHRASES)


def build_agent_trace(extracted: dict, route: str):
    return [
        {
            "agent": QUERY_UNDERSTANDING_AGENT,
            "role": "rewrite ambiguous user wording, then extract country, visa, age, occupation, gender, relationship, and follow-up context",
            "intent": extracted.get("intent"),
            "country_ocr_code": extracted.get("ocr_code"),
            "visa_type": extracted.get("visa_type"),
            "rewritten_query": (extracted.get("rewrite_model") or {}).get("rewritten_query"),
        },
        {
            "agent": INTENT_ROUTER_AGENT,
            "role": "route the message to inquiry, eligibility, or chitchat handling",
            "task_type": route,
            "model_task_type": (extracted.get("router_model") or {}).get("task_type"),
            "answer_agent": answer_agent_for_route(route),
        },
    ]


def _combine_rewrite_text(rewrite_model: dict):
    rewritten = str((rewrite_model or {}).get("rewritten_query") or "").strip()
    country_text = str((rewrite_model or {}).get("country_text") or "").strip()

    if rewritten and country_text and country_text.lower() not in rewritten.lower():
        return f"{rewritten} {country_text}"

    return rewritten or country_text


def _missing(value):
    return value in (None, "",) or value == [] or value == {}


def _merge_understanding(primary: dict, rewritten: dict | None, rewrite_model: dict):
    if not rewritten:
        result = dict(primary)
    else:
        result = dict(primary)
        primary_intent = primary.get("intent")
        rewritten_intent = rewritten.get("intent")

        if primary_intent in {None, "", "general_question"} and rewritten_intent not in {None, "", "general_question"}:
            result["intent"] = rewritten_intent

        if primary_intent == "chitchat" and rewritten_intent in INQUIRY_INTENTS | ELIGIBILITY_INTENTS:
            result["intent"] = rewritten_intent

        for field in EXTRACTION_FIELDS:
            if _missing(result.get(field)) and not _missing(rewritten.get(field)):
                result[field] = rewritten.get(field)

    result["rewrite_model"] = rewrite_model or {}
    result["rewritten_query"] = (rewrite_model or {}).get("rewritten_query")
    result["rewrite_country_text"] = (rewrite_model or {}).get("country_text")
    return result


def understand_message(user_message: str, context: dict, gemini_service):
    rewrite_model = {}
    rewritten_extracted = None

    if gemini_service and hasattr(gemini_service, "rewrite_query"):
        rewrite_model = gemini_service.rewrite_query(user_message, context) or {}

    extracted = analyze_message(
        user_message=user_message,
        context=context,
        gemini_service=gemini_service,
    )

    rewritten_text = _combine_rewrite_text(rewrite_model)
    if rewritten_text and rewritten_text.strip() != str(user_message or "").strip():
        rewritten_extracted = analyze_message(
            user_message=rewritten_text,
            context=context,
            gemini_service=None,
        )

    extracted = _merge_understanding(extracted, rewritten_extracted, rewrite_model)
    if extracted.get("ocr_code") == "KWT" and is_kuwait_current_location_reference(user_message):
        for field in ("country", "ocr_code", "country_name", "country_name_en"):
            extracted[field] = None
    if extracted.get("country") and is_non_applicant_country_reference(user_message, extracted.get("country")):
        for field in ("country", "ocr_code", "country_name", "country_name_en"):
            extracted[field] = None

    route = route_for_intent(extracted.get("intent"))
    router_model = {}

    if gemini_service and hasattr(gemini_service, "route_task"):
        router_model = gemini_service.route_task(user_message, context, extracted) or {}
        model_route = router_model.get("task_type")
        if extracted.get("intent") == "general_question" and model_route in {"inquiry", "eligibility", "chitchat"}:
            route = model_route
        elif (
            model_route == "eligibility"
            and extracted.get("intent") in INQUIRY_INTENTS
            and extracted.get("visa_type")
            and (extracted.get("age") is not None or extracted.get("occupation") or extracted.get("gender"))
        ):
            route = model_route

        if (
            route == "eligibility"
            and extracted.get("intent") in INQUIRY_INTENTS | {"general_question"}
            and extracted.get("intent") not in {"inside_kuwait_visa_inquiry", "visa_comparison_inquiry", "dependent_residency_inquiry", "residency_admin_inquiry"}
            and asks_personal_eligibility(user_message)
        ):
            extracted["intent"] = "eligibility_check"

    if extracted.get("intent") in {"inside_kuwait_visa_inquiry", "visa_comparison_inquiry", "dependent_residency_inquiry", "residency_admin_inquiry"}:
        route = "inquiry"

    extracted["task_type"] = route
    extracted["query_agent"] = QUERY_UNDERSTANDING_AGENT
    extracted["router_agent"] = INTENT_ROUTER_AGENT
    extracted["router_model"] = router_model
    extracted["answer_agent"] = answer_agent_for_route(route)
    extracted["agent_trace"] = build_agent_trace(extracted, route)

    return extracted


def apply_agent_metadata(decision: dict, extracted: dict):
    decision_intent = decision.get("intent")
    extracted_intent = extracted.get("intent")
    if decision_intent and decision_intent != extracted_intent:
        route = route_for_intent(decision_intent)
    else:
        route = extracted.get("task_type") or route_for_intent(decision_intent or extracted_intent)
    answer_agent = extracted.get("answer_agent") or answer_agent_for_route(route)

    decision["task_type"] = route
    decision["query_agent"] = extracted.get("query_agent") or QUERY_UNDERSTANDING_AGENT
    decision["router_agent"] = extracted.get("router_agent") or INTENT_ROUTER_AGENT
    decision["answer_agent"] = answer_agent
    decision["agent_trace"] = extracted.get("agent_trace") or build_agent_trace(
        {**extracted, "intent": decision.get("intent") or extracted.get("intent")},
        route,
    )

    return decision
