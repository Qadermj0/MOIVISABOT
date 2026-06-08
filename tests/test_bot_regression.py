import os
import unittest

os.environ["GEMINI_ENABLED"] = "false"
os.environ["GEMINI_FINAL_ANSWER_ENABLED"] = "false"

from fastapi.testclient import TestClient

from backend import main
from backend.agentic_pipeline import understand_message
from backend.context_store import sessions
from backend.intent_engine import resolve_applicant_country


def visa_item(ocr_code, country_ar, country_en, visa_type, visa_name, *, age=(0, 100), occupations=None, relationships=None, gender=None):
    rules = {
        "age": {
            "minAge": age[0],
            "maxAge": age[1],
        },
    }
    if occupations is not None:
        rules["newOccupation"] = [
            {"ArabicDescription": ar, "DescriptionEn": en}
            for ar, en in occupations
        ]
    if relationships is not None:
        rules["relationship"] = [
            {"relationNameAr": ar, "relationNameEn": en}
            for ar, en in relationships
        ]
    if gender is not None:
        rules["gender"] = gender

    return {
        "visaType": visa_type,
        "typeOfVisa": visa_name,
        "countryRule": {
            "ArabicDescription": country_ar,
            "LatinDescription": country_en,
            "OcrCode": ocr_code,
            "rules": rules,
        },
        "generalRules": {},
    }


class FakeVisaApi:
    def __init__(self):
        self.data = {}
        self._add(
            "JOR",
            "الأردن",
            "JORDAN",
            [
                visa_item(
                    "JOR",
                    "الأردن",
                    "JORDAN",
                    8,
                    "سمة دخول زيارة تجارية",
                    occupations=[
                        ("القضاة وأعضاء النيابة العامة والمحامين ", "Judges, public prosecutors and lawyers"),
                        ("الرؤساء ونوابهم ومساعديهم بجميع مسمياتهم", "Presidents and deputies"),
                        ("ضابط مبيعات", "Sales Officer"),
                    ],
                    gender=["female"],
                ),
                visa_item(
                    "JOR",
                    "الأردن",
                    "JORDAN",
                    16,
                    "سمة دخول للسياحة",
                    age=(0, 100),
                    occupations=[
                        ("أعضاء المجالس ونوابهم ومساعدوهم", "All related Titles for Members of Councils and their Deputies and Assistants"),
                        ("الرؤساء ونوابهم ومساعدوهم بجميع مسمياتهم", "All related Titles for Presidents and their Deputies and Assistants"),
                    ],
                ),
                visa_item(
                    "JOR",
                    "الأردن",
                    "JORDAN",
                    10,
                    "سمة دخول زيارة عائلية",
                    occupations=[
                        ("المحاسبون", "Accountants"),
                        (
                            "الوظائف الأساسية والفنية لنظم المعلومات والشبكات والحاسوب والمواقع الإلكترونية",
                            "Main and Technical Professions in Information Systems, Networks, Computers, and Electronic Websites",
                        ),
                    ],
                    relationships=[("الزوجة", "Wife"), ("الابن", "Son")],
                ),
            ],
        )
        self._add(
            "DEU",
            "ألمانيا",
            "GERMANY",
            [
                visa_item(
                    "DEU",
                    "ألمانيا",
                    "GERMANY",
                    8,
                    "سمة دخول زيارة تجارية",
                    occupations=[
                        ("المحامون", "Lawyers"),
                        ("أساتذة الجامعات", "University Professors"),
                    ],
                    gender=["female"],
                ),
                visa_item(
                    "DEU",
                    "ألمانيا",
                    "GERMANY",
                    20,
                    "سمة دخول خاصة",
                    age=(0, 60),
                    occupations=[
                        ("أستاذ أصول التربية", "Professor of Education Principles"),
                        ("أستاذ آداب", "Professor of Literature"),
                        ("أستاذ أرصاد", "Professor of Meteorology"),
                    ],
                    relationships=[],
                ),
                visa_item(
                    "DEU",
                    "ألمانيا",
                    "GERMANY",
                    16,
                    "سمة دخول للسياحة",
                    age=(0, 100),
                    occupations=[
                        ("المحامون", "Lawyers"),
                        ("أساتذة الجامعات", "University Professors"),
                    ],
                ),
            ],
        )
        self._add(
            "AAA",
            "الشيشان",
            "CHECHENIA",
            [
                visa_item(
                    "AAA",
                    "الشيشان",
                    "CHECHENIA",
                    8,
                    "سمة دخول زيارة تجارية",
                    occupations=[
                        ("الخبراء ونوابهم ومساعديهم بجميع مسمياتهم", "Experts and deputies"),
                        ("استشاري", "Consultant"),
                    ],
                    gender=["female"],
                ),
            ],
        )
        self._add(
            "CYP",
            "Cyprus",
            "CYPRUS",
            [
                visa_item(
                    "CYP",
                    "Cyprus",
                    "CYPRUS",
                    8,
                    "Commercial Visit Entry Visa",
                    occupations=[
                        ("Real estate owners", "Real estate Owners"),
                        ("Presidents", "All related Titles for Presidents and their Deputies and Assistants"),
                    ],
                    gender=["female"],
                ),
                visa_item(
                    "CYP",
                    "Cyprus",
                    "CYPRUS",
                    16,
                    "Tourism Entry Visa",
                    occupations=[
                        ("Presidents", "All related Titles for Presidents and their Deputies and Assistants"),
                    ],
                ),
            ],
        )
        self._add(
            "ARM",
            "أرمينيا",
            "ARMINIA",
            [
                visa_item(
                    "ARM",
                    "أرمينيا",
                    "ARMINIA",
                    8,
                    "سمة دخول زيارة تجارية",
                    occupations=[
                        ("الأطباء والجراحون ونوابهم ومساعديهم بجميع مسمياتهم، فنيين ومساعدين المهن الطبية والطبية المساعدة، الصيادلة", "Doctors, surgeons, medical assistants and pharmacists"),
                    ],
                    gender=["female"],
                ),
            ],
        )
        self._add(
            "BRN",
            "بوروني",
            "BRUNEI",
            [
                visa_item("BRN", "بوروني", "BRUNEI", 16, "سمة دخول للسياحة", occupations=[]),
            ],
        )
        self._add(
            "RUS",
            "روسيا",
            "RUSSIA",
            [
                visa_item("RUS", "روسيا", "RUSSIA", 16, "سمة دخول للسياحة", occupations=[]),
                visa_item("RUS", "روسيا", "RUSSIA", 8, "سمة دخول زيارة تجارية", occupations=[]),
            ],
        )
        self._add(
            "IND",
            "India",
            "INDIA",
            [
                visa_item(
                    "IND",
                    "India",
                    "INDIA",
                    16,
                    "Tourism Entry Visa",
                    occupations=[
                        ("Council members", "All related Titles for Members of Councils and their Deputies and Assistants"),
                        ("Presidents", "All related Titles for Presidents and their Deputies and Assistants"),
                    ],
                    relationships=[("Sister", "Sister"), ("Father", "Father")],
                ),
                visa_item(
                    "IND",
                    "India",
                    "INDIA",
                    10,
                    "Family Visit Entry Visa",
                    occupations=[
                        (
                            "IT professionals",
                            "Main and Technical Professions in Information Systems, Networks, Computers, and Electronic Websites",
                        ),
                        ("Presidents", "All related Titles for Presidents and their Deputies and Assistants"),
                    ],
                    relationships=[("Sister", "Sister"), ("Father", "Father")],
                ),
            ],
        )
        self._add(
            "QAT",
            "قطر",
            "QATAR",
            [
                visa_item(
                    "QAT",
                    "قطر",
                    "QATAR",
                    16,
                    "سمة دخول للسياحة",
                    occupations=[
                        ("الرؤساء ونوابهم ومساعديهم بجميع مسمياتهم", "Presidents and deputies"),
                    ],
                ),
                visa_item(
                    "QAT",
                    "قطر",
                    "QATAR",
                    8,
                    "سمة دخول زيارة تجارية",
                    occupations=[
                        ("المهندسون ونوابهم ومساعديهم بجميع مسمياتهم", "All related titles for Engineers and their Deputies and Assistants"),
                    ],
                ),
                visa_item(
                    "QAT",
                    "قطر",
                    "QATAR",
                    2,
                    "سمة دخول عمل أهلي",
                    occupations=[
                        ("المهندسون ونوابهم ومساعديهم بجميع مسمياتهم", "All related titles for Engineers and their Deputies and Assistants"),
                    ],
                ),
            ],
        )

    def _add(self, ocr_code, country_ar, country_en, items):
        self.data[ocr_code] = items

    def _response(self, items):
        return {"result": {"data": items}}

    def get_visa_types_by_country(self, ocr_code):
        return self._response(self.data.get(str(ocr_code).upper(), []))

    def get_visa_details(self, ocr_code, visa_type):
        for item in self.data.get(str(ocr_code).upper(), []):
            if item.get("visaType") == int(visa_type):
                return self._response([item])
        return self._response([])


class FailingVisaApi(FakeVisaApi):
    def get_visa_types_by_country(self, ocr_code):
        raise RuntimeError("simulated visa API outage")

    def get_visa_details(self, ocr_code, visa_type):
        raise RuntimeError("simulated visa API outage")


class BotRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_visa_api = main.visa_api
        main.visa_api = FakeVisaApi()
        main.gemini_service.enabled = False
        main.gemini_service.client = None
        main.gemini_service.final_answer_enabled = False
        cls.client = TestClient(main.app)

    @classmethod
    def tearDownClass(cls):
        main.visa_api = cls.original_visa_api

    def setUp(self):
        sessions.clear()

    def chat(self, message, session_id="test-session", language="ar"):
        response = self.client.post(
            "/api/chat",
            json={
                "session_id": session_id,
                "message": message,
                "language": language,
            },
        )
        self.assertEqual(response.status_code, 200)
        return response.json()

    def test_jordanian_judge_question_is_eligibility_and_asks_for_age(self):
        data = self.chat("مرحبا انا اردني مهنتي القضاه هل يمكنني التقديم على فيزا 8")

        self.assertEqual(data["extracted"]["intent"], "eligibility_check")
        self.assertEqual(data["decision"]["status"], "NEED_MORE_INFO")
        self.assertEqual(data["decision"]["country_ocr_code"], "JOR")
        self.assertEqual(data["decision"]["visa_type"], 8)
        self.assertIn("age", data["decision"]["missing_fields"])
        self.assertTrue(any(check["field"] == "occupation" and check["passed"] for check in data["decision"]["checks"]))

    def test_jordanian_judge_with_age_is_approved(self):
        data = self.chat("انا اردني مهنتي قاضي عمري 30 هل يمكنني التقديم على فيزا 8")

        self.assertEqual(data["decision"]["status"], "APPROVED")
        self.assertTrue(any(check["field"] == "occupation" and check["passed"] for check in data["decision"]["checks"]))
        self.assertTrue(any(check["field"] == "age" and check["passed"] for check in data["decision"]["checks"]))

    def test_pharmacist_occupation_variants_match_allowed_pharmacists(self):
        occupations = [
            {
                "ArabicDescription": "الأطباء والجراحون ونوابهم ومساعديهم بجميع مسمياتهم، فنيين ومساعدين المهن الطبية والطبية المساعدة، الصيادلة"
            }
        ]

        from backend.rules_engine import occupation_matches

        for occupation in ["صيدلي", "صيدلاني", "pharmacist", "الصيادلة"]:
            with self.subTest(occupation=occupation):
                matched, matched_name = occupation_matches(occupation, occupations)
                self.assertTrue(matched)
                self.assertIn("الصيادلة", matched_name)

    def test_impossible_minor_professional_is_blocked_even_if_age_rule_allows_zero(self):
        data = self.chat("انا محامي عمري 5 سنوات من المانيا هل يمكنني التقديم على فيزا 8")

        self.assertEqual(data["decision"]["status"], "NOT_APPROVED")
        self.assertTrue(
            any(
                check["field"] == "age_occupation_consistency" and check["passed"] is False
                for check in data["decision"]["checks"]
            )
        )

    def test_chechen_nationality_uses_aaa_not_antarctica_and_passport_upload_is_guarded(self):
        data = self.chat(
            "أنا مواطن أحمل الجنسية (الشيشانية) وأعمل بمهنة (مدير مبيعات). "
            "أريد التقديم على سمة دخول زيارة تجارية (رقم (8) لزيارة دولة الكويت. "
            "هل مهنتي مسموحة؟ وهل سأواجه أي مشكلة عند رفع صورة جواز سفري للنظام؟"
        )

        self.assertEqual(data["extracted"]["ocr_code"], "AAA")
        self.assertEqual(data["decision"]["country_ocr_code"], "AAA")
        self.assertEqual(data["decision"]["country"], "الشيشان")
        self.assertNotIn("القارة القطبية", data["answer"])
        self.assertIn("لا أقدر أؤكد", data["answer"])

    def test_tourist_visa_age_question_is_information_not_full_check(self):
        data = self.chat("for visa 16 from jordan what age is allowed", language="en")

        self.assertEqual(data["extracted"]["intent"], "age_details")
        self.assertEqual(data["decision"]["status"], "INFO")
        self.assertIn("0", data["answer"])
        self.assertIn("100", data["answer"])
        self.assertNotIn("Occupation", data["answer"])

    def test_indian_tourist_check_does_not_treat_nationality_as_occupation(self):
        data = self.chat("can i apply for tourist visa. i'm indian", language="en")

        self.assertEqual(data["extracted"]["intent"], "eligibility_check")
        self.assertEqual(data["extracted"]["ocr_code"], "IND")
        self.assertEqual(data["extracted"]["visa_type"], 16)
        self.assertIsNone(data["extracted"]["occupation"])
        self.assertEqual(data["decision"]["status"], "NEED_MORE_INFO")
        self.assertIn("age", data["decision"]["missing_fields"])
        self.assertIn("occupation", data["decision"]["missing_fields"])
        self.assertFalse(
            any(
                check["field"] == "occupation" and check["passed"] is False
                for check in data["decision"]["checks"]
            )
        )

    def test_vacation_purpose_sets_tourist_visa_for_followup_check(self):
        session_id = "vacation-followup"
        first = self.chat("i went to kuwait for a vacation this week can i apply", session_id=session_id, language="en")

        self.assertEqual(first["extracted"]["intent"], "eligibility_check")
        self.assertEqual(first["extracted"]["visa_type"], 16)
        self.assertIn("country", first["decision"]["missing_fields"])

        second = self.chat("indian", session_id=session_id, language="en")

        self.assertEqual(second["extracted"]["intent"], "eligibility_check")
        self.assertEqual(second["context"]["ocr_code"], "IND")
        self.assertEqual(second["context"]["visa_type"], 16)
        self.assertEqual(second["decision"]["status"], "NEED_MORE_INFO")
        self.assertIn("age", second["decision"]["missing_fields"])
        self.assertIn("occupation", second["decision"]["missing_fields"])

        third = self.chat("okay i need to check if i can to apply", session_id=session_id, language="en")

        self.assertEqual(third["extracted"]["intent"], "eligibility_check")
        self.assertEqual(third["decision"]["visa_type"], 16)
        self.assertEqual(third["decision"]["status"], "NEED_MORE_INFO")
        self.assertIn("age", third["decision"]["missing_fields"])
        self.assertIn("occupation", third["decision"]["missing_fields"])

    def test_clickable_visa_list_selection_starts_eligibility_check(self):
        session_id = "clickable-visa-selection"
        list_response = self.chat("what visas are available for jordan", session_id=session_id, language="en")

        self.assertEqual(list_response["decision"]["intent"], "list_visa_types")
        self.assertTrue(list_response["decision"]["visa_types"])

        selected = self.chat(
            "I want to check eligibility for Visa No. 10",
            session_id=session_id,
            language="en",
        )

        self.assertEqual(selected["extracted"]["intent"], "eligibility_check")
        self.assertEqual(selected["context"]["ocr_code"], "JOR")
        self.assertEqual(selected["context"]["visa_type"], 10)
        self.assertEqual(selected["decision"]["status"], "NEED_MORE_INFO")
        self.assertIn("age", selected["decision"]["missing_fields"])
        self.assertIn("occupation", selected["decision"]["missing_fields"])

    def test_apply_request_country_followup_keeps_eligibility_flow_and_language_switch(self):
        session_id = "visa16-apply-country-language"
        first = self.chat("hey i need to apply for visa 16", session_id=session_id, language="en")

        self.assertEqual(first["extracted"]["intent"], "eligibility_check")
        self.assertEqual(first["context"]["visa_type"], 16)
        self.assertIn("country", first["decision"]["missing_fields"])

        second = self.chat("jordanian", session_id=session_id, language="en")

        self.assertEqual(second["extracted"]["intent"], "eligibility_check")
        self.assertEqual(second["context"]["ocr_code"], "JOR")
        self.assertEqual(second["context"]["visa_type"], 16)
        self.assertEqual(second["decision"]["status"], "NEED_MORE_INFO")
        self.assertIn("age", second["decision"]["missing_fields"])
        self.assertIn("occupation", second["decision"]["missing_fields"])

        confirmation = self.chat("yes i went", session_id=session_id, language="en")

        self.assertEqual(confirmation["extracted"]["intent"], "eligibility_check")
        self.assertEqual(confirmation["decision"]["status"], "NEED_MORE_INFO")
        self.assertIn("age", confirmation["decision"]["missing_fields"])
        self.assertIn("occupation", confirmation["decision"]["missing_fields"])

        arabic = self.chat("give me result in arabic", session_id=session_id, language="en")

        self.assertEqual(arabic["context"]["language"], "ar")
        self.assertEqual(arabic["extracted"]["intent"], "eligibility_check")
        self.assertIn("العمر", arabic["answer"])
        self.assertIn("المهنة", arabic["answer"])
        self.assertNotIn("Age Requirement", arabic["answer"])

    def test_country_change_keeps_selected_tourist_visa_without_using_old_applicant_data(self):
        session_id = "tourist-country-switch"
        self.chat("can i apply for tourist visa. i'm jordanian", session_id=session_id, language="en")
        self.chat("i am 26 years old as software eng", session_id=session_id, language="en")
        data = self.chat("i am indian", session_id=session_id, language="en")

        self.assertEqual(data["extracted"]["intent"], "provide_country")
        self.assertEqual(data["context"]["ocr_code"], "IND")
        self.assertEqual(data["context"]["visa_type"], 16)
        self.assertIsNone(data["context"]["age"])
        self.assertIsNone(data["context"]["occupation"])
        self.assertIn("Visa No. 16", data["answer"])

    def test_president_and_member_of_council_match_english_rule_categories(self):
        from backend.rules_engine import occupation_matches

        occupations = [
            {
                "EnglishDescription": "All related Titles for Members of Councils and their Deputies and Assistants",
            },
            {
                "EnglishDescription": "All related Titles for Presidents and their Deputies and Assistants",
            },
        ]

        for user_occupation in ["president", "presidents", "Member of Council", "council member"]:
            with self.subTest(user_occupation=user_occupation):
                matched, matched_name = occupation_matches(user_occupation, occupations)
                self.assertTrue(matched)
                self.assertIsNotNone(matched_name)

    def test_short_software_eng_is_extracted_as_occupation(self):
        session_id = "software-eng-short"
        self.chat("i am indian for family visa", session_id=session_id, language="en")
        data = self.chat("i am 26 years old as software eng", session_id=session_id, language="en")

        self.assertEqual(data["extracted"]["occupation"], "software eng")
        self.assertEqual(data["decision"]["status"], "APPROVED")
        self.assertTrue(any(check["field"] == "occupation" and check["passed"] for check in data["decision"]["checks"]))

    def test_president_and_member_followups_are_not_treated_as_missing_occupation(self):
        session_id = "president-member-followups"
        self.chat("i am indian for tourist visa", session_id=session_id, language="en")

        president = self.chat("35 president", session_id=session_id, language="en")
        self.assertEqual(president["extracted"]["occupation"], "president")
        self.assertNotIn("occupation", president["decision"]["missing_fields"])
        self.assertTrue(any(check["field"] == "occupation" and check["passed"] for check in president["decision"]["checks"]))

        member = self.chat("Member of Council 35", session_id=session_id, language="en")
        self.assertEqual(member["extracted"]["occupation"], "member of council")
        self.assertNotIn("occupation", member["decision"]["missing_fields"])
        self.assertTrue(any(check["field"] == "occupation" and check["passed"] for check in member["decision"]["checks"]))

    def test_ten_presidents_extracts_occupation_and_blocks_impossible_age(self):
        session_id = "ten-presidents"
        self.chat("i am indian for tourist visa", session_id=session_id, language="en")
        data = self.chat("10 presidents", session_id=session_id, language="en")

        self.assertEqual(data["extracted"]["age"], 10)
        self.assertEqual(data["extracted"]["occupation"], "president")
        self.assertNotIn("occupation", data["decision"]["missing_fields"])
        self.assertTrue(any(check["field"] == "occupation" and check["passed"] for check in data["decision"]["checks"]))
        self.assertTrue(
            any(
                check["field"] == "age_occupation_consistency" and check["passed"] is False
                for check in data["decision"]["checks"]
            )
        )

    def test_family_visa_request_replaces_previous_tourist_context(self):
        self.chat("for tourist visa", session_id="family-switch", language="en")
        self.chat("india", session_id="family-switch", language="en")
        data = self.chat("for family visa", session_id="family-switch", language="en")

        self.assertEqual(data["extracted"]["visa_type"], 10)
        self.assertEqual(data["context"]["visa_type"], 10)
        self.assertEqual(data["decision"]["visa_type"], 10)
        self.assertIn("Family visit entry visa", data["answer"])
        self.assertNotIn("Tourism Entry Visa", data["answer"])

    def test_english_description_and_nested_occupations_are_displayed(self):
        from backend.rules_engine import build_occupation_list

        visa_data = {
            "countryRule": {
                "rules": {
                    "newOccupation": [
                        {
                            "ArabicDescription": "Arabic judge category",
                            "EnglishDescription": "Judges, Members of the Public Prosecution, and Lawyers",
                        },
                        {
                            "ArabicDescription": "Parent category",
                            "subOccupations": [
                                {
                                    "ArabicDescription": "Nested Arabic category",
                                    "EnglishDescription": "Nested English Occupation",
                                }
                            ],
                        },
                    ]
                }
            },
            "generalRules": {},
        }

        occupations = build_occupation_list(visa_data)
        english_names = [item["occupation_name_en"] for item in occupations]
        labels = [item["label"] for item in occupations]

        self.assertIn("Judges, Members of the Public Prosecution, and Lawyers", english_names)
        self.assertIn("Nested English Occupation", english_names)
        self.assertTrue(any("Judges, Members" in label for label in labels))
        self.assertTrue(any("Nested English Occupation" in label for label in labels))

    def test_generic_professor_and_specialist_names_are_expanded_from_arabic(self):
        from backend.rules_engine import build_occupation_list, occupation_matches

        visa_data = {
            "countryRule": {
                "rules": {
                    "newOccupation": [
                        {
                            "ArabicDescription": "أستاذ أصول التربية",
                            "EnglishDescription": "PROFESSOR",
                        },
                        {
                            "ArabicDescription": "أستاذ آداب",
                            "EnglishDescription": "PROFESSOR",
                        },
                        {
                            "ArabicDescription": "أخصائى توجيه مهني",
                            "EnglishDescription": "SPECIALIST",
                        },
                        {
                            "ArabicDescription": "القضاة وأعضاء النيابة العامة والمحامين",
                            "EnglishDescription": "Judges, Members of the Public Prosecution, and Lawyers",
                        },
                    ]
                }
            },
            "generalRules": {},
        }

        occupations = build_occupation_list(visa_data)
        english_names = [item["occupation_name_en"] for item in occupations]

        self.assertIn("Professor of Education Principles", english_names)
        self.assertIn("Professor of Literature", english_names)
        self.assertIn("Vocational Guidance Specialist", english_names)
        self.assertIn("Judges, Members of the Public Prosecution, and Lawyers", english_names)
        self.assertNotIn("PROFESSOR", english_names)
        self.assertNotIn("SPECIALIST", english_names)

        matched, matched_name = occupation_matches(
            "Professor of Literature",
            visa_data["countryRule"]["rules"]["newOccupation"],
        )
        self.assertTrue(matched)
        self.assertEqual(matched_name, "Professor of Literature")

    def test_english_occupation_details_use_expanded_names(self):
        from backend.response_builder import build_occupation_details_answer

        raw_visa_details = {
            "visaType": 6,
            "typeOfVisa": "Study entry visa",
            "countryRule": {
                "ArabicDescription": "Germany",
                "LatinDescription": "GERMANY",
                "OcrCode": "DEU",
                "rules": {
                    "newOccupation": [
                        {"ArabicDescription": "أستاذ أصول التربية", "EnglishDescription": "PROFESSOR"},
                        {"ArabicDescription": "أستاذ آداب", "EnglishDescription": "PROFESSOR"},
                        {"ArabicDescription": "أخصائى توجيه مهني", "EnglishDescription": "SPECIALIST"},
                    ]
                },
            },
            "generalRules": {},
        }
        decision = {
            "visa_type": 6,
            "visa_name": "Study entry visa",
            "raw_visa_details": raw_visa_details,
        }
        session = {"country_en": "Germany", "ocr_code": "DEU", "language": "en"}

        answer = build_occupation_details_answer("what are the occupations for visa 6", decision, session)

        self.assertIn("Professor of Education Principles", answer)
        self.assertIn("Professor of Literature", answer)
        self.assertIn("Vocational Guidance Specialist", answer)
        self.assertNotIn("- PROFESSOR", answer)
        self.assertNotIn("- SPECIALIST", answer)

    def test_software_programmer_matches_it_profession_category(self):
        from backend.rules_engine import occupation_matches

        occupations = [
            {
                "ArabicDescription": "IT professionals",
                "EnglishDescription": "Main and Technical Professions in Information Systems, Networks, Computers, and Electronic Websites",
            }
        ]

        matched, matched_name = occupation_matches("software programmer", occupations)

        self.assertTrue(matched)
        self.assertIn("Information Systems", matched_name)

    def test_software_programmer_is_allowed_after_family_visa_context(self):
        self.chat("for family visa from india", session_id="software-programmer", language="en")
        data = self.chat("software programmer 23", session_id="software-programmer", language="en")

        self.assertEqual(data["extracted"]["intent"], "eligibility_check")
        self.assertEqual(data["context"]["visa_type"], 10)
        self.assertEqual(data["decision"]["status"], "APPROVED")
        self.assertTrue(any(check["field"] == "occupation" and check["passed"] for check in data["decision"]["checks"]))

    def test_arabic_age_first_app_developer_extracts_age_and_occupation(self):
        session_id = "arabic-age-first-app-developer"
        self.chat("مرحبا بدي اقدم على فيزا 10", session_id=session_id)
        self.chat("من الاردن", session_id=session_id)

        data = self.chat("33 انا مطور تطبيقات", session_id=session_id)

        self.assertEqual(data["extracted"]["intent"], "eligibility_check")
        self.assertEqual(data["extracted"]["age"], 33)
        self.assertEqual(data["extracted"]["occupation"], "مطور تطبيقات")
        self.assertEqual(data["context"]["occupation"], "مطور تطبيقات")
        self.assertEqual(data["decision"]["status"], "APPROVED")
        self.assertNotIn("occupation", data["decision"]["missing_fields"])
        self.assertTrue(any(check["field"] == "occupation" and check["passed"] for check in data["decision"]["checks"]))

    def test_thanks_after_eligibility_result_is_chitchat_not_repeated_result(self):
        session_id = "thanks-after-result"
        self.chat("مرحبا بدي اقدم على فيزا 10", session_id=session_id)
        self.chat("من الاردن", session_id=session_id)
        self.chat("33 انا مطور تطبيقات", session_id=session_id)

        data = self.chat("شكرا", session_id=session_id)

        self.assertEqual(data["extracted"]["intent"], "chitchat")
        self.assertEqual(data["decision"]["intent"], "chitchat")
        self.assertEqual(data["decision"]["status"], "INFO")
        self.assertIn("العفو", data["answer"])
        self.assertNotIn("الحالة", data["answer"])
        self.assertNotIn("سمة دخول", data["answer"])

    def test_simple_courtesy_bypasses_rewrite_and_router_models(self):
        class NoisyGemini:
            def rewrite_query(self, user_message, context):
                return {
                    "rewritten_query": "اعطني نتيجة الاهلية لفيزا 10 من لبنان العمر 33 المهنة اصحاب العقارات"
                }

            def route_task(self, user_message, context, extracted):
                return {"task_type": "eligibility"}

        extracted = understand_message(
            "شكرا",
            {
                "country": "لبنان",
                "country_en": "Lebanon",
                "ocr_code": "LBN",
                "visa_type": 10,
                "age": 33,
                "occupation": "أصحاب العقارات",
                "last_intent": "eligibility_check",
                "language": "ar",
            },
            NoisyGemini(),
        )

        self.assertEqual(extracted["intent"], "chitchat")
        self.assertEqual(extracted["task_type"], "chitchat")
        self.assertEqual(extracted["rewrite_model"], {})
        self.assertEqual(extracted["router_model"], {})

    def test_real_estate_first_message_preserves_visa_and_occupation_when_country_is_added(self):
        session_id = "real-estate-country-followup"
        first = self.chat(
            "I have real estate can i apply for visa 8 please",
            session_id=session_id,
            language="en",
        )

        self.assertEqual(first["extracted"]["intent"], "eligibility_check")
        self.assertEqual(first["extracted"]["visa_type"], 8)
        self.assertEqual(first["extracted"]["occupation"], "real estate owner")
        self.assertEqual(first["context"]["visa_type"], 8)
        self.assertEqual(first["context"]["occupation"], "real estate owner")
        self.assertIn("country", first["decision"]["missing_fields"])

        second = self.chat("cyprus", session_id=session_id, language="en")

        self.assertEqual(second["context"]["ocr_code"], "CYP")
        self.assertEqual(second["context"]["visa_type"], 8)
        self.assertEqual(second["context"]["occupation"], "real estate owner")
        self.assertIn("Visa No. 8", second["answer"])
        self.assertNotIn("Visa No. 16", second["answer"])

    def test_real_estate_owner_phrasing_is_allowed_for_cyprus_visa_8(self):
        session_id = "real-estate-approved"
        self.chat(
            "I have real estate can i apply for visa 8 please",
            session_id=session_id,
            language="en",
        )
        self.chat("cyprus", session_id=session_id, language="en")
        data = self.chat("77 and i have real estate", session_id=session_id, language="en")

        self.assertEqual(data["extracted"]["occupation"], "real estate owner")
        self.assertEqual(data["context"]["visa_type"], 8)
        self.assertEqual(data["decision"]["status"], "APPROVED")
        self.assertTrue(any(check["field"] == "occupation" and check["passed"] for check in data["decision"]["checks"]))

    def test_real_state_typo_matches_real_estate_owner_category(self):
        from backend.rules_engine import occupation_matches

        occupations = [
            {
                "EnglishDescription": "Real estate Owners",
            }
        ]

        for user_occupation in ["real state", "have real estate", "property owner"]:
            with self.subTest(user_occupation=user_occupation):
                matched, matched_name = occupation_matches(user_occupation, occupations)
                self.assertTrue(matched)
                self.assertEqual(matched_name, "Real estate Owners")

    def test_country_switch_in_same_conversation_uses_latest_country(self):
        first = self.chat("شو التأشيرات للاردنيين", session_id="switch")
        self.assertEqual(first["decision"]["ocr_code"], "JOR")

        second = self.chat("طيب الروس شو عندهم", session_id="switch")
        self.assertEqual(second["extracted"]["ocr_code"], "RUS")
        self.assertEqual(second["decision"]["ocr_code"], "RUS")
        self.assertIn("روسيا", second["answer"])

    def test_register_wording_is_eligibility_not_visa_details(self):
        data = self.chat("انا من الاردن و ابغى اسجل على فيزا 8")

        self.assertEqual(data["extracted"]["intent"], "eligibility_check")
        self.assertEqual(data["decision"]["visa_type"], 8)
        self.assertEqual(data["decision"]["status"], "NEED_MORE_INFO")
        self.assertIn("age", data["decision"]["missing_fields"])
        self.assertIn("occupation", data["decision"]["missing_fields"])

    def test_bring_wife_switches_from_commercial_visit_to_family_visit_check(self):
        session_id = "bring-wife-after-commercial"
        first = self.chat("انا من الاردن بدي اقدم على فيزا 8", session_id=session_id)

        self.assertEqual(first["extracted"]["intent"], "eligibility_check")
        self.assertEqual(first["context"]["visa_type"], 8)

        second = self.chat("ما بدي خلص هل بقدر اجسب زوجتي على الكويت", session_id=session_id)

        self.assertEqual(second["extracted"]["intent"], "eligibility_check")
        self.assertEqual(second["extracted"]["visa_type"], 10)
        self.assertEqual(second["extracted"]["relationship"], "الزوجة")
        self.assertEqual(second["context"]["visa_type"], 10)
        self.assertEqual(second["decision"]["visa_type"], 10)
        self.assertEqual(second["decision"]["status"], "NEED_MORE_INFO")
        self.assertIn("age", second["decision"]["missing_fields"])
        self.assertIn("occupation", second["decision"]["missing_fields"])
        self.assertTrue(any(check["field"] == "relationship" and check["passed"] for check in second["decision"]["checks"]))
        self.assertIn("الزوجة", second["answer"])

    def test_inside_kuwait_tourist_question_does_not_use_kuwait_as_nationality(self):
        session_id = "inside-kuwait-tourist"
        data = self.chat(
            "هل يمكنني التقديم على فيزا سياحية من داخل الكويت وأنا داخل بفيزا زيارة سابقة؟",
            session_id=session_id,
        )

        self.assertEqual(data["extracted"]["intent"], "inside_kuwait_visa_inquiry")
        self.assertIsNone(data["extracted"]["ocr_code"])
        self.assertEqual(data["context"]["visa_type"], 16)
        self.assertNotEqual(data["context"].get("ocr_code"), "KWT")
        self.assertIn("داخل الكويت", data["answer"])
        self.assertIn("جنسيتك", data["answer"])

        follow_up = self.chat("77 مبرمج", session_id=session_id)

        self.assertNotEqual(follow_up["context"].get("ocr_code"), "KWT")
        self.assertEqual(follow_up["decision"]["status"], "NEED_MORE_INFO")
        self.assertIn("country", follow_up["decision"]["missing_fields"])

    def test_work_location_country_is_not_treated_as_nationality(self):
        message = "انا شغال في البحرين مهندس هل بقدر اطلع الكويت ؟"
        country = resolve_applicant_country(message)
        self.assertIsNone(country)

        data = self.chat(message, session_id="work-location-not-nationality")

        self.assertIsNone(data["extracted"]["ocr_code"])
        self.assertIsNone(data["context"].get("ocr_code"))
        self.assertEqual(data["context"]["occupation"], "مهندس")
        self.assertEqual(data["decision"]["status"], "NEED_MORE_INFO")
        self.assertIn("country", data["decision"]["missing_fields"])
        self.assertIn("الجنسية", data["answer"])
        self.assertNotIn("فيزا رقم 8", data["answer"])

    def test_generic_visit_followup_uses_tourist_visa_and_suggests_alternatives_when_occupation_fails(self):
        session_id = "qatari-engineer-tourist-alternatives"
        first = self.chat("مرحبا انا مهندس اشتغل في مدريد بقدر اطلع زيارة على الكويت", session_id=session_id)
        self.assertEqual(first["extracted"]["intent"], "eligibility_check")
        self.assertEqual(first["context"]["occupation"], "مهندس")
        self.assertIn("country", first["decision"]["missing_fields"])

        second = self.chat("قطر", session_id=session_id)
        self.assertEqual(second["context"]["ocr_code"], "QAT")
        self.assertEqual(second["context"]["occupation"], "مهندس")

        third = self.chat("يعني ك زيارة ابغى اروح الكويت", session_id=session_id)

        self.assertEqual(third["context"]["visa_type"], 16)
        self.assertEqual(third["decision"]["status"], "NOT_APPROVED")
        self.assertTrue(any(check["field"] == "occupation" and check["passed"] is False for check in third["decision"]["checks"]))
        self.assertNotIn("age", third["decision"]["missing_fields"])
        self.assertTrue(any(item["visa_type"] == 8 for item in third["decision"].get("alternative_visas", [])))
        self.assertNotIn("العمر", third["answer"])
        self.assertIn("فيزا رقم 8", third["answer"])

    def test_rewrite_agent_cannot_turn_work_location_into_nationality(self):
        class WorkLocationRewriteGemini:
            def rewrite_query(self, user_message, context):
                return {
                    "rewritten_query": "مقدم الطلب يعمل في البحرين بمهنة مهندس ويريد معرفة إمكانية دخول الكويت؛ جنسية مقدم الطلب غير مذكورة.",
                    "country_text": "البحرين",
                    "intent_hint": "eligibility",
                    "confidence": 0.9,
                }

            def route_task(self, user_message, context, extracted):
                return {"task_type": "eligibility", "confidence": 1.0, "reason": "simulated"}

        extracted = understand_message(
            "انا شغال في البحرين مهندس هل بقدر اطلع الكويت ؟",
            {},
            WorkLocationRewriteGemini(),
        )

        self.assertIsNone(extracted["ocr_code"])
        self.assertIsNone(extracted["country"])
        self.assertEqual(extracted["occupation"], "مهندس")

    def test_negating_previous_country_clears_context_and_asks_for_nationality(self):
        session_id = "negate-previous-country"
        sessions[session_id] = {
            "country": "البحرين",
            "country_en": "Bahrain",
            "ocr_code": "BHR",
            "visa_type": None,
            "age": None,
            "occupation": "مهندس",
            "gender": None,
            "relationship": None,
            "last_intent": "list_visa_types",
            "language": "ar",
        }

        data = self.chat("بس انا مو بحريني", session_id=session_id)

        self.assertIsNone(data["context"].get("ocr_code"))
        self.assertEqual(data["decision"]["status"], "NEED_MORE_INFO")
        self.assertIn("country", data["decision"]["missing_fields"])
        self.assertIn("الجنسية", data["answer"])
        self.assertNotIn("الفيز المتاحة", data["answer"])

    def test_sudden_switch_from_tourism_to_wife_living_with_me_is_dependent_residency(self):
        session_id = "tourism-to-wife-residency"
        self.chat("شو شروط الفيزا السياحية؟", session_id=session_id)
        data = self.chat("طيب بطلت سياحة، بدي أجيب زوجتي تعيش معي، شو الأوراق؟", session_id=session_id)

        self.assertEqual(data["extracted"]["intent"], "dependent_residency_inquiry")
        self.assertEqual(data["decision"]["intent"], "dependent_residency_inquiry")
        self.assertIn("التحاق", data["answer"])
        self.assertNotIn("نتيجة الفحص", data["answer"])

    def test_visa_comparison_is_not_locked_to_previous_tourist_context_or_residence_city(self):
        session_id = "visa-comparison"
        self.chat("شو شروط الفيزا السياحية؟", session_id=session_id)
        data = self.chat("أيهما أسهل لمقيم في دبي: فيزا السياحة ولا فيزا الزيارة التجارية؟", session_id=session_id)

        self.assertEqual(data["extracted"]["intent"], "visa_comparison_inquiry")
        self.assertIsNone(data["extracted"]["ocr_code"])
        self.assertIn("مقارنة", data["answer"])
        self.assertIn("جنسية", data["answer"])

    def test_support_hours_interruption_preserves_pending_eligibility_context(self):
        session_id = "support-interruption"
        self.chat("can i apply for family visa from india", session_id=session_id, language="en")
        self.chat("23", session_id=session_id, language="en")

        support = self.chat("قبل ما أقولك، هل الموقع شغال يوم السبت؟", session_id=session_id)
        self.assertEqual(support["extracted"]["intent"], "system_support_inquiry")
        self.assertEqual(support["context"]["ocr_code"], "IND")
        self.assertEqual(support["context"]["visa_type"], 10)

        resumed = self.chat("أنا محاسب (Accountant)", session_id=session_id)
        self.assertEqual(resumed["extracted"]["intent"], "eligibility_check")
        self.assertEqual(resumed["context"]["ocr_code"], "IND")
        self.assertEqual(resumed["context"]["visa_type"], 10)
        self.assertTrue(any(check["field"] == "occupation" for check in resumed["decision"]["checks"]))

    def test_modern_and_colloquial_occupation_synonyms_match_rule_categories(self):
        from backend.rules_engine import occupation_matches

        occupations = [
            {
                "EnglishDescription": "Main and Technical Professions in Information Systems, Networks, Computers, and Electronic Websites",
            },
            {
                "EnglishDescription": "All related Titles for Presidents and their Deputies and Assistants",
            },
            {
                "EnglishDescription": "All related Titles for General Managers and Managers as well their Deputies and Assistants",
            },
            {
                "EnglishDescription": "Specialist",
                "ArabicDescription": "اختصاصي",
            },
            {
                "EnglishDescription": "Owners, Managers, and Representatives of Companies and Institutions",
            },
            {
                "EnglishDescription": "Doctors and Surgeons",
                "ArabicDescription": "الأطباء والجراحون",
            },
        ]

        for user_occupation in [
            "Full Stack Developer",
            "DevOps Engineer",
            "Data Scientist",
            "نظم معلومات",
            "CEO",
            "HR Specialist",
            "PR Manager",
            "راعي أعمال",
            "دكتور",
        ]:
            with self.subTest(user_occupation=user_occupation):
                matched, matched_name = occupation_matches(user_occupation, occupations)
                self.assertTrue(matched)
                self.assertIsNotNone(matched_name)

    def test_residency_admin_question_is_not_dependent_residency(self):
        data = self.chat(
            "قم (8) وانتهت صلاحية الزيارة قبل يومين. هل يمكنني تحويل هذه الزيارة "
            "إلى إقامة عمل مادة 18 دون مغادرة البلاد؟ أنا أحمل الجنسية الأردنية"
        )

        self.assertEqual(data["extracted"]["intent"], "residency_admin_inquiry")
        self.assertEqual(data["decision"]["intent"], "residency_admin_inquiry")
        self.assertNotIn("التحاق بعائل", data["answer"])
        self.assertIn("تحويل", data["answer"])

    def test_relationship_question_for_visa_without_relationships_is_not_allowed(self):
        data = self.chat("انا من المانيا فيزا 20 هل يمكنني التقديم مع زوجتي")

        self.assertEqual(data["extracted"]["intent"], "relationship_check")
        self.assertEqual(data["decision"]["status"], "NOT_APPROVED")
        self.assertTrue(any(check["field"] == "relationship" and check["passed"] is False for check in data["decision"]["checks"]))

    def test_system_support_question_does_not_request_country(self):
        data = self.chat("هل ممكن تواجهني مشكلة عند رفع صورة جواز السفر؟")

        self.assertEqual(data["extracted"]["intent"], "system_support_inquiry")
        self.assertEqual(data["decision"]["status"], "INFO")
        self.assertIn("خارج", data["answer"])
        self.assertNotIn("من أي دولة", data["answer"])

    def test_api_error_answer_is_careful_not_raw_outage_template(self):
        original = main.visa_api
        main.visa_api = FailingVisaApi()
        try:
            data = self.chat("شو التأشيرات للاردنيين", session_id="api-error")
        finally:
            main.visa_api = original

        self.assertEqual(data["decision"]["status"], "API_ERROR")
        self.assertIn("حاولت جلب", data["answer"])
        self.assertNotIn("تعذر الاتصال", data["answer"])

    def test_common_nationality_aliases_are_resolved(self):
        examples = {
            "شو التأشيرات للبحرينيين": "BHR",
            "انا من بروني": "BRN",
            "انا من بروناي": "BRN",
            "طيب الروس شو عندهم": "RUS",
            "الباكستانيين شو عندهم": "PAK",
            "الهنود شو عندهم": "IND",
            "السعوديين": "SAU",
            "القطريين": "QAT",
            "انا كوري شو متوفر لي فيز": "KOR",
            "الصينيين شو عندهم": "CHN",
            "المصريين شو عندهم": "EGY",
        }

        for message, expected_ocr in examples.items():
            with self.subTest(message=message):
                country = resolve_applicant_country(message)
                self.assertIsNotNone(country)
                self.assertEqual(country["ocr_code"], expected_ocr)

    def test_brunei_country_only_is_understood(self):
        data = self.chat("انا من بروني", session_id="brunei")

        self.assertEqual(data["extracted"]["intent"], "provide_country")
        self.assertEqual(data["extracted"]["ocr_code"], "BRN")
        self.assertEqual(data["decision"]["ocr_code"], "BRN")

    def test_rewrite_agent_cannot_turn_plain_country_statement_into_visa_list(self):
        class RewriteOnlyGemini:
            def rewrite_query(self, user_message, context):
                return {
                    "rewritten_query": "ما أنواع الفيزا المتوفرة لمواطني بروناي؟",
                    "country_text": "بروناي",
                    "intent_hint": "visa list",
                    "confidence": 0.9,
                }

            def route_task(self, user_message, context, extracted):
                return {"task_type": "inquiry", "confidence": 1.0, "reason": "simulated"}

        extracted = understand_message("انا من بروني", {}, RewriteOnlyGemini())

        self.assertEqual(extracted["intent"], "provide_country")
        self.assertEqual(extracted["ocr_code"], "BRN")

    def test_armenian_pharmacist_is_allowed_for_commercial_visit(self):
        data = self.chat(
            "أنا مواطن من أرمينيا، أبلغ من العمر 40 عاماً، وأعمل في مهنة صيدلي. "
            "أريد التقديم على سمة دخول زيارة تجارية (رقم 8). هل تسمح لي؟"
        )

        self.assertEqual(data["extracted"]["ocr_code"], "ARM")
        self.assertEqual(data["extracted"]["visa_type"], 8)
        self.assertEqual(data["extracted"]["age"], 40)
        self.assertEqual(data["extracted"]["occupation"], "صيدلي")
        self.assertEqual(data["extracted"]["gender"], "male")
        self.assertEqual(data["decision"]["status"], "APPROVED")
        self.assertTrue(any(check["field"] == "occupation" and check["passed"] for check in data["decision"]["checks"]))


if __name__ == "__main__":
    unittest.main()
