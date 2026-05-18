import logging
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from .visa_api import visa_api
from .gemini_service import gemini_service
from .context_store import get_session, update_session, reset_session
from .countries import list_countries
from .agentic_pipeline import (
    answer_agent_for_route,
    apply_agent_metadata,
    build_agent_trace,
    understand_message,
)
from .rules_engine import (
    extract_first_visa_data,
    check_eligibility,
    build_visa_types_list,
    build_occupation_list,
    build_relationship_list,
    get_occupation_rules,
    occupation_matches,
)
from .intent_engine import CHECK_WORDS, has_any, is_negated_applicant_country_reference
from .visa_type_matcher import resolve_visa_type_from_text
from .response_builder import build_chat_answer, visa_name_for
from .speech_service import (
    SpeechServiceConfigError,
    SpeechServiceRequestError,
    google_speech_service,
)


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
logger = logging.getLogger(__name__)


app = FastAPI(title="Kuwait Visa Consular Assistant")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: str | None = None


class FormCheckRequest(BaseModel):
    ocr_code: str
    visa_type: int | None = None
    age: int | None = None
    occupation: str | None = None
    gender: str | None = None
    relationship: str | list[str] | None = None


class SpeechToTextRequest(BaseModel):
    audio_base64: str
    mime_type: str | None = None
    language: str | None = None


def english_display_name(value):
    if not isinstance(value, str):
        return value
    value = value.strip()
    return value.title() if value.isupper() else value


def final_answer(user_message: str, decision: dict, session: dict, extracted: dict, language: str | None = None):
    decision = apply_agent_metadata(decision, extracted)
    fallback_answer = build_chat_answer(user_message, decision, session, extracted)
    gemini_answer = gemini_service.generate_final_answer(
        user_message=user_message,
        decision=decision,
        fallback_answer=fallback_answer,
        preferred_language=language,
    )
    decision["answer_source"] = "gemini" if gemini_answer else "fallback"
    if gemini_service.last_error:
        decision["gemini_error"] = gemini_service.last_error
    return gemini_answer or fallback_answer


def intent_for_resolved_visa(message: str):
    return "eligibility_check" if has_any(message, CHECK_WORDS) else "visa_details"


def build_info_decision(visa_data: dict | None, intent: str, session: dict):
    visa_data = visa_data or {}
    country_rule = visa_data.get("countryRule") or {}
    visa_type = visa_data.get("visaType") or session.get("visa_type")

    return {
        "status": "INFO",
        "intent": intent,
        "visa_type": visa_type,
        "visa_name": visa_data.get("typeOfVisa") or visa_name_for(visa_type),
        "visa_name_en": None,
        "country": country_rule.get("ArabicDescription") or session.get("country"),
        "country_ar": country_rule.get("ArabicDescription") or session.get("country"),
        "country_en": english_display_name(country_rule.get("LatinDescription") or session.get("country_en")),
        "country_ocr_code": country_rule.get("OcrCode") or session.get("ocr_code"),
        "ocr_code": country_rule.get("OcrCode") or session.get("ocr_code"),
        "checks": [],
        "missing_fields": [],
        "raw_visa_details": visa_data,
    }


def resolve_occupation_for_rules(visa_data: dict | None, occupation: str | None, context: dict | None = None):
    occupation_text = str(occupation or "").strip()
    if not visa_data or not occupation_text:
        return occupation, None

    occupation_rules = get_occupation_rules(visa_data)
    if not occupation_rules:
        return occupation, None

    matched, _ = occupation_matches(occupation_text, occupation_rules)
    if matched:
        return occupation, None

    occupation_options = []
    for item in build_occupation_list(visa_data):
        option = item.get("occupation_name_en") or item.get("label") or item.get("value")
        if option and option not in occupation_options:
            occupation_options.append(option)

    model_match = gemini_service.match_occupation(
        occupation_text,
        occupation_options,
        context=context or {},
    )

    if not model_match or not model_match.get("matched"):
        return occupation, model_match or None

    try:
        confidence = float(model_match.get("confidence") or 0)
    except (TypeError, ValueError):
        confidence = 0
    if confidence < 0.7:
        return occupation, model_match

    for candidate in (
        model_match.get("matched_value"),
        model_match.get("normalized_occupation"),
    ):
        if not candidate:
            continue
        model_matched, matched_name = occupation_matches(candidate, occupation_rules)
        if model_matched:
            model_match["matched_value"] = matched_name or candidate
            return matched_name or candidate, model_match

    return occupation, model_match


def has_failed_occupation_check(decision: dict | None):
    return any(
        check.get("field") == "occupation" and check.get("passed") is False
        for check in ((decision or {}).get("checks") or [])
    )


def _visa_data_from_list_item_or_api(ocr_code: str, item: dict):
    if isinstance(item, dict) and (item.get("countryRule") or item.get("generalRules")):
        return item

    visa_type = (item or {}).get("visaType") or (item or {}).get("visa_type")
    if not visa_type:
        return None

    details = visa_api.get_visa_details(ocr_code, int(visa_type))
    return extract_first_visa_data(details)


def find_occupation_alternative_visas(
    ocr_code: str | None,
    current_visa_type,
    occupation: str | None,
    preloaded_visa_types_data: dict | None = None,
    limit: int = 5,
):
    if not ocr_code or not occupation:
        return []

    try:
        api_data = preloaded_visa_types_data or visa_api.get_visa_types_by_country(ocr_code)
        raw_items = (api_data.get("result", {}) or {}).get("data", []) if isinstance(api_data, dict) else []
    except Exception:
        logger.exception(
            "Failed to fetch visa list while searching alternatives for country=%s",
            ocr_code,
        )
        return []

    alternatives = []
    seen = set()
    for item in raw_items:
        visa_type = item.get("visaType") or item.get("visa_type")
        if not visa_type or int(visa_type) == int(current_visa_type or 0) or visa_type in seen:
            continue
        seen.add(visa_type)

        try:
            visa_data = _visa_data_from_list_item_or_api(ocr_code, item)
            occupation_rules = get_occupation_rules(visa_data)
            matched, matched_name = occupation_matches(occupation, occupation_rules)
        except Exception:
            logger.exception(
                "Failed to inspect alternative visa=%s for country=%s",
                visa_type,
                ocr_code,
            )
            continue

        if not matched:
            continue

        visa_name = (visa_data or {}).get("typeOfVisa") or item.get("typeOfVisa") or visa_name_for(visa_type)
        if not visa_name or "غير متوفر" in str(visa_name) or "not available" in str(visa_name).lower():
            continue

        alternatives.append({
            "visa_type": visa_type,
            "visa_name": visa_name,
            "visa_name_en": english_display_name(item.get("visa_name_en")) or None,
            "matched_occupation": matched_name,
        })

    priority = {
        8: 0,
        10: 1,
        2: 2,
        1: 3,
        20: 4,
        16: 5,
        6: 6,
    }
    alternatives.sort(key=lambda item: (priority.get(int(item.get("visa_type") or 9999), 50), int(item.get("visa_type") or 9999)))
    return alternatives[:limit]


def attach_occupation_alternative_visas(
    decision: dict,
    ocr_code: str | None,
    current_visa_type,
    occupation: str | None,
    preloaded_visa_types_data: dict | None = None,
):
    if not has_failed_occupation_check(decision):
        return decision

    decision["alternative_visas"] = find_occupation_alternative_visas(
        ocr_code,
        current_visa_type,
        occupation,
        preloaded_visa_types_data=preloaded_visa_types_data,
    )
    return decision


def language_requested_in_message(message: str):
    text = str(message or "").strip().lower()
    if not text:
        return None

    if any(
        phrase in text
        for phrase in (
            "in english",
            "english result",
            "answer in english",
            "بالانجليزي",
            "بالإنجليزي",
            "انجليزي",
            "إنجليزي",
        )
    ):
        return "en"

    if any(
        phrase in text
        for phrase in (
            "in arabic",
            "arabic result",
            "answer in arabic",
            "بالعربي",
            "بالعربية",
            "العربي",
            "العربية",
            "عربي",
        )
    ):
        return "ar"

    return None


def normalize_language_code(language: str | None):
    normalized = str(language or "").strip().lower()
    if normalized in {"ar", "ar-kw", "ar-sa", "arabic", "العربية"}:
        return "ar"
    if normalized in {"en", "en-us", "en-gb", "english"}:
        return "en"
    if normalized in {"fr", "fr-fr", "french", "français", "francais"}:
        return "fr"
    if normalized in {"de", "de-de", "german", "deutsch"}:
        return "de"
    if normalized in {"es", "es-es", "spanish", "español", "espanol"}:
        return "es"
    return normalized or None


def resolve_message_language(message: str, preferred_language: str | None, session: dict):
    requested = language_requested_in_message(message)
    if requested:
        return requested

    normalized = normalize_language_code(preferred_language)

    if re.search(r"[\u0600-\u06ff]", message or ""):
        return "ar"

    if re.search(r"[A-Za-z]", message or ""):
        if normalized in {"fr", "de", "es"}:
            return normalized
        return "en"

    return normalize_language_code(session.get("language")) or normalized or "en"


def retarget_extracted_intent(extracted: dict, intent: str, route: str):
    extracted["intent"] = intent
    extracted["task_type"] = route
    extracted["answer_agent"] = answer_agent_for_route(route)
    extracted["agent_trace"] = build_agent_trace(extracted, route)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/countries")
def countries():
    return {"data": list_countries()}


@app.get("/api/visa-types/{ocr_code}")
def get_visa_types(ocr_code: str):
    api_data = visa_api.get_visa_types_by_country(ocr_code)
    return {
        "raw": api_data,
        "visa_types": build_visa_types_list(api_data)
    }


@app.get("/api/visa-details/{ocr_code}/{visa_type}")
def get_visa_details(ocr_code: str, visa_type: int):
    return visa_api.get_visa_details(ocr_code, visa_type)


@app.get("/api/occupations/{ocr_code}/{visa_type}")
def get_occupations(ocr_code: str, visa_type: int):
    details = visa_api.get_visa_details(ocr_code, visa_type)
    visa_data = extract_first_visa_data(details)
    return {
        "ocr_code": ocr_code,
        "visa_type": visa_type,
        "occupations": build_occupation_list(visa_data),
    }


@app.get("/api/relationships/{ocr_code}/{visa_type}")
def get_relationships(ocr_code: str, visa_type: int):
    details = visa_api.get_visa_details(ocr_code, visa_type)
    visa_data = extract_first_visa_data(details)
    return {
        "ocr_code": ocr_code,
        "visa_type": visa_type,
        "relationships": build_relationship_list(visa_data),
    }


@app.post("/api/reset-session/{session_id}")
def reset_chat_session(session_id: str):
    return reset_session(session_id)


@app.post("/api/speech-to-text")
def speech_to_text(req: SpeechToTextRequest):
    try:
        result = google_speech_service.transcribe(
            audio_base64=req.audio_base64,
            mime_type=req.mime_type,
            language=req.language,
        )
    except SpeechServiceConfigError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except SpeechServiceRequestError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    if not result.transcript:
        raise HTTPException(status_code=422, detail="No speech was detected. Please try again.")

    return {
        "transcript": result.transcript,
        "language_code": result.language_code,
        "confidence": result.confidence,
    }


@app.post("/api/form-check")
def form_check(req: FormCheckRequest):
    if not req.visa_type:
        visa_types_data = visa_api.get_visa_types_by_country(req.ocr_code)

        return {
            "status": "INFO",
            "mode": "visa_types",
            "ocr_code": req.ocr_code,
            "visa_types": build_visa_types_list(visa_types_data),
            "raw": visa_types_data
        }

    details = visa_api.get_visa_details(req.ocr_code, req.visa_type)
    visa_data = extract_first_visa_data(details)
    effective_occupation, occupation_match_model = resolve_occupation_for_rules(
        visa_data,
        req.occupation,
        context={
            "ocr_code": req.ocr_code,
            "visa_type": req.visa_type,
            "source": "direct_eligibility_check",
        },
    )

    decision = check_eligibility(
        visa_data,
        {
            "age": req.age,
            "occupation": effective_occupation,
            "gender": req.gender,
            "relationship": req.relationship
        }
    )
    attach_occupation_alternative_visas(
        decision,
        req.ocr_code,
        req.visa_type,
        effective_occupation,
    )

    if occupation_match_model:
        decision["occupation_match_model"] = occupation_match_model
    decision["raw_visa_details"] = visa_data

    return decision


@app.post("/api/chat")
def chat(req: ChatRequest):
    session = get_session(req.session_id)
    previous_last_intent = session.get("last_intent")
    message_language = resolve_message_language(req.message, req.language, session)

    extracted = understand_message(
        user_message=req.message,
        context=session,
        gemini_service=gemini_service
    )

    previous_ocr_code = session.get("ocr_code")
    previous_visa_type = session.get("visa_type")
    if previous_ocr_code and is_negated_applicant_country_reference(req.message, previous_ocr_code):
        for key in ("country", "country_en", "ocr_code"):
            session[key] = None
        previous_ocr_code = None

    if previous_ocr_code and extracted.get("ocr_code") and extracted.get("ocr_code") != previous_ocr_code:
        for key in ("age", "occupation", "gender", "relationship"):
            session[key] = None
    if previous_visa_type and extracted.get("visa_type") and extracted.get("visa_type") != previous_visa_type:
        for key in ("age", "occupation", "gender", "relationship"):
            session[key] = None

    intent = extracted.get("intent")
    should_update_applicant_fields = intent == "eligibility_check"

    update_data = {
        "country": extracted.get("country_name"),
        "country_en": english_display_name(extracted.get("country_name_en")),
        "ocr_code": extracted.get("ocr_code"),
        "visa_type": extracted.get("visa_type"),
        "age": extracted.get("age") if should_update_applicant_fields else None,
        "occupation": extracted.get("occupation") if should_update_applicant_fields else None,
        "gender": extracted.get("gender") if should_update_applicant_fields else None,
        "last_intent": intent,
        "language": message_language,
    }

    session = update_session(req.session_id, update_data)
    if intent in {"relationship_check", "relationship_reset"}:
        session["relationship"] = None

    ocr_code = session.get("ocr_code")
    visa_type = session.get("visa_type")
    preloaded_visa_types_data = None
    preloaded_visa_types = None
    info_only_intents = {"chitchat", "context_question", "provide_country", "dependent_residency_inquiry", "residency_admin_inquiry", "inside_kuwait_visa_inquiry", "visa_comparison_inquiry", "system_support_inquiry"}
    completes_pending_eligibility_country = (
        intent == "provide_country"
        and previous_last_intent == "eligibility_check"
        and previous_visa_type
        and not previous_ocr_code
        and ocr_code
        and visa_type
    )
    if completes_pending_eligibility_country:
        intent = "eligibility_check"
        extracted["visa_type"] = visa_type
        retarget_extracted_intent(extracted, intent, "eligibility")
        session["last_intent"] = intent

    if ocr_code and not extracted.get("visa_type") and intent not in info_only_intents:
        try:
            preloaded_visa_types_data = visa_api.get_visa_types_by_country(ocr_code)
            preloaded_visa_types = build_visa_types_list(preloaded_visa_types_data)
            visa_name_match = resolve_visa_type_from_text(req.message, preloaded_visa_types)
        except Exception:
            logger.exception(
                "Failed to preload visa types for country=%s",
                ocr_code,
            )
            visa_name_match = None

        if visa_name_match:
            extracted["visa_type"] = visa_name_match["visa_type"]
            extracted["visa_name_match"] = {
                "matched_name": visa_name_match.get("matched_name"),
                "score": visa_name_match.get("score"),
            }
            session = update_session(req.session_id, {"visa_type": visa_name_match["visa_type"]})
            intent = intent_for_resolved_visa(req.message)
            retarget_extracted_intent(
                extracted,
                intent,
                "eligibility" if intent == "eligibility_check" else "inquiry",
            )
            session["last_intent"] = intent
            visa_type = session.get("visa_type")

    if intent == "relationship_reset":
        if ocr_code and visa_type and any(session.get(key) is not None for key in ("age", "occupation", "gender")):
            try:
                details = visa_api.get_visa_details(ocr_code, int(visa_type))
                visa_data = extract_first_visa_data(details)
                effective_occupation, occupation_match_model = resolve_occupation_for_rules(
                    visa_data,
                    session.get("occupation"),
                    context={
                        "ocr_code": ocr_code,
                        "visa_type": visa_type,
                        "country": session.get("country_en") or session.get("country"),
                        "source": "chat_relationship_reset",
                        "message": req.message,
                    },
                )
                if occupation_match_model and occupation_match_model.get("matched") and effective_occupation:
                    session["occupation"] = effective_occupation
                decision = check_eligibility(
                    visa_data,
                    {
                        "age": session.get("age"),
                        "occupation": effective_occupation,
                        "gender": session.get("gender"),
                        "relationship": None,
                    }
                )
                attach_occupation_alternative_visas(
                    decision,
                    ocr_code,
                    visa_type,
                    effective_occupation,
                    preloaded_visa_types_data=preloaded_visa_types_data,
                )
                decision["intent"] = intent
                if occupation_match_model:
                    decision["occupation_match_model"] = occupation_match_model
                decision["raw_visa_details"] = visa_data
                decision["country_ar"] = decision.get("country_ar") or session.get("country")
                decision["country_en"] = english_display_name(decision.get("country_en") or session.get("country_en"))
                decision["applicant_data"] = {
                    "age": session.get("age"),
                    "occupation": effective_occupation,
                    "gender": session.get("gender"),
                    "relationship": None,
                }
            except Exception:
                logger.exception(
                    "Failed to fetch visa details during relationship reset for country=%s visa_type=%s",
                    ocr_code,
                    visa_type,
                )
                decision = {
                    "status": "API_ERROR",
                    "intent": intent,
                }
        else:
            decision = {
                "status": "INFO",
                "intent": intent,
            }

        return {
            "answer": final_answer(req.message, decision, session, extracted, message_language),
            "context": session,
            "extracted": extracted,
            "decision": decision
        }

    if intent in info_only_intents:
        decision = {
            "status": "INFO",
            "intent": intent,
            "visa_type": session.get("visa_type"),
            "visa_name": visa_name_for(session.get("visa_type")),
            "country": session.get("country"),
            "country_ar": session.get("country"),
            "country_en": english_display_name(session.get("country_en")),
            "ocr_code": session.get("ocr_code"),
            "country_ocr_code": session.get("ocr_code"),
        }

        return {
            "answer": final_answer(req.message, decision, session, extracted, message_language),
            "context": session,
            "extracted": extracted,
            "decision": decision
        }

    if not ocr_code:
        decision = {
            "status": "NEED_MORE_INFO",
            "intent": intent,
            "missing_fields": ["country"],
            "visa_type": visa_type,
            "visa_name": visa_name_for(visa_type),
            "message": "Country is required to continue."
        }

        return {
            "answer": final_answer(req.message, decision, session, extracted, message_language),
            "context": session,
            "extracted": extracted,
            "decision": decision
        }

    if intent == "list_visa_types":
        try:
            api_data = preloaded_visa_types_data or visa_api.get_visa_types_by_country(ocr_code)
            visa_types = preloaded_visa_types or build_visa_types_list(api_data)
        except Exception:
            logger.exception(
                "Failed to fetch visa types for country=%s intent=%s",
                ocr_code,
                intent,
            )
            decision = {
                "status": "API_ERROR",
                "intent": intent,
            }

            return {
                "answer": final_answer(req.message, decision, session, extracted, message_language),
                "context": session,
                "extracted": extracted,
                "decision": decision
            }

        decision = {
            "status": "INFO",
            "intent": "list_visa_types",
            "country": session.get("country"),
            "country_ar": session.get("country"),
            "country_en": english_display_name(session.get("country_en")),
            "ocr_code": ocr_code,
            "visa_types": visa_types
        }

        return {
            "answer": final_answer(req.message, decision, session, extracted, message_language),
            "context": session,
            "extracted": extracted,
            "decision": decision
        }

    if not visa_type:
        try:
            api_data = preloaded_visa_types_data or visa_api.get_visa_types_by_country(ocr_code)
            visa_types = preloaded_visa_types or build_visa_types_list(api_data)
        except Exception:
            logger.exception(
                "Failed to fetch visa types while visa type is missing for country=%s intent=%s",
                ocr_code,
                intent,
            )
            decision = {
                "status": "API_ERROR",
                "intent": intent,
            }

            return {
                "answer": final_answer(req.message, decision, session, extracted, message_language),
                "context": session,
                "extracted": extracted,
                "decision": decision
            }

        decision = {
            "status": "NEED_MORE_INFO",
            "intent": intent,
            "country": session.get("country"),
            "country_ar": session.get("country"),
            "country_en": english_display_name(session.get("country_en")),
            "ocr_code": ocr_code,
            "missing_fields": ["visa_type"],
            "available_visa_types": visa_types
        }

        return {
            "answer": final_answer(req.message, decision, session, extracted, message_language),
            "context": session,
            "extracted": extracted,
            "decision": decision
        }

    try:
        details = visa_api.get_visa_details(ocr_code, int(visa_type))
    except Exception:
        logger.exception(
            "Failed to fetch visa details for country=%s visa_type=%s intent=%s",
            ocr_code,
            visa_type,
            intent,
        )
        decision = {
            "status": "API_ERROR",
            "intent": intent,
        }

        return {
            "answer": final_answer(req.message, decision, session, extracted, message_language),
            "context": session,
            "extracted": extracted,
            "decision": decision
        }

    visa_data = extract_first_visa_data(details)

    if intent in {"visa_details", "age_details", "occupation_details", "relationship_details", "occupation_confirmation"}:
        decision = build_info_decision(visa_data, intent, session)
        effective_occupation = session.get("occupation")
        occupation_match_model = None
    else:
        effective_occupation, occupation_match_model = resolve_occupation_for_rules(
            visa_data,
            session.get("occupation"),
            context={
                "ocr_code": ocr_code,
                "visa_type": visa_type,
                "country": session.get("country_en") or session.get("country"),
                "source": "chat",
                "message": req.message,
            },
        )
        if occupation_match_model and occupation_match_model.get("matched") and effective_occupation:
            session["occupation"] = effective_occupation

        relationship_for_check = (
            extracted.get("relationship")
            if intent == "relationship_check" or (intent == "eligibility_check" and int(visa_type) == 10)
            else None
        )

        decision = check_eligibility(
            visa_data,
            {
                "age": session.get("age"),
                "occupation": effective_occupation,
                "gender": session.get("gender"),
                "relationship": relationship_for_check
            }
        )
        attach_occupation_alternative_visas(
            decision,
            ocr_code,
            visa_type,
            effective_occupation,
            preloaded_visa_types_data=preloaded_visa_types_data,
        )

    decision["intent"] = intent
    if intent == "relationship_check":
        relationship_checks = [
            check for check in (decision.get("checks") or [])
            if check.get("field") == "relationship"
        ]
        decision["missing_fields"] = []
        if any(check.get("passed") is False for check in relationship_checks):
            decision["status"] = "NOT_APPROVED"
        elif any(check.get("passed") is True for check in relationship_checks):
            decision["status"] = "APPROVED"

    decision["raw_visa_details"] = visa_data
    if occupation_match_model:
        decision["occupation_match_model"] = occupation_match_model
    decision["country_ar"] = decision.get("country_ar") or session.get("country")
    decision["country_en"] = english_display_name(decision.get("country_en") or session.get("country_en"))
    decision["applicant_data"] = {
        "age": session.get("age"),
        "occupation": effective_occupation,
        "gender": session.get("gender"),
        "relationship": relationship_for_check if "relationship_for_check" in locals() else None,
    }

    return {
        "answer": final_answer(req.message, decision, session, extracted, message_language),
        "context": session,
        "extracted": extracted,
        "decision": decision
    }


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
