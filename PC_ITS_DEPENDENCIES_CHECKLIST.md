# PC ITS - Dependency Checklist

Data audit: 2026-05-11  
Macchina: pc its  
Repository: `C:\LiveDraftCompanion`  
Branch: `main`  
Remote: `https://github.com/MrChuck118/live-draft-companion.git`

## Sintesi

- Stato finale ambiente Python MVP: pronto.
- Dipendenze Python richieste da `requirements.txt`: installate.
- Conflitti pip: assenti.
- Dipendenze esterne raggiungibili: Data Dragon, OpenRouter model listing, Tailwind CDN.
- Mancanze residue: `python`/`py` non sono nel PATH, `.env` con API key non configurato, League of Legends non presente su questo PC.

## Checklist Sistema

| Voce | Richiesta | Stato iniziale | Azione eseguita | Stato finale | Note |
|---|---|---|---|---|---|
| Sistema operativo | Windows 10/11 | Windows 10 Pro rilevato | Nessuna | OK | `Get-ComputerInfo` indica Windows 10 Pro; alcune query CIM sono negate da policy PC |
| Git | Necessario | Presente | Verificato | OK | `git version 2.53.0.windows.3` |
| Repository locale | Necessario | Presente e pulito | Verificato | OK | `origin/main`, ultimo commit locale/remoto `80a2166` prima di questa checklist |
| Python runtime | Python 3.12.10 | Presente in `.venv` | Verificato | OK | `.\.venv\Scripts\python.exe --version` -> `Python 3.12.10` |
| Python nel PATH | Consigliato | Mancante | Non modificato | Warning | `where.exe python py` non trova interpreti; usare `.venv` o percorso assoluto |
| Virtualenv | Necessaria | Presente | Verificata | OK | `.venv` ignorata da Git |
| pip | Necessario | Presente | Verificato | OK | `pip 25.0.1`; update disponibile ma non necessario |
| Browser | Necessario per UI | Edge e Chrome presenti | Verificato | OK | Firefox non presente; basta un browser default |
| Microsoft C++ Build Tools | Non richiesto dopo ERRATA-004 | Non rilevato | Nessuna | OK | Non serve con `psutil>=5.9.8,<8` perche usa wheel |
| League of Legends client | Necessario solo live mode | Non rilevato | Non installato | Manuale | Su pc its usare sim mode; live mode richiede installazione manuale |
| `.env` | Necessario per chiamate AI reali | Assente | Non creato con placeholder | Manuale | Creare da `.env.example` e inserire `OPENROUTER_API_KEY` reale |

## Checklist Librerie Python Dirette

Tutte le dipendenze sotto sono installate nella virtualenv `C:\LiveDraftCompanion\.venv`.

| Pacchetto | Richiesto da | Stato iniziale | Azione eseguita | Versione finale | Stato finale |
|---|---|---|---|---|---|
| `fastapi` | Backend API locale | Installato | Verifica import | `0.136.1` | OK |
| `uvicorn[standard]` | ASGI server | Installato | Verifica `python -m uvicorn --version` | `0.46.0` | OK |
| `jinja2` | Template HTML | Installato | Verifica import | `3.1.6` | OK |
| `httpx` | HTTP client backend per LCU/Data Dragon/OpenRouter | Installato | Verifica import | `0.28.1` | OK |
| `pydantic` | Modelli e validazione | Installato | Verifica import | `2.13.4` | OK |
| `pydantic-settings` | Config `.env` | Installato | Verifica import | `2.14.1` | OK |
| `sqlalchemy` | SQLite ORM | Installato | Verifica import | `2.0.49` | OK |
| `aiosqlite` | SQLite async | Installato | Verifica import | `0.22.1` | OK |
| `openai` | SDK OpenRouter-compatible | Installato | Verifica import | `2.36.0` | OK |
| `python-dotenv` | Lettura `.env` | Installato | Verifica import | `1.2.2` | OK |
| `sse-starlette` | SSE opzionale | Installato | Verifica import | `3.4.2` | OK |
| `pyinstaller` | Build `.exe` | Installato | Verifica `python -m PyInstaller --version` | `6.20.0` | OK |
| `pytest` | Test | Installato | Verifica `python -m pytest --version` | `9.0.3` | OK |
| `pytest-asyncio` | Test async | Installato | Verifica import | `1.3.0` | OK |
| `psutil` | LCU process discovery | Installato con errata | Reinstall confermato | `7.2.2` | OK |

## Checklist Dipendenze Transitive Critiche

| Pacchetto | Uso | Versione finale | Stato |
|---|---|---|---|
| `starlette` | Base FastAPI/SSE | `1.0.0` | OK |
| `httptools` | Uvicorn standard | `0.7.1` | OK |
| `watchfiles` | Uvicorn reload/watch | `1.1.1` | OK |
| `websockets` | Uvicorn standard | `16.0` | OK |
| `PyYAML` | Uvicorn standard | `6.0.3` | OK |
| `pyinstaller-hooks-contrib` | PyInstaller hooks | `2026.5` | OK |
| `pywin32-ctypes` | PyInstaller Windows support | `0.2.3` | OK |
| `sqlite3` | SQLite stdlib Python | `3.49.1` | OK |

## Checklist Servizi Esterni

| Servizio | Richiesto da | Verifica | Stato finale | Note |
|---|---|---|---|---|
| Data Dragon | M1 cache LoL | `GET https://ddragon.leagueoflegends.com/api/versions.json` -> HTTP 200 | OK | Necessario per T06-T12 |
| OpenRouter API | AI runtime | `GET https://openrouter.ai/api/v1/models` -> HTTP 200 | OK | Chiamate reali richiedono API key |
| Tailwind CDN | UI via CDN | `GET https://cdn.tailwindcss.com` con redirect -> HTTP 200 | OK | Versione servita: `/3.4.17` |
| GitHub remote | Version control | `origin` configurato | OK | Push gia funzionante in iterazione precedente |
| LCU locale | Live mode | Client/lockfile non presenti | Manuale | Atteso su pc its se non c'e LoL installato |

## Installazione / Download Eseguiti

- Eseguito `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
- Esito: tutte le dipendenze risultavano gia installate (`Requirement already satisfied`).
- Nessuna nuova libreria Python mancante da scaricare.
- Nessun pacchetto esterno pesante installato manualmente: LoL client e API key OpenRouter richiedono intervento utente.

## Comandi Di Verifica Utili Su PC ITS

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest --version
.\.venv\Scripts\python.exe -m uvicorn --version
.\.venv\Scripts\python.exe -m PyInstaller --version
```

## Note Operative

- Su pc its usare sempre `.\.venv\Scripts\python.exe` invece di `python`, finche Python non viene aggiunto al PATH.
- Le entrypoint `.exe` in `.venv\Scripts` possono dare falsi negativi in ambienti sandbox; le verifiche robuste passano da `python -m`.
- `httpx` resta una dipendenza backend Python. L'ERRATA-002 sostituisce HTMX con Vanilla JS + `fetch` nel frontend, non sostituisce `httpx`.
- Per sviluppo e demo su pc its, partire in modalita simulazione:

```env
DRAFT_PROVIDER_MODE=sim
DRAFT_PROVIDER_FILE=tests/mock_drafts/balanced_mid.json
```

- Prima delle chiamate AI reali serve creare `.env` da `.env.example` e inserire `OPENROUTER_API_KEY`.
