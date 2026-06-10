sessions = {}


DEFAULT_CONTEXT = {
    "country": None,
    "country_en": None,
    "ocr_code": None,
    "visa_type": None,
    "age": None,
    "occupation": None,
    "gender": None,
    "relationship": None,
    "applicants": [],
    "pending_fields": [],
    "last_intent": None,
    "language": None
}


def new_context():
    return {
        key: value.copy() if isinstance(value, list) else value
        for key, value in DEFAULT_CONTEXT.items()
    }


def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = new_context()

    return sessions[session_id]


def update_session(session_id: str, data: dict):
    session = get_session(session_id)

    for key, value in data.items():
        if value not in [None, "", [], {}]:
            session[key] = value

    return session


def reset_session(session_id: str):
    sessions[session_id] = new_context()
    return sessions[session_id]
