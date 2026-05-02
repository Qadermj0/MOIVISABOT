const SESSION_KEY = "kuwaitVisaSmartAssistant.sessionId";
const API_BASE = "";

const state = {
  sessionId: getOrCreateSessionId(),
  countries: [],
  visaTypes: [],
  occupations: [],
  selectedCountry: null,
  isCountriesLoaded: false,
  isOccupationsLoading: false,
};

const elements = {
  chatMessages: document.getElementById("chatMessages"),
  chatForm: document.getElementById("chatForm"),
  chatInput: document.getElementById("chatInput"),
  sendChatButton: document.getElementById("sendChatButton"),
  resetChatButton: document.getElementById("resetChatButton"),
  chatStatus: document.getElementById("chatStatus"),
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
  genderSelect: document.getElementById("genderSelect"),
  relationshipInput: document.getElementById("relationshipInput"),
  checkEligibilityButton: document.getElementById("checkEligibilityButton"),
  eligibilityStatus: document.getElementById("eligibilityStatus"),
  eligibilityResult: document.getElementById("eligibilityResult"),
};

document.addEventListener("DOMContentLoaded", () => {
  bindEvents();
  loadCountries();
});

function bindEvents() {
  elements.chatForm.addEventListener("submit", handleChatSubmit);
  elements.resetChatButton.addEventListener("click", handleResetConversation);
  elements.chatInput.addEventListener("input", autoSizeChatInput);

  elements.openEligibilityButton.addEventListener("click", openEligibilityModal);
  elements.closeEligibilityButton.addEventListener("click", closeEligibilityModal);
  elements.cancelEligibilityButton.addEventListener("click", closeEligibilityModal);
  elements.eligibilityModal.addEventListener("click", handleBackdropClick);
  elements.countrySelect.addEventListener("change", handleCountryChange);
  elements.visaTypeSelect.addEventListener("change", handleVisaTypeChange);
  elements.eligibilityForm.addEventListener("submit", handleEligibilitySubmit);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && elements.eligibilityModal.classList.contains("is-open")) {
      closeEligibilityModal();
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

  appendMessage("user", message);
  elements.chatInput.value = "";
  autoSizeChatInput();
  setChatLoading(true, "Sending message...");

  const loadingMessage = appendLoadingMessage("assistant", "Preparing response...");

  try {
    const data = await apiRequest("/api/chat", {
      method: "POST",
      body: JSON.stringify({
        session_id: state.sessionId,
        message,
      }),
    });

    loadingMessage.remove();
    appendMessage("assistant", getAssistantReply(data));
    setChatStatus("");
  } catch (error) {
    loadingMessage.remove();
    appendMessage(
      "assistant",
      "The assistant could not complete the request. Please try again in a moment."
    );
    setChatStatus(error.message, "error");
  } finally {
    setChatLoading(false);
  }
}

async function handleResetConversation() {
  setChatLoading(true, "Resetting conversation...");

  try {
    await apiRequest(`/api/reset-session/${encodeURIComponent(state.sessionId)}`, {
      method: "POST",
    });

    resetChatMessages();
    setChatStatus("Conversation reset.", "success");
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
    "Welcome. Please share the applicant nationality, visa type, age, occupation, gender, and any companion or relationship details that apply."
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
}

function createMessageElement(role, text) {
  const article = document.createElement("article");
  article.className = `message ${role === "user" ? "user-message" : "assistant-message"}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.setAttribute("aria-hidden", "true");
  avatar.textContent = role === "user" ? "You" : "MOI";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  renderFormattedText(bubble, text);

  article.append(avatar, bubble);
  return article;
}

function renderFormattedText(container, text) {
  container.innerHTML = "";

  const cleanText = String(text || "").trim();

  if (!cleanText) {
    const paragraph = document.createElement("p");
    paragraph.textContent = "No readable response was returned.";
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
    if (/^[-*•]\s+/.test(line)) {
      if (!currentList) {
        currentList = document.createElement("ul");
        container.appendChild(currentList);
      }

      const li = document.createElement("li");
      li.innerHTML = formatInlineMarkdown(
        line.replace(/^[-*•]\s+/, "")
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
  html = html.replace(/✅/g, `<span class="inline-check">✓</span>`);
  html = html.replace(/❌/g, `<span class="inline-cross">✕</span>`);

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

  return "I received the response, but no readable answer was provided.";
}

function isJsonString(value) {
  const text = value.trim();
  return text.startsWith("{") || text.startsWith("[") || text.includes("```json");
}

function formatDecisionAsText(decision) {
  const visaTypes = normalizeVisaTypes(decision);
  if (visaTypes.length) {
    return [
      "Available visa types:",
      ...visaTypes.map((type) => `- ${formatVisaTypeLabel(type)}`),
    ].join("\n");
  }

  const status = formatStatus(decision?.status);
  const missing = normalizeList(decision?.missing_fields);
  const failed = normalizeChecks(decision?.checks).filter((check) => check.passed === false);
  const passed = normalizeChecks(decision?.checks).filter((check) => check.passed === true);

  const lines = [`Status: ${status}`];

  if (decision?.visa_type || decision?.visa_name) {
    lines.push(`Visa: ${formatVisaTypeLabel({ visa_type: decision.visa_type, visa_name: decision.visa_name })}`);
  }

  if (decision?.country) {
    lines.push(`Applicant Country: ${decision.country}`);
  }

  if (passed.length) {
    lines.push("", "Passed checks:", ...passed.map((check) => `- ${check.message || formatFieldName(check.field)}`));
  }

  if (failed.length) {
    lines.push("", "Failed checks:", ...failed.map((check) => `- ${check.message || formatFieldName(check.field)}`));
  }

  if (missing.length) {
    lines.push("", "Missing fields:", ...missing.map((field) => `- ${formatFieldName(field)}`));
  }

  if (decision?.message) {
    lines.push("", decision.message);
  }

  if (decision?.reason) {
    lines.push("", decision.reason);
  }

  return lines.join("\n");
}

function setChatLoading(isLoading, status = "") {
  elements.sendChatButton.disabled = isLoading;
  elements.resetChatButton.disabled = isLoading;
  elements.chatInput.disabled = isLoading;
  setChatStatus(status);
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
  setEligibilityStatus("Loading countries...");
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
  elements.countrySelect.appendChild(createOption("", "Select applicant country"));

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
  elements.visaTypeSelect.appendChild(createOption("", "Loading visa types..."));
  setEligibilityStatus("Loading visa types...");

  try {
    const data = await apiRequest(`/api/visa-types/${encodeURIComponent(ocrCode)}`);
    state.visaTypes = normalizeVisaTypes(data);
    populateVisaTypes();
    setEligibilityStatus(state.visaTypes.length ? "" : "No visa types were returned for this country.");
  } catch (error) {
    state.visaTypes = [];
    elements.visaTypeSelect.innerHTML = "";
    elements.visaTypeSelect.appendChild(createOption("", "Select a visa type"));
    setEligibilityStatus(error.message, "error");
  } finally {
    elements.visaTypeSelect.disabled = false;
  }
}

function resetDirectCheckAfterCountry() {
  state.visaTypes = [];
  state.occupations = [];
  state.isOccupationsLoading = false;
  elements.visaTypeSelect.innerHTML = "";
  elements.visaTypeSelect.appendChild(createOption("", "Select a visa type"));
  resetOccupationOptions();
  hideConditionalFields();
  clearDirectInputs();
  elements.eligibilityResult.innerHTML = "";
}

function populateVisaTypes() {
  elements.visaTypeSelect.innerHTML = "";
  elements.visaTypeSelect.appendChild(createOption("", "Select a visa type"));

  state.visaTypes.forEach((visaType) => {
    elements.visaTypeSelect.appendChild(
      createOption(String(visaType.visa_type), formatVisaTypeLabel(visaType))
    );
  });
}

async function handleVisaTypeChange() {
  elements.eligibilityResult.innerHTML = "";
  state.occupations = [];
  state.isOccupationsLoading = false;
  resetOccupationOptions();

  if (elements.visaTypeSelect.value) {
    showConditionalFields();
    await loadOccupationsForSelectedVisa();
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
  elements.relationshipInput.value = "";
}

async function loadOccupationsForSelectedVisa() {
  const ocrCode = elements.countrySelect.value;
  const visaType = elements.visaTypeSelect.value;

  if (!ocrCode || !visaType) {
    resetOccupationOptions();
    return;
  }

  state.isOccupationsLoading = true;
  elements.checkEligibilityButton.disabled = true;
  resetOccupationOptions("Loading available occupations...");
  setEligibilityStatus("Loading available occupations...");

  try {
    const data = await apiRequest(
      `/api/occupations/${encodeURIComponent(ocrCode)}/${encodeURIComponent(visaType)}`
    );

    if (ocrCode !== elements.countrySelect.value || visaType !== elements.visaTypeSelect.value) {
      return;
    }

    state.occupations = normalizeOccupations(data);
    populateOccupations();
    setEligibilityStatus("");
  } catch (error) {
    if (ocrCode === elements.countrySelect.value && visaType === elements.visaTypeSelect.value) {
      state.occupations = [];
      resetOccupationOptions("Could not load occupations");
      setEligibilityStatus(error.message, "error");
    }
  } finally {
    if (ocrCode === elements.countrySelect.value && visaType === elements.visaTypeSelect.value) {
      state.isOccupationsLoading = false;
      elements.checkEligibilityButton.disabled = false;
      syncOccupationSelectState();
    }
  }
}

function resetOccupationOptions(label = "Select an occupation") {
  elements.occupationInput.innerHTML = "";
  elements.occupationInput.appendChild(createOption("", label));
  syncOccupationSelectState();
}

function populateOccupations() {
  elements.occupationInput.innerHTML = "";

  if (!state.occupations.length) {
    elements.occupationInput.appendChild(createOption("", "No occupation restriction for this visa"));
    syncOccupationSelectState();
    return;
  }

  elements.occupationInput.appendChild(createOption("", "Select an available occupation"));

  state.occupations.forEach((occupation) => {
    elements.occupationInput.appendChild(
      createOption(occupation.value, occupation.label)
    );
  });

  syncOccupationSelectState();
}

function syncOccupationSelectState() {
  elements.occupationInput.disabled =
    state.isOccupationsLoading ||
    !elements.visaTypeSelect.value ||
    !state.occupations.length;
}

async function handleEligibilitySubmit(event) {
  event.preventDefault();

  const ocrCode = elements.countrySelect.value;
  const visaType = elements.visaTypeSelect.value;

  if (!ocrCode || !visaType) {
    return;
  }

  setEligibilityLoading(true, "Checking eligibility...");
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
        relationship: optionalText(elements.relationshipInput.value),
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
  elements.checkEligibilityButton.disabled = isLoading;
  elements.countrySelect.disabled = isLoading;
  elements.visaTypeSelect.disabled = isLoading;
  elements.ageInput.disabled = isLoading;
  elements.occupationInput.disabled = isLoading || state.isOccupationsLoading || !state.occupations.length;
  elements.genderSelect.disabled = isLoading;
  elements.relationshipInput.disabled = isLoading;
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
  heading.textContent = "Eligibility Result";
  card.appendChild(heading);

  const summary = document.createElement("div");
  summary.className = "result-summary";

  summary.appendChild(createSummaryItem("Status", formatStatus(status), getStatusBadgeClass(status)));
  summary.appendChild(createSummaryItem("Visa Number", data?.visa_type || selectedVisa?.visa_type || "Not provided"));
  summary.appendChild(createSummaryItem("Visa Name", data?.visa_name || selectedVisa?.visa_name || "Not provided"));
  summary.appendChild(createSummaryItem("Applicant Country", data?.country || formatCountryLabel(state.selectedCountry) || "Not provided"));

  card.appendChild(summary);

  renderCheckSection(card, "Passed checks", passedChecks, "pass", "No passed checks were returned.");
  renderCheckSection(card, "Failed checks", failedChecks, "fail", data?.reason || "No failed checks were returned.");
  renderMissingFields(card, missingFields);

  elements.eligibilityResult.appendChild(card);
}

function renderVisaTypesOnlyResult(card, visaTypes) {
  const heading = document.createElement("h3");
  heading.textContent = "Available Visa Types";
  card.appendChild(heading);

  if (!visaTypes.length) {
    const note = document.createElement("p");
    note.className = "empty-note";
    note.textContent = "No visa types were returned.";
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
  heading.textContent = "Missing fields";
  section.appendChild(heading);

  if (!missingFields.length) {
    const note = document.createElement("p");
    note.className = "empty-note";
    note.textContent = "No missing fields were returned.";
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
    return { value: item, label: item };
  }

  if (!item || typeof item !== "object") {
    return { value: "", label: "" };
  }

  const value =
    item.value ||
    item.occupation_name_ar ||
    item.occupationNameAr ||
    item.ArabicDescription ||
    item.occupation_name_en ||
    item.occupationNameEn ||
    item.DescriptionEn ||
    item.label ||
    "";

  return {
    value,
    label: item.label || formatOccupationLabel(item, value),
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
    "";

  if (nameAr && nameEn && nameAr !== nameEn) {
    return `${nameAr} - ${nameEn}`;
  }

  return nameAr || nameEn || fallback || "Occupation";
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

  if (number && name) {
    return `Visa No. ${number} - ${name}`;
  }

  if (number) {
    return `Visa No. ${number}`;
  }

  return name || "Visa type not provided";
}

function formatCountryLabel(country) {
  if (!country) {
    return "";
  }

  const name = country.country_name_en || country.name || country.ocr_code;
  return country.ocr_code ? `${name} (${country.ocr_code})` : name;
}

function formatStatus(status) {
  const normalized = String(status || "").toUpperCase();

  if (normalized === "APPROVED") {
    return "Approved";
  }

  if (normalized === "NOT_APPROVED") {
    return "Not Approved";
  }

  if (normalized === "NEED_MORE_INFO") {
    return "Need More Information";
  }

  if (normalized === "INFO") {
    return "Information";
  }

  return "Need More Information";
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

function formatFieldName(field) {
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

function createOption(value, label) {
  const option = document.createElement("option");
  option.value = value;
  option.textContent = label;
  return option;
}
