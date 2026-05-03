from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from .visa_api import visa_api
from .gemini_service import gemini_service
from .context_store import get_session, update_session, reset_session
from .countries import list_countries
from .rules_engine import (
    extract_first_visa_data,
    check_eligibility,
    build_visa_types_list,
    build_occupation_list,
    build_relationship_list,
)
from .intent_engine import analyze_message
from .response_builder import build_chat_answer, visa_name_for


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


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


class FormCheckRequest(BaseModel):
    ocr_code: str
    visa_type: int | None = None
    age: int | None = None
    occupation: str | None = None
    gender: str | None = None
    relationship: str | list[str] | None = None


def english_display_name(value):
    if not isinstance(value, str):
        return value
    value = value.strip()
    return value.title() if value.isupper() else value


def final_answer(user_message: str, decision: dict, session: dict, extracted: dict):
    fallback_answer = build_chat_answer(user_message, decision, session, extracted)
    gemini_answer = gemini_service.generate_final_answer(
        user_message=user_message,
        decision=decision,
        fallback_answer=fallback_answer,
    )
    decision["answer_source"] = "gemini" if gemini_answer else "fallback"
    if gemini_service.last_error:
        decision["gemini_error"] = gemini_service.last_error
    return gemini_answer or fallback_answer


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

    decision = check_eligibility(
        visa_data,
        {
            "age": req.age,
            "occupation": req.occupation,
            "gender": req.gender,
            "relationship": req.relationship
        }
    )

    decision["raw_visa_details"] = visa_data

    return decision


@app.post("/api/chat")
def chat(req: ChatRequest):
    session = get_session(req.session_id)

    extracted = analyze_message(
        user_message=req.message,
        context=session,
        gemini_service=gemini_service
    )

    update_data = {
        "country": extracted.get("country_name"),
        "country_en": english_display_name(extracted.get("country_name_en")),
        "ocr_code": extracted.get("ocr_code"),
        "visa_type": extracted.get("visa_type"),
        "age": extracted.get("age"),
        "occupation": extracted.get("occupation"),
        "gender": extracted.get("gender"),
        "last_intent": extracted.get("intent"),
    }

    # IMPORTANT:
    # update relationship only if user explicitly mentioned it
    if extracted.get("relationship"):
        update_data["relationship"] = extracted.get("relationship")

    session = update_session(req.session_id, update_data)

    intent = extracted.get("intent")
    ocr_code = session.get("ocr_code")
    visa_type = session.get("visa_type")

    if intent in {"chitchat", "context_question", "provide_country"}:
        decision = {
            "status": "INFO",
            "intent": intent,
        }

        return {
            "answer": final_answer(req.message, decision, session, extracted),
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
            "answer": final_answer(req.message, decision, session, extracted),
            "context": session,
            "extracted": extracted,
            "decision": decision
        }

    if intent == "list_visa_types":
        try:
            api_data = visa_api.get_visa_types_by_country(ocr_code)
            visa_types = build_visa_types_list(api_data)
        except Exception:
            decision = {
                "status": "API_ERROR",
                "intent": intent,
            }

            return {
                "answer": final_answer(req.message, decision, session, extracted),
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
            "answer": final_answer(req.message, decision, session, extracted),
            "context": session,
            "extracted": extracted,
            "decision": decision
        }

    if not visa_type:
        try:
            api_data = visa_api.get_visa_types_by_country(ocr_code)
            visa_types = build_visa_types_list(api_data)
        except Exception:
            decision = {
                "status": "API_ERROR",
                "intent": intent,
            }

            return {
                "answer": final_answer(req.message, decision, session, extracted),
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
            "answer": final_answer(req.message, decision, session, extracted),
            "context": session,
            "extracted": extracted,
            "decision": decision
        }

    try:
        details = visa_api.get_visa_details(ocr_code, int(visa_type))
    except Exception:
        decision = {
            "status": "API_ERROR",
            "intent": intent,
        }

        return {
            "answer": final_answer(req.message, decision, session, extracted),
            "context": session,
            "extracted": extracted,
            "decision": decision
        }

    visa_data = extract_first_visa_data(details)

    decision = check_eligibility(
        visa_data,
        {
            "age": session.get("age"),
            "occupation": session.get("occupation"),
            "gender": session.get("gender"),
            "relationship": extracted.get("relationship") or session.get("relationship")
        }
    )

    decision["intent"] = intent
    decision["raw_visa_details"] = visa_data
    decision["country_ar"] = decision.get("country_ar") or session.get("country")
    decision["country_en"] = english_display_name(decision.get("country_en") or session.get("country_en"))
    decision["applicant_data"] = {
        "age": session.get("age"),
        "occupation": session.get("occupation"),
        "gender": session.get("gender"),
        "relationship": extracted.get("relationship") or session.get("relationship"),
    }

    return {
        "answer": final_answer(req.message, decision, session, extracted),
        "context": session,
        "extracted": extracted,
        "decision": decision
    }


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
