// Live Draft Companion - draft-state polling (M6a/T47).
// Vanilla JS + fetch (ERRATA-002, no framework, no build step).
// Polls GET /api/draft-state every 2s and updates the draft grid.
// Suggestion rendering is T48; full error banner is T49b.

"use strict";

const POLL_INTERVAL_MS = 2000;
const ROLE_ORDER = ["TOP", "JUNGLE", "MID", "ADC", "SUPPORT"];

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
    renderDraft(await response.json());
  } catch (err) {
    // Network down: keep last state, retry on next tick (T49b owns UX).
    console.debug("draft-state poll failed", err);
  }
}

function start() {
  pollDraftState();
  window.setInterval(pollDraftState, POLL_INTERVAL_MS);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", start);
} else {
  start();
}
