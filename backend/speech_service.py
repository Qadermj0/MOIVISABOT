import base64
import os
import re
from dataclasses import dataclass
from typing import Any

import requests
from dotenv import load_dotenv

from . import config


ARABIC_RE = re.compile(r"[\u0600-\u06ff]")
LATIN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]")


class SpeechServiceError(Exception):
    pass


class SpeechServiceConfigError(SpeechServiceError):
    pass


class SpeechServiceRequestError(SpeechServiceError):
    pass


@dataclass
class SpeechTranscript:
    transcript: str
    language_code: str | None
    confidence: float | None
    raw: dict[str, Any]


class GoogleSpeechService:
    def __init__(self):
        self.last_error: str | None = None

    def transcribe(self, audio_base64: str, mime_type: str | None = None, language: str | None = None) -> SpeechTranscript:
        load_dotenv(override=False)
        self.last_error = None

        audio_content = self._decode_audio(audio_base64)
        self._validate_size(audio_content)

        if self._api_version() == "v2":
            return self._transcribe_v2(audio_content, language)
        return self._transcribe_v1(audio_content, mime_type, language)

    def _transcribe_v1(self, audio_content: bytes, mime_type: str | None, language: str | None) -> SpeechTranscript:
        api_key = self._api_key()
        if not api_key:
            raise SpeechServiceConfigError(
                "Google Speech is not configured. Set SPEECH_API_KEYS or GOOGLE_SPEECH_API_KEY."
            )

        url = self._v1_recognize_url(api_key)
        headers = {"Content-Type": "application/json; charset=utf-8"}
        audio_base64 = base64.b64encode(audio_content).decode("ascii")
        candidates: list[SpeechTranscript] = []

        for language_codes in self._v1_language_batches(language):
            body = {
                "config": self._v1_config(mime_type, language_codes),
                "audio": {
                    "content": audio_base64,
                },
            }
            data = self._post_json(url, headers, body)
            result = self._extract_transcript(data)
            if result.transcript:
                candidates.append(result)

        return self._best_transcript(candidates)

    def _transcribe_v2(self, audio_content: bytes, language: str | None) -> SpeechTranscript:
        project_id = self._project_id()
        location = self._location()
        url = self._recognize_url(project_id, location)
        headers = {"Content-Type": "application/json; charset=utf-8"}

        access_token = self._configured_access_token()
        api_key = self._api_key()
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        elif api_key:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}key={api_key}"
        else:
            access_token = self._default_access_token()
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            else:
                raise SpeechServiceConfigError(
                    "Google Speech is not configured. Set SPEECH_API_KEYS or GOOGLE_SPEECH_API_KEY."
                )

        body = {
            "config": {
                "autoDecodingConfig": {},
                "languageCodes": self._language_codes(language),
                "model": self._model(),
                "features": {
                    "enableAutomaticPunctuation": True,
                },
            },
            "content": base64.b64encode(audio_content).decode("ascii"),
        }

        data = self._post_json(url, headers, body)
        return self._extract_transcript(data)

    def _post_json(self, url: str, headers: dict[str, str], body: dict[str, Any]) -> dict[str, Any]:
        try:
            response = requests.post(
                url,
                headers=headers,
                json=body,
                timeout=self._timeout_seconds(),
            )
        except requests.RequestException as exc:
            self.last_error = str(exc)
            raise SpeechServiceRequestError("Could not reach Google Speech-to-Text.") from exc

        return self._parse_response(response)

    def _decode_audio(self, value: str) -> bytes:
        audio = str(value or "").strip()
        if not audio:
            raise SpeechServiceRequestError("No audio was received.")

        if audio.startswith("data:") and "," in audio:
            audio = audio.split(",", 1)[1]

        try:
            return base64.b64decode(audio, validate=True)
        except (ValueError, TypeError) as exc:
            raise SpeechServiceRequestError("Audio data is not valid base64.") from exc

    def _validate_size(self, audio_content: bytes) -> None:
        max_mb = self._max_audio_mb()
        max_bytes = int(max_mb * 1024 * 1024)
        if len(audio_content) > max_bytes:
            raise SpeechServiceRequestError(
                f"Audio is too large. Maximum size is {max_mb:g} MB."
            )

    def _parse_response(self, response: requests.Response) -> dict[str, Any]:
        try:
            data = response.json()
        except ValueError:
            data = {}

        if response.ok:
            return data

        message = data.get("error", {}).get("message") or data.get("message") or "Google Speech-to-Text failed."
        if "speech.recognizers.recognize" in message:
            message = (
                "Google Speech-to-Text denied the recognize request. Chirp 3 uses Speech-to-Text V2, "
                "which requires the IAM permission speech.recognizers.recognize on the recognizer resource. "
                "An API key can identify the project, but it does not grant that IAM permission."
            )
        self.last_error = message
        raise SpeechServiceRequestError(message)

    def _extract_transcript(self, data: dict[str, Any]) -> SpeechTranscript:
        text_parts: list[str] = []
        language_code: str | None = None
        confidence: float | None = None

        for result in data.get("results", []):
            if not language_code:
                language_code = result.get("languageCode")

            alternatives = result.get("alternatives") or []
            if not alternatives:
                continue

            best = alternatives[0]
            transcript = str(best.get("transcript") or "").strip()
            if transcript:
                text_parts.append(transcript)

            if confidence is None and isinstance(best.get("confidence"), (int, float)):
                confidence = float(best["confidence"])

        return SpeechTranscript(
            transcript=" ".join(text_parts).strip(),
            language_code=language_code,
            confidence=confidence,
            raw=data,
        )

    def _best_transcript(self, candidates: list[SpeechTranscript]) -> SpeechTranscript:
        if not candidates:
            return SpeechTranscript("", None, None, {})

        return max(
            candidates,
            key=self._candidate_score,
        )

    def _candidate_score(self, item: SpeechTranscript) -> tuple[float, int]:
        confidence = item.confidence if item.confidence is not None else 0.0
        transcript = item.transcript or ""
        language_code = (item.language_code or "").lower()

        if language_code.startswith("ar") and not ARABIC_RE.search(transcript):
            confidence -= 0.35

        if not language_code.startswith("ar") and ARABIC_RE.search(transcript):
            confidence -= 0.35

        if language_code.startswith(("en", "fr", "de", "es")) and LATIN_RE.search(transcript):
            confidence += 0.08

        return (confidence, len(transcript))

    def _v1_recognize_url(self, api_key: str) -> str:
        endpoint = self._env("GOOGLE_SPEECH_API_ENDPOINT", config.GOOGLE_SPEECH_API_ENDPOINT).strip()
        endpoint = endpoint.rstrip("/") if endpoint else "https://speech.googleapis.com"
        if endpoint.endswith("/v1/speech:recognize"):
            return f"{endpoint}?key={api_key}"
        return f"{endpoint}/v1/speech:recognize?key={api_key}"

    def _v1_config(self, mime_type: str | None, language_codes: list[str]) -> dict[str, Any]:
        config_body: dict[str, Any] = {
            "encoding": self._v1_audio_encoding(mime_type),
            "sampleRateHertz": self._sample_rate_hertz(),
            "languageCode": language_codes[0],
            "enableAutomaticPunctuation": True,
        }

        alternatives = language_codes[1:4]
        if alternatives and self._use_alternative_languages():
            config_body["alternativeLanguageCodes"] = alternatives

        model = self._model()
        if model:
            config_body["model"] = model

        return config_body

    def _v1_audio_encoding(self, mime_type: str | None) -> str:
        normalized = str(mime_type or "").lower()
        if "ogg" in normalized:
            return "OGG_OPUS"
        return "WEBM_OPUS"

    def _v1_language_batches(self, language: str | None) -> list[list[str]]:
        ordered = self._ordered_language_codes(language)
        if len(ordered) <= 1:
            return [ordered]

        if not self._use_alternative_languages():
            return [[code] for code in ordered]

        batches = []
        for primary in ordered:
            batch = [primary]
            for candidate in ordered:
                if candidate != primary and len(batch) < 4:
                    batch.append(candidate)
            batches.append(batch)
        return batches

    def _recognize_url(self, project_id: str, location: str) -> str:
        endpoint = self._env("GOOGLE_SPEECH_API_ENDPOINT", config.GOOGLE_SPEECH_API_ENDPOINT).strip()
        if not endpoint:
            endpoint = "https://speech.googleapis.com" if location == "global" else f"https://{location}-speech.googleapis.com"

        endpoint = endpoint.rstrip("/")
        recognizer = "projects/{project}/locations/{location}/recognizers/_".format(
            project=project_id,
            location=location,
        )
        return f"{endpoint}/v2/{recognizer}:recognize"

    def _language_codes(self, language: str | None) -> list[str]:
        return self._ordered_language_codes(language)

    def _ordered_language_codes(self, language: str | None) -> list[str]:
        configured = [
            item.strip()
            for item in str(self._env("GOOGLE_SPEECH_LANGUAGE_CODES", config.GOOGLE_SPEECH_LANGUAGE_CODES) or "").split(",")
            if item.strip()
        ]

        language_map = {
            "ar": "ar-KW",
            "en": "en-US",
            "fr": "fr-FR",
            "de": "de-DE",
            "es": "es-ES",
        }
        default_codes = ["ar-KW", "en-US", "fr-FR", "de-DE", "es-ES"]
        codes = configured or default_codes
        primary = language_map.get(str(language or "").lower())

        deduped: list[str] = []
        for code in codes:
            if code not in deduped:
                deduped.append(code)

        if primary and primary in deduped:
            return [primary, *[code for code in deduped if code != primary]]
        return deduped

    def _project_id(self) -> str:
        project_id = (
            self._env("GOOGLE_SPEECH_PROJECT_ID", "")
            or self._env("GOOGLE_CLOUD_PROJECT", "")
            or config.GOOGLE_SPEECH_PROJECT_ID
            or ""
        ).strip()
        if project_id:
            return project_id
        raise SpeechServiceConfigError("Set GOOGLE_SPEECH_PROJECT_ID or GOOGLE_CLOUD_PROJECT for Speech-to-Text.")

    def _location(self) -> str:
        return self._env("GOOGLE_SPEECH_LOCATION", config.GOOGLE_SPEECH_LOCATION or "us").strip()

    def _model(self) -> str:
        return self._env("GOOGLE_SPEECH_MODEL", config.GOOGLE_SPEECH_MODEL or "latest_short").strip()

    def _api_version(self) -> str:
        return self._env("GOOGLE_SPEECH_API_VERSION", config.GOOGLE_SPEECH_API_VERSION or "v1").strip().lower()

    def _use_alternative_languages(self) -> bool:
        value = self._env("GOOGLE_SPEECH_USE_ALTERNATIVE_LANGUAGES", str(config.GOOGLE_SPEECH_USE_ALTERNATIVE_LANGUAGES))
        return str(value).strip().lower() in {"1", "true", "yes", "on"}

    def _sample_rate_hertz(self) -> int:
        try:
            return int(self._env("GOOGLE_SPEECH_SAMPLE_RATE_HERTZ", str(config.GOOGLE_SPEECH_SAMPLE_RATE_HERTZ)))
        except (TypeError, ValueError):
            return config.GOOGLE_SPEECH_SAMPLE_RATE_HERTZ

    def _timeout_seconds(self) -> float:
        try:
            return float(self._env("GOOGLE_SPEECH_TIMEOUT_SECONDS", str(config.GOOGLE_SPEECH_TIMEOUT_SECONDS)))
        except (TypeError, ValueError):
            return config.GOOGLE_SPEECH_TIMEOUT_SECONDS

    def _max_audio_mb(self) -> float:
        try:
            return float(self._env("GOOGLE_SPEECH_MAX_AUDIO_MB", str(config.GOOGLE_SPEECH_MAX_AUDIO_MB)))
        except (TypeError, ValueError):
            return config.GOOGLE_SPEECH_MAX_AUDIO_MB

    def _api_key(self) -> str:
        return (
            self._env("SPEECH_API_KEYS", "")
            or self._env("SPEECH_API_KEY", "")
            or self._env("GOOGLE_SPEECH_API_KEY", "")
            or self._env("GOOGLE_CLOUD_SPEECH_API_KEY", "")
            or self._env("SPEECH_TO_TEXT_API_KEY", "")
            or config.GOOGLE_SPEECH_API_KEY
            or ""
        ).strip()

    def _configured_access_token(self) -> str | None:
        return (
            self._env("GOOGLE_SPEECH_ACCESS_TOKEN", "")
            or config.GOOGLE_SPEECH_ACCESS_TOKEN
            or ""
        ).strip()

    def _default_access_token(self) -> str | None:
        try:
            import google.auth
            from google.auth.transport.requests import Request
        except ImportError:
            return None

        try:
            credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
            credentials.refresh(Request())
            return credentials.token
        except Exception as exc:
            self.last_error = str(exc)
            return None

    def _env(self, name: str, default: str) -> str:
        return os.getenv(name, default)


google_speech_service = GoogleSpeechService()
