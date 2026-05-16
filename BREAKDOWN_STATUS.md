# Live Draft Companion - Breakdown Status

Data: 2026-05-16
Macchina: PC casa (LoL installato in `E:\Riot Games\League of Legends`)
Repo locale: c:\live-draft-companion
Repo GitHub: https://github.com/MrChuck118/live-draft-companion
Branch: main

Nota: questo file e' la prosecuzione **versionata nel repo** del precedente
`LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md` (che era un file Desktop di
"pc its", fuori dal repo e non raggiungibile da questa macchina). Da qui in
avanti lo stato forward-looking vive qui + nel `PROMPT_LOG.md`.

## Stato generale

- Specifica base: `LiveDraftCompanion_TechnicalSpec_v2.3.md` (FROZEN)
- Documento con precedenza in caso di conflitto: `SPEC_ERRATA.md`
- Breakdown operativo: `breakdown_tasks_v2.1_corretto.md`
- Principio operativo: Demo Mode First
- Provider AI: DeepSeek API diretta (`deepseek-chat` primario, `deepseek-reasoner` fallback), ERRATA-006
- Frontend MVP: HTML + Tailwind CDN + Vanilla JS + fetch (ERRATA-002)
- Suite test: 83/83 PASSED (`pytest tests/`)
- Prossimo task tecnico: M6a/T47 (`static/app.js` Vanilla JS polling `/api/draft-state`). T41-T44+T46 CHIUSI. M5/T40 resta IN SOSPESO (vedi In sospeso), procede per scelta utente

## Avanzamento per modulo

| Modulo | Stato | Note |
|---|---|---|
| M0 Setup (T01-T05b) | CHIUSO (T05b manuale a parte) | venv su PC casa OK; cache Data Dragon ripopolata (INC-009); T05b reclutamento panel = azione manuale utente, non fatta |
| M1 Data Dragon (T06-T12) | CHIUSO | patch 16.10.1, 172 champ / 705 item / 17 keystone; ERRATA-004 (psutil), ERRATA-005 (Luden) |
| M2 Models+Validators (T13-T22) | CHIUSO | 28 test validators |
| M3 Prompt+AIClient (T23-T31) | CHIUSO lato codice + RUNTIME CHIUSO | DoD runtime OPEN-001 (T27/T31) verdi su DeepSeek 2026-05-16 |
| M4 FileProvider (T32-T35) | CHIUSO lato codice + RUNTIME CHIUSO | T35 sim mode 5/5 VALID reale su DeepSeek 2026-05-16; scenari PLUMBING (OPEN-002) |
| M5 LCU Provider (T36-T40) | T36-T39 CHIUSI (codice+live-validati); T40 PARZIALE/IN SOSPESO | vedi sotto |
| M6a/M6b FastAPI+UI+suggest+errori | M6a IN CORSO: T41-T44+T46 CHIUSI (codice+runtime) | T41 main+config; T42 launcher; T43 `GET /`; T44 `GET /api/draft-state`+providers; T46 shell index.html Tailwind; T47 da fare |
| M7a/M7b Cache+History+SuggestionService+storico | NON iniziato | |
| M8 Test sistematici (T57-T65) | NON iniziato | T58/T62 dipendono da OPEN-002 |
| M9 Demo+packaging (T66-T71) | NON iniziato | |
| M10 Presentazione (T72-T73) | NON iniziato | |

## M5 dettaglio (T36-T40)

| Task | Stato | Note |
|---|---|---|
| T36 lockfile parser+discovery | CHIUSO + LIVE OK | `parse_lockfile`+`find_lockfile`+`psutil`; verificato live su path reale `E:\...` |
| T37 lcu_request httpx verify=False | CHIUSO + LIVE OK | HTTP 200 gameflow live; privacy `git grep lol-summoner` nessun match |
| T38 GameflowMonitor polling 2s | CHIUSO + LIVE OK | `ChampSelect` rilevato live |
| T39 parse champ-select + LCUProvider | CHIUSO + LIVE OK (parte non numerica) | `DraftState` reale live, mapping championId->nome OK, zero summoner |
| T40 test live LCU | **IN SOSPESO** | integrazione live VALIDATA; DoD numerico `>=5 bans / >=10 actions` NON soddisfatto in custom-vs-bot (INC-010 / spec 14.2). Da rieseguire `scripts/lcu_live_check.py` in un draft reale con ban (umani/tournament) |

## Cosa e' CHIUSO (non in sospeso)

- M0-M4 completi lato codice; M3/M4 runtime AI reale chiuso su DeepSeek (OPEN-001 parte runtime).
- M5/T36-T39 chiusi lato codice E validati live su PC casa (lockfile/psutil/`E:\`, auth, gameflow, champ-select parsing, mapping, privacy 10.1).
- Suite 69/69 PASSED.

## Cosa e' IN SOSPESO

1. **T40 DoD numerico** (`>=5 bans`, `>=10 actions`): non riproducibile in custom-vs-bot (INC-010, conferma di spec 14.2 / INC-001). Richiede un draft reale con ban effettivi. Rieseguire `scripts/lcu_live_check.py`. Mitigazione gia attiva: sim mode (`FileProvider`) 5/5 VALID.
2. **OPEN-002**: dati reali scenari benchmark 09/05 (`test_scenarios.md`) NON nel repo; mock attuali sono PLUMBING. Blocca la significativita di T57/T62 e del benchmark T58. Utente li fornisce da casa.
3. **OPEN-001 residuo**: revocare la API key OpenRouter esposta in chat (`...e26d34`) su openrouter.ai (INC-007). Non blocca codice (provider = DeepSeek).
4. **T58/T62**: benchmark p95 e panel valutatori, subordinati a OPEN-002.
5. **T05b**: reclutamento panel valutatori (1-2 amici Gold/Plat+), azione manuale utente non ancora fatta.
6. **Finding pytest** (PLOG-2026-05-15-032): `pytest` nudo dalla root collide su basename `test_sim_mode.py` (scripts vs tests). Workaround: usare `pytest tests/` (69/69). Fix opzionale non bloccante.

## Come riprendere

```powershell
git clone https://github.com/MrChuck118/live-draft-companion.git
cd live-draft-companion
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python -c "import asyncio; from app.data_dragon import populate_cache; asyncio.run(populate_cache())"
```

Poi creare `.env` da `.env.example` con `DEEPSEEK_API_KEY` reale (mai in chat, INC-007).

- Test completi: `.\.venv\Scripts\python.exe -m pytest tests/` (atteso 69/69).
- Verifica live LCU (T40): aprire LoL, entrare in champ select, poi
  `$env:PYTHONPATH="."; .\.venv\Scripts\python.exe scripts\lcu_live_check.py`.
- T41 CHIUSO 2026-05-16 (`app/main.py` FastAPI + lifecycle, `app/config.py` pydantic-settings; uvicorn runtime VERDE). Commit 3457994 su main.
- T42 CHIUSO 2026-05-16 (`launcher.py` in-process uvicorn + port fallback 8000->8003 + auto-browser; smoke reale: 8000 free->8000, 8000 busy->8001, HTTP 200). Commit 387b9f9 su main.
- T43 CHIUSO 2026-05-16 (`GET /` -> `templates/index.html` minimale; smoke reale GET / HTTP 200 text/html "In attesa del client LoL"). Commit e552945 su main.
- T44 CHIUSO 2026-05-16 (`GET /api/draft-state` + `app/providers.py` factory sim/live; smoke reale sim HTTP 200 application/json DraftState completo). Commit dff2c51 su main.
- T46 CHIUSO 2026-05-16 (`templates/index.html` shell completo Tailwind CDN: header/status/error-banner hidden/draft-grid/suggestions/history; suite 83/83; smoke reale GET / HTTP 200). Commit IN ATTESA di ok utente.
- T40 resta in sospeso ma il breakdown procede.
- Prossimo task: M6a/T47 (`static/app.js` Vanilla JS polling `/api/draft-state`).

## Riferimenti documentali

- `PROMPT_LOG.md`: registro iterazioni (ultimo: PLOG-2026-05-16-047).
- `INCIDENTS.md`: INC-001..INC-010.
- `SPEC_ERRATA.md`: ERRATA-001..ERRATA-006.
- `README.md`: stato sintetico corrente.
