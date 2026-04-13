const API_BASE_URL = (window.__API_BASE_URL__ || "http://localhost:8000/api/v1").replace(/\/$/, "");

const elements = {
  form: document.getElementById("time-entry-form"),
  submitBtn: document.getElementById("submit-btn"),
  formStatus: document.getElementById("form-status"),
  entriesStatus: document.getElementById("entries-status"),
  entriesTbody: document.getElementById("entries-tbody"),
  refreshBtn: document.getElementById("refresh-btn"),
};

function setStatus(el, message, type) {
  if (!el) return;
  el.textContent = message || "";
  el.classList.remove("error", "success");
  if (type) el.classList.add(type);
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    let detail = "";
    try {
      const data = await response.json();
      detail = data.message || data.detail || JSON.stringify(data);
    } catch (_) {
      // ignore
    }
    throw new Error(`Request failed (${response.status}): ${detail}`);
  }
  if (response.status === 204) return null;
  return response.json();
}

async function loadEntries() {
  setStatus(elements.entriesStatus, "Loading entries...", "");
  elements.entriesTbody.innerHTML = "";
  try {
    const entries = await fetchJson(`${API_BASE_URL}/time-entries/`);
    if (!Array.isArray(entries) || entries.length === 0) {
      setStatus(elements.entriesStatus, "No entries yet. Be the first to log time today.", "");
      return;
    }
    const rowsHtml = entries
      .sort((a, b) => new Date(b.date) - new Date(a.date) || (b.created_at || "").localeCompare(a.created_at || ""))
      .map((entry) => renderEntryRow(entry))
      .join("");
    elements.entriesTbody.innerHTML = rowsHtml;
    setStatus(elements.entriesStatus, `Loaded ${entries.length} entr${entries.length === 1 ? "y" : "ies"}.`, "success");
  } catch (error) {
    console.error(error);
    setStatus(elements.entriesStatus, `Failed to load entries: ${error.message}`, "error");
  }
}

function renderEntryRow(entry) {
  const safe = (value) => (value == null ? "" : String(value));
  const notes = safe(entry.notes);
  const date = safe(entry.date);
  const person = safe(entry.person_name);
  const activity = safe(entry.activity);
  const duration = safe(entry.duration_minutes);

  return `<tr data-id="${entry.id}">
    <td>${date}</td>
    <td>${person}</td>
    <td>${activity}</td>
    <td>${duration}</td>
    <td>${notes}</td>
    <td>
      <button type="button" class="secondary" data-action="delete" data-id="${entry.id}">Delete</button>
    </td>
  </tr>`;
}

function getFormData() {
  const formData = new FormData(elements.form);
  const date = formData.get("date");
  const person_name = formData.get("person_name").trim();
  const activity = formData.get("activity").trim();
  const durationRaw = formData.get("duration_minutes");
  const notesRaw = formData.get("notes");

  const errors = [];
  if (!date) errors.push("Date is required.");
  if (!person_name) errors.push("Person name is required.");
  if (!activity) errors.push("Activity is required.");

  const duration = Number(durationRaw);
  if (!durationRaw || Number.isNaN(duration) || duration <= 0) {
    errors.push("Duration must be a positive number of minutes.");
  }

  return {
    data: {
      date,
      person_name,
      activity,
      duration_minutes: duration,
      notes: notesRaw && notesRaw.trim() ? notesRaw.trim() : null,
    },
    errors,
  };
}

async function handleSubmit(event) {
  event.preventDefault();
  setStatus(elements.formStatus, "", "");

  const { data, errors } = getFormData();
  if (errors.length > 0) {
    setStatus(elements.formStatus, errors.join(" "), "error");
    return;
  }

  elements.submitBtn.disabled = true;
  setStatus(elements.formStatus, "Saving entry...", "");

  try {
    await fetchJson(`${API_BASE_URL}/time-entries/`, {
      method: "POST",
      body: JSON.stringify(data),
    });
    elements.form.reset();
    setStatus(elements.formStatus, "Entry added.", "success");
    await loadEntries();
  } catch (error) {
    console.error(error);
    setStatus(elements.formStatus, `Failed to save entry: ${error.message}`, "error");
  } finally {
    elements.submitBtn.disabled = false;
  }
}

async function handleEntriesClick(event) {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const action = target.getAttribute("data-action");
  if (action !== "delete") return;

  const id = target.getAttribute("data-id");
  if (!id) return;

  if (!confirm("Delete this entry? This cannot be undone.")) return;

  target.disabled = true;
  try {
    await fetchJson(`${API_BASE_URL}/time-entries/${id}`, { method: "DELETE" });
    await loadEntries();
  } catch (error) {
    console.error(error);
    setStatus(elements.entriesStatus, `Failed to delete entry: ${error.message}`, "error");
  } finally {
    target.disabled = false;
  }
}

function init() {
  if (elements.form) {
    elements.form.addEventListener("submit", handleSubmit);
  }
  if (elements.entriesTbody) {
    elements.entriesTbody.addEventListener("click", handleEntriesClick);
  }
  if (elements.refreshBtn) {
    elements.refreshBtn.addEventListener("click", () => {
      loadEntries();
    });
  }
  loadEntries();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
