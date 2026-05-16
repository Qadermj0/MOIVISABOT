import threading
import time

import requests
import urllib3
from .config import KUWAIT_VISA_API_BASE, VISA_API_CACHE_TTL_SECONDS, VISA_API_TIMEOUT_SECONDS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class VisaApiService:
    def __init__(self):
        self.base_url = KUWAIT_VISA_API_BASE
        self.session = requests.Session()
        self.timeout = VISA_API_TIMEOUT_SECONDS
        self.cache_ttl = VISA_API_CACHE_TTL_SECONDS
        self._cache = {}
        self._stale_cache = {}
        self._cache_lock = threading.Lock()

    def _cache_get(self, key):
        if self.cache_ttl <= 0:
            return None

        with self._cache_lock:
            cached = self._cache.get(key)
            if not cached:
                return None

            expires_at, value = cached
            if expires_at <= time.monotonic():
                self._cache.pop(key, None)
                return None

            return value

    def _stale_cache_get(self, key):
        with self._cache_lock:
            return self._stale_cache.get(key)

    def _cache_set(self, key, value):
        with self._cache_lock:
            self._stale_cache[key] = value
            if self.cache_ttl > 0:
                expires_at = time.monotonic() + self.cache_ttl
                self._cache[key] = (expires_at, value)

    def _get_rules(self, params: dict):
        cache_key = tuple(sorted(params.items()))
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cached

        url = f"{self.base_url}/getVisaTypesByCountry"
        last_error = None

        for attempt in range(3):
            try:
                response = self.session.get(url, params=params, verify=False, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                self._cache_set(cache_key, data)
                return data
            except Exception as exc:
                last_error = exc
                if attempt < 2:
                    time.sleep(0.35 * (attempt + 1))

        stale = self._stale_cache_get(cache_key)
        if stale is not None:
            return stale

        raise last_error

    def get_visa_types_by_country(self, ocr_code: str):
        params = {"ocrCode": ocr_code}
        return self._get_rules(params)

    def get_visa_details(self, ocr_code: str, visa_type: int):
        params = {
            "ocrCode": ocr_code,
            "visaType": visa_type
        }
        return self._get_rules(params)


visa_api = VisaApiService()
