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
    "last_intent": None
}


def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = DEFAULT_CONTEXT.copy()

    return sessions[session_id]


def update_session(session_id: str, data: dict):
    session = get_session(session_id)

    for key, value in data.items():
        if value not in [None, "", [], {}]:
            session[key] = value

    return session


def reset_session(session_id: str):
    sessions[session_id] = DEFAULT_CONTEXT.copy()
    return sessions[session_id]
