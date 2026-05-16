from __future__ import annotations

import difflib

from .intent_engine import normalize_text


TOKEN_REPLACEMENTS = {
    "سما": "سمه",
    "سمه": "سمه",
    "تاشيره": "فيزا",
    "تأشيره": "فيزا",
}

COMMON_TOKENS = {
    "ابي",
    "ابغى",
    "اقدر",
    "اقدم",
    "التقديم",
    "انا",
    "بقدر",
    "دخول",
    "رقم",
    "سمه",
    "على",
    "عن",
    "فيزا",
    "للتقديم",
    "للكويت",
    "من",
    "نوع",
    "visa",
    "entry",
    "apply",
    "can",
    "i",
    "no",
    "number",
}

VISA_ALIASES = {
    1: ["سمة دخول عمل بالحكومة", "عمل حكومة", "عمل حكومي", "government work"],
    2: ["سمة دخول عمل اهلي", "عمل اهلي", "عمل خاص", "private sector work"],
    3: ["سمة دخول عامل منزلي", "عامل منزلي", "domestic worker"],
    6: ["سمة دخول دراسة", "دراسة", "طالب", "study visa", "student visa"],
    7: ["سمة دخول علاج", "علاج", "medical treatment"],
    8: ["سمة دخول زيارة تجارية", "زيارة تجارية", "تجارية", "commercial visit", "business visit"],
    9: ["سمة دخول زيارة حكومية", "زيارة حكومية", "حكومية", "government visit"],
    10: ["سمة دخول زيارة عائلية", "زيارة عائلية", "عائلية", "family visit", "family visa", "family visit visa", "family entry visa"],
    11: ["سمة دخول زيارة لسفارة", "زيارة سفارة", "سفارة", "embassy visit"],
    14: ["سمة عودة عدة سفرات", "عودة عدة سفرات", "عدة سفرات", "multiple return"],
    16: ["سمة دخول للسياحة", "سياحة", "سياحي", "tourism", "tourist visa"],
    19: ["سمة عودة", "عودة", "return visa"],
    20: ["سمة دخول خاصة", "سمة الدخول الخاصة", "سمه دخول خاصه", "الخاصة", "خاصه", "special entry", "special visa"],
}


def normalize_visa_token(token: str) -> str:
    value = normalize_text(token)
    for prefix in ("وال", "بال", "كال", "فال", "لل", "ال", "ل", "ب"):
        if value.startswith(prefix) and len(value) > len(prefix) + 2:
            value = value[len(prefix):]
            break
    return TOKEN_REPLACEMENTS.get(value, value)


def visa_tokens(value: str, *, meaningful_only: bool = False) -> list[str]:
    tokens = []
    for token in normalize_text(value).split():
        normalized = normalize_visa_token(token)
        if not normalized:
            continue
        if meaningful_only and normalized in COMMON_TOKENS:
            continue
        tokens.append(normalized)
    return tokens


def normalized_phrase(value: str) -> str:
    return " ".join(visa_tokens(value))


def visa_candidate_names(visa_type: int | None, visa_item: dict) -> list[str]:
    names = [
        visa_item.get("visa_name"),
        visa_item.get("visa_name_en"),
        *VISA_ALIASES.get(int(visa_type or 0), []),
    ]
    cleaned = []
    seen = set()
    for name in names:
        normalized = normalized_phrase(str(name or ""))
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        cleaned.append(str(name))
    return cleaned


def phrase_window_scores(message_tokens: list[str], candidate_tokens: list[str]) -> float:
    if not message_tokens or not candidate_tokens:
        return 0

    candidate = " ".join(candidate_tokens)
    best = 0.0
    window_size = max(1, len(candidate_tokens))
    for start in range(0, max(1, len(message_tokens) - window_size + 1)):
        window = " ".join(message_tokens[start:start + window_size])
        best = max(best, difflib.SequenceMatcher(None, window, candidate).ratio())
    return best


def score_visa_name(message: str, candidate_name: str) -> float:
    message_phrase = normalized_phrase(message)
    candidate_phrase = normalized_phrase(candidate_name)
    if not candidate_phrase:
        return 0

    message_meaningful = set(visa_tokens(message, meaningful_only=True))
    candidate_meaningful = visa_tokens(candidate_name, meaningful_only=True)
    if not candidate_meaningful:
        return 0

    score = 0.0
    if candidate_phrase in message_phrase:
        score = max(score, 96 + min(len(candidate_meaningful), 4))

    overlap = sum(1 for token in candidate_meaningful if token in message_meaningful)
    if overlap == len(candidate_meaningful):
        score = max(score, 82 + min(len(candidate_meaningful) * 3, 12))
    elif overlap >= 2 and overlap / len(candidate_meaningful) >= 0.67:
        score = max(score, 68 + overlap)

    fuzzy = phrase_window_scores(visa_tokens(message), visa_tokens(candidate_name))
    if fuzzy >= 0.9:
        score = max(score, 76 + fuzzy * 10)

    return score


def resolve_visa_type_from_text(message: str, visa_types: list[dict]) -> dict | None:
    ranked = []

    for item in visa_types or []:
        visa_type = item.get("visa_type")
        try:
            visa_type_int = int(visa_type)
        except (TypeError, ValueError):
            continue

        best_score = 0.0
        best_name = None
        for name in visa_candidate_names(visa_type_int, item):
            score = score_visa_name(message, name)
            if score > best_score:
                best_score = score
                best_name = name

        if best_score:
            ranked.append((best_score, visa_type_int, best_name, item))

    if not ranked:
        return None

    ranked.sort(key=lambda row: row[0], reverse=True)
    best = ranked[0]
    second_score = ranked[1][0] if len(ranked) > 1 else 0

    if best[0] < 75 or best[0] - second_score < 5:
        return None

    return {
        "visa_type": best[1],
        "matched_name": best[2],
        "score": round(best[0], 2),
        "visa_item": best[3],
    }
