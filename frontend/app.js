const SESSION_KEY = "kuwaitVisaSmartAssistant.sessionId";
const LANGUAGE_KEY = "kuwaitVisaSmartAssistant.language";
const API_BASE = "";
const DEFAULT_LANGUAGE = "en";

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
    startEligibility: "Start Eligibility Check",
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
    closeModal: "Close modal",
    countryLabel: "Applicant Country / Nationality",
    visaTypeLabel: "Visa Type",
    ageLabel: "Age",
    agePlaceholder: "Applicant age",
    occupationLabel: "Occupation",
    genderLabel: "Gender",
    relationshipLabel: "Relationship / Companion",
    checkEligibility: "Check Eligibility",
    cancel: "Cancel",
    selectCountry: "Select applicant country",
    selectVisaType: "Select a visa type",
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
    status: "Status",
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
    approved: "Approved",
    notApproved: "Not Approved",
    needMoreInfo: "Need More Information",
    information: "Information",
    visaNo: "Visa No.",
    visaTypeMissing: "Visa type not provided",
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
    startEligibility: "ابدأ فحص الأهلية",
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
    closeModal: "إغلاق النافذة",
    countryLabel: "دولة / جنسية مقدم الطلب",
    visaTypeLabel: "نوع التأشيرة",
    ageLabel: "العمر",
    agePlaceholder: "عمر مقدم الطلب",
    occupationLabel: "المهنة",
    genderLabel: "الجنس",
    relationshipLabel: "صلة القرابة / المرافق",
    checkEligibility: "فحص الأهلية",
    cancel: "إلغاء",
    selectCountry: "اختر دولة مقدم الطلب",
    selectVisaType: "اختر نوع التأشيرة",
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
    status: "الحالة",
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
    approved: "مطابق",
    notApproved: "غير مطابق",
    needMoreInfo: "تحتاج معلومات إضافية",
    information: "معلومات",
    visaNo: "تأشيرة رقم",
    visaTypeMissing: "نوع التأشيرة غير متوفر",
    genderMaleOnlyNote: "ملاحظة: هذه التأشيرة متاحة للذكور فقط حسب قيود الجنس الظاهرة في البيانات.",
    genderFemaleOnlyNote: "ملاحظة: هذه التأشيرة متاحة للإناث فقط حسب قيود الجنس الظاهرة في البيانات.",
    userAvatar: "أنت",
  },
};

const state = {
  sessionId: getOrCreateSessionId(),
  language: getStoredLanguage(),
  countries: [],
  visaTypes: [],
  occupations: [],
  relationships: [],
  selectedRelationships: [],
  selectedCountry: null,
  isCountriesLoaded: false,
  isOccupationsLoading: false,
  isRelationshipsLoading: false,
  isVoiceRecording: false,
  isVoiceProcessing: false,
  mediaRecorder: null,
  voiceStream: null,
  voiceChunks: [],
  voiceRecordingTimer: null,
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
  openEligibilityButton: document.getElementById("openEligibilityButton"),
  eligibilityModal: document.getElementById("eligibilityModal"),
  closeEligibilityButton: document.getElementById("closeEligibilityButton"),
  cancelEligibilityButton: document.getElementById("cancelEligibilityButton"),
  eligibilityForm: document.getElementById("eligibilityForm"),
  countrySelect: document.getElementById("countrySelect"),
  visaTypeGroup: document.getElementById("visaTypeGroup"),
  visaTypeSelect: document.getElementById("visaTypeSelect"),
  ageInput: document.getElementById("ageInput"),
  occupationInput: document.getElementById("occupationInput"),
  occupationSingleSelect: document.getElementById("occupationSingleSelect"),
  occupationTrigger: document.getElementById("occupationTrigger"),
  occupationSelectionText: document.getElementById("occupationSelectionText"),
  occupationSearchInput: document.getElementById("occupationSearchInput"),
  occupationMenu: document.getElementById("occupationMenu"),
  genderSelect: document.getElementById("genderSelect"),
  relationshipMultiSelect: document.getElementById("relationshipMultiSelect"),
  relationshipInput: document.getElementById("relationshipInput"),
  relationshipSelectionText: document.getElementById("relationshipSelectionText"),
  relationshipMenu: document.getElementById("relationshipMenu"),
  checkEligibilityButton: document.getElementById("checkEligibilityButton"),
  eligibilityStatus: document.getElementById("eligibilityStatus"),
  eligibilityResult: document.getElementById("eligibilityResult"),
};

document.addEventListener("DOMContentLoaded", () => {
  bindEvents();
  applyLanguage(state.language);
  loadCountries();
});

function bindEvents() {
  elements.chatForm.addEventListener("submit", handleChatSubmit);
  elements.resetChatButton.addEventListener("click", handleResetConversation);
  elements.chatInput.addEventListener("input", autoSizeChatInput);
  elements.chatInput.addEventListener("keydown", handleChatInputKeyDown);
  elements.voiceInputButton.addEventListener("click", handleVoiceInputClick);
  elements.languageButton.addEventListener("click", toggleLanguageMenu);
  elements.languageOptions.forEach((button) => {
    button.addEventListener("click", handleLanguageSelection);
  });

  elements.openEligibilityButton.addEventListener("click", openEligibilityModal);
  elements.closeEligibilityButton.addEventListener("click", closeEligibilityModal);
  elements.cancelEligibilityButton.addEventListener("click", closeEligibilityModal);
  elements.eligibilityModal.addEventListener("click", handleBackdropClick);
  elements.countrySelect.addEventListener("change", handleCountryChange);
  elements.visaTypeSelect.addEventListener("change", handleVisaTypeChange);
  elements.occupationTrigger.addEventListener("click", toggleOccupationMenu);
  elements.occupationTrigger.addEventListener("keydown", handleOccupationTriggerKeyDown);
  elements.occupationSearchInput.addEventListener("input", renderOccupationOptions);
  elements.occupationSearchInput.addEventListener("keydown", handleOccupationSearchKeyDown);
  elements.occupationMenu.addEventListener("click", handleOccupationOptionClick);
  elements.relationshipInput.addEventListener("click", toggleRelationshipMenu);
  elements.eligibilityForm.addEventListener("submit", handleEligibilitySubmit);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && elements.eligibilityModal.classList.contains("is-open")) {
      closeOccupationMenu();
      closeRelationshipMenu();
      closeEligibilityModal();
    }

    if (event.key === "Escape") {
      closeLanguageMenu();
    }
  });

  document.addEventListener("click", (event) => {
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

function getOrCreateSessionId() {
  const existing = localStorage.getItem(SESSION_KEY);
  if (existing) {
    return existing;
  }

  const generated = crypto.randomUUID
    ? crypto.randomUUID()
    : `session-${Date.now()}-${Math.random().toString(16).slice(2)}`;

  localStorage.setItem(SESSION_KEY, generated);
  return generated;
}

function getStoredLanguage() {
  const stored = localStorage.getItem(LANGUAGE_KEY);
  return translations[stored] ? stored : DEFAULT_LANGUAGE;
}

function t(key) {
  return translations[state.language]?.[key] || translations[DEFAULT_LANGUAGE][key] || key;
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

  elements.languageLabel.textContent = isArabic ? "العربية" : "English";
  elements.languageOptions.forEach((option) => {
    option.setAttribute("aria-selected", String(option.dataset.language === nextLanguage));
  });

  syncGenderOptions();
  syncInitialGreeting();
  refreshLanguageDependentControls();
  closeLanguageMenu();
}

function syncGenderOptions() {
  const selected = elements.genderSelect.value;
  elements.genderSelect.innerHTML = "";
  elements.genderSelect.appendChild(createOption("", t("selectGender")));
  elements.genderSelect.appendChild(createOption("male", t("male")));
  elements.genderSelect.appendChild(createOption("female", t("female")));
  elements.genderSelect.value = selected;
}

function syncInitialGreeting() {
  const hasUserMessages = Boolean(elements.chatMessages.querySelector(".user-message"));
  if (!hasUserMessages) {
    elements.chatMessages.innerHTML = "";
    appendMessage("assistant", t("welcomeMessage"));
  }
}

function refreshLanguageDependentControls() {
  const selectedCountry = elements.countrySelect.value;
  const selectedVisaType = elements.visaTypeSelect.value;
  const selectedOccupation = elements.occupationInput.value;

  if (state.isCountriesLoaded) {
    populateCountries();
    elements.countrySelect.value = selectedCountry;
  }

  if (state.visaTypes.length) {
    populateVisaTypes();
    elements.visaTypeSelect.value = selectedVisaType;
  } else {
    elements.visaTypeSelect.innerHTML = "";
    elements.visaTypeSelect.appendChild(createOption("", t("selectVisaType")));
  }

  if (state.occupations.length) {
    populateOccupations();
    elements.occupationInput.value = selectedOccupation;
    syncOccupationSelectionText();
    renderOccupationOptions();
  } else {
    resetOccupationOptions();
  }

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

function handleLanguageSelection(event) {
  event.stopPropagation();
  applyLanguage(event.currentTarget.dataset.language);
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
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
      }),
    });

    appendMessage("assistant", getAssistantReply(data));
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

  try {
    await apiRequest(`/api/reset-session/${encodeURIComponent(state.sessionId)}`, {
      method: "POST",
    });

    resetChatMessages();
    setChatStatus(t("conversationReset"), "success");
  } catch (error) {
    setChatStatus(error.message, "error");
  } finally {
    setChatLoading(false);
  }
}

function resetChatMessages() {
  elements.chatMessages.innerHTML = "";
  appendMessage(
    "assistant",
    t("welcomeMessage")
  );
}

function appendLoadingMessage(role, text) {
  const message = createMessageElement(role, text);
  message.classList.add("is-loading");
  elements.chatMessages.appendChild(message);
  scrollChatToBottom();
  return message;
}

function appendMessage(role, text) {
  const message = createMessageElement(role, text);
  elements.chatMessages.appendChild(message);
  scrollChatToBottom();
  return message;
}

function createMessageElement(role, text) {
  const article = document.createElement("article");
  article.className = `message ${role === "user" ? "user-message" : "assistant-message"}`;

  const avatar = document.createElement("div");
  avatar.className = role === "user" ? "message-avatar" : "message-avatar message-avatar-image";
  avatar.setAttribute("aria-hidden", "true");

  if (role === "user") {
    avatar.textContent = t("userAvatar");
  } else {
    const image = document.createElement("img");
    image.src = "logo.svg";
    image.alt = "";
    avatar.appendChild(image);
  }

  const content = document.createElement("div");
  content.className = "message-content";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  renderFormattedText(bubble, text);

  const time = document.createElement("span");
  time.className = "message-time";
  time.textContent = formatMessageTime(new Date());

  content.append(bubble, time);
  article.append(avatar, content);
  return article;
}

function renderFormattedText(container, text) {
  container.innerHTML = "";

  const cleanText = String(text || "").trim();

  if (!cleanText) {
    const paragraph = document.createElement("p");
    paragraph.textContent = t("noReadableResponse");
    container.appendChild(paragraph);
    return;
  }

  const lines = cleanText.split("\n").map((line) => line.trim());

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
      if (!currentList) {
        currentList = document.createElement("ul");
        container.appendChild(currentList);
      }

      const li = document.createElement("li");
      li.innerHTML = formatInlineMarkdown(
        line.replace(/^[-*\u2022]\s+/, "")
      );

      currentList.appendChild(li);
      return;
    }

    currentList = null;

    const p = document.createElement("p");
    p.innerHTML = formatInlineMarkdown(line);
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
  }
}

function populateCountries() {
  elements.countrySelect.innerHTML = "";
  elements.countrySelect.appendChild(createOption("", t("selectCountry")));

  state.countries.forEach((country) => {
    const label = formatCountryLabel(country);
    const option = createOption(country.ocr_code, label);
    option.dataset.countryName = country.country_name_en || country.ocr_code;
    elements.countrySelect.appendChild(option);
  });
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

  if (!state.isCountriesLoaded) {
    loadCountries();
  }

  window.setTimeout(() => {
    elements.countrySelect.focus();
  }, 0);
}

function closeEligibilityModal() {
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

  resetDirectCheckAfterCountry();

  if (!ocrCode) {
    elements.visaTypeGroup.classList.add("hidden");
    setEligibilityStatus("");
    return;
  }

    elements.visaTypeGroup.classList.remove("hidden");
  elements.visaTypeSelect.disabled = true;
  elements.visaTypeSelect.innerHTML = "";
  elements.visaTypeSelect.appendChild(createOption("", t("loadingVisaTypes")));
  setEligibilityStatus(t("loadingVisaTypes"));

  try {
    const data = await apiRequest(`/api/visa-types/${encodeURIComponent(ocrCode)}`);
    state.visaTypes = normalizeVisaTypes(data);
    populateVisaTypes();
    setEligibilityStatus(state.visaTypes.length ? "" : t("noVisaTypes"));
  } catch (error) {
    state.visaTypes = [];
    elements.visaTypeSelect.innerHTML = "";
    elements.visaTypeSelect.appendChild(createOption("", t("selectVisaType")));
    setEligibilityStatus(error.message, "error");
  } finally {
    elements.visaTypeSelect.disabled = false;
  }
}

function resetDirectCheckAfterCountry() {
  state.visaTypes = [];
  state.occupations = [];
  state.relationships = [];
  state.selectedRelationships = [];
  state.isOccupationsLoading = false;
  state.isRelationshipsLoading = false;
  elements.visaTypeSelect.innerHTML = "";
  elements.visaTypeSelect.appendChild(createOption("", t("selectVisaType")));
  resetOccupationOptions();
  resetRelationshipOptions();
  hideConditionalFields();
  clearDirectInputs();
  elements.eligibilityResult.innerHTML = "";
}

function populateVisaTypes() {
  elements.visaTypeSelect.innerHTML = "";
  elements.visaTypeSelect.appendChild(createOption("", t("selectVisaType")));

  state.visaTypes.forEach((visaType) => {
    elements.visaTypeSelect.appendChild(
      createOption(String(visaType.visa_type), formatVisaTypeLabel(visaType))
    );
  });
}

async function handleVisaTypeChange() {
  elements.eligibilityResult.innerHTML = "";
  state.occupations = [];
  state.relationships = [];
  state.selectedRelationships = [];
  state.isOccupationsLoading = false;
  state.isRelationshipsLoading = false;
  resetOccupationOptions();
  resetRelationshipOptions();

  if (elements.visaTypeSelect.value) {
    showConditionalFields();
    await Promise.all([
      loadOccupationsForSelectedVisa(),
      loadRelationshipsForSelectedVisa(),
    ]);
    return;
  }

  hideConditionalFields();
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
  state.selectedRelationships = [];
  syncOccupationSelectionText();
  renderOccupationOptions();
  closeOccupationMenu();
  updateRelationshipSelectionText();
  closeRelationshipMenu();
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
      `/api/occupations/${encodeURIComponent(ocrCode)}/${encodeURIComponent(visaType)}`
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

  const isOpen = elements.occupationSingleSelect.classList.toggle("is-open");
  elements.occupationTrigger.setAttribute("aria-expanded", String(isOpen));
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

  elements.occupationSingleSelect.classList.add("is-open");
  elements.occupationTrigger.setAttribute("aria-expanded", "true");
  setModalSelectOpen(true);
  renderOccupationOptions();
  window.setTimeout(() => elements.occupationSearchInput.focus(), 0);
}

function closeOccupationMenu() {
  elements.occupationSingleSelect.classList.remove("is-open");
  elements.occupationTrigger.setAttribute("aria-expanded", "false");
  setModalSelectOpen(false);
}

function setModalSelectOpen(isOpen) {
  elements.eligibilityModal.querySelector(".modal")?.classList.toggle("has-open-select", isOpen);
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
      primary: nameAr || nameEn || fallback,
      secondary: nameAr && nameEn && normalizeDisplayText(nameAr) !== normalizeDisplayText(nameEn) ? nameEn : "",
    };
  }

  return {
    primary: nameEn || nameAr || fallback,
    secondary: nameAr && nameEn && normalizeDisplayText(nameAr) !== normalizeDisplayText(nameEn) ? nameAr : "",
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
      `/api/relationships/${encodeURIComponent(ocrCode)}/${encodeURIComponent(visaType)}`
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
  elements.relationshipMenu.innerHTML = "";
  updateRelationshipSelectionText(label);
  closeRelationshipMenu();
  syncRelationshipSelectState();
}

function populateRelationships() {
  elements.relationshipMenu.innerHTML = "";
  state.selectedRelationships = [];

  if (!state.relationships.length) {
    updateRelationshipSelectionText(t("noRelationshipRestriction"));
    closeRelationshipMenu();
    syncRelationshipSelectState();
    return;
  }

  state.relationships.forEach((relationship) => {
    const option = document.createElement("label");
    option.className = "multi-select-option";
    option.setAttribute("role", "option");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = relationship.value;
    checkbox.addEventListener("change", handleRelationshipSelectionChange);

    const text = document.createElement("span");
    text.textContent = relationship.label;

    option.append(checkbox, text);
    elements.relationshipMenu.appendChild(option);
  });

  updateRelationshipSelectionText();
  syncRelationshipSelectState();
}

function handleRelationshipSelectionChange() {
  state.selectedRelationships = Array.from(
    elements.relationshipMenu.querySelectorAll("input[type='checkbox']:checked")
  ).map((checkbox) => checkbox.value);

  updateRelationshipSelectionText();
}

function toggleRelationshipMenu(event) {
  event.stopPropagation();

  if (elements.relationshipInput.disabled || !state.relationships.length) {
    return;
  }

  closeOccupationMenu();
  const isOpen = elements.relationshipMultiSelect.classList.toggle("is-open");
  elements.relationshipInput.setAttribute("aria-expanded", String(isOpen));
}

function closeRelationshipMenu() {
  elements.relationshipMultiSelect.classList.remove("is-open");
  elements.relationshipInput.setAttribute("aria-expanded", "false");
}

function updateRelationshipSelectionText(placeholder = t("selectRelationships")) {
  if (!state.selectedRelationships.length) {
    elements.relationshipSelectionText.textContent = placeholder;
    return;
  }

  const labels = state.selectedRelationships
    .map((value) => state.relationships.find((relationship) => relationship.value === value)?.label || value);

  elements.relationshipSelectionText.textContent = labels.join(", ");
}

function syncRelationshipSelectState() {
  elements.relationshipInput.disabled =
    state.isRelationshipsLoading ||
    !elements.visaTypeSelect.value ||
    !state.relationships.length;
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
      }),
    });

    renderEligibilityResult(data);
    setEligibilityStatus("");
  } catch (error) {
    setEligibilityStatus(error.message, "error");
  } finally {
    setEligibilityLoading(false);
  }
}

function setEligibilityLoading(isLoading, status = "") {
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
  const card = document.createElement("section");
  card.className = "result-card";

  if (isVisaTypesOnlyResponse(data, visaTypes)) {
    renderVisaTypesOnlyResult(card, visaTypes);
    elements.eligibilityResult.appendChild(card);
    return;
  }

  const status = data?.status || "NEED_MORE_INFO";
  const checks = normalizeChecks(data?.checks);
  const passedChecks = checks.filter((check) => check.passed === true);
  const failedChecks = checks.filter((check) => check.passed === false);
  const missingFields = normalizeList(data?.missing_fields);
  const selectedVisa = getSelectedVisaType();

  const heading = document.createElement("h3");
  heading.textContent = t("eligibilityResult");
  card.appendChild(heading);

  const summary = document.createElement("div");
  summary.className = "result-summary";

  summary.appendChild(createSummaryItem(t("status"), formatStatus(status), getStatusBadgeClass(status)));
  summary.appendChild(createSummaryItem(t("visaNumber"), data?.visa_type || selectedVisa?.visa_type || t("notProvided")));
  summary.appendChild(createSummaryItem(t("visaName"), data?.visa_name || selectedVisa?.visa_name || t("notProvided")));
  summary.appendChild(createSummaryItem(t("applicantCountry"), data?.country || formatCountryLabel(state.selectedCountry) || t("notProvided")));

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

  elements.eligibilityResult.appendChild(card);
}

function renderVisaTypesOnlyResult(card, visaTypes) {
  const heading = document.createElement("h3");
  heading.textContent = t("availableVisaTypesTitle");
  card.appendChild(heading);

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
    text.textContent = check.message || formatFieldName(check.field);
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
        return {
          visa_type: item,
          visa_name: item === 16 || item === "16" ? "\u0633\u0645\u0629 \u062f\u062e\u0648\u0644 \u0644\u0644\u0633\u064a\u0627\u062d\u0629" : "",
        };
      }

      return {
        visa_type: item.visa_type ?? item.visaType ?? item.id ?? item.number ?? "",
        visa_name: item.visa_name || item.typeOfVisa || item.name || item.description || "",
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
    return nameAr || nameEn || fallback || t("occupationLabel");
  }

  if (nameEn && nameAr && normalizeDisplayText(nameEn) !== normalizeDisplayText(nameAr)) {
    return `${nameEn} - ${nameAr}`;
  }

  return nameEn || nameAr || fallback || t("occupationLabel");
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
    return { value: item, label: item };
  }

  if (!item || typeof item !== "object") {
    return { value: "", label: "" };
  }

  const value =
    item.value ||
    item.relation_name_ar ||
    item.relationNameAr ||
    item.arabicDescription ||
    item.ArabicDescription ||
    item.relation_name_en ||
    item.relationNameEn ||
    item.DescriptionEn ||
    item.label ||
    "";

  return {
    value,
    label: item.label || formatRelationshipLabel(item, value),
  };
}

function formatRelationshipLabel(relationship, fallback = "") {
  const nameAr =
    relationship.relation_name_ar ||
    relationship.relationNameAr ||
    relationship.arabicDescription ||
    relationship.ArabicDescription ||
    "";
  const nameEn =
    relationship.relation_name_en ||
    relationship.relationNameEn ||
    relationship.DescriptionEn ||
    "";

  if (nameAr && nameEn && nameAr !== nameEn) {
    return `${nameAr} - ${nameEn}`;
  }

  return nameAr || nameEn || fallback || "Relationship";
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
  const name = visaType?.visa_name || visaType?.typeOfVisa || visaType?.name || "";
  const prefix = t("visaNo");

  if (number && name) {
    return `${prefix} ${number} - ${name}`;
  }

  if (number) {
    return `${prefix} ${number}`;
  }

  return name || t("visaTypeMissing");
}

function formatCountryLabel(country) {
  if (!country) {
    return "";
  }

  const name =
    state.language === "ar"
      ? country.country_name_ar || country.country_name_en || country.name || country.ocr_code
      : country.country_name_en || country.name || country.ocr_code;
  return country.ocr_code ? `${name} (${country.ocr_code})` : name;
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
