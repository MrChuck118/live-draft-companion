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
- Stato codice applicativo: M3, M4 chiusi e M5/T36-T37 chiusi lato codice (T23-T37: prompts, ai_client chain/validation/logging, DraftStateProvider, FileProvider, 5 mock draft, sim mode script, LCU lockfile parser+discovery, lcu_request httpx verify=False privacy-safe). DoD runtime OPEN-001 (T27/T31/T35) CHIUSE su DeepSeek diretto il 2026-05-16 (5/5 sim VALID). Suite 60/60 PASSED
- Prossimo task tecnico: M5/T38 polling gameflow session (asyncio, ogni 2s) (M5 = Should)
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
