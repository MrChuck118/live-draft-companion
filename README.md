# Live Draft Companion

Live Draft Companion e un assistente AI desktop per la fase di draft di League of Legends, sviluppato come progetto per il corso AI Projects Development di ITS ICT Academy Roma.

L'obiettivo del MVP e leggere automaticamente lo stato del champion select tramite LCU API, generare 3 suggerimenti di pick per il ruolo dell'utente, mostrare build essenziale, keystone rune e spiegazione in italiano, e mantenere tutto entro un target di latenza p95 di 30 secondi.

## Stato Attuale

- Data avvio iterazione build: 2026-05-11
- Specifica di riferimento: v2.3 FROZEN del 2026-05-09
- Errata di riferimento: v1 del 2026-05-11
- Breakdown operativo: v2.1 del 2026-05-11
- Modalita operativa: Demo Mode First
- Provider AI: DeepSeek API diretta (`deepseek-chat` primario, `deepseek-reasoner` fallback). Strategia A/B OpenRouter superata (vedi ERRATA-006, 2026-05-15)
- Frontend MVP: HTML, Tailwind CDN, Vanilla JS + fetch
- Stato codice applicativo: M3, M4 chiusi; M5/T36-T39 chiusi lato codice E validati live su PC casa (lockfile/psutil su path reale E:\, auth, gameflow, champ-select parsing, mapping championId->nome, privacy 10.1). DoD runtime OPEN-001 (T27/T31/T35) CHIUSE su DeepSeek 2026-05-16 (5/5 sim VALID). M6a IN CORSO: T41 CHIUSO (`app/main.py` FastAPI + lifecycle, `app/config.py` pydantic-settings; uvicorn runtime VERDE, log `App ready`), T42 CHIUSO (`launcher.py` in-process uvicorn + port fallback 8000->8003 + auto-browser; smoke reale: 8000 free->8000, busy->8001, HTTP 200), T43 CHIUSO (`GET /` -> `templates/index.html` minimale; smoke reale GET / HTTP 200 "In attesa del client LoL"), T44 CHIUSO (`GET /api/draft-state` + `app/providers.py` factory sim/live; smoke reale sim HTTP 200 application/json DraftState completo), T46 CHIUSO (`templates/index.html` shell completo Tailwind CDN), T47 CHIUSO (`static/app.js` Vanilla JS polling 2s + mount StaticFiles). **M6a COMPLETO** (T41-T44+T46+T47). M7a IN CORSO: T50 CHIUSO (tabelle `cache`+`history` single-DB; ERRATA-007/INC-011), T51 CHIUSO (`CacheService` get/set in `suggestion_service.py`, TTL 30gg), T52 CHIUSO (verifica salvataggio cache: TTL 30gg + persistenza su disco/restart), T53 CHIUSO (`HistoryRepository.save` feedback=unrated + model_used), T45b CHIUSO (`SuggestionService` orchestratore hash/cache/prompt/AI-chain/validate/save). **M7a COMPLETO**. M6b IN CORSO: T45 CHIUSO (`POST /api/suggest` sottile -> SuggestionService; 422/503 controllati), T48 CHIUSO (`static/app.js` bottone -> POST /api/suggest -> render 3 card), T49 CHIUSO (loading spinner durante chiamata AI + disclaimer RF-019 sopra i suggerimenti). Suite 105/105 PASSED
- M5/T40 IN SOSPESO: integrazione live validata, ma DoD numerico (>=5 bans, >=10 actions) non riproducibile in custom-vs-bot (INC-010, conferma spec 14.2/INC-001); da rieseguire `scripts/lcu_live_check.py` in un draft reale con ban. Mitigazione gia attiva (sim mode 5/5). Il breakdown procede comunque (scelta utente)
- Prossimo task tecnico: M6b/T49b (error banner + stato errori UI/backend); chiusura T40 quando disponibile un draft reale con ban
- Stato dettagliato e cose in sospeso: vedi `BREAKDOWN_STATUS.md`
- Open issues (da rivedere): OPEN-001 - parte runtime sbloccabile CHIUSA su DeepSeek (T27/T31/T35 verdi, INC-008 risolto, ERRATA-006); residui: revocare la key OpenRouter esposta (INC-007); T58/T62 ancora aperti perche subordinati a OPEN-002. OPEN-002 dati scenario benchmark 09/05 (test_scenarios.md) NON nel repo, utente li aggiunge da casa, nel frattempo scenari plumbing documentati

## Funzionalita MVP

- App Windows distribuita come `.exe` con backend FastAPI locale e UI browser su `localhost`.
- Lettura del client League of Legends via LCU API con lockfile e `httpx` lato backend.
- Modalita simulazione tramite `FileProvider`, basata su draft state JSON.
- Data Dragon cache locale per campioni, oggetti e rune.
- Prompt AI con vincoli rigidi: spiegazioni in italiano, nomi champion/item/rune in inglese, output JSON validato.
- Chain di fallback modelli AI configurabile da `.env`.
- Cache locale degli output AI per draft state identici.
- Storico SQLite dei consigli con feedback utente.
- Error handling visibile in UI per problemi LCU, rete, timeout AI, rate limit e output non valido.

## Stack Tecnico

- Python 3.12.10
- FastAPI + uvicorn
- HTML/CSS/JavaScript con Tailwind via CDN
- httpx async lato backend per LCU e Data Dragon
- Vanilla JS + fetch lato frontend per chiamare le API locali
- Pydantic v2 + pydantic-settings
- SQLite + SQLAlchemy + aiosqlite
- DeepSeek API diretta tramite SDK OpenAI-compatible
- PyInstaller per packaging Windows
- pytest / pytest-asyncio per test

## Struttura Prevista

```text
app/                 Backend FastAPI, provider, servizi, modelli e validatori
static/              JavaScript e asset statici UI
templates/           Template HTML
prompts/             System prompt e user template
tests/mock_drafts/   Draft state JSON per modalita simulazione
logs/                Log locali non versionati
scripts/             Script di test, benchmark e utilita
```

## Setup Previsto

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -c "import asyncio; from app.data_dragon import populate_cache; asyncio.run(populate_cache())"
```

Poi configurare `DEEPSEEK_API_KEY` in `.env` e scegliere modalita live o simulazione. La key DeepSeek va scritta solo nel file `.env` locale, mai in chat o in file versionati (vedi INC-007).

Il comando `populate_cache()` scarica i dati statici da Data Dragon e crea la cache locale `data_dragon.db` (gitignored). Su una macchina pulita questo passo e prerequisito alla suite test: senza, i validator di legality falliscono con `no such table: champions` (vedi INC-009).

## Modalita Simulazione

La modalita simulazione e prioritaria per ridurre il rischio demo:

```env
DRAFT_PROVIDER_MODE=sim
DRAFT_PROVIDER_FILE=tests/mock_drafts/balanced_mid.json
```

## Documentazione Di Processo

- `PROMPT_LOG.md`: registro prompt, iterazioni, benchmark e decisioni.
- `INCIDENTS.md`: registro incidenti, rischi tecnici e mitigazioni.

## Disclaimer

I suggerimenti sono generati da AI e possono sbagliare. La decisione finale resta sempre al giocatore. L'app non automatizza azioni nel client di gioco e non deve leggere o trasmettere summoner name o altri dati personali non necessari.
