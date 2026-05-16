// Live Draft Companion - draft-state polling + suggestions (M6a/T47, M6b/T48).
// Vanilla JS + fetch (ERRATA-002, no framework, no build step).
// Polls GET /api/draft-state every 2s; "Suggerisci ora" -> POST /api/suggest
// and renders the Top-3 cards. Loading spinner = T49; error banner = T49b.

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

function setSpinner(visible) {
  const spinner = document.getElementById("loading-spinner");
  if (spinner) {
    spinner.classList.toggle("hidden", !visible);
  }
}

async function requestSuggestions() {
  if (!latestDraftState) {
    // No draft captured yet; UX feedback is T49b.
    return;
  }
  setSpinner(true);
  try {
    const response = await fetch("/api/suggest", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(latestDraftState),
    });
    if (!response.ok) {
      // Minimal non-crash handling; full error banner is T49b.
      return;
    }
    renderSuggestions(await response.json());
  } catch (err) {
    // Network down; T49b owns the user-facing error UX.
    console.debug("suggest request failed", err);
  } finally {
    setSpinner(false);
  }
}

function start() {
  pollDraftState();
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
