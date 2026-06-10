const SESSION_KEY = "kuwaitVisaSmartAssistant.sessionId";
const LANGUAGE_KEY = "kuwaitVisaSmartAssistant.language";
const THEME_KEY = "kuwaitVisaUi.theme";
const API_BASE = "";
const DEFAULT_LANGUAGE = "en";
const DEFAULT_THEME = "light";
const VISA_DATA_REFRESH_TOKEN = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
const VISA_TYPE_NAMES_EN = {
  1: "Government work entry visa",
  2: "Private sector work entry visa",
  3: "Domestic worker entry visa",
  6: "Study entry visa",
  7: "Medical treatment entry visa",
  8: "Commercial visit entry visa",
  9: "Government visit entry visa",
  10: "Family visit entry visa",
  11: "Embassy visit entry visa",
  14: "Multiple-return visa",
  16: "Tourism entry visa",
  19: "Return visa",
  20: "Special entry visa",
};

const RELATIONSHIP_EXACT_TRANSLATIONS_EN = {
  "الأب": "Father",
  "الاب": "Father",
  "الأم": "Mother",
  "الام": "Mother",
  "الأخ": "Brother",
  "الاخ": "Brother",
  "الأخت": "Sister",
  "الاخت": "Sister",
  "الابن": "Son",
  "الإبن": "Son",
  "الابنة": "Daughter",
  "الإبنة": "Daughter",
  "الزوج": "Husband",
  "الزوجة": "Wife",
  "الزوجة الثانية": "Second wife",
  "الزوجة الثالثة": "Third wife",
  "العم": "Paternal uncle",
  "العمة": "Paternal aunt",
  "الخال": "Maternal uncle",
  "الخالة": "Maternal aunt",
  "الجد": "Grandfather",
  "الجدة": "Grandmother",
  "ولىالامر": "Guardian",
  "ولي الامر": "Guardian",
  "قريب": "Relative",
  "صديق": "Friend",
  "رجل دين": "Cleric",
  "غير محددة": "Unspecified relationship",
  "قريب -قوة الشرطة": "Police force relative",
  "قريب-قوة الشرطة": "Police force relative",
  "قريب-قوة الجيش": "Army force relative",
  "قريب -قوة الجيش": "Army force relative",
  "قريب-قوةالحرس الوطني": "National Guard relative",
  "قريب-قوةالحرس​الوطنى": "National Guard relative",
};

const RELATIONSHIP_WORD_TRANSLATIONS_EN = {
  "اب": "father",
  "ابو": "father",
  "والد": "father",
  "ام": "mother",
  "والده": "mother",
  "اخ": "brother",
  "شقيق": "brother",
  "اخت": "sister",
  "ابن": "son",
  "ابنه": "daughter",
  "بنت": "daughter",
  "زوج": "husband",
  "زوجه": "wife",
  "عم": "paternal uncle",
  "عمه": "paternal aunt",
  "خال": "maternal uncle",
  "خاله": "maternal aunt",
  "جد": "grandfather",
  "جده": "grandmother",
  "حفيد": "grandson",
  "حفيده": "granddaughter",
  "والدته": "mother",
  "والده": "mother",
  "والد": "father",
  "الوالده": "mother",
  "الوالد": "father",
  "حفيدت": "granddaughter",
  "الحفيد": "grandson",
  "الحفيده": "granddaughter",
  "الحفيدت": "granddaughter",
  "ثانيه": "second",
  "الثانيه": "second",
  "ثالثه": "third",
  "الثالثه": "third",
  "قريب": "relative",
  "صديق": "friend",
  "رجل": "man",
  "دين": "religion",
};

const translations = {
  en: {
    pageTitle: "Kuwait Visa AI Assistant",
    selectedLanguageAria: "Selected language: English",
    stateName: "STATE OF KUWAIT",
    ministryName: "MINISTRY OF INTERIOR",
    heroTitleLead: "Kuwait Visa",
    heroTitleAccent: "AI Assistant",
    heroSubtitle: "Your smart guide for visa information and eligibility support",
    eligibilityTitle: "Check Your Eligibility",
    eligibilityDescription: "Answer a few questions and get instant eligibility result.",
    guideChatSupport: "Chat guidance",
    guideDirectCheck: "Direct check",
    guideOfficialLinks: "Official links",
    kuwaitPortalTitle: "Kuwait Visa Portal",
    kuwaitPortalText: "Official visa applications and account access",
    visitKuwaitTitle: "Visit Kuwait",
    visitKuwaitText: "Tourism experiences and destination guide",
    touristVisaStat: "Tourist Visa",
    familyVisaStat: "Family Visa",
    businessVisaStat: "Business Visa",
    governmentVisaStat: "Government Visa",
    thousand: "Thousand",
    visasIssued2025: "Visas issued in 2025",
    startEligibility: "Direct Check",
    secureChatTitle: "Secure Chat Session",
    secureChatDescription: "Your data is safe and protected",
    resetConversation: "Reset Conversation",
    welcomeMessage: "Welcome! I am your Kuwait Visa Assistant. Please share the applicant nationality, visa type, age, occupation, gender, and any companion or relationship details that apply.",
    typingLabel: "MOI Assistant is typing",
    typingStatus: "MOI Assistant is typing...",
    chatPlaceholder: "Ask about visas...",
    attachFile: "Attach file",
    voiceInput: "Voice input",
    voiceListening: "Listening... Tap the microphone again to send.",
    voiceTranscribing: "Transcribing your voice...",
    voiceUnsupported: "Voice input is not supported in this browser.",
    voicePermissionError: "Microphone access was blocked. Please allow microphone access and try again.",
    voiceNoSpeech: "I could not detect speech. Please try again.",
    voiceTranscriptionError: "Could not transcribe the voice message. Please try again.",
    sendMessage: "Send message",
    officialNote: "This is an official service of the Ministry of Interior, State of Kuwait.",
    directService: "Direct Service",
    directEligibilityTitle: "Direct Eligibility Check",
    directEligibilitySubtitle: "A guided eligibility studio for faster, clearer decisions.",
    closeModal: "Close modal",
    stepCountry: "Country",
    stepVisa: "Visa",
    stepDetails: "Details",
    stepResult: "Result",
    countryPanelTitle: "Choose applicant country",
    countryPanelDescription: "Search and select the applicant nationality.",
    visaPanelTitle: "Select visa type",
    visaPanelDescription: "Only visa types available for the selected country are shown.",
    detailsPanelTitle: "Complete applicant details",
    detailsPanelDescription: "Fill only the details that apply to this visa rule.",
    snapshotKicker: "Live Summary",
    snapshotTitle: "Application Snapshot",
    countryLabel: "Applicant Country / Nationality",
    visaTypeLabel: "Visa Type",
    ageLabel: "Age",
    agePlaceholder: "Applicant age",
    occupationLabel: "Occupation",
    genderLabel: "Gender",
    relationshipLabel: "Relationship / Companion",
    checkEligibility: "Check Eligibility",
    cancel: "Cancel",
    startOver: "Start Over",
    selectCountry: "Select applicant country",
    selectVisaType: "Select a visa type",
    searchCountries: "Search countries...",
    searchVisaTypes: "Search visa types...",
    searchGenders: "Search genders...",
    searchRelationships: "Search relationships...",
    noCountryMatches: "No matching countries.",
    noVisaTypeMatches: "No matching visa types.",
    noGenderMatches: "No matching genders.",
    noRelationshipMatches: "No matching relationships.",
    loadingCountries: "Loading countries...",
    loadingVisaTypes: "Loading visa types...",
    noVisaTypes: "No visa types were returned for this country.",
    selectOccupation: "Select an occupation",
    loadingOccupations: "Loading available occupations...",
    noOccupationRestriction: "No occupation restriction for this visa",
    selectAvailableOccupation: "Select an available occupation",
    searchOccupations: "Search occupations...",
    noOccupationMatches: "No matching occupations.",
    couldNotLoadOccupations: "Could not load occupations",
    selectRelationships: "Select relationships",
    loadingRelationships: "Loading available relationships...",
    loadingVisaRules: "Loading visa rules...",
    noRelationshipRestriction: "No allowed relationships are listed for this visa",
    couldNotLoadRelationships: "Could not load relationships",
    selectGender: "Select gender",
    male: "Male",
    female: "Female",
    checkingEligibility: "Checking eligibility...",
    resettingConversation: "Resetting conversation...",
    conversationReset: "Conversation reset.",
    chatError: "The assistant could not complete the request. Please try again in a moment.",
    noReadableResponse: "No readable response was returned.",
    unreadableAnswer: "I received the response, but no readable answer was provided.",
    availableVisaTypes: "Available visa types:",
    chooseVisaToCheck: "Choose a visa to check eligibility:",
    status: "Eligibility",
    visa: "Visa",
    applicantCountry: "Applicant Country",
    passedChecks: "Passed checks",
    failedChecks: "Failed checks",
    missingFields: "Missing fields",
    eligibilityResult: "Eligibility Result",
    visaNumber: "Visa Number",
    visaName: "Visa Name",
    notProvided: "Not provided",
    noPassedChecks: "No passed checks were returned.",
    noFailedChecks: "No failed checks were returned.",
    noMissingFields: "No missing fields were returned.",
    availableVisaTypesTitle: "Available Visa Types",
    noVisaTypesReturned: "No visa types were returned.",
    approved: "Eligible",
    notApproved: "Not Eligible",
    needMoreInfo: "Need More Information",
    information: "Information",
    visaNo: "Visa No.",
    visaTypeMissing: "Visa type not provided",
    visaNameMissing: "Visa name not available",
    occupationNameMissing: "Occupation name not available",
    relationshipNameMissing: "Relationship name not available",
    checkPassed: "passed",
    checkFailed: "did not pass",
    genderMaleOnlyNote: "Note: this visa is available to male applicants only according to the visible gender restriction.",
    genderFemaleOnlyNote: "Note: this visa is available to female applicants only according to the visible gender restriction.",
    userAvatar: "You",
  },
  ar: {
    pageTitle: "مساعد تأشيرة الكويت الذكي",
    selectedLanguageAria: "اللغة المختارة: العربية",
    stateName: "دولة الكويت",
    ministryName: "وزارة الداخلية",
    heroTitleLead: "تأشيرة الكويت",
    heroTitleAccent: "المساعد الذكي",
    heroSubtitle: "دليلك الذكي لمعلومات التأشيرات ودعم فحص الأهلية",
    eligibilityTitle: "تحقق من أهليتك",
    eligibilityDescription: "أجب عن بعض الأسئلة واحصل على نتيجة أهلية فورية.",
    guideChatSupport: "إرشاد المحادثة",
    guideDirectCheck: "فحص مباشر",
    guideOfficialLinks: "روابط رسمية",
    kuwaitPortalTitle: "بوابة تأشيرة الكويت",
    kuwaitPortalText: "طلبات التأشيرات الرسمية والوصول للحساب",
    visitKuwaitTitle: "زوروا الكويت",
    visitKuwaitText: "دليل السياحة والتجارب في الكويت",
    touristVisaStat: "تأشيرة سياحية",
    familyVisaStat: "تأشيرة عائلية",
    businessVisaStat: "تأشيرة أعمال",
    governmentVisaStat: "تأشيرة حكومية",
    thousand: "ألف",
    visasIssued2025: "تأشيرات صدرت في 2025",
    startEligibility: "الفحص المباشر",
    secureChatTitle: "جلسة محادثة آمنة",
    secureChatDescription: "بياناتك آمنة ومحمية",
    resetConversation: "إعادة ضبط المحادثة",
    welcomeMessage: "مرحباً! أنا مساعد تأشيرة الكويت. يرجى مشاركة جنسية مقدم الطلب، نوع التأشيرة، العمر، المهنة، الجنس، وأي تفاصيل خاصة بالمرافق أو صلة القرابة إن وجدت.",
    typingLabel: "مساعد الداخلية يكتب",
    typingStatus: "مساعد الداخلية يكتب...",
    chatPlaceholder: "اسأل عن التأشيرات...",
    attachFile: "إرفاق ملف",
    voiceInput: "إدخال صوتي",
    voiceListening: "يتم الاستماع... اضغط على الميكروفون مرة أخرى للإرسال.",
    voiceTranscribing: "جاري تحويل الصوت إلى نص...",
    voiceUnsupported: "الإدخال الصوتي غير مدعوم في هذا المتصفح.",
    voicePermissionError: "تم حظر الوصول إلى الميكروفون. يرجى السماح باستخدام الميكروفون والمحاولة مرة أخرى.",
    voiceNoSpeech: "لم أتمكن من التقاط صوت واضح. يرجى المحاولة مرة أخرى.",
    voiceTranscriptionError: "تعذر تحويل الرسالة الصوتية إلى نص. يرجى المحاولة مرة أخرى.",
    sendMessage: "إرسال الرسالة",
    officialNote: "هذه خدمة رسمية من وزارة الداخلية في دولة الكويت.",
    directService: "خدمة مباشرة",
    directEligibilityTitle: "فحص الأهلية المباشر",
    directEligibilitySubtitle: "تجربة ذكية موجهة للوصول إلى نتيجة أوضح وأسرع.",
    closeModal: "إغلاق النافذة",
    stepCountry: "الدولة",
    stepVisa: "التأشيرة",
    stepDetails: "التفاصيل",
    stepResult: "النتيجة",
    countryPanelTitle: "اختر دولة مقدم الطلب",
    countryPanelDescription: "ابحث واختر جنسية مقدم الطلب.",
    visaPanelTitle: "اختر نوع التأشيرة",
    visaPanelDescription: "تظهر فقط أنواع التأشيرات المتاحة للدولة المختارة.",
    detailsPanelTitle: "أكمل تفاصيل مقدم الطلب",
    detailsPanelDescription: "أدخل فقط التفاصيل المطلوبة حسب قواعد هذه التأشيرة.",
    snapshotKicker: "ملخص مباشر",
    snapshotTitle: "ملخص الطلب",
    countryLabel: "دولة / جنسية مقدم الطلب",
    visaTypeLabel: "نوع التأشيرة",
    ageLabel: "العمر",
    agePlaceholder: "عمر مقدم الطلب",
    occupationLabel: "المهنة",
    genderLabel: "الجنس",
    relationshipLabel: "صلة القرابة / المرافق",
    checkEligibility: "فحص الأهلية",
    cancel: "إلغاء",
    startOver: "البدء من جديد",
    selectCountry: "اختر دولة مقدم الطلب",
    selectVisaType: "اختر نوع التأشيرة",
    searchCountries: "ابحث عن دولة...",
    searchVisaTypes: "ابحث عن نوع تأشيرة...",
    searchGenders: "ابحث عن الجنس...",
    searchRelationships: "ابحث عن صلة قرابة...",
    noCountryMatches: "لا توجد دول مطابقة.",
    noVisaTypeMatches: "لا توجد أنواع تأشيرات مطابقة.",
    noGenderMatches: "لا توجد نتائج مطابقة.",
    noRelationshipMatches: "لا توجد صلات قرابة مطابقة.",
    loadingCountries: "جاري تحميل الدول...",
    loadingVisaTypes: "جاري تحميل أنواع التأشيرات...",
    noVisaTypes: "لم يتم العثور على أنواع تأشيرات لهذه الدولة.",
    selectOccupation: "اختر المهنة",
    loadingOccupations: "جاري تحميل المهن المتاحة...",
    noOccupationRestriction: "لا يوجد تقييد مهنة لهذه التأشيرة",
    selectAvailableOccupation: "اختر مهنة متاحة",
    searchOccupations: "ابحث عن مهنة...",
    noOccupationMatches: "لا توجد مهن مطابقة.",
    couldNotLoadOccupations: "تعذر تحميل المهن",
    selectRelationships: "اختر صلات القرابة",
    loadingRelationships: "جاري تحميل صلات القرابة المتاحة...",
    loadingVisaRules: "جاري تحميل قواعد التأشيرة...",
    noRelationshipRestriction: "لا توجد علاقات أو مرافقون مسموحون لهذه التأشيرة",
    couldNotLoadRelationships: "تعذر تحميل صلات القرابة",
    selectGender: "اختر الجنس",
    male: "ذكر",
    female: "أنثى",
    checkingEligibility: "جاري فحص الأهلية...",
    resettingConversation: "جاري إعادة ضبط المحادثة...",
    conversationReset: "تمت إعادة ضبط المحادثة.",
    chatError: "تعذر على المساعد إكمال الطلب. يرجى المحاولة بعد قليل.",
    noReadableResponse: "لم يتم إرجاع رد قابل للقراءة.",
    unreadableAnswer: "وصلني الرد، لكن لا توجد إجابة قابلة للعرض.",
    availableVisaTypes: "أنواع التأشيرات المتاحة:",
    chooseVisaToCheck: "اختر فيزا لبدء فحص الأهلية:",
    status: "الأهلية",
    visa: "التأشيرة",
    applicantCountry: "دولة مقدم الطلب",
    passedChecks: "الفحوصات المطابقة",
    failedChecks: "الفحوصات غير المطابقة",
    missingFields: "الحقول الناقصة",
    eligibilityResult: "نتيجة الأهلية",
    visaNumber: "رقم التأشيرة",
    visaName: "اسم التأشيرة",
    notProvided: "غير مذكور",
    noPassedChecks: "لم يتم إرجاع فحوصات مطابقة.",
    noFailedChecks: "لم يتم إرجاع فحوصات غير مطابقة.",
    noMissingFields: "لا توجد حقول ناقصة.",
    availableVisaTypesTitle: "أنواع التأشيرات المتاحة",
    noVisaTypesReturned: "لم يتم إرجاع أنواع تأشيرات.",
    approved: "مؤهل",
    notApproved: "غير مؤهل",
    needMoreInfo: "تحتاج معلومات إضافية",
    information: "معلومات",
    visaNo: "تأشيرة رقم",
    visaTypeMissing: "نوع التأشيرة غير متوفر",
    visaNameMissing: "اسم التأشيرة غير متوفر",
    occupationNameMissing: "اسم المهنة غير متوفر",
    relationshipNameMissing: "اسم صلة القرابة غير متوفر",
    checkPassed: "مطابق",
    checkFailed: "غير مطابق",
    genderMaleOnlyNote: "ملاحظة: هذه التأشيرة متاحة للذكور فقط حسب قيود الجنس الظاهرة في البيانات.",
    genderFemaleOnlyNote: "ملاحظة: هذه التأشيرة متاحة للإناث فقط حسب قيود الجنس الظاهرة في البيانات.",
    userAvatar: "أنت",
  },
};

const state = {
  sessionId: getOrCreateSessionId(),
  language: getStoredLanguage(),
  theme: getStoredTheme(),
  countries: [],
  visaTypes: [],
  occupations: [],
  relationships: [],
  selectedRelationships: [],
  selectedCountry: null,
  isCountriesLoaded: false,
  isEligibilityLoading: false,
  currentEligibilityStep: "country",
  hasEligibilityResult: false,
  isOccupationsLoading: false,
  isRelationshipsLoading: false,
  isVoiceRecording: false,
  isVoiceProcessing: false,
  mediaRecorder: null,
  voiceStream: null,
  voiceChunks: [],
  voiceRecordingTimer: null,
  visaDataRefreshToken: VISA_DATA_REFRESH_TOKEN,
};

const elements = {
  chatCard: document.querySelector(".chat-card"),
  chatMessages: document.getElementById("chatMessages"),
  chatForm: document.getElementById("chatForm"),
  chatInput: document.getElementById("chatInput"),
  voiceInputButton: document.getElementById("voiceInputButton"),
  sendChatButton: document.getElementById("sendChatButton"),
  resetChatButton: document.getElementById("resetChatButton"),
  chatStatus: document.getElementById("chatStatus"),
  typingPreview: document.getElementById("typingPreview"),
  languageButton: document.getElementById("languageButton"),
  languageLabel: document.getElementById("languageLabel"),
  languageMenu: document.getElementById("languageMenu"),
  languageOptions: document.querySelectorAll("[data-language]"),
  themeToggleButton: document.getElementById("themeToggleButton"),
  themeToggleIcon: document.getElementById("themeToggleIcon"),
  heroLightVideo: document.getElementById("heroLightVideo"),
  heroDarkVideo: document.getElementById("heroDarkVideo"),
  openEligibilityButton: document.getElementById("openEligibilityButton"),
  eligibilityModal: document.getElementById("eligibilityModal"),
  closeEligibilityButton: document.getElementById("closeEligibilityButton"),
  cancelEligibilityButton: document.getElementById("cancelEligibilityButton"),
  eligibilityForm: document.getElementById("eligibilityForm"),
  countrySelect: document.getElementById("countrySelect"),
  countrySmartSelect: document.getElementById("countrySmartSelect"),
  countryTrigger: document.getElementById("countryTrigger"),
  countrySelectionText: document.getElementById("countrySelectionText"),
  countrySearchInput: document.getElementById("countrySearchInput"),
  countryMenu: document.getElementById("countryMenu"),
  visaTypeGroup: document.getElementById("visaTypeGroup"),
  visaTypeSelect: document.getElementById("visaTypeSelect"),
  visaTypeSmartSelect: document.getElementById("visaTypeSmartSelect"),
  visaTypeTrigger: document.getElementById("visaTypeTrigger"),
  visaTypeSelectionText: document.getElementById("visaTypeSelectionText"),
  visaTypeSearchInput: document.getElementById("visaTypeSearchInput"),
  visaTypeMenu: document.getElementById("visaTypeMenu"),
  ageInput: document.getElementById("ageInput"),
  occupationInput: document.getElementById("occupationInput"),
  occupationSingleSelect: document.getElementById("occupationSingleSelect"),
  occupationTrigger: document.getElementById("occupationTrigger"),
  occupationSelectionText: document.getElementById("occupationSelectionText"),
  occupationSearchInput: document.getElementById("occupationSearchInput"),
  occupationMenu: document.getElementById("occupationMenu"),
  genderSelect: document.getElementById("genderSelect"),
  genderSmartSelect: document.getElementById("genderSmartSelect"),
  genderTrigger: document.getElementById("genderTrigger"),
  genderSelectionText: document.getElementById("genderSelectionText"),
  genderSearchInput: document.getElementById("genderSearchInput"),
  genderMenu: document.getElementById("genderMenu"),
  relationshipMultiSelect: document.getElementById("relationshipMultiSelect"),
  relationshipInput: document.getElementById("relationshipInput"),
  relationshipSelectionText: document.getElementById("relationshipSelectionText"),
  relationshipSearchInput: document.getElementById("relationshipSearchInput"),
  relationshipMenu: document.getElementById("relationshipMenu"),
  checkEligibilityButton: document.getElementById("checkEligibilityButton"),
  eligibilityStatus: document.getElementById("eligibilityStatus"),
  eligibilityResult: document.getElementById("eligibilityResult"),
  wizardSteps: document.querySelectorAll(".wizard-step"),
  wizardPanels: document.querySelectorAll("[data-wizard-panel]"),
  snapshotCountry: document.getElementById("snapshotCountry"),
  snapshotVisa: document.getElementById("snapshotVisa"),
  snapshotAge: document.getElementById("snapshotAge"),
  snapshotOccupation: document.getElementById("snapshotOccupation"),
  snapshotGender: document.getElementById("snapshotGender"),
  snapshotRelationship: document.getElementById("snapshotRelationship"),
};

const searchableSelects = {
  country: {
    select: elements.countrySelect,
    container: elements.countrySmartSelect,
    trigger: elements.countryTrigger,
    text: elements.countrySelectionText,
    search: elements.countrySearchInput,
    menu: elements.countryMenu,
    placeholder: () => t("selectCountry"),
    empty: () => t("noCountryMatches"),
  },
  visaType: {
    select: elements.visaTypeSelect,
    container: elements.visaTypeSmartSelect,
    trigger: elements.visaTypeTrigger,
    text: elements.visaTypeSelectionText,
    search: elements.visaTypeSearchInput,
    menu: elements.visaTypeMenu,
    placeholder: () => t("selectVisaType"),
    empty: () => t("noVisaTypeMatches"),
  },
  gender: {
    select: elements.genderSelect,
    container: elements.genderSmartSelect,
    trigger: elements.genderTrigger,
    text: elements.genderSelectionText,
    search: elements.genderSearchInput,
    menu: elements.genderMenu,
    placeholder: () => t("selectGender"),
    empty: () => t("noGenderMatches"),
  },
};

document.addEventListener("DOMContentLoaded", () => {
  bindEvents();
  applyTheme(state.theme);
  applyLanguage(state.language);
  loadCountries();
});

function bindEvents() {
  elements.chatForm.addEventListener("submit", handleChatSubmit);
  elements.resetChatButton.addEventListener("click", handleResetConversation);
  elements.chatInput.addEventListener("input", autoSizeChatInput);
  elements.chatInput.addEventListener("keydown", handleChatInputKeyDown);
  elements.voiceInputButton.addEventListener("click", handleVoiceInputClick);
  elements.languageButton.addEventListener("click", handleLanguageToggle);
  elements.languageOptions.forEach((button) => {
    button.addEventListener("click", handleLanguageSelection);
  });
  elements.themeToggleButton?.addEventListener("click", toggleTheme);

  elements.openEligibilityButton.addEventListener("click", openEligibilityModal);
  elements.closeEligibilityButton.addEventListener("click", closeEligibilityModal);
  elements.cancelEligibilityButton.addEventListener("click", closeEligibilityModal);
  elements.eligibilityModal.addEventListener("click", handleBackdropClick);
  bindSearchableSelectEvents();
  elements.countrySelect.addEventListener("change", handleCountryChange);
  elements.visaTypeSelect.addEventListener("change", handleVisaTypeChange);
  elements.occupationTrigger.addEventListener("click", toggleOccupationMenu);
  elements.occupationTrigger.addEventListener("keydown", handleOccupationTriggerKeyDown);
  elements.occupationSearchInput.addEventListener("input", renderOccupationOptions);
  elements.occupationSearchInput.addEventListener("keydown", handleOccupationSearchKeyDown);
  elements.occupationMenu.addEventListener("click", handleOccupationOptionClick);
  elements.relationshipInput.addEventListener("click", toggleRelationshipMenu);
  elements.relationshipSearchInput.addEventListener("input", renderRelationshipOptions);
  elements.relationshipSearchInput.addEventListener("keydown", handleRelationshipSearchKeyDown);
  elements.ageInput.addEventListener("input", syncEligibilitySnapshot);
  elements.genderSelect.addEventListener("change", syncEligibilitySnapshot);
  elements.occupationInput.addEventListener("change", syncEligibilitySnapshot);
  elements.wizardSteps.forEach((step) => {
    step.addEventListener("click", handleWizardStepClick);
  });
  elements.eligibilityForm.addEventListener("submit", handleEligibilitySubmit);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && elements.eligibilityModal.classList.contains("is-open")) {
      if (hasOpenDirectSelect()) {
        closeAllSearchableSelects();
        closeOccupationMenu();
        closeRelationshipMenu();
        return;
      }

      closeAllSearchableSelects();
      closeOccupationMenu();
      closeRelationshipMenu();
      closeEligibilityModal();
    }

    if (event.key === "Escape") {
      closeLanguageMenu();
    }
  });

  document.addEventListener("click", (event) => {
    closeSearchableSelectsOutside(event.target);

    if (!elements.occupationSingleSelect.contains(event.target)) {
      closeOccupationMenu();
    }

    if (!elements.relationshipMultiSelect.contains(event.target)) {
      closeRelationshipMenu();
    }

    if (!elements.languageButton.contains(event.target) && !elements.languageMenu.contains(event.target)) {
      closeLanguageMenu();
    }
  });
}

function bindSearchableSelectEvents() {
  Object.keys(searchableSelects).forEach((key) => {
    const config = searchableSelects[key];
    if (!config.container || !config.trigger || !config.search || !config.menu || !config.select) {
      return;
    }

    config.trigger.addEventListener("click", (event) => toggleSearchableSelect(key, event));
    config.trigger.addEventListener("keydown", (event) => handleSearchableTriggerKeyDown(key, event));
    config.search.addEventListener("input", () => renderSearchableSelectOptions(key));
    config.search.addEventListener("keydown", (event) => handleSearchableSearchKeyDown(key, event));
    config.menu.addEventListener("click", (event) => handleSearchableOptionClick(key, event));
  });
}

function handleWizardStepClick(event) {
  const step = event.currentTarget.dataset.stepTarget;
  if (!isWizardStepAvailable(step)) {
    return;
  }

  setEligibilityStep(step);
}

function isWizardStepAvailable(step) {
  if (step === "country") {
    return true;
  }

  if (step === "visa") {
    return Boolean(elements.countrySelect.value);
  }

  if (step === "details") {
    return Boolean(elements.countrySelect.value && elements.visaTypeSelect.value);
  }

  if (step === "result") {
    return state.hasEligibilityResult;
  }

  return false;
}

function getAutomaticEligibilityStep() {
  if (state.hasEligibilityResult) {
    return "result";
  }

  if (elements.visaTypeSelect.value) {
    return "details";
  }

  if (elements.countrySelect.value) {
    return "visa";
  }

  return "country";
}

function setEligibilityStep(step = getAutomaticEligibilityStep()) {
  state.currentEligibilityStep = step;

  elements.wizardSteps.forEach((button) => {
    const target = button.dataset.stepTarget;
    const isActive = target === step;
    const isAvailable = isWizardStepAvailable(target);
    button.classList.toggle("is-active", isActive);
    button.classList.toggle("is-complete", isStepComplete(target));
    button.disabled = !isAvailable;
    button.setAttribute("aria-current", isActive ? "step" : "false");
  });

  elements.wizardPanels.forEach((panel) => {
    const isActive = panel.dataset.wizardPanel === step;
    panel.classList.toggle("hidden", !isActive);
    panel.classList.toggle("is-active", isActive);
  });

  // When result step is active, hide all wizard panels and show result in their place
  if (step === "result") {
    elements.wizardPanels.forEach((panel) => {
      panel.classList.add("hidden");
      panel.classList.remove("is-active");
    });
    elements.eligibilityResult.classList.remove("hidden");
  } else {
    elements.eligibilityResult.classList.add("hidden");
  }
}

function isStepComplete(step) {
  if (step === "country") {
    return Boolean(elements.countrySelect.value);
  }

  if (step === "visa") {
    return Boolean(elements.visaTypeSelect.value);
  }

  if (step === "details") {
    return state.hasEligibilityResult;
  }

  if (step === "result") {
    return state.hasEligibilityResult;
  }

  return false;
}

function syncEligibilityExperience(step = getAutomaticEligibilityStep()) {
  syncEligibilitySnapshot();
  setEligibilityStep(step);
}

function toggleSearchableSelect(key, event) {
  event.stopPropagation();

  const config = searchableSelects[key];
  if (!config || config.trigger.disabled || config.select.disabled) {
    return;
  }

  const shouldOpen = !config.container.classList.contains("is-open");
  closeAllSearchableSelects(key);
  closeOccupationMenu();
  closeRelationshipMenu();
  setSearchableSelectOpen(key, shouldOpen);
}

function openSearchableSelect(key) {
  const config = searchableSelects[key];
  if (!config || config.trigger.disabled || config.select.disabled) {
    return;
  }

  closeAllSearchableSelects(key);
  closeOccupationMenu();
  closeRelationshipMenu();
  setSearchableSelectOpen(key, true);
}

function closeSearchableSelect(key) {
  setSearchableSelectOpen(key, false);
}

function closeAllSearchableSelects(exceptKey = "") {
  Object.keys(searchableSelects).forEach((key) => {
    if (key !== exceptKey) {
      closeSearchableSelect(key);
    }
  });
}

function closeSearchableSelectsOutside(target) {
  Object.entries(searchableSelects).forEach(([key, config]) => {
    if (config.container && !config.container.contains(target)) {
      closeSearchableSelect(key);
    }
  });
}

function hasOpenDirectSelect() {
  return Boolean(
    elements.eligibilityModal.querySelector(".smart-select.is-open, .single-select.is-open, .multi-select.is-open")
  );
}

function setSearchableSelectOpen(key, isOpen) {
  const config = searchableSelects[key];
  if (!config) {
    return;
  }

  config.container.classList.toggle("is-open", isOpen);
  config.trigger.setAttribute("aria-expanded", String(isOpen));
  setActiveSelectLayer(config.container, isOpen);
  setModalSelectOpen(isOpen);

  if (!isOpen) {
    return;
  }

  config.search.value = "";
  renderSearchableSelectOptions(key);
  window.setTimeout(() => config.search.focus(), 0);
}

function handleSearchableTriggerKeyDown(key, event) {
  if (["Enter", " ", "ArrowDown"].includes(event.key)) {
    event.preventDefault();
    openSearchableSelect(key);
  }
}

function handleSearchableSearchKeyDown(key, event) {
  if (event.key === "Escape") {
    event.preventDefault();
    event.stopPropagation();
    closeSearchableSelect(key);
    searchableSelects[key].trigger.focus();
    return;
  }

  if (event.key !== "Enter") {
    return;
  }

  const firstOption = searchableSelects[key].menu.querySelector(".smart-select-option");
  if (!firstOption) {
    return;
  }

  event.preventDefault();
  setSearchableSelectValue(key, firstOption.dataset.value);
  closeSearchableSelect(key);
  searchableSelects[key].trigger.focus();
}

function handleSearchableOptionClick(key, event) {
  const option = event.target.closest(".smart-select-option");
  if (!option) {
    return;
  }

  setSearchableSelectValue(key, option.dataset.value);
  closeSearchableSelect(key);
  searchableSelects[key].trigger.focus();
}

function setSearchableSelectValue(key, value) {
  const config = searchableSelects[key];
  config.select.value = value || "";
  config.select.dispatchEvent(new Event("change", { bubbles: true }));
  syncSearchableSelect(key);
}

function syncAllSearchableSelects() {
  Object.keys(searchableSelects).forEach(syncSearchableSelect);
}

function syncSearchableSelect(key) {
  syncSearchableSelectText(key);
  renderSearchableSelectOptions(key);
  syncSearchableSelectState(key);
}

function syncSearchableSelectText(key) {
  const config = searchableSelects[key];
  if (!config) {
    return;
  }

  const selectedOption = config.select.selectedOptions[0];
  const fallbackOption = config.select.querySelector("option[value='']");
  const label = selectedOption?.value
    ? getSearchableOptionPrimary(selectedOption)
    : fallbackOption?.textContent || config.placeholder();

  config.text.textContent = label;
  config.trigger.title = label;
}

function syncSearchableSelectState(key) {
  const config = searchableSelects[key];
  if (!config) {
    return;
  }

  const isDisabled = Boolean(config.select.disabled);
  config.trigger.disabled = isDisabled;
  config.container.classList.toggle("is-disabled", isDisabled);

  if (isDisabled) {
    closeSearchableSelect(key);
  }
}

function renderSearchableSelectOptions(key) {
  const config = searchableSelects[key];
  if (!config) {
    return;
  }

  config.menu.innerHTML = "";
  const options = Array.from(config.select.options).filter((option) => option.value);

  if (!options.length) {
    const empty = document.createElement("div");
    empty.className = "single-select-empty";
    empty.textContent = config.select.options[0]?.textContent || config.placeholder();
    config.menu.appendChild(empty);
    return;
  }

  const query = normalizeDisplayText(config.search.value);
  const filteredOptions = options.filter((option) => {
    if (!query) {
      return true;
    }

    return normalizeDisplayText(getSearchableOptionSearchText(option)).includes(query);
  });

  if (!filteredOptions.length) {
    const empty = document.createElement("div");
    empty.className = "single-select-empty";
    empty.textContent = config.empty();
    config.menu.appendChild(empty);
    return;
  }

  filteredOptions.forEach((selectOption) => {
    const option = document.createElement("button");
    option.type = "button";
    option.className = "single-select-option smart-select-option";
    option.dataset.value = selectOption.value;
    option.setAttribute("role", "option");
    option.setAttribute("aria-selected", String(selectOption.value === config.select.value));

    const row = document.createElement("span");
    row.className = "smart-select-option-row";

    const badgeText = selectOption.dataset.badge || "";
    if (badgeText) {
      const badge = document.createElement("span");
      badge.className = "smart-select-option-badge";
      badge.textContent = badgeText;
      row.appendChild(badge);
    }

    const copy = document.createElement("span");
    copy.className = "smart-select-option-copy";

    const primary = document.createElement("span");
    primary.className = "single-select-option-primary";
    primary.textContent = getSearchableOptionPrimary(selectOption);
    copy.appendChild(primary);

    const secondaryText = selectOption.dataset.secondary || "";
    if (secondaryText) {
      const secondary = document.createElement("span");
      secondary.className = "single-select-option-secondary";
      secondary.textContent = secondaryText;
      copy.appendChild(secondary);
    }

    row.appendChild(copy);
    option.appendChild(row);
    config.menu.appendChild(option);
  });
}

function getSearchableOptionPrimary(option) {
  return option.dataset.primary || option.textContent || "";
}

function getSearchableOptionSearchText(option) {
  return [
    option.textContent,
    option.value,
    option.dataset.primary,
    option.dataset.secondary,
    option.dataset.badge,
    option.dataset.search,
  ].join(" ");
}

function getOrCreateSessionId() {
  const existing = localStorage.getItem(SESSION_KEY);
  if (existing) {
    return existing;
  }

  const generated = createSessionId();
  localStorage.setItem(SESSION_KEY, generated);
  return generated;
}

function createSessionId() {
  const generated = crypto.randomUUID
    ? crypto.randomUUID()
    : `session-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  return generated;
}

function getStoredLanguage() {
  const stored = localStorage.getItem(LANGUAGE_KEY);
  return translations[stored] ? stored : DEFAULT_LANGUAGE;
}

function getStoredTheme() {
  const stored = localStorage.getItem(THEME_KEY);
  return stored === "dark" ? "dark" : DEFAULT_THEME;
}

function t(key) {
  return translations[state.language]?.[key] || translations[DEFAULT_LANGUAGE][key] || key;
}

function normalizeActionLanguage(language) {
  return String(language || "").toLowerCase().startsWith("ar") ? "ar" : "en";
}

function tForLanguage(key, language) {
  const normalized = normalizeActionLanguage(language);
  return translations[normalized]?.[key] || translations[DEFAULT_LANGUAGE][key] || key;
}

function applyTheme(theme) {
  const nextTheme = theme === "dark" ? "dark" : DEFAULT_THEME;
  state.theme = nextTheme;
  localStorage.setItem(THEME_KEY, nextTheme);
  document.documentElement.dataset.theme = nextTheme;

  const isDark = nextTheme === "dark";
  if (elements.themeToggleButton) {
    elements.themeToggleButton.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
    elements.themeToggleButton.setAttribute("aria-pressed", String(isDark));
  }

  if (elements.themeToggleIcon) {
    elements.themeToggleIcon.src = isDark ? "day-theme.svg" : "night-theme.svg";
    elements.themeToggleIcon.alt = "";
  }

  [elements.heroLightVideo, elements.heroDarkVideo].forEach((video) => {
    if (!video) {
      return;
    }
    video.muted = true;
    const shouldPlay = (isDark && video === elements.heroDarkVideo) || (!isDark && video === elements.heroLightVideo);
    if (shouldPlay) {
      video.play?.().catch(() => {});
    }
  });
}

function toggleTheme() {
  applyTheme(state.theme === "dark" ? "light" : "dark");
}

function applyLanguage(language) {
  const nextLanguage = translations[language] ? language : DEFAULT_LANGUAGE;
  state.language = nextLanguage;
  localStorage.setItem(LANGUAGE_KEY, nextLanguage);

  const isArabic = nextLanguage === "ar";
  document.documentElement.lang = nextLanguage;
  document.documentElement.dir = isArabic ? "rtl" : "ltr";
  document.body.classList.toggle("is-arabic", isArabic);
  document.title = t("pageTitle");

  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    node.placeholder = t(node.dataset.i18nPlaceholder);
  });

  document.querySelectorAll("[data-i18n-aria-label]").forEach((node) => {
    node.setAttribute("aria-label", t(node.dataset.i18nAriaLabel));
  });

  elements.languageLabel.textContent = isArabic ? "English" : "\u0627\u0644\u0639\u0631\u0628\u064a\u0629";
  elements.languageOptions.forEach((option) => {
    if (option.dataset.language === "ar") {
      option.textContent = "\u0627\u0644\u0639\u0631\u0628\u064a\u0629";
    }
    if (option.dataset.language === "en") {
      option.textContent = "English";
    }
    option.setAttribute("aria-selected", String(option.dataset.language === nextLanguage));
  });

  syncGenderOptions();
  syncInitialGreeting();
  refreshLanguageDependentControls();
  syncEligibilityExperience(state.currentEligibilityStep);
  closeLanguageMenu();
}

function syncGenderOptions() {
  const selected = elements.genderSelect.value;
  elements.genderSelect.innerHTML = "";
  elements.genderSelect.appendChild(createOption("", t("selectGender")));
  const maleOption = createOption("male", t("male"));
  maleOption.dataset.search = "male ذكر";
  maleOption.dataset.primary = t("male");

  const femaleOption = createOption("female", t("female"));
  femaleOption.dataset.search = "female أنثى";
  femaleOption.dataset.primary = t("female");

  elements.genderSelect.append(maleOption, femaleOption);
  elements.genderSelect.value = selected;
  syncSearchableSelect("gender");
}

function syncInitialGreeting() {
  const hasUserMessages = Boolean(elements.chatMessages.querySelector(".user-message"));
  if (!hasUserMessages) {
    elements.chatMessages.innerHTML = "";
    appendWelcomeMessage();
  }
}

function refreshLanguageDependentControls() {
  const selectedCountry = elements.countrySelect.value;
  const selectedVisaType = elements.visaTypeSelect.value;
  const selectedOccupation = elements.occupationInput.value;

  if (state.isCountriesLoaded) {
    populateCountries();
    elements.countrySelect.value = selectedCountry;
    syncSearchableSelect("country");
  }

  if (state.visaTypes.length) {
    populateVisaTypes();
    elements.visaTypeSelect.value = selectedVisaType;
    syncSearchableSelect("visaType");
  } else {
    elements.visaTypeSelect.innerHTML = "";
    elements.visaTypeSelect.appendChild(createOption("", t("selectVisaType")));
    syncSearchableSelect("visaType");
  }

  if (state.occupations.length) {
    populateOccupations();
    elements.occupationInput.value = selectedOccupation;
    syncOccupationSelectionText();
    renderOccupationOptions();
  } else {
    resetOccupationOptions();
  }

  renderRelationshipOptions();
  updateRelationshipSelectionText();
}

function toggleLanguageMenu(event) {
  event.stopPropagation();
  const switcher = elements.languageButton.closest(".language-switcher");
  const isOpen = switcher.classList.toggle("is-open");
  elements.languageButton.setAttribute("aria-expanded", String(isOpen));
}

function closeLanguageMenu() {
  const switcher = elements.languageButton.closest(".language-switcher");
  switcher.classList.remove("is-open");
  elements.languageButton.setAttribute("aria-expanded", "false");
}

function handleLanguageToggle(event) {
  event.stopPropagation();
  applyLanguage(state.language === "ar" ? "en" : "ar");
}

function handleLanguageSelection(event) {
  event.stopPropagation();
  applyLanguage(event.currentTarget.dataset.language);
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    cache: "no-store",
    ...options,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-cache",
      "Pragma": "no-cache",
      "X-Visa-Data-Refresh": state.visaDataRefreshToken,
      ...(options.headers || {}),
    },
  });

  const text = await response.text();
  const data = text ? tryParseJson(text) : {};

  if (!response.ok) {
    const message =
      data?.detail ||
      data?.message ||
      `Request failed with status ${response.status}.`;
    throw new Error(message);
  }

  return data;
}

function withVisaDataRefresh(path) {
  const separator = path.includes("?") ? "&" : "?";
  return `${path}${separator}fresh=${encodeURIComponent(state.visaDataRefreshToken)}`;
}

function tryParseJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    return { message: text };
  }
}

async function handleChatSubmit(event) {
  event.preventDefault();

  const message = elements.chatInput.value.trim();
  if (!message) {
    return;
  }

  elements.chatInput.value = "";
  autoSizeChatInput();
  await submitChatMessage(message);
}

function handleChatInputKeyDown(event) {
  if (event.key !== "Enter" || event.shiftKey || event.isComposing) {
    return;
  }

  event.preventDefault();
  elements.chatForm.requestSubmit();
}

async function submitChatMessage(message, language = detectMessageLanguage(message)) {
  appendMessage("user", message);
  setChatLoading(true, t("typingStatus"), true);

  try {
    const data = await apiRequest("/api/chat", {
      method: "POST",
      body: JSON.stringify({
        session_id: state.sessionId,
        message,
        language,
        fresh_master_data: state.visaDataRefreshToken,
      }),
    });

    appendMessage("assistant", getAssistantReply(data), {
      decision: data?.decision,
      responseLanguage: data?.context?.language || language,
    });
    setChatStatus("");
  } catch (error) {
    appendMessage(
      "assistant",
      t("chatError")
    );
    setChatStatus(error.message, "error");
  } finally {
    setChatLoading(false);
  }
}

async function handleVoiceInputClick() {
  if (state.isVoiceProcessing) {
    return;
  }

  if (state.isVoiceRecording) {
    stopVoiceRecording();
    return;
  }

  await startVoiceRecording();
}

async function startVoiceRecording() {
  if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {
    setChatStatus(t("voiceUnsupported"), "error");
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
      },
    });
    const mimeType = getSupportedVoiceMimeType();
    const options = mimeType ? { mimeType } : undefined;
    const recorder = new MediaRecorder(stream, options);

    state.voiceChunks = [];
    state.voiceStream = stream;
    state.mediaRecorder = recorder;

    recorder.addEventListener("dataavailable", (event) => {
      if (event.data?.size) {
        state.voiceChunks.push(event.data);
      }
    });

    recorder.addEventListener("stop", () => {
      finalizeVoiceRecording(recorder.mimeType || mimeType || "audio/webm");
    }, { once: true });

    recorder.start();
    setVoiceRecordingState(true);
    setChatStatus(t("voiceListening"), "success");
    state.voiceRecordingTimer = window.setTimeout(stopVoiceRecording, 55000);
  } catch (error) {
    cleanupVoiceStream();
    setVoiceRecordingState(false);
    setChatStatus(t("voicePermissionError"), "error");
  }
}

function stopVoiceRecording() {
  if (!state.mediaRecorder || state.mediaRecorder.state === "inactive") {
    return;
  }

  try {
    state.mediaRecorder.requestData();
  } catch {
    // The browser may already have flushed the final chunk.
  }

  state.mediaRecorder.stop();
}

async function finalizeVoiceRecording(mimeType) {
  window.clearTimeout(state.voiceRecordingTimer);
  state.voiceRecordingTimer = null;
  cleanupVoiceStream();
  setVoiceRecordingState(false);

  const chunks = state.voiceChunks.splice(0);
  state.mediaRecorder = null;

  const blob = new Blob(chunks, { type: mimeType });
  if (!blob.size) {
    setChatStatus(t("voiceNoSpeech"), "error");
    return;
  }

  await processVoiceRecording(blob);
}

async function processVoiceRecording(blob) {
  setVoiceProcessingState(true);
  setChatStatus(t("voiceTranscribing"));

  try {
    const audioBase64 = await blobToBase64(blob);
    const data = await apiRequest("/api/speech-to-text", {
      method: "POST",
      body: JSON.stringify({
        audio_base64: audioBase64,
        mime_type: blob.type || "audio/webm",
        language: state.language,
      }),
    });

    const transcript = String(data?.transcript || "").trim();
    if (!transcript) {
      throw new Error(t("voiceNoSpeech"));
    }

    await submitChatMessage(transcript, normalizeSpeechLanguage(data?.language_code) || detectMessageLanguage(transcript));
  } catch (error) {
    setChatStatus(error.message || t("voiceTranscriptionError"), "error");
  } finally {
    setVoiceProcessingState(false);
  }
}

function normalizeSpeechLanguage(languageCode) {
  const normalized = String(languageCode || "").trim().toLowerCase();
  if (!normalized) {
    return "";
  }

  if (normalized.startsWith("ar")) return "ar";
  if (normalized.startsWith("en")) return "en";
  if (normalized.startsWith("fr")) return "fr";
  if (normalized.startsWith("de")) return "de";
  if (normalized.startsWith("es")) return "es";
  return normalized.split("-")[0];
}

function detectMessageLanguage(text) {
  return /[\u0600-\u06ff]/.test(String(text || "")) ? "ar" : "en";
}

function getSupportedVoiceMimeType() {
  const candidates = [
    "audio/webm;codecs=opus",
    "audio/webm",
    "audio/ogg;codecs=opus",
    "audio/ogg",
  ];

  return candidates.find((mimeType) => MediaRecorder.isTypeSupported(mimeType)) || "";
}

function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const value = String(reader.result || "");
      resolve(value.includes(",") ? value.split(",", 2)[1] : value);
    };
    reader.onerror = () => reject(reader.error || new Error(t("voiceTranscriptionError")));
    reader.readAsDataURL(blob);
  });
}

function setVoiceRecordingState(isRecording) {
  state.isVoiceRecording = isRecording;
  elements.chatInput.disabled = isRecording;
  elements.sendChatButton.disabled = isRecording;
  elements.resetChatButton.disabled = isRecording;
  updateVoiceButtonState();
}

function setVoiceProcessingState(isProcessing) {
  state.isVoiceProcessing = isProcessing;
  elements.chatInput.disabled = isProcessing;
  elements.sendChatButton.disabled = isProcessing;
  elements.resetChatButton.disabled = isProcessing;
  updateVoiceButtonState();
}

function cleanupVoiceStream() {
  if (!state.voiceStream) {
    return;
  }

  state.voiceStream.getTracks().forEach((track) => track.stop());
  state.voiceStream = null;
}

function updateVoiceButtonState() {
  elements.voiceInputButton.classList.toggle("is-recording", state.isVoiceRecording);
  elements.voiceInputButton.classList.toggle("is-processing", state.isVoiceProcessing);
  elements.voiceInputButton.disabled =
    state.isVoiceProcessing ||
    (!state.isVoiceRecording && elements.chatInput.disabled);
  elements.voiceInputButton.setAttribute("aria-pressed", String(state.isVoiceRecording));
}

async function handleResetConversation() {
  setChatLoading(true, t("resettingConversation"));
  const previousSessionId = state.sessionId;

  try {
    await apiRequest(`/api/reset-session/${encodeURIComponent(previousSessionId)}`, {
      method: "POST",
    });
  } catch (error) {
    console.warn("Could not reset previous chat session on the server.", error);
  } finally {
    state.sessionId = createSessionId();
    localStorage.setItem(SESSION_KEY, state.sessionId);
    resetChatMessages();
    setChatStatus(t("conversationReset"), "success");
    setChatLoading(false);
  }
}

function resetChatMessages() {
  elements.chatMessages.innerHTML = "";
  appendWelcomeMessage();
}

function appendWelcomeMessage() {
  return appendMessage("assistant", t("welcomeMessage"), { welcomeMessage: true });
}

function appendLoadingMessage(role, text) {
  const message = createMessageElement(role, text);
  message.classList.add("is-loading");
  elements.chatMessages.appendChild(message);
  scrollChatToBottom();
  return message;
}

function appendMessage(role, text, metadata = {}) {
  const message = createMessageElement(role, text, metadata);
  elements.chatMessages.appendChild(message);
  scrollChatToBottom();
  return message;
}

function createMessageElement(role, text, metadata = {}) {
  const article = document.createElement("article");
  article.className = `message ${role === "user" ? "user-message" : "assistant-message"}`;
  if (metadata.welcomeMessage) {
    article.dataset.welcomeMessage = "true";
  }

  const avatar = document.createElement("div");
  avatar.className = role === "user" ? "message-avatar" : "message-avatar message-avatar-image";
  avatar.setAttribute("aria-hidden", "true");

  if (role === "user") {
    avatar.textContent = t("userAvatar");
  } else {
    const image = document.createElement("img");
    image.src = "logo.svg?v=kuwait-ui-1";
    image.alt = "";
    avatar.appendChild(image);
  }

  const content = document.createElement("div");
  content.className = "message-content";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  renderFormattedText(bubble, text, role === "assistant" ? metadata : {});

  const time = document.createElement("span");
  time.className = "message-time";
  time.textContent = formatMessageTime(new Date());

  content.append(bubble, time);
  article.append(avatar, content);
  return article;
}

function createMessageActionPanel(metadata = {}) {
  const decision = metadata?.decision || {};
  const visaTypes = normalizeVisaTypes(decision);
  if (!visaTypes.length) {
    return null;
  }

  const panelLanguage = normalizeActionLanguage(metadata.responseLanguage || state.language);
  const panel = document.createElement("div");
  panel.className = "visa-action-panel";

  const hint = document.createElement("p");
  hint.className = "visa-action-hint";
  hint.textContent = tForLanguage("chooseVisaToCheck", panelLanguage);

  const grid = document.createElement("div");
  grid.className = "visa-action-grid";

  visaTypes.forEach((visaType) => {
    const number = String(visaType.visa_type || visaType.visaType || "").trim();
    if (!number) {
      return;
    }

    const button = document.createElement("button");
    const name = formatVisaTypeNameForLanguage(visaType, panelLanguage);
    const label = formatVisaTypeLabelForLanguage(visaType, panelLanguage);
    button.className = "visa-action-button";
    button.type = "button";
    button.dataset.visaType = number;
    button.dataset.visaLabel = label;
    button.dataset.responseLanguage = panelLanguage;
    button.setAttribute("aria-label", `${tForLanguage("chooseVisaToCheck", panelLanguage)} ${label}`);

    const numberSpan = document.createElement("span");
    numberSpan.className = "visa-action-number";
    numberSpan.textContent = `${tForLanguage("visaNo", panelLanguage)} ${number}`;

    const nameSpan = document.createElement("span");
    nameSpan.className = "visa-action-name";
    nameSpan.textContent = name || tForLanguage("visaNameMissing", panelLanguage);

    const arrow = document.createElement("span");
    arrow.className = "visa-action-arrow";
    arrow.setAttribute("aria-hidden", "true");
    arrow.textContent = panelLanguage === "ar" ? "←" : "→";

    button.append(numberSpan, nameSpan, arrow);
    button.addEventListener("click", handleVisaActionClick);
    grid.appendChild(button);
  });

  if (!grid.children.length) {
    return null;
  }

  panel.append(hint, grid);
  return panel;
}

function getVisaActionContext(metadata = {}) {
  const decision = metadata?.decision || {};
  const visaTypes = normalizeVisaTypes(decision);
  if (!visaTypes.length) {
    return null;
  }

  const language = normalizeActionLanguage(metadata.responseLanguage || state.language);
  const byNumber = new Map();

  visaTypes.forEach((visaType) => {
    const number = String(visaType.visa_type || visaType.visaType || "").trim();
    if (!number) {
      return;
    }

    byNumber.set(number, {
      language,
      number,
      label: formatVisaTypeLabelForLanguage(visaType, language),
    });
  });

  return byNumber.size ? { byNumber, language } : null;
}

function getVisaActionForLine(line, actionContext) {
  if (!actionContext?.byNumber?.size) {
    return null;
  }

  const text = String(line || "");
  const match =
    text.match(/\bVisa\s*No\.?\s*(\d+)\b/i) ||
    text.match(/(?:فيزا|تأشيرة|التأشيرة|سمة|رقم)[^\d]{0,18}(\d+)/i);

  return match ? actionContext.byNumber.get(match[1]) || null : null;
}

function createInlineVisaAction(displayHtml, action) {
  const button = document.createElement("button");
  button.className = "inline-visa-action";
  button.type = "button";
  button.dataset.visaType = action.number;
  button.dataset.visaLabel = action.label;
  button.dataset.responseLanguage = action.language;
  button.setAttribute("aria-label", `${tForLanguage("chooseVisaToCheck", action.language)} ${action.label}`);

  const label = document.createElement("span");
  label.className = "inline-visa-label";
  label.innerHTML = displayHtml;

  const arrow = document.createElement("span");
  arrow.className = "inline-visa-arrow";
  arrow.setAttribute("aria-hidden", "true");
  arrow.textContent = action.language === "ar" ? "\u2190" : "\u2192";

  button.append(label, arrow);
  button.addEventListener("click", handleVisaActionClick);
  return button;
}

async function handleVisaActionClick(event) {
  const button = event.currentTarget;
  const visaType = button.dataset.visaType;
  if (!visaType || elements.sendChatButton.disabled || state.isVoiceRecording || state.isVoiceProcessing) {
    return;
  }

  const language = normalizeActionLanguage(button.dataset.responseLanguage || state.language);
  const message = language === "ar"
    ? `أريد فحص الأهلية لفيزا رقم ${visaType}`
    : `I want to check eligibility for Visa No. ${visaType}`;

  await submitChatMessage(message, language);
}

function renderFormattedText(container, text, metadata = {}) {
  container.innerHTML = "";

  const cleanText = String(text || "").trim();

  if (!cleanText) {
    const paragraph = document.createElement("p");
    paragraph.textContent = t("noReadableResponse");
    container.appendChild(paragraph);
    return;
  }

  const lines = cleanText.split("\n").map((line) => line.trim());
  const visaActionContext = getVisaActionContext(metadata);

  let currentList = null;

  lines.forEach((line) => {
    if (!line) {
      currentList = null;
      return;
    }

    // Headings ### ## #
    if (/^###\s+/.test(line) || /^##\s+/.test(line) || /^#\s+/.test(line)) {
      currentList = null;

      const level = line.startsWith("###")
        ? "h3"
        : line.startsWith("##")
        ? "h2"
        : "h1";

      const heading = document.createElement(level);
      heading.innerHTML = formatInlineMarkdown(
        line.replace(/^#{1,3}\s+/, "")
      );

      container.appendChild(heading);
      return;
    }

    // Bullet list
    if (/^[-*\u2022]\s+/.test(line)) {
      const listText = line.replace(/^[-*\u2022]\s+/, "");
      const formattedLine = formatInlineMarkdown(listText);
      const visaAction = getVisaActionForLine(listText, visaActionContext);

      if (!currentList) {
        currentList = document.createElement("ul");
        container.appendChild(currentList);
      }

      const li = document.createElement("li");

      if (visaAction) {
        li.className = "visa-inline-item";
        li.appendChild(createInlineVisaAction(formattedLine, visaAction));
      } else {
        li.innerHTML = formattedLine;
      }

      currentList.appendChild(li);
      return;
    }

    currentList = null;

    const p = document.createElement("p");
    const formattedLine = formatInlineMarkdown(line);
    const visaAction = getVisaActionForLine(line, visaActionContext);

    if (visaAction) {
      p.className = "visa-inline-line";
      p.appendChild(createInlineVisaAction(formattedLine, visaAction));
    } else {
      p.innerHTML = formattedLine;
    }
    container.appendChild(p);
  });
}


function formatInlineMarkdown(text) {
  let html = text;

  // bold
  html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // checkmarks to styled span
  html = html.replace(/\u2705/g, `<span class="inline-check">\u2713</span>`);
  html = html.replace(/\u274C/g, `<span class="inline-cross">\u2715</span>`);

  return html;
}

function getAssistantReply(data) {
  if (typeof data?.answer === "string" && !isJsonString(data.answer)) {
    return data.answer;
  }

  if (data?.decision) {
    return formatDecisionAsText(data.decision);
  }

  if (typeof data?.answer === "string") {
    const parsed = tryParseJson(data.answer);
    if (parsed?.decision) {
      return formatDecisionAsText(parsed.decision);
    }
  }

  return t("unreadableAnswer");
}

function isJsonString(value) {
  const text = value.trim();
  return text.startsWith("{") || text.startsWith("[") || text.includes("```json");
}

function formatDecisionAsText(decision) {
  const visaTypes = normalizeVisaTypes(decision);
  if (visaTypes.length) {
    return [
      t("availableVisaTypes"),
      ...visaTypes.map((type) => `- ${formatVisaTypeLabel(type)}`),
    ].join("\n");
  }

  const status = formatStatus(decision?.status);
  const missing = normalizeList(decision?.missing_fields);
  const failed = normalizeChecks(decision?.checks).filter((check) => check.passed === false);
  const passed = normalizeChecks(decision?.checks).filter((check) => check.passed === true);

  const lines = [`${t("status")}: ${status}`];

  if (decision?.visa_type || decision?.visa_name) {
    lines.push(`${t("visa")}: ${formatVisaTypeLabel({ visa_type: decision.visa_type, visa_name: decision.visa_name })}`);
  }

  if (decision?.country) {
    lines.push(`${t("applicantCountry")}: ${decision.country}`);
  }

  if (passed.length) {
    lines.push("", `${t("passedChecks")}:`, ...passed.map((check) => `- ${check.message || formatFieldName(check.field)}`));
  }

  if (failed.length) {
    lines.push("", `${t("failedChecks")}:`, ...failed.map((check) => `- ${check.message || formatFieldName(check.field)}`));
  }

  if (missing.length) {
    lines.push("", `${t("missingFields")}:`, ...missing.map((field) => `- ${formatFieldName(field)}`));
  }

  if (decision?.message) {
    lines.push("", decision.message);
  }

  if (decision?.reason) {
    lines.push("", decision.reason);
  }

  return lines.join("\n");
}

function setChatLoading(isLoading, status = "", showTyping = false) {
  elements.sendChatButton.disabled = isLoading;
  elements.resetChatButton.disabled = isLoading;
  elements.chatInput.disabled = isLoading;
  elements.chatMessages.querySelectorAll(".visa-action-button, .inline-visa-action").forEach((button) => {
    button.disabled = isLoading;
  });
  elements.chatCard.classList.toggle("is-typing", isLoading && showTyping);
  updateVoiceButtonState();
  setChatStatus(status);
}

function formatMessageTime(date) {
  return date.toLocaleTimeString(state.language === "ar" ? "ar" : undefined, {
    hour: "numeric",
    minute: "2-digit",
  });
}

function setChatStatus(message, type) {
  setStatus(elements.chatStatus, message, type);
}

function scrollChatToBottom() {
  elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function autoSizeChatInput() {
  elements.chatInput.style.height = "auto";
  elements.chatInput.style.height = `${Math.min(elements.chatInput.scrollHeight, 145)}px`;
}

async function loadCountries() {
  setEligibilityStatus(t("loadingCountries"));
  elements.countrySelect.disabled = true;
  syncSearchableSelect("country");

  try {
    const data = await apiRequest("/api/countries");
    state.countries = normalizeCountries(data);
    state.isCountriesLoaded = true;
    populateCountries();
    setEligibilityStatus("");
  } catch (error) {
    setEligibilityStatus(error.message, "error");
  } finally {
    elements.countrySelect.disabled = false;
    syncSearchableSelect("country");
  }
}

function populateCountries() {
  elements.countrySelect.innerHTML = "";
  elements.countrySelect.appendChild(createOption("", t("selectCountry")));

  state.countries.forEach((country) => {
    const label = formatCountryLabel(country);
    const option = createOption(country.ocr_code, label);
    const primary = formatCountryName(country);

    option.dataset.countryName = country.country_name_en || country.ocr_code;
    option.dataset.primary = primary;
    option.dataset.secondary = state.language === "ar" ? "" : country.ocr_code;
    option.dataset.badge = state.language === "ar" ? "" : country.ocr_code;
    option.dataset.search = [
      country.country_name_en,
      country.country_name_ar,
      country.ocr_code,
    ].join(" ");
    elements.countrySelect.appendChild(option);
  });

  syncSearchableSelect("country");
}

function normalizeCountries(data) {
  const items = Array.isArray(data) ? data : data?.data || data?.countries || [];

  return items
    .map((item) => ({
      country_name_en: item.country_name_en || item.countryNameEn || item.name_en || item.name || "",
      country_name_ar: item.country_name_ar || item.countryNameAr || "",
      ocr_code: String(item.ocr_code || item.ocrCode || item.code || "").toUpperCase(),
    }))
    .filter((country) => country.ocr_code)
    .sort((a, b) => formatCountryLabel(a).localeCompare(formatCountryLabel(b)));
}

function openEligibilityModal() {
  elements.eligibilityModal.classList.add("is-open");
  elements.eligibilityModal.setAttribute("aria-hidden", "false");
  syncEligibilityExperience();

  if (!state.isCountriesLoaded) {
    loadCountries();
  }

  window.setTimeout(() => {
    elements.countryTrigger.focus();
  }, 0);
}

function closeEligibilityModal() {
  closeAllSearchableSelects();
  closeOccupationMenu();
  closeRelationshipMenu();
  elements.eligibilityModal.classList.remove("is-open");
  elements.eligibilityModal.setAttribute("aria-hidden", "true");
}

function handleBackdropClick(event) {
  if (event.target === elements.eligibilityModal) {
    closeEligibilityModal();
  }
}

async function handleCountryChange() {
  const ocrCode = elements.countrySelect.value;
  state.selectedCountry = state.countries.find((country) => country.ocr_code === ocrCode) || null;
  state.hasEligibilityResult = false;

  resetDirectCheckAfterCountry();

  if (!ocrCode) {
    elements.visaTypeGroup.classList.add("hidden");
    setEligibilityStatus("");
    syncEligibilityExperience("country");
    return;
  }

  elements.visaTypeGroup.classList.remove("hidden");
  elements.visaTypeSelect.disabled = true;
  elements.visaTypeSelect.innerHTML = "";
  elements.visaTypeSelect.appendChild(createOption("", t("loadingVisaTypes")));
  syncSearchableSelect("visaType");
  setEligibilityStatus(t("loadingVisaTypes"));

  try {
    const data = await apiRequest(withVisaDataRefresh(`/api/visa-types/${encodeURIComponent(ocrCode)}`));
    state.visaTypes = normalizeVisaTypes(data);
    populateVisaTypes();
    setEligibilityStatus(state.visaTypes.length ? "" : t("noVisaTypes"));
    syncEligibilityExperience("visa");
  } catch (error) {
    state.visaTypes = [];
    elements.visaTypeSelect.innerHTML = "";
    elements.visaTypeSelect.appendChild(createOption("", t("selectVisaType")));
    syncSearchableSelect("visaType");
    setEligibilityStatus(error.message, "error");
  } finally {
    elements.visaTypeSelect.disabled = false;
    syncSearchableSelect("visaType");
  }
}

function resetDirectCheckAfterCountry() {
  state.hasEligibilityResult = false;
  state.visaTypes = [];
  state.occupations = [];
  state.relationships = [];
  state.selectedRelationships = [];
  state.isOccupationsLoading = false;
  state.isRelationshipsLoading = false;
  elements.visaTypeSelect.innerHTML = "";
  elements.visaTypeSelect.appendChild(createOption("", t("selectVisaType")));
  syncSearchableSelect("visaType");
  resetOccupationOptions();
  resetRelationshipOptions();
  hideConditionalFields();
  clearDirectInputs();
  elements.eligibilityResult.innerHTML = "";
  syncEligibilityExperience();
}

function populateVisaTypes() {
  elements.visaTypeSelect.innerHTML = "";
  elements.visaTypeSelect.appendChild(createOption("", t("selectVisaType")));

  state.visaTypes.forEach((visaType) => {
    const option = createOption(String(visaType.visa_type), formatVisaTypeLabel(visaType));
    option.dataset.primary = formatVisaTypeName(visaType);
    option.dataset.secondary = `${t("visaNo")} ${visaType.visa_type}`;
    option.dataset.badge = String(visaType.visa_type);
    option.dataset.search = [
      visaType.visa_type,
      visaType.visa_name,
      visaType.visa_name_en,
      visaType.typeOfVisa,
      visaType.name,
    ].join(" ");
    elements.visaTypeSelect.appendChild(option);
  });

  syncSearchableSelect("visaType");
}

async function handleVisaTypeChange() {
  elements.eligibilityResult.innerHTML = "";
  state.hasEligibilityResult = false;
  state.occupations = [];
  state.relationships = [];
  state.selectedRelationships = [];
  state.isOccupationsLoading = false;
  state.isRelationshipsLoading = false;
  resetOccupationOptions();
  resetRelationshipOptions();

  if (elements.visaTypeSelect.value) {
    showConditionalFields();
    syncEligibilityExperience("details");
    await Promise.all([
      loadOccupationsForSelectedVisa(),
      loadRelationshipsForSelectedVisa(),
    ]);
    return;
  }

  hideConditionalFields();
  syncEligibilityExperience();
}

function showConditionalFields() {
  document.querySelectorAll(".conditional-field").forEach((field) => {
    field.classList.remove("hidden");
  });
  elements.checkEligibilityButton.classList.remove("hidden");
}

function hideConditionalFields() {
  document.querySelectorAll(".conditional-field").forEach((field) => {
    field.classList.add("hidden");
  });
  elements.checkEligibilityButton.classList.add("hidden");
}

function clearDirectInputs() {
  elements.ageInput.value = "";
  elements.occupationInput.value = "";
  elements.genderSelect.value = "";
  syncSearchableSelect("gender");
  state.selectedRelationships = [];
  syncOccupationSelectionText();
  renderOccupationOptions();
  closeOccupationMenu();
  updateRelationshipSelectionText();
  renderRelationshipOptions();
  closeRelationshipMenu();
  syncEligibilitySnapshot();
}

function syncEligibilitySnapshot() {
  const selectedVisa = getSelectedVisaType();
  const selectedOccupation = getSelectedOccupation();
  const selectedGenderOption = elements.genderSelect.selectedOptions[0];
  const selectedRelationships = getSelectedRelationshipLabels();

  setSnapshotValue(elements.snapshotCountry, formatCountryLabel(state.selectedCountry));
  setSnapshotValue(elements.snapshotVisa, selectedVisa ? formatVisaTypeLabel(selectedVisa) : "");
  setSnapshotValue(elements.snapshotAge, elements.ageInput.value);
  setSnapshotValue(elements.snapshotOccupation, selectedOccupation ? formatOccupationLabel(selectedOccupation) : "");
  setSnapshotValue(elements.snapshotGender, selectedGenderOption?.value ? selectedGenderOption.textContent : "");
  setSnapshotValue(elements.snapshotRelationship, selectedRelationships.join(", "));
}

function setSnapshotValue(element, value) {
  if (!element) {
    return;
  }

  const label = String(value || "").trim() || t("notProvided");
  const item = element.closest(".snapshot-item");
  element.textContent = label;
  element.classList.toggle("is-empty", label === t("notProvided"));
  item?.classList.toggle("is-empty", label === t("notProvided"));
  item?.classList.toggle("has-value", label !== t("notProvided"));
}

function getSelectedOccupation() {
  const selectedValue = elements.occupationInput.value;
  return state.occupations.find((occupation) => occupation.value === selectedValue) || null;
}

function getSelectedRelationshipLabels() {
  return state.selectedRelationships.map((value) => {
    const relationship = state.relationships.find((item) => item.value === value);
    return relationship ? formatRelationshipLabel(relationship) : value;
  });
}

async function loadOccupationsForSelectedVisa() {
  const ocrCode = elements.countrySelect.value;
  const visaType = elements.visaTypeSelect.value;

  if (!ocrCode || !visaType) {
    resetOccupationOptions();
    return;
  }

  state.isOccupationsLoading = true;
  syncDirectCheckButtonState();
  resetOccupationOptions(t("loadingOccupations"));
  setEligibilityStatus(t("loadingOccupations"));

  try {
    const data = await apiRequest(
      withVisaDataRefresh(`/api/occupations/${encodeURIComponent(ocrCode)}/${encodeURIComponent(visaType)}`)
    );

    if (ocrCode !== elements.countrySelect.value || visaType !== elements.visaTypeSelect.value) {
      return;
    }

    state.occupations = normalizeOccupations(data);
    populateOccupations();
    if (!state.isRelationshipsLoading) {
      setEligibilityStatus("");
    }
  } catch (error) {
    if (ocrCode === elements.countrySelect.value && visaType === elements.visaTypeSelect.value) {
      state.occupations = [];
      resetOccupationOptions(t("couldNotLoadOccupations"));
      setEligibilityStatus(error.message, "error");
    }
  } finally {
    if (ocrCode === elements.countrySelect.value && visaType === elements.visaTypeSelect.value) {
      state.isOccupationsLoading = false;
      syncOccupationSelectState();
      syncDirectCheckButtonState();
    }
  }
}

function resetOccupationOptions(label = t("selectOccupation")) {
  elements.occupationInput.innerHTML = "";
  elements.occupationInput.appendChild(createOption("", label));
  elements.occupationInput.value = "";
  elements.occupationSearchInput.value = "";
  updateOccupationSelectionText(label);
  renderOccupationOptions();
  closeOccupationMenu();
  syncOccupationSelectState();
}

function populateOccupations() {
  elements.occupationInput.innerHTML = "";
  elements.occupationSearchInput.value = "";

  if (!state.occupations.length) {
    elements.occupationInput.appendChild(createOption("", t("noOccupationRestriction")));
    updateOccupationSelectionText(t("noOccupationRestriction"));
    renderOccupationOptions();
    closeOccupationMenu();
    syncOccupationSelectState();
    return;
  }

  elements.occupationInput.appendChild(createOption("", t("selectAvailableOccupation")));

  state.occupations.forEach((occupation) => {
    elements.occupationInput.appendChild(
      createOption(occupation.value, formatOccupationLabel(occupation, occupation.label || occupation.value))
    );
  });

  syncOccupationSelectionText();
  renderOccupationOptions();
  syncOccupationSelectState();
}

function syncOccupationSelectState() {
  const isDisabled =
    state.isOccupationsLoading ||
    !elements.visaTypeSelect.value ||
    !state.occupations.length;
  setOccupationSelectDisabled(isDisabled);
}

function setOccupationSelectDisabled(isDisabled) {
  elements.occupationInput.disabled = isDisabled;
  elements.occupationTrigger.disabled = isDisabled;
  elements.occupationSearchInput.disabled = isDisabled;
  elements.occupationSingleSelect.classList.toggle("is-disabled", isDisabled);
  if (isDisabled) {
    closeOccupationMenu();
  }
}

function toggleOccupationMenu(event) {
  event.stopPropagation();

  if (elements.occupationTrigger.disabled || !state.occupations.length) {
    return;
  }

  closeAllSearchableSelects();
  const isOpen = elements.occupationSingleSelect.classList.toggle("is-open");
  elements.occupationTrigger.setAttribute("aria-expanded", String(isOpen));
  setActiveSelectLayer(elements.occupationSingleSelect, isOpen);
  setModalSelectOpen(isOpen);

  if (isOpen) {
    closeRelationshipMenu();
    renderOccupationOptions();
    window.setTimeout(() => elements.occupationSearchInput.focus(), 0);
  }
}

function openOccupationMenu() {
  if (elements.occupationTrigger.disabled || !state.occupations.length) {
    return;
  }

  closeAllSearchableSelects();
  elements.occupationSingleSelect.classList.add("is-open");
  elements.occupationTrigger.setAttribute("aria-expanded", "true");
  setActiveSelectLayer(elements.occupationSingleSelect, true);
  setModalSelectOpen(true);
  renderOccupationOptions();
  window.setTimeout(() => elements.occupationSearchInput.focus(), 0);
}

function closeOccupationMenu() {
  elements.occupationSingleSelect.classList.remove("is-open");
  elements.occupationTrigger.setAttribute("aria-expanded", "false");
  setActiveSelectLayer(elements.occupationSingleSelect, false);
  setModalSelectOpen(false);
}

function setActiveSelectLayer(selectElement, isOpen) {
  selectElement.closest(".field-group")?.classList.toggle("is-select-open", isOpen);
}

function setModalSelectOpen() {
  const modal = elements.eligibilityModal.querySelector(".modal");
  if (!modal) {
    return;
  }

  const hasOpenSelect = Boolean(
    modal.querySelector(".smart-select.is-open, .single-select.is-open, .multi-select.is-open")
  );
  modal.classList.toggle("has-open-select", hasOpenSelect);
}

function handleOccupationTriggerKeyDown(event) {
  if (["Enter", " ", "ArrowDown"].includes(event.key)) {
    event.preventDefault();
    openOccupationMenu();
  }
}

function handleOccupationSearchKeyDown(event) {
  if (event.key === "Escape") {
    event.preventDefault();
    event.stopPropagation();
    closeOccupationMenu();
    elements.occupationTrigger.focus();
    return;
  }

  if (event.key !== "Enter") {
    return;
  }

  const firstOption = elements.occupationMenu.querySelector(".single-select-option");
  if (!firstOption) {
    return;
  }

  event.preventDefault();
  setOccupationValue(firstOption.dataset.value);
  closeOccupationMenu();
  elements.occupationTrigger.focus();
}

function handleOccupationOptionClick(event) {
  const option = event.target.closest(".single-select-option");
  if (!option) {
    return;
  }

  setOccupationValue(option.dataset.value);
  closeOccupationMenu();
  elements.occupationTrigger.focus();
}

function setOccupationValue(value) {
  elements.occupationInput.value = value || "";
  elements.occupationInput.dispatchEvent(new Event("change", { bubbles: true }));
  syncOccupationSelectionText();
  renderOccupationOptions();
  syncEligibilitySnapshot();
}

function syncOccupationSelectionText() {
  updateOccupationSelectionText(t("selectAvailableOccupation"));
}

function updateOccupationSelectionText(placeholder = t("selectOccupation")) {
  const selectedValue = elements.occupationInput.value;
  const selectedOccupation = state.occupations.find((occupation) => occupation.value === selectedValue);
  const label = selectedOccupation
    ? formatOccupationLabel(selectedOccupation, selectedOccupation.label || selectedOccupation.value)
    : placeholder;

  elements.occupationSelectionText.textContent = label;
  elements.occupationTrigger.title = label;
}

function renderOccupationOptions() {
  if (!elements.occupationMenu) {
    return;
  }

  elements.occupationMenu.innerHTML = "";

  if (!state.occupations.length) {
    const empty = document.createElement("div");
    empty.className = "single-select-empty";
    empty.textContent = elements.occupationSelectionText.textContent || t("noOccupationRestriction");
    elements.occupationMenu.appendChild(empty);
    return;
  }

  const query = normalizeDisplayText(elements.occupationSearchInput.value);
  const filteredOccupations = state.occupations.filter((occupation) => {
    if (!query) {
      return true;
    }

    const searchable = normalizeDisplayText([
      occupation.label,
      occupation.value,
      occupation.occupation_name_ar,
      occupation.occupation_name_en,
    ].join(" "));
    return searchable.includes(query);
  });

  if (!filteredOccupations.length) {
    const empty = document.createElement("div");
    empty.className = "single-select-empty";
    empty.textContent = t("noOccupationMatches");
    elements.occupationMenu.appendChild(empty);
    return;
  }

  filteredOccupations.forEach((occupation) => {
    const option = document.createElement("button");
    option.type = "button";
    option.className = "single-select-option";
    option.dataset.value = occupation.value;
    option.setAttribute("role", "option");
    option.setAttribute("aria-selected", String(occupation.value === elements.occupationInput.value));

    const parts = getOccupationDisplayParts(occupation);
    const primary = document.createElement("span");
    primary.className = "single-select-option-primary";
    primary.textContent = parts.primary;
    option.appendChild(primary);

    if (parts.secondary) {
      const secondary = document.createElement("span");
      secondary.className = "single-select-option-secondary";
      secondary.textContent = parts.secondary;
      option.appendChild(secondary);
    }

    elements.occupationMenu.appendChild(option);
  });
}

function getOccupationDisplayParts(occupation) {
  const nameAr = occupation.occupation_name_ar || "";
  const nameEn = occupation.occupation_name_en || "";
  const fallback = occupation.label || occupation.value || t("occupationLabel");

  if (state.language === "ar") {
    return {
      primary: nameAr || (containsArabic(fallback) ? fallback : "") || t("occupationNameMissing"),
      secondary: "",
    };
  }

  return {
    primary: nameEn || (!containsArabic(fallback) ? fallback : "") || t("occupationNameMissing"),
    secondary: "",
  };
}

async function loadRelationshipsForSelectedVisa() {
  const ocrCode = elements.countrySelect.value;
  const visaType = elements.visaTypeSelect.value;

  if (!ocrCode || !visaType) {
    resetRelationshipOptions();
    return;
  }

  state.isRelationshipsLoading = true;
  syncDirectCheckButtonState();
  resetRelationshipOptions(t("loadingRelationships"));
  setEligibilityStatus(t("loadingVisaRules"));

  try {
    const data = await apiRequest(
      withVisaDataRefresh(`/api/relationships/${encodeURIComponent(ocrCode)}/${encodeURIComponent(visaType)}`)
    );

    if (ocrCode !== elements.countrySelect.value || visaType !== elements.visaTypeSelect.value) {
      return;
    }

    state.relationships = normalizeRelationships(data);
    populateRelationships();
    if (!state.isOccupationsLoading) {
      setEligibilityStatus("");
    }
  } catch (error) {
    if (ocrCode === elements.countrySelect.value && visaType === elements.visaTypeSelect.value) {
      state.relationships = [];
      resetRelationshipOptions(t("couldNotLoadRelationships"));
      setEligibilityStatus(error.message, "error");
    }
  } finally {
    if (ocrCode === elements.countrySelect.value && visaType === elements.visaTypeSelect.value) {
      state.isRelationshipsLoading = false;
      syncRelationshipSelectState();
      syncDirectCheckButtonState();
    }
  }
}

function resetRelationshipOptions(label = t("selectRelationships")) {
  state.selectedRelationships = [];
  elements.relationshipSearchInput.value = "";
  elements.relationshipMenu.innerHTML = "";
  updateRelationshipSelectionText(label);
  renderRelationshipOptions(label);
  closeRelationshipMenu();
  syncRelationshipSelectState();
}

function populateRelationships() {
  elements.relationshipSearchInput.value = "";
  state.selectedRelationships = [];

  if (!state.relationships.length) {
    updateRelationshipSelectionText(t("noRelationshipRestriction"));
    renderRelationshipOptions(t("noRelationshipRestriction"));
    closeRelationshipMenu();
    syncRelationshipSelectState();
    return;
  }

  renderRelationshipOptions();
  updateRelationshipSelectionText();
  syncRelationshipSelectState();
}

function renderRelationshipOptions(emptyText = "") {
  elements.relationshipMenu.innerHTML = "";

  if (!state.relationships.length) {
    const empty = document.createElement("div");
    empty.className = "single-select-empty";
    empty.textContent = emptyText || elements.relationshipSelectionText.textContent || t("noRelationshipRestriction");
    elements.relationshipMenu.appendChild(empty);
    return;
  }

  const query = normalizeDisplayText(elements.relationshipSearchInput.value);
  const filteredRelationships = state.relationships.filter((relationship) => {
    if (!query) {
      return true;
    }

    return normalizeDisplayText([
      formatRelationshipLabel(relationship),
      relationship.value,
      relationship.relation_name_ar,
      relationship.relation_name_en,
    ].join(" ")).includes(query);
  });

  if (!filteredRelationships.length) {
    const empty = document.createElement("div");
    empty.className = "single-select-empty";
    empty.textContent = t("noRelationshipMatches");
    elements.relationshipMenu.appendChild(empty);
    return;
  }

  filteredRelationships.forEach((relationship) => {
    const option = document.createElement("label");
    const isSelected = state.selectedRelationships.includes(relationship.value);
    option.className = "multi-select-option";
    option.setAttribute("role", "option");
    option.setAttribute("aria-selected", String(isSelected));

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = relationship.value;
    checkbox.checked = isSelected;
    checkbox.addEventListener("change", handleRelationshipSelectionChange);

    const text = document.createElement("span");
    text.textContent = formatRelationshipLabel(relationship);

    option.append(checkbox, text);
    elements.relationshipMenu.appendChild(option);
  });
}

function handleRelationshipSelectionChange(event) {
  const { value, checked } = event.currentTarget;
  const nextSelection = new Set(state.selectedRelationships);

  if (checked) {
    nextSelection.add(value);
  } else {
    nextSelection.delete(value);
  }

  state.selectedRelationships = Array.from(nextSelection);

  updateRelationshipSelectionText();
  renderRelationshipOptions();
  syncEligibilitySnapshot();
}

function toggleRelationshipMenu(event) {
  event.stopPropagation();

  if (elements.relationshipInput.disabled || !state.relationships.length) {
    return;
  }

  closeAllSearchableSelects();
  closeOccupationMenu();
  const isOpen = elements.relationshipMultiSelect.classList.toggle("is-open");
  elements.relationshipInput.setAttribute("aria-expanded", String(isOpen));
  setActiveSelectLayer(elements.relationshipMultiSelect, isOpen);
  setModalSelectOpen(isOpen);

  if (isOpen) {
    elements.relationshipSearchInput.value = "";
    renderRelationshipOptions();
    window.setTimeout(() => elements.relationshipSearchInput.focus(), 0);
  }
}

function closeRelationshipMenu() {
  elements.relationshipMultiSelect.classList.remove("is-open");
  elements.relationshipInput.setAttribute("aria-expanded", "false");
  setActiveSelectLayer(elements.relationshipMultiSelect, false);
  setModalSelectOpen(false);
}

function updateRelationshipSelectionText(placeholder = t("selectRelationships")) {
  if (!state.selectedRelationships.length) {
    elements.relationshipSelectionText.textContent = placeholder;
    elements.relationshipInput.title = placeholder;
    return;
  }

  const labels = getSelectedRelationshipLabels();

  elements.relationshipSelectionText.textContent = labels.join(", ");
  elements.relationshipInput.title = labels.join(", ");
}

function syncRelationshipSelectState() {
  elements.relationshipInput.disabled =
    state.isEligibilityLoading ||
    state.isRelationshipsLoading ||
    !elements.visaTypeSelect.value ||
    !state.relationships.length;
  elements.relationshipSearchInput.disabled = elements.relationshipInput.disabled;
  elements.relationshipMultiSelect.classList.toggle("is-disabled", elements.relationshipInput.disabled);

  if (elements.relationshipInput.disabled) {
    closeRelationshipMenu();
  }
}

function handleRelationshipSearchKeyDown(event) {
  if (event.key === "Escape") {
    event.preventDefault();
    event.stopPropagation();
    closeRelationshipMenu();
    elements.relationshipInput.focus();
  }
}

function syncDirectCheckButtonState() {
  elements.checkEligibilityButton.disabled =
    state.isOccupationsLoading ||
    state.isRelationshipsLoading;
}

async function handleEligibilitySubmit(event) {
  event.preventDefault();

  const ocrCode = elements.countrySelect.value;
  const visaType = elements.visaTypeSelect.value;

  if (!ocrCode || !visaType) {
    return;
  }

  setEligibilityLoading(true, t("checkingEligibility"));
  elements.eligibilityResult.innerHTML = "";

  try {
    const data = await apiRequest("/api/form-check", {
      method: "POST",
      body: JSON.stringify({
        ocr_code: ocrCode,
        visa_type: Number(visaType),
        age: parseOptionalInteger(elements.ageInput.value),
        occupation: optionalText(elements.occupationInput.value),
        gender: optionalText(elements.genderSelect.value),
        relationship: optionalList(state.selectedRelationships),
        fresh_master_data: state.visaDataRefreshToken,
      }),
    });

    renderEligibilityResult(data);
    state.hasEligibilityResult = true;
    syncEligibilityExperience("result");
    setEligibilityStatus("");
  } catch (error) {
    setEligibilityStatus(error.message, "error");
  } finally {
    setEligibilityLoading(false);
  }
}

function setEligibilityLoading(isLoading, status = "") {
  state.isEligibilityLoading = isLoading;
  elements.checkEligibilityButton.disabled = isLoading || state.isOccupationsLoading || state.isRelationshipsLoading;
  elements.countrySelect.disabled = isLoading;
  elements.visaTypeSelect.disabled = isLoading;
  elements.ageInput.disabled = isLoading;
  setOccupationSelectDisabled(
    isLoading ||
      state.isOccupationsLoading ||
      !elements.visaTypeSelect.value ||
      !state.occupations.length
  );
  elements.genderSelect.disabled = isLoading;
  elements.relationshipInput.disabled = isLoading || state.isRelationshipsLoading || !state.relationships.length;
  elements.relationshipSearchInput.disabled = elements.relationshipInput.disabled;
  syncAllSearchableSelects();
  syncRelationshipSelectState();
  setEligibilityStatus(status);
}

function setEligibilityStatus(message, type) {
  setStatus(elements.eligibilityStatus, message, type);
}

function setStatus(element, message, type) {
  element.textContent = message || "";
  element.classList.toggle("is-error", type === "error");
  element.classList.toggle("is-success", type === "success");
}

function renderEligibilityResult(data) {
  elements.eligibilityResult.innerHTML = "";

  const visaTypes = normalizeVisaTypes(data);
  const status = data?.status || "NEED_MORE_INFO";
  const statusTone = getStatusTone(status);
  const card = document.createElement("section");
  card.className = `result-card result-card-${statusTone}`;

  if (isVisaTypesOnlyResponse(data, visaTypes)) {
    renderVisaTypesOnlyResult(card, visaTypes);
    elements.eligibilityResult.appendChild(card);
    return;
  }

  const checks = normalizeChecks(data?.checks);
  const passedChecks = checks.filter((check) => check.passed === true);
  const failedChecks = checks.filter((check) => check.passed === false);
  const missingFields = normalizeList(data?.missing_fields);
  const selectedVisa = getSelectedVisaType();

  card.appendChild(createResultHeader(t("eligibilityResult"), formatStatus(status), statusTone));

  const summary = document.createElement("div");
  summary.className = "result-summary";

  summary.appendChild(createSummaryItem(t("status"), formatStatus(status), getStatusBadgeClass(status)));
  summary.appendChild(createSummaryItem(t("visaNumber"), data?.visa_type || selectedVisa?.visa_type || t("notProvided")));
  summary.appendChild(createSummaryItem(t("visaName"), formatVisaTypeName({ ...selectedVisa, ...data }) || t("notProvided")));
  summary.appendChild(createSummaryItem(t("applicantCountry"), formatCountryLabel(state.selectedCountry) || t("notProvided")));

  card.appendChild(summary);

  const genderNote = formatGenderPolicyNote(data);
  if (genderNote) {
    const note = document.createElement("p");
    note.className = "empty-note result-note";
    note.textContent = genderNote;
    card.appendChild(note);
  }

  renderCheckSection(card, t("passedChecks"), passedChecks, "pass", t("noPassedChecks"));
  renderCheckSection(card, t("failedChecks"), failedChecks, "fail", data?.reason || t("noFailedChecks"));
  renderMissingFields(card, missingFields);

  // Add Start Over button
  const actions = document.createElement("div");
  actions.className = "result-actions";
  const resetBtn = document.createElement("button");
  resetBtn.className = "result-reset-button";
  resetBtn.type = "button";
  resetBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v6h6"/></svg><span>' + t("startOver") + '</span>';
  resetBtn.addEventListener("click", function() {
    elements.countrySelect.value = "";
    syncSearchableSelect("country");
    handleCountryChange();
    syncEligibilityExperience("country");
  });
  actions.appendChild(resetBtn);
  card.appendChild(actions);

  elements.eligibilityResult.appendChild(card);
}

function renderVisaTypesOnlyResult(card, visaTypes) {
  card.classList.add("result-card-info");
  card.appendChild(createResultHeader(t("availableVisaTypesTitle"), t("information"), "info"));

  if (!visaTypes.length) {
    const note = document.createElement("p");
    note.className = "empty-note";
    note.textContent = t("noVisaTypesReturned");
    card.appendChild(note);
    return;
  }

  const list = document.createElement("ul");
  list.className = "visa-list";

  visaTypes.forEach((visaType) => {
    const item = document.createElement("li");
    const mark = document.createElement("span");
    mark.className = "mark mark-info";
    mark.textContent = "i";
    const text = document.createElement("span");
    text.textContent = formatVisaTypeLabel(visaType);
    item.append(mark, text);
    list.appendChild(item);
  });

  card.appendChild(list);

  // Add Start Over button
  const actions = document.createElement("div");
  actions.className = "result-actions";
  const resetBtn = document.createElement("button");
  resetBtn.className = "result-reset-button";
  resetBtn.type = "button";
  resetBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v6h6"/></svg><span>' + t("startOver") + '</span>';
  resetBtn.addEventListener("click", function() {
    elements.countrySelect.value = "";
    syncSearchableSelect("country");
    handleCountryChange();
    syncEligibilityExperience("country");
  });
  actions.appendChild(resetBtn);
  card.appendChild(actions);
}

function createResultHeader(title, subtitle, tone) {
  const header = document.createElement("div");
  header.className = "result-card-header";

  const icon = document.createElement("span");
  icon.className = `result-status-icon result-status-${tone}`;
  icon.textContent = getResultToneIcon(tone);

  const copy = document.createElement("span");
  copy.className = "result-card-title";

  const heading = document.createElement("h3");
  heading.textContent = title;

  const description = document.createElement("p");
  description.textContent = subtitle;

  copy.append(heading, description);
  header.append(icon, copy);
  return header;
}

function renderCheckSection(card, title, checks, markType, emptyText) {
  const section = document.createElement("div");
  section.className = "check-section";

  const heading = document.createElement("h4");
  heading.textContent = title;
  section.appendChild(heading);

  if (!checks.length) {
    const note = document.createElement("p");
    note.className = "empty-note";
    note.textContent = emptyText;
    section.appendChild(note);
    card.appendChild(section);
    return;
  }

  const list = document.createElement("ul");
  list.className = "check-list";

  checks.forEach((check) => {
    const item = document.createElement("li");
    const mark = document.createElement("span");
    mark.className = `mark ${markType === "pass" ? "mark-pass" : "mark-fail"}`;
    mark.textContent = markType === "pass" ? "\u2713" : "\u2715";
    const text = document.createElement("span");
    text.textContent = formatCheckMessage(check, markType);
    item.append(mark, text);
    list.appendChild(item);
  });

  section.appendChild(list);
  card.appendChild(section);
}

function renderMissingFields(card, missingFields) {
  const section = document.createElement("div");
  section.className = "check-section";

  const heading = document.createElement("h4");
  heading.textContent = t("missingFields");
  section.appendChild(heading);

  if (!missingFields.length) {
    const note = document.createElement("p");
    note.className = "empty-note";
    note.textContent = t("noMissingFields");
    section.appendChild(note);
    card.appendChild(section);
    return;
  }

  const list = document.createElement("ul");
  list.className = "check-list";

  missingFields.forEach((field) => {
    const item = document.createElement("li");
    const mark = document.createElement("span");
    mark.className = "mark mark-info";
    mark.textContent = "i";
    const text = document.createElement("span");
    text.textContent = formatFieldName(field);
    item.append(mark, text);
    list.appendChild(item);
  });

  section.appendChild(list);
  card.appendChild(section);
}

function createSummaryItem(label, value, badgeClass = "") {
  const item = document.createElement("div");
  item.className = "summary-item";

  const labelElement = document.createElement("span");
  labelElement.className = "summary-label";
  labelElement.textContent = label;

  const valueElement = document.createElement("span");
  valueElement.className = badgeClass ? `summary-value status-badge ${badgeClass}` : "summary-value";
  valueElement.textContent = value;

  item.append(labelElement, valueElement);
  return item;
}

function formatCheckMessage(check, markType) {
  const field = formatFieldName(check?.field);
  const result = markType === "pass" ? t("checkPassed") : t("checkFailed");

  if (state.language === "ar") {
    return `${field}: ${result}`;
  }

  const message = check?.message || "";
  return message && !containsArabic(message) ? message : `${field}: ${result}`;
}

function normalizeVisaTypes(data) {
  const items =
    data?.visa_types ||
    data?.available_visa_types ||
    data?.data ||
    (Array.isArray(data) ? data : []);

  if (!Array.isArray(items)) {
    return [];
  }

  return items
    .map((item) => {
      if (typeof item === "number" || typeof item === "string") {
        const numericType = Number(item);
        return {
          visa_type: item,
          visa_name: item === 16 || item === "16" ? "\u0633\u0645\u0629 \u062f\u062e\u0648\u0644 \u0644\u0644\u0633\u064a\u0627\u062d\u0629" : "",
          visa_name_en: VISA_TYPE_NAMES_EN[numericType] || "",
        };
      }

      const visaType = item.visa_type ?? item.visaType ?? item.id ?? item.number ?? "";
      return {
        visa_type: visaType,
        visa_name: item.visa_name || item.typeOfVisa || item.name_ar || item.description_ar || item.description || "",
        visa_name_en: item.visa_name_en || item.visaNameEn || item.name_en || item.description_en || VISA_TYPE_NAMES_EN[Number(visaType)] || "",
      };
    })
    .filter((item) => item.visa_type !== "");
}

function normalizeChecks(checks) {
  return Array.isArray(checks) ? checks : [];
}

function normalizeList(value) {
  if (!value) {
    return [];
  }
  return Array.isArray(value) ? value : [value];
}

function normalizeOccupations(data) {
  const items =
    data?.occupations ||
    data?.data ||
    (Array.isArray(data) ? data : []);

  if (!Array.isArray(items)) {
    return [];
  }

  const seen = new Set();
  const occupations = [];

  items.forEach((item) => {
    const occupation = normalizeOccupation(item);
    if (!occupation.value) {
      return;
    }

    const key = occupation.value.trim().toLowerCase();
    if (seen.has(key)) {
      return;
    }

    seen.add(key);
    occupations.push(occupation);
  });

  return occupations;
}

function normalizeOccupation(item) {
  if (typeof item === "string") {
    return { value: item, label: item, occupation_name_ar: "", occupation_name_en: item };
  }

  if (!item || typeof item !== "object") {
    return { value: "", label: "", occupation_name_ar: "", occupation_name_en: "" };
  }

  const nameAr =
    item.occupation_name_ar ||
    item.occupationNameAr ||
    item.ArabicDescription ||
    "";
  const nameEn =
    item.occupation_name_en ||
    item.occupationNameEn ||
    item.DescriptionEn ||
    item.EnglishDescription ||
    "";

  const value =
    item.value ||
    nameAr ||
    nameEn ||
    item.label ||
    "";

  return {
    value,
    label: formatOccupationLabel({ ...item, occupation_name_ar: nameAr, occupation_name_en: nameEn }, item.label || value),
    occupation_name_ar: nameAr,
    occupation_name_en: nameEn,
  };
}

function formatOccupationLabel(occupation, fallback = "") {
  const nameAr =
    occupation.occupation_name_ar ||
    occupation.occupationNameAr ||
    occupation.ArabicDescription ||
    "";
  const nameEn =
    occupation.occupation_name_en ||
    occupation.occupationNameEn ||
    occupation.DescriptionEn ||
    occupation.EnglishDescription ||
    "";

  if (state.language === "ar") {
    return nameAr || (containsArabic(fallback) ? fallback : "") || t("occupationNameMissing");
  }

  return nameEn || (!containsArabic(fallback) ? fallback : "") || t("occupationNameMissing");
}

function normalizeDisplayText(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/[أإآ]/g, "ا")
    .replace(/ى/g, "ي")
    .replace(/ة/g, "ه")
    .replace(/[^\w\s\u0600-\u06ff]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function containsArabic(value) {
  return /[\u0600-\u06ff]/.test(String(value || ""));
}

function normalizeArabicRelationshipKey(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/[\u064b-\u065f\u0670]/g, "")
    .replace(/[\u200b-\u200f]/g, "")
    .replace(/ـ/g, "")
    .replace(/[أإآ]/g, "ا")
    .replace(/ى/g, "ي")
    .replace(/ؤ/g, "و")
    .replace(/ئ/g, "ي")
    .replace(/ة/g, "ه")
    .replace(/[()]/g, " ")
    .replace(/[^\w\s\u0600-\u06ff]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function stripArabicArticle(value) {
  return String(value || "").replace(/^ال/, "");
}

function getExactRelationshipTranslationEn(value) {
  const normalizedValue = normalizeArabicRelationshipKey(value);
  if (!normalizedValue) {
    return "";
  }

  return Object.entries(RELATIONSHIP_EXACT_TRANSLATIONS_EN).find(([arabicName]) => (
    normalizeArabicRelationshipKey(arabicName) === normalizedValue
  ))?.[1] || "";
}

function getRelationshipCode(relationship) {
  return String(
    relationship?.relation_code ||
    relationship?.relationCode ||
    relationship?.code ||
    ""
  ).trim();
}

function relationshipWordTranslationEn(value) {
  const normalized = stripArabicArticle(normalizeArabicRelationshipKey(value));
  return RELATIONSHIP_WORD_TRANSLATIONS_EN[normalized] || "";
}

function formatGeneratedRelationshipLabel(value) {
  const label = String(value || "").replace(/\s+/g, " ").trim();
  if (!label || containsArabic(label)) {
    return "";
  }

  return label.charAt(0).toUpperCase() + label.slice(1);
}

function translateArabicRelationshipNounPhrase(value, depth = 0) {
  if (depth > 8) {
    return "";
  }

  const text = normalizeArabicRelationshipKey(value);
  if (!text) {
    return "";
  }

  const exact = getExactRelationshipTranslationEn(text);
  if (exact) {
    return exact.toLowerCase();
  }

  const directWord = relationshipWordTranslationEn(text);
  if (directWord) {
    return directWord;
  }

  const generated = translateArabicRelationshipPhraseEn(text, depth + 1);
  if (generated) {
    return generated.toLowerCase();
  }

  const translatedWords = text
    .split(/\s+/)
    .map((word) => relationshipWordTranslationEn(word))
    .filter(Boolean);

  return translatedWords.join(" ");
}

function translateArabicRelationshipPhraseEn(value, depth = 0) {
  if (depth > 8) {
    return "";
  }

  const text = normalizeArabicRelationshipKey(value);
  if (!text) {
    return "";
  }

  const exact = getExactRelationshipTranslationEn(text);
  if (exact) {
    return exact;
  }

  const normalizedPrefixes = [
    ["والده", "mother of"],
    ["والد", "father of"],
    ["زوجه", "wife of"],
    ["زوج", "husband of"],
    ["ابنه", "daughter of"],
    ["بنت", "daughter of"],
    ["ابن", "son of"],
    ["اخت", "sister of"],
    ["اخ", "brother of"],
    ["شقيق", "brother of"],
    ["ام", "mother of"],
    ["اب", "father of"],
    ["حفيدت", "granddaughter of"],
    ["حفيده", "granddaughter of"],
    ["حفيد", "grandson of"],
  ];

  for (const [prefix, englishPrefix] of normalizedPrefixes) {
    if (text === prefix || text === `ال${prefix}`) {
      return formatGeneratedRelationshipLabel(relationshipWordTranslationEn(text) || englishPrefix.replace(/ of$/, ""));
    }

    const withoutArticle = stripArabicArticle(text);
    const matchText = withoutArticle.startsWith(prefix) ? withoutArticle : "";
    if (!matchText || matchText.length <= prefix.length) {
      continue;
    }

    const rest = matchText.slice(prefix.length).trim();
    if (!rest) {
      continue;
    }

    const translatedRest = translateArabicRelationshipNounPhrase(rest, depth + 1) || "relative";
    return formatGeneratedRelationshipLabel(`${englishPrefix} ${translatedRest}`);
  }

  const translated = relationshipWordTranslationEn(text);
  if (translated) {
    return formatGeneratedRelationshipLabel(translated);
  }

  return "";
}

function translateRelationshipNameToEnglish(nameAr, relationship = {}) {
  if (!nameAr || !containsArabic(nameAr)) {
    return "";
  }

  const exact = getExactRelationshipTranslationEn(nameAr);
  if (exact) {
    return exact;
  }

  const generated = translateArabicRelationshipPhraseEn(nameAr);
  if (generated) {
    return generated;
  }

  const code = getRelationshipCode(relationship);
  return code ? `Relationship code ${code}` : "Family relationship";
}

function normalizeRelationships(data) {
  const items =
    data?.relationships ||
    data?.data ||
    (Array.isArray(data) ? data : []);

  if (!Array.isArray(items)) {
    return [];
  }

  const seen = new Set();
  const relationships = [];

  items.forEach((item) => {
    const relationship = normalizeRelationship(item);
    if (!relationship.value) {
      return;
    }

    const key = relationship.value.trim().toLowerCase();
    if (seen.has(key)) {
      return;
    }

    seen.add(key);
    relationships.push(relationship);
  });

  return relationships;
}

function normalizeRelationship(item) {
  if (typeof item === "string") {
    const translatedName = containsArabic(item) ? translateRelationshipNameToEnglish(item) : item;
    return {
      value: item,
      label: state.language === "ar" ? item : translatedName,
      relation_name_ar: containsArabic(item) ? item : "",
      relation_name_en: translatedName,
      relation_code: "",
    };
  }

  if (!item || typeof item !== "object") {
    return { value: "", label: "" };
  }

  const relationCode = getRelationshipCode(item);
  const relationNameAr = nameArFromRelationship(item);
  const relationNameEn = nameEnFromRelationship({
    ...item,
    relation_code: relationCode,
    relation_name_ar: relationNameAr,
  });
  const value =
    item.value ||
    relationNameAr ||
    relationNameEn ||
    item.label ||
    "";

  return {
    value,
    label: formatRelationshipLabel({
      ...item,
      relation_code: relationCode,
      relation_name_ar: relationNameAr,
      relation_name_en: relationNameEn,
    }, value),
    relation_code: relationCode,
    relation_name_ar: relationNameAr,
    relation_name_en: relationNameEn,
  };
}

function formatRelationshipLabel(relationship, fallback = "") {
  const nameAr = nameArFromRelationship(relationship);
  const nameEn = nameEnFromRelationship(relationship);

  if (state.language === "ar") {
    return nameAr || (containsArabic(fallback) ? fallback : "") || t("relationshipNameMissing");
  }

  return nameEn || (!containsArabic(fallback) ? fallback : "") || t("relationshipNameMissing");
}

function nameArFromRelationship(relationship) {
  return relationship?.relation_name_ar ||
    relationship?.relationNameAr ||
    relationship?.arabicDescription ||
    relationship?.ArabicDescription ||
    "";
}

function nameEnFromRelationship(relationship) {
  const directName =
    relationship?.relation_name_en ||
    relationship?.relationNameEn ||
    relationship?.DescriptionEn ||
    "";

  if (directName && normalizeDisplayText(directName) !== normalizeDisplayText(translations.en.relationshipNameMissing)) {
    return directName;
  }

  return translateRelationshipNameToEnglish(nameArFromRelationship(relationship), relationship);
}

function isVisaTypesOnlyResponse(data, visaTypes) {
  if (!visaTypes.length) {
    return false;
  }

  return data?.mode === "visa_types" || data?.status === "INFO" || !data?.checks;
}

function getSelectedVisaType() {
  const selectedValue = elements.visaTypeSelect.value;
  return state.visaTypes.find((visaType) => String(visaType.visa_type) === selectedValue) || null;
}

function formatVisaTypeLabel(visaType) {
  const number = visaType?.visa_type || visaType?.visaType || "";
  const name = formatVisaTypeName(visaType);
  const prefix = t("visaNo");

  if (number && name) {
    return `${prefix} ${number} - ${name}`;
  }

  if (number) {
    return `${prefix} ${number}`;
  }

  return name || t("visaTypeMissing");
}

function formatVisaTypeLabelForLanguage(visaType, language) {
  const normalized = normalizeActionLanguage(language);
  const number = visaType?.visa_type || visaType?.visaType || "";
  const name = formatVisaTypeNameForLanguage(visaType, normalized);
  const prefix = tForLanguage("visaNo", normalized);

  if (number && name) {
    return `${prefix} ${number} - ${name}`;
  }

  if (number) {
    return `${prefix} ${number}`;
  }

  return name || tForLanguage("visaTypeMissing", normalized);
}

function formatVisaTypeName(visaType) {
  return formatVisaTypeNameForLanguage(visaType, state.language);
}

function formatVisaTypeNameForLanguage(visaType, language) {
  if (!visaType) {
    return "";
  }

  const normalized = normalizeActionLanguage(language);
  const number = Number(visaType.visa_type || visaType.visaType || "");
  const arabicName =
    visaType.visa_name ||
    visaType.typeOfVisa ||
    visaType.name_ar ||
    visaType.description_ar ||
    "";
  const englishName =
    visaType.visa_name_en ||
    visaType.visaNameEn ||
    visaType.name_en ||
    visaType.description_en ||
    VISA_TYPE_NAMES_EN[number] ||
    "";

  if (normalized === "ar") {
    return arabicName && containsArabic(arabicName) ? arabicName : tForLanguage("visaNameMissing", normalized);
  }

  return englishName && !containsArabic(englishName) ? englishName : tForLanguage("visaNameMissing", normalized);
}

function formatCountryLabel(country) {
  if (!country) {
    return "";
  }

  const name = formatCountryName(country);
  if (state.language === "ar") {
    return name;
  }

  return country.ocr_code ? `${name} (${country.ocr_code})` : name;
}

function formatCountryName(country) {
  if (!country) {
    return "";
  }

  if (state.language === "ar") {
    return country.country_name_ar || country.ocr_code;
  }

  const englishName = country.country_name_en || country.name || "";
  return englishName && !containsArabic(englishName) ? englishName : country.ocr_code;
}

function formatStatus(status) {
  const normalized = String(status || "").toUpperCase();

  if (normalized === "APPROVED") {
    return t("approved");
  }

  if (normalized === "NOT_APPROVED") {
    return t("notApproved");
  }

  if (normalized === "NEED_MORE_INFO") {
    return t("needMoreInfo");
  }

  if (normalized === "INFO") {
    return t("information");
  }

  return t("needMoreInfo");
}

function getStatusBadgeClass(status) {
  const normalized = String(status || "").toUpperCase();

  if (normalized === "APPROVED") {
    return "status-approved";
  }

  if (normalized === "NOT_APPROVED") {
    return "status-not-approved";
  }

  return "status-more-info";
}

function getStatusTone(status) {
  const normalized = String(status || "").toUpperCase();

  if (normalized === "APPROVED") {
    return "approved";
  }

  if (normalized === "NOT_APPROVED") {
    return "denied";
  }

  return "info";
}

function getResultToneIcon(tone) {
  if (tone === "approved") {
    return "\u2713";
  }

  if (tone === "denied") {
    return "!";
  }

  return "i";
}

function formatGenderPolicyNote(data) {
  const policy = data?.details?.gender_policy || {};
  const allowed = new Set(normalizeList(policy.allowed));
  const restricted = new Set(normalizeList(policy.restricted));

  if (allowed.has("male") && restricted.has("female")) {
    return t("genderMaleOnlyNote");
  }

  if (allowed.has("female") && restricted.has("male")) {
    return t("genderFemaleOnlyNote");
  }

  return "";
}

function formatFieldName(field) {
  const fieldNames = {
    en: {
      country: "Country / Nationality",
      visa_type: "Visa Type",
      age: "Age",
      occupation: "Occupation",
      gender: "Gender",
      relationship: "Relationship / Companion",
      valid_age: "Valid Age",
    },
    ar: {
      country: "الدولة / الجنسية",
      visa_type: "نوع التأشيرة",
      age: "العمر",
      occupation: "المهنة",
      gender: "الجنس",
      relationship: "صلة القرابة / المرافق",
      valid_age: "العمر الصحيح",
    },
  };

  if (fieldNames[state.language]?.[field]) {
    return fieldNames[state.language][field];
  }

  return String(field || "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function parseOptionalInteger(value) {
  const cleaned = String(value || "").trim();
  return cleaned ? Number.parseInt(cleaned, 10) : null;
}

function optionalText(value) {
  const cleaned = String(value || "").trim();
  return cleaned || null;
}

function optionalList(values) {
  return Array.isArray(values) && values.length ? values : null;
}

function createOption(value, label) {
  const option = document.createElement("option");
  option.value = value;
  option.textContent = label;
  return option;
}
