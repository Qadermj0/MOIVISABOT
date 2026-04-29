import requests
import urllib3
from .config import KUWAIT_VISA_API_BASE

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class VisaApiService:
    def __init__(self):
        self.base_url = KUWAIT_VISA_API_BASE

    def get_visa_types_by_country(self, ocr_code: str):
        url = f"{self.base_url}/getVisaTypesByCountry"
        params = {"ocrCode": ocr_code}

        response = requests.get(url, params=params, verify=False, timeout=60)
        response.raise_for_status()
        return response.json()

    def get_visa_details(self, ocr_code: str, visa_type: int):
        url = f"{self.base_url}/getVisaTypesByCountry"
        params = {
            "ocrCode": ocr_code,
            "visaType": visa_type
        }

        response = requests.get(url, params=params, verify=False, timeout=60)
        response.raise_for_status()
        return response.json()


visa_api = VisaApiService()