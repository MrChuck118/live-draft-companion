# PROMPT_LOG.md

Registro delle iterazioni, dei prompt e delle decisioni operative del progetto Live Draft Companion.

Regola operativa: prima di chiudere ogni iterazione singola, aggiungere qui una entry con messaggi, contesto letto, decisioni prese, test o verifiche eseguite, e prossima azione.

## PLOG-2026-05-09-001 - Benchmark runtime modelli AI

- Data: 2026-05-09
- Fonte: `LiveDraftCompanion_TechnicalSpec_v2.3.md`, sezioni 7.2, 9.2, 14.2 e registro versioni.
- Scopo: benchmark preliminare dei modelli OpenRouter candidati per il runtime MVP.

### Risultati documentati

- `google/gemma-4-31b-it:free`: 1/3 chiamate riuscite; output JSON valido, compliance ban/pick OK, spiegazioni in italiano corrette, latenza osservata 12s; rate limit upstream dopo la prima chiamata.
- `qwen/qwen3-next-80b-a3b-instruct:free`: 0/3 nel benchmark citato per rate limit upstream Venice; mantenuto come fallback finale in Strategia A.
- `deepseek/deepseek-v4-flash`: 2/3 chiamate riuscite; costo stimato circa $0.0002 a chiamata; latenza osservata 17-26s; alcuni problemi di nomi item tradotti e mojibake da mitigare con validatori.
- `qwen/qwen3.6-plus`: 3/3 chiamate riuscite e qualita migliore, ma latenza 68-90s; escluso dal runtime live per incompatibilita con target p95 <=30s.

### Decisioni derivate

- Target latenza MVP: p95 <=30s, non <=10s.
- Strategia default post-errata: Strategia A free-only.
- Vincoli prompt da mantenere: `explanation` in italiano, nomi champion/item/rune in inglese Data Dragon, UTF-8 esplicito e anti-mojibake.

## PLOG-2026-05-11-001 - Orientamento pre-build / Lez 4

- Data: 2026-05-11
- Modalita: sola lettura e piano; nessuna costruzione del prodotto avviata.
- Stato richiesta: piano esposto all'utente e approvato.

### Messaggi catalogati

- USER-001: chiede di usare `prompt_log` come registro di ogni iterazione prima dell'output, usare `incidents` per gli incidenti, iniziare a seguire il breakdown dalla prima lezione prendendo la data odierna, leggere integralmente i tre documenti indicati, controllare la repo, elaborare un piano validato, proporre README riassuntivo, e non inventare/ne iniziare a costruire.
- CODEX-001: comunica che operera in sola lettura e piano, leggendo i tre documenti, la repo locale e i file `prompt_log`/`incidents`.
- CODEX-002: comunica che `C:\LiveDraftCompanion` contiene solo `prompt_log` e `incidents`, entrambi vuoti, e non e una repo Git.
- CODEX-003: comunica che il breakdown indica come prima unita M0/T01-T05b, ma che esiste una discrepanza pratica da risolvere perche la workspace aperta non e la clone prevista.
- CODEX-004: comunica che la verifica web diretta del link GitHub non ha restituito contenuto utile e passa a verifica tecnica `git ls-remote`.
- CODEX-005: comunica che il remoto esiste, `main` punta a `0ca1767`, e clona in `C:\tmp\live-draft-companion-inspect` per ispezione separata.
- CODEX-006: comunica che aggiornera solo i registri locali prima della risposta finale, come documentazione di processo.

### Materiale letto/verificato

- `C:\Users\user\Downloads\breakdown_tasks_v2.1_corretto.md`
  - righe lette: 917
  - dimensione: 61636 byte
  - SHA256: F36B26B2567AADCA8B6540AD5A34FC372CB3E85532BED6DECBD5BFB23E443232
- `C:\Users\user\Downloads\LiveDraftCompanion_TechnicalSpec_v2.3.md`
  - righe lette: 972
  - dimensione: 75801 byte
  - SHA256: 40812730AB0D93A46E1E40547656F33040F4169A1E4DBE40AC4A659BE0473878
- `C:\Users\user\Downloads\LiveDraftCompanion_SPEC_ERRATA.md`
  - righe lette: 183
  - dimensione: 11013 byte
  - SHA256: 67EAAFDA08C04CEDFE81F6BB491E14FDD29DF80A3E11CDAE203F58E5803565C0
- Workspace locale `C:\LiveDraftCompanion`
  - non era una repo Git
  - conteneva solo `prompt_log` e `incidents`
- Repo GitHub `https://github.com/MrChuck118/live-draft-companion`
  - `git ls-remote` riuscito
  - `main`/`HEAD`: `0ca1767cf18ca55aea0f5c3047fa7126f8158d15`
  - clone di ispezione in `C:\tmp\live-draft-companion-inspect`
  - file repo attuali: `README.md`, `LICENSE`, `.gitignore`
  - README attuale: placeholder breve
  - LICENSE: MIT
  - `.gitignore`: template Python; include `.env`, `build/`, `dist/`, `*.spec`; manca esplicitamente gestione tracciabile di `logs/` e manca un pattern generico `*.db`

### Piano approvato

- Riallineare `C:\LiveDraftCompanion` alla repo GitHub ufficiale preservando i registri locali.
- Normalizzare i registri in `PROMPT_LOG.md` e `INCIDENTS.md`.
- Chiudere la parte verificabile di M0/T01.
- Preparare struttura M0/T02.
- Preparare documentazione base M0/T05.
- Preparare `.env.example`, `.gitignore` e README iniziale.
- Non iniziare codice applicativo prima di ulteriore approvazione.

## PLOG-2026-05-11-002 - M0 setup repo, documentazione e ambiente

- Data: 2026-05-11
- Stato: completato fino a T03b con errata operativa su `psutil`.
- Scope: setup repository, struttura directory, registri canonici, `.env.example`, README iniziale, virtualenv e installazione dipendenze.

### Messaggi catalogati

- USER-002: approva il piano con "ok piano pefetto procediamo".
- CODEX-007: comunica che procedera con M0 senza codice applicativo.
- CODEX-008: comunica che inizializza Git nella cartella corrente e aggancia `origin/main` preservando i registri locali.
- CODEX-009: comunica che il problema `dubious ownership` viene gestito con `safe.directory` temporaneo.
- CODEX-010: comunica che crea struttura M0 e file canonici.
- CODEX-011: comunica che provera T03/T03b, cioe Python, requirements, virtualenv e verifica `psutil`.
- CODEX-012: comunica che `python` e `py` non sono nel PATH, ma Python 3.12.10 esiste al percorso assoluto.
- CODEX-013: comunica che `psutil<5.7.0` fallisce su Python 3.12.10 e che applichera ERRATA-004.
- CODEX-014: comunica che con pin corretto l'ambiente passa, import core OK e `psutil` importa come `7.2.2`.

### Azioni eseguite

- Inizializzata `C:\LiveDraftCompanion` come repo Git locale.
- Aggiunto remote `origin` a `https://github.com/MrChuck118/live-draft-companion.git`.
- Eseguito fetch di `origin/main` e checkout locale di `main`.
- Creati registri canonici `PROMPT_LOG.md` e `INCIDENTS.md`.
- Creati `README.md`, `.env.example`, `requirements.txt`, `SPEC_ERRATA.md`.
- Creata struttura directory: `app/`, `static/`, `templates/`, `prompts/`, `tests/mock_drafts/`, `logs/`, `scripts/`.
- Aggiunti `.gitkeep` alle directory vuote.
- Aggiornato `.gitignore` per `.env`, log runtime, database SQLite, build, dist e spec PyInstaller.
- Creata `.venv` con Python 3.12.10.
- Installate dipendenze dopo correzione pin `psutil`.

### Verifiche eseguite

- `git ls-remote` su repo ufficiale: OK, `main` a `0ca1767cf18ca55aea0f5c3047fa7126f8158d15`.
- `.\.venv\Scripts\python.exe -c "from fastapi import FastAPI; from openai import OpenAI; from sqlalchemy import create_engine; print('OK')"`: OK.
- `.\.venv\Scripts\python.exe -c "import psutil; print(psutil.__version__)"`: `7.2.2`.
- `git check-ignore .env logs/test.log data_dragon.db build/test.txt dist/test.txt app.spec`: tutti ignorati.

### Incidenti collegati

- `INC-002`: workspace locale non allineata alla repo GitHub, risolto.
- `INC-003`: `psutil<5.7.0` non installabile su Python 3.12.10, risolto con ERRATA-004.
- `INC-004`: `python` e `py` non presenti nel PATH della sessione, mitigato.

### Prossima azione proposta

Passare a M1/T06 `data_dragon.py` e `fetch_versions()`.

### Commit e push

- Commit setup M0: `96bd181` (`T01-T05: initialize project setup`).
- Push su `origin/main`: riuscito, remoto aggiornato da `0ca1767` a `96bd181`.

## PLOG-2026-05-11-003 - Audit dipendenze pc its

- Data: 2026-05-11
- Scope: controllare librerie e dipendenze necessarie su questo PC, chiamato `pc its`, installare/scaricare cio che manca e aggiornare una checklist Markdown.
- Output prodotto: `PC_ITS_DEPENDENCIES_CHECKLIST.md`.

### Messaggi catalogati

- USER-003: chiede di controllare tutte le librerie e dipendenze necessarie su questo PC, chiamarlo `pc its`, creare una checklist in Markdown, scaricare le dipendenze mancanti installabili e aggiornare la checklist.
- CODEX-015: comunica che fara audit reale, checklist, installazione delle mancanze gestibili e aggiornamento finale.
- CODEX-016: comunica che Git, `.venv`, `pip check` e pacchetti Python principali risultano OK, ma `python` e `py` non sono nel PATH.
- CODEX-017: comunica che gli import Python sono OK e che le CLI saranno verificate con `python -m`.
- CODEX-018: comunica che crea la checklist `pc its` e distingue tra dipendenze installabili e azioni manuali.

### Verifiche eseguite

- `git status --short`: working tree inizialmente pulito.
- `git --version`: `2.53.0.windows.3`.
- `where.exe python py`: nessun interprete nel PATH.
- `.\.venv\Scripts\python.exe --version`: `Python 3.12.10`.
- `.\.venv\Scripts\python.exe -m pip --version`: `pip 25.0.1`.
- `.\.venv\Scripts\python.exe -m pip check`: nessun requisito rotto.
- Import diretti: `fastapi`, `uvicorn`, `jinja2`, `httpx`, `pydantic`, `pydantic_settings`, `sqlalchemy`, `aiosqlite`, `openai`, `dotenv`, `sse_starlette`, `PyInstaller`, `pytest`, `pytest_asyncio`, `psutil`: OK.
- CLI via `python -m`: PyInstaller `6.20.0`, pytest `9.0.3`, uvicorn `0.46.0`.
- `pip install -r requirements.txt`: tutte le dipendenze gia soddisfatte.
- Data Dragon versions endpoint: HTTP 200.
- OpenRouter models endpoint: HTTP 200.
- Tailwind CDN: HTTP 200 dopo redirect.
- Browser: Edge e Chrome presenti; Firefox assente.
- LoL client/lockfile: non rilevati nei path standard `C:\Riot Games` ed `E:\Riot Games`.
- `.env`: assente; richiede configurazione manuale con API key reale.

### Esito

- Nessuna libreria Python mancante da scaricare.
- Checklist creata e aggiornata.
- Residui manuali: aggiungere Python al PATH se desiderato, configurare `.env`, installare LoL solo se si vuole live mode su pc its.

## PLOG-2026-05-11-004 - Chiarimento errata su `httpx` vs Vanilla JS

- Data: 2026-05-11
- Scope: chiarire se `httpx` sia stato sostituito dall'ERRATA-002.

### Messaggi catalogati

- USER-004: segnala che la spec errata ha valenza maggiore della spec v2.3 e chiede se `httpx` sia stato sostituito da Vanilla JS, oppure se sta interpretando male.
- CODEX-019: verifica `SPEC_ERRATA.md` locale, `LiveDraftCompanion_SPEC_ERRATA.md` originale e `LiveDraftCompanion_TechnicalSpec_v2.3.md`.

### Verifica

- ERRATA-002 riguarda la riga UI/Frontend: `HTML + CSS (Tailwind via CDN) + Vanilla JS + fetch`.
- ERRATA-002 chiude la decisione frontend e scarta HTMX dal MVP.
- La spec v2.3 mantiene `httpx` come client HTTP backend per LCU, Data Dragon e OpenRouter.
- Nessuna voce errata sostituisce `httpx`.

### Decisione

- La precedenza dell'errata e confermata.
- Interpretazione corretta: Vanilla JS + `fetch` sostituisce HTMX/Jinja server-rendered come scelta frontend, non `httpx`.
- `httpx` resta in `requirements.txt`.
- README e checklist pc its sono stati aggiornati per indicare esplicitamente `httpx` come backend-only.

## PLOG-2026-05-11-005 - Chiarimento su `requirements.txt`

- Data: 2026-05-11
- Scope: spiegare il ruolo di `requirements.txt`.

### Messaggi catalogati

- USER-005: chiede "`requirements.txt`? cos'e?"
- CODEX-020: spiega che `requirements.txt` e il file standard Python che elenca le librerie da installare nella virtualenv del progetto con `pip install -r requirements.txt`.

### Decisione

- `requirements.txt` resta nel repo per rendere replicabile il setup su pc its, PC di casa o PC Academy.
- Le dipendenze elencate sono backend/tooling Python, non librerie frontend.
