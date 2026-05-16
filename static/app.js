// Live Draft Companion - draft-state polling + suggestions (M6a/T47, M6b/T48).
// Vanilla JS + fetch (ERRATA-002, no framework, no build step).
// Polls GET /api/draft-state every 2s; "Suggerisci ora" -> POST /api/suggest
// and renders the Top-3 cards. Loading spinner = T49; error banner = T49b.
// History list + feedback buttons = T56.

"use strict";

const POLL_INTERVAL_MS = 2000;
const ROLE_ORDER = ["TOP", "JUNGLE", "MID", "ADC", "SUPPORT"];

let latestDraftState = null;

function renderList(el, items) {
  el.replaceChildren();
  for (const text of items) {
    const li = document.createElement("li");
    li.textContent = text;
    el.appendChild(li);
  }
}

function pickLabel(pick) {
  const champion = pick && pick.champion ? pick.champion : "—";
  const role = pick && pick.role ? pick.role : "?";
  return `${role}: ${champion}`;
}

function sortByRole(team) {
  return [...team].sort(
    (a, b) => ROLE_ORDER.indexOf(a.role) - ROLE_ORDER.indexOf(b.role)
  );
}

function renderDraft(state) {
  const status = document.getElementById("status");
  if (status) {
    status.textContent = `Draft attivo - ruolo: ${state.user_role}`;
    status.classList.remove("text-amber-400");
    status.classList.add("text-emerald-400");
  }

  const bans = document.getElementById("bans-list");
  if (bans) {
    renderList(
      bans,
      (state.bans || []).filter((b) => b).map((b) => b)
    );
  }

  const ally = document.getElementById("ally-team");
  if (ally) {
    renderList(ally, sortByRole(state.ally_team || []).map(pickLabel));
  }

  const enemy = document.getElementById("enemy-team");
  if (enemy) {
    renderList(enemy, sortByRole(state.enemy_team || []).map(pickLabel));
  }
}

async function pollDraftState() {
  try {
    const response = await fetch("/api/draft-state", {
      headers: { Accept: "application/json" },
    });
    if (!response.ok) {
      // Minimal non-crash handling; full error banner is T49b.
      return;
    }
    latestDraftState = await response.json();
    renderDraft(latestDraftState);
  } catch (err) {
    // Network down: keep last state, retry on next tick (T49b owns UX).
    console.debug("draft-state poll failed", err);
  }
}

function suggestionCard(suggestion) {
  const card = document.createElement("div");
  card.className = "rounded-lg bg-slate-700 p-4";

  const title = document.createElement("h3");
  title.className = "mb-1 text-base font-semibold";
  title.textContent = `#${suggestion.rank} ${suggestion.champion}`;
  card.appendChild(title);

  const keystone = document.createElement("p");
  keystone.className = "mb-2 text-xs uppercase tracking-wide text-indigo-300";
  keystone.textContent = suggestion.keystone;
  card.appendChild(keystone);

  const build = document.createElement("ul");
  build.className = "mb-2 list-disc pl-5 text-sm text-slate-300";
  for (const item of suggestion.build_path || []) {
    const li = document.createElement("li");
    li.textContent = item;
    build.appendChild(li);
  }
  card.appendChild(build);

  const explanation = document.createElement("p");
  explanation.className = "text-sm text-slate-200";
  explanation.textContent = suggestion.explanation;
  card.appendChild(explanation);

  return card;
}

function renderSuggestions(output) {
  const container = document.getElementById("suggestions");
  if (!container) {
    return;
  }
  container.replaceChildren();
  for (const suggestion of output.suggestions || []) {
    container.appendChild(suggestionCard(suggestion));
  }
}

function formatTimestamp(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "";
  }
  return date.toLocaleString("it-IT", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function feedbackLabel(feedback) {
  if (feedback === "good") {
    return "Feedback: utile";
  }
  if (feedback === "bad") {
    return "Feedback: inutile";
  }
  return "Feedback: non valutato";
}

function suggestionSummary(output) {
  const suggestions = output && output.suggestions ? output.suggestions : [];
  return suggestions
    .map((suggestion) => `#${suggestion.rank} ${suggestion.champion}`)
    .join(" | ");
}

function applyButtonState(button, active) {
  button.classList.remove(
    "border-emerald-500",
    "border-rose-500",
    "bg-emerald-600",
    "bg-rose-600",
    "text-white",
    "border-slate-600",
    "bg-slate-900",
    "text-slate-300"
  );
  if (active && button.dataset.feedback === "good") {
    button.classList.add("border-emerald-500", "bg-emerald-600", "text-white");
  } else if (active && button.dataset.feedback === "bad") {
    button.classList.add("border-rose-500", "bg-rose-600", "text-white");
  } else {
    button.classList.add("border-slate-600", "bg-slate-900", "text-slate-300");
  }
  button.setAttribute("aria-pressed", active ? "true" : "false");
}

function setHistoryFeedbackState(item, feedback) {
  item.dataset.feedback = feedback;
  const status = item.querySelector("[data-feedback-status]");
  if (status) {
    status.textContent = feedbackLabel(feedback);
    status.classList.toggle("text-emerald-300", feedback === "good");
    status.classList.toggle("text-rose-300", feedback === "bad");
    status.classList.toggle("text-slate-400", feedback === "unrated");
  }
  for (const button of item.querySelectorAll("[data-feedback]")) {
    applyButtonState(button, button.dataset.feedback === feedback);
  }
}

function feedbackButton(historyId, feedback, label, item) {
  const button = document.createElement("button");
  button.type = "button";
  button.dataset.historyId = String(historyId);
  button.dataset.feedback = feedback;
  button.className =
    "rounded-md border px-3 py-1 text-xs font-medium transition hover:border-slate-400";
  button.textContent = label;
  button.addEventListener("click", () =>
    submitHistoryFeedback(historyId, feedback, item)
  );
  return button;
}

function historyItem(entry) {
  const item = document.createElement("li");
  item.className = "border-t border-slate-700 py-3 first:border-t-0";
  item.dataset.historyId = String(entry.id);

  const header = document.createElement("div");
  header.className = "mb-1 flex flex-wrap items-center justify-between gap-2";

  const meta = document.createElement("p");
  meta.className = "text-xs uppercase tracking-wide text-slate-500";
  const role = entry.draft_state && entry.draft_state.user_role
    ? entry.draft_state.user_role
    : "?";
  meta.textContent = `${formatTimestamp(entry.timestamp)} | ${role} | ${entry.model_used}`;
  header.appendChild(meta);

  const status = document.createElement("span");
  status.dataset.feedbackStatus = "true";
  status.className = "text-xs font-medium text-slate-400";
  header.appendChild(status);
  item.appendChild(header);

  const summary = document.createElement("p");
  summary.className = "mb-2 text-sm font-medium text-slate-100";
  summary.textContent = suggestionSummary(entry.output);
  item.appendChild(summary);

  const actions = document.createElement("div");
  actions.className = "flex flex-wrap gap-2";
  actions.appendChild(feedbackButton(entry.id, "good", "Utile", item));
  actions.appendChild(feedbackButton(entry.id, "bad", "Inutile", item));
  item.appendChild(actions);

  setHistoryFeedbackState(item, entry.feedback || "unrated");
  return item;
}

function renderHistory(entries) {
  const list = document.getElementById("history-list");
  if (!list) {
    return;
  }
  list.replaceChildren();
  if (!entries || entries.length === 0) {
    const empty = document.createElement("li");
    empty.className = "py-2 text-sm text-slate-500";
    empty.textContent = "Nessun suggerimento nello storico.";
    list.appendChild(empty);
    return;
  }
  for (const entry of entries) {
    list.appendChild(historyItem(entry));
  }
}

async function loadHistory() {
  try {
    const response = await fetch("/api/history", {
      headers: { Accept: "application/json" },
    });
    if (!response.ok) {
      showError(await errorMessageFrom(response));
      return;
    }
    renderHistory(await response.json());
  } catch (err) {
    console.debug("history request failed", err);
    showError("Storico non disponibile, riprova.");
  }
}

async function submitHistoryFeedback(historyId, feedback, item) {
  clearError();
  try {
    const response = await fetch("/api/history/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ history_id: historyId, feedback }),
    });
    if (!response.ok) {
      showError(await errorMessageFrom(response));
      return;
    }
    setHistoryFeedbackState(item, feedback);
  } catch (err) {
    console.debug("history feedback request failed", err);
    showError("Feedback non salvato, riprova.");
  }
}

function setSpinner(visible) {
  const spinner = document.getElementById("loading-spinner");
  if (spinner) {
    spinner.classList.toggle("hidden", !visible);
  }
}

function showError(userMessage) {
  const banner = document.getElementById("error-banner");
  const message = document.getElementById("error-message");
  if (message) {
    message.textContent = userMessage;
  }
  if (banner) {
    banner.classList.remove("hidden");
    banner.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}

function clearError() {
  const banner = document.getElementById("error-banner");
  if (banner) {
    banner.classList.add("hidden");
  }
}

async function errorMessageFrom(response) {
  // Uniform contract {error_code, user_message} from the backend (T49b).
  try {
    const body = await response.json();
    if (body && body.user_message) {
      return body.user_message;
    }
  } catch (err) {
    console.debug("error body not JSON", err);
  }
  return "Si è verificato un errore, riprova.";
}

async function requestSuggestions() {
  if (!latestDraftState) {
    // No draft captured yet; UX feedback is T49b.
    return;
  }
  clearError();
  setSpinner(true);
  try {
    const response = await fetch("/api/suggest", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(latestDraftState),
    });
    if (!response.ok) {
      showError(await errorMessageFrom(response));
      return;
    }
    const output = await response.json();
    renderSuggestions(output);
    await loadHistory();
  } catch (err) {
    // Network down (no connectivity): surface a clear message, app stays usable.
    console.debug("suggest request failed", err);
    showError("Rete non disponibile, riprova.");
  } finally {
    // Button is never disabled, so it stays clickable; spinner always hidden.
    setSpinner(false);
  }
}

function start() {
  pollDraftState();
  loadHistory();
  window.setInterval(pollDraftState, POLL_INTERVAL_MS);

  const button = document.getElementById("suggest-button");
  if (button) {
    button.addEventListener("click", requestSuggestions);
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", start);
} else {
  start();
}
