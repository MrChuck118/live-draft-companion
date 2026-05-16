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
- Suite test: 132/132 PASSED (`pytest tests/`)
- Prossimo task tecnico: M8/T60 (fallback chain integration test). M6a + M6b + M7a + M7b COMPLETI; M8/T57-T59 CHIUSI. M5/T40 resta IN SOSPESO (vedi In sospeso), procede per scelta utente

## Avanzamento per modulo

| Modulo | Stato | Note |
|---|---|---|
| M0 Setup (T01-T05b) | CHIUSO (T05b manuale a parte) | bootstrap PC casa validato; cache Data Dragon ripopolata (INC-009); venv ripristinata dopo rottura interprete locale (INC-012); T05b reclutamento panel = azione manuale utente, non fatta |
| M1 Data Dragon (T06-T12) | CHIUSO | patch 16.10.1, 172 champ / 705 item / 17 keystone; ERRATA-004 (psutil), ERRATA-005 (Luden) |
| M2 Models+Validators (T13-T22) | CHIUSO | 28 test validators |
| M3 Prompt+AIClient (T23-T31) | CHIUSO lato codice + RUNTIME CHIUSO | DoD runtime OPEN-001 (T27/T31) verdi su DeepSeek 2026-05-16 |
| M4 FileProvider (T32-T35) | CHIUSO lato codice + RUNTIME CHIUSO | T35 sim mode 5/5 VALID reale su DeepSeek 2026-05-16; scenari PLUMBING (OPEN-002) |
| M5 LCU Provider (T36-T40) | T36-T39 CHIUSI (codice+live-validati); T40 PARZIALE/IN SOSPESO | vedi sotto |
| M6a FastAPI base + UI shell | **COMPLETO** (T41-T44+T46+T47) | main+config, launcher, `GET /`, `GET /api/draft-state`+providers, shell Tailwind, app.js polling 2s |
| M6b suggest endpoint + UI + errori | **COMPLETO** (T45+T48+T49+T49b) | endpoint sottile; render 3 card; spinner+disclaimer; contratto errori uniforme + banner UI + log ERROR |
| M7a Cache+History+SuggestionService | **COMPLETO** (T50-T53 + T45b) | tabelle single-DB; CacheService; HistoryRepository; SuggestionService orchestratore |
| M7b storico feedback UI | **COMPLETO** (T54-T56) | T54 endpoint feedback; T55 GET history; T56 UI storico + feedback |
| M8 Test sistematici (T57-T65) | IN CORSO (T57-T59 chiusi; prossimo T60) | 15 mock draft strutturali in repo; T58 plumbing benchmark eseguito; T59 cache hit OK; qualita output aperta in INC-013; T62 resta dipendente da OPEN-002/T05b |
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
- Suite 132/132 PASSED.

## Cosa e' IN SOSPESO

1. **T40 DoD numerico** (`>=5 bans`, `>=10 actions`): non riproducibile in custom-vs-bot (INC-010, conferma di spec 14.2 / INC-001). Richiede un draft reale con ban effettivi. Rieseguire `scripts/lcu_live_check.py`. Mitigazione gia attiva: sim mode (`FileProvider`) 5/5 VALID.
2. **OPEN-002**: dati reali scenari benchmark 09/05 (`test_scenarios.md`) NON nel repo; i 15 mock T57 sono scenari strutturali/PLUMBING. T58 e stato eseguito come benchmark plumbing; la significativita reale di qualita/panel T62 resta bloccata. Utente li fornisce da casa.
3. **OPEN-001 residuo**: revocare la API key OpenRouter esposta in chat (`...e26d34`) su openrouter.ai (INC-007). Non blocca codice (provider = DeepSeek).
4. **T62 / benchmark reale semantico**: panel valutatori e giudizio qualita subordinati a OPEN-002 + T05b.
5. **T05b**: reclutamento panel valutatori (1-2 amici Gold/Plat+), azione manuale utente non ancora fatta.
6. **Finding pytest** (PLOG-2026-05-15-032): `pytest` nudo dalla root collide su basename `test_sim_mode.py` (scripts vs tests). Workaround: usare `pytest tests/` (atteso 132/132 quando l'ambiente Python e funzionante). Fix opzionale non bloccante.

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

- Test completi: `.\.venv\Scripts\python.exe -m pytest tests/` (atteso 132/132; se fallisce per interprete mancante, vedi INC-012 e ricrea la venv con un Python 3.12 valido).
- Verifica live LCU (T40): aprire LoL, entrare in champ select, poi
  `$env:PYTHONPATH="."; .\.venv\Scripts\python.exe scripts\lcu_live_check.py`.
- T41 CHIUSO 2026-05-16 (`app/main.py` FastAPI + lifecycle, `app/config.py` pydantic-settings; uvicorn runtime VERDE). Commit 3457994 su main.
- T42 CHIUSO 2026-05-16 (`launcher.py` in-process uvicorn + port fallback 8000->8003 + auto-browser; smoke reale: 8000 free->8000, 8000 busy->8001, HTTP 200). Commit 387b9f9 su main.
- T43 CHIUSO 2026-05-16 (`GET /` -> `templates/index.html` minimale; smoke reale GET / HTTP 200 text/html "In attesa del client LoL"). Commit e552945 su main.
- T44 CHIUSO 2026-05-16 (`GET /api/draft-state` + `app/providers.py` factory sim/live; smoke reale sim HTTP 200 application/json DraftState completo). Commit dff2c51 su main.
- T46 CHIUSO 2026-05-16 (`templates/index.html` shell completo Tailwind CDN). Commit d096474 su main.
- T47 CHIUSO 2026-05-16 (`static/app.js` Vanilla JS polling 2s + mount StaticFiles + wiring shell). **M6a COMPLETO**. Commit 1cd8928 su main.
- T50 CHIUSO 2026-05-16 (`app/db.py` tabelle `cache`+`history` single-DB; ERRATA-007 + INC-011, Opzione A). Commit 92697ce su main.
- T51 CHIUSO 2026-05-16 (`CacheService` get/set in `app/suggestion_service.py`, NON in ai_client.py; TTL 30gg). Commit cc57934 su main.
- T52 CHIUSO 2026-05-16 (verifica salvataggio cache: TTL 30gg + persistenza su disco/restart). Commit 2a93b59 su main.
- T53 CHIUSO 2026-05-16 (`HistoryRepository.save`). Commit 2ca52f9 su main.
- T45b CHIUSO 2026-05-16 (`SuggestionService` orchestratore). **M7a COMPLETO**. Commit 498e63e su main.
- T45 CHIUSO 2026-05-16 (`POST /api/suggest` sottile -> SuggestionService). Commit 04684a2 su main.
- T48 CHIUSO 2026-05-16 (`static/app.js` render 3 card). Commit 9726b1e su main.
- T49 CHIUSO 2026-05-16 (spinner + disclaimer RF-019 sopra suggerimenti). Commit 48ed05b su main.
- T49b CHIUSO 2026-05-16 (contratto errori uniforme `{error_code,user_message}` 422/502/503, handler RequestValidationError, log ERROR `logs/errors.log`, banner UI showError/clearError/scrollIntoView, bottone mai disabilitato; suite 110/110; smoke reale conforme). **M6b COMPLETO**. Nessun nuovo pattern errore -> niente INCIDENTS. Commit 04a14fa su main.
- T54 CHIUSO 2026-05-16 (`POST /api/history/feedback` -> `HistoryRepository.update_feedback`, validazione `good|bad`, 404 record assente, contratto errori uniforme; suite 115/115). M7b avviato.
- T55 CHIUSO 2026-05-16 (`GET /api/history` -> array JSON ultime 50 entries, newest-first, con `id`, `timestamp`, `draft_state`, `output`, `model_used`, `feedback`; suite 118/118).
- T56 CHIUSO 2026-05-16 (`static/app.js` storico UI: fetch `GET /api/history`, render righe compatte, bottoni `Utile`/`Inutile` -> `POST /api/history/feedback`, conferma visiva `aria-pressed`, banner T49b sugli errori; suite 119/119). **M7b COMPLETO**.
- T57 CHIUSO 2026-05-16 (15 scenari JSON in `tests/mock_drafts/`, 3 per ruolo TOP/JUNGLE/MID/ADC/SUPPORT, copertura AD-heavy/AP-heavy/balanced + edge first/last pick, aggressive bans, meta picks out; tutti caricabili via FileProvider; suite 131/131). Nota: scenari PLUMBING, non dati benchmark reali OPEN-002.
- T58 CHIUSO 2026-05-16 (`scripts/benchmark_30_calls.py`; 30 chiamate reali DeepSeek in sim mode, cache bypass; 17/30 success, p95_all 4166 ms <= 30000 ms, fallback 0%, rate limit 0, timeout 0, token usage 25698 prompt / 9285 completion, cost reported `null` per response SDK; report `logs/benchmark_30_calls_20260516_212130.json`). INC-013 aperto per 13/30 `ai_output_invalid` post-validator.
- T59 CHIUSO 2026-05-16 (`scripts/test_cache_hit.py`; scenario `last_pick_support` eseguito 2 volte: prima run 1 riga `logs/ai_calls_*.jsonl`, seconda run 0 righe, log `cache hit` presente; suite 132/132). Primo tentativo su `ad_heavy_top` ha confermato INC-013 (`ai_output_invalid`), poi scenario stabile OK.
- T40 resta in sospeso ma il breakdown procede.
- Prossimo task: M8/T60 (fallback chain integration test).

## Riferimenti documentali

- `PROMPT_LOG.md`: registro iterazioni (ultimo: PLOG-2026-05-16-065).
- `INCIDENTS.md`: INC-001..INC-013.
- `SPEC_ERRATA.md`: ERRATA-001..ERRATA-007.
- `README.md`: stato sintetico corrente.
