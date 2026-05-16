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

## PLOG-2026-05-11-006 - Perche `httpx` resta in `requirements.txt`

- Data: 2026-05-11
- Scope: chiarire perche `httpx` compare tra le dipendenze Python.

### Messaggi catalogati

- USER-006: chiarisce che la domanda era allusiva: voleva sapere perche `httpx` fosse nella lista `requirements.txt`.
- CODEX-021: ribadisce che `httpx` serve al backend, non al frontend.

### Verifica

- Spec v2.3: `httpx` e indicato per LCU API diretta, Data Dragon/OpenRouter HTTP client e setup replicabile.
- ERRATA-002: sostituisce HTMX con Vanilla JS + `fetch` solo nel frontend.
- Breakdown T06-T12: Data Dragon richiede chiamate HTTP dal backend.
- Breakdown T36-T37: LCU provider richiede chiamate HTTP backend con `verify=False`.

### Decisione

- `httpx` resta in `requirements.txt`.
- Motivazione: backend Python deve chiamare Data Dragon, LCU locale e, se necessario, servizi HTTP esterni. Vanilla JS + `fetch` vale solo per il browser che chiama le API FastAPI locali.

## PLOG-2026-05-11-007 - Handoff prima cambio PC

- Data: 2026-05-11
- Scope: verificare commit/push, controllare coerenza delle operazioni fatte finora, creare un file Markdown sul Desktop con lo stato del breakdown.

### Messaggi catalogati

- USER-007: comunica che deve andare a casa e continuera su un altro PC; chiede di controllare commit/push, validare le operazioni fatte finora e creare un file Markdown sul Desktop fuori dal progetto con il punto del breakdown.
- CODEX-022: verifica stato Git locale/remoto, controlli ambiente, file tracciati e coerenza con spec/errata/breakdown.

### Verifiche eseguite

- `git fetch origin main`: riuscito.
- `HEAD` e `origin/main` iniziali allineati a `25019434a6dcb8217f9cba05d152aef34f1a2587`, con solo `PROMPT_LOG.md` modificato localmente dal chiarimento precedente.
- `pip check`: nessun requisito rotto.
- Import core: `fastapi`, `openai`, `sqlalchemy`, `httpx`, `psutil`: OK.
- Ignorati correttamente: `.env`, `.venv`, `logs/test.log`, `data_dragon.db`, `build/test.txt`, `dist/test.txt`, `app.spec`.
- File documentali presenti: `README.md`, `PROMPT_LOG.md`, `INCIDENTS.md`, `SPEC_ERRATA.md`, `PC_ITS_DEPENDENCIES_CHECKLIST.md`, `requirements.txt`, `.env.example`.
- Struttura M0 presente e tracciata tramite `.gitkeep`: `app/`, `static/`, `templates/`, `prompts/`, `tests/mock_drafts/`, `logs/`, `scripts/`.
- `requirements.txt`: confermati `fastapi`, `uvicorn[standard]`, `httpx`, `psutil>=5.9.8,<8`.

### Esito

- Operazioni fin qui coerenti con breakdown v2.1, spec v2.3 ed errata.
- M0 e T03/T03b risultano chiusi, con ERRATA-004 documentata.
- Nessun codice applicativo iniziato.
- Prossimo task: M1/T06, `app/data_dragon.py` con `fetch_versions()`.
- File handoff Desktop richiesto: `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`.

## PLOG-2026-05-13-001 - Ripresa breakdown e piano M1/T06

- Data: 2026-05-13
- Scope: ripresa lavori dopo handoff, solo lettura/verifica/piano; nessuna costruzione del prodotto avviata.
- Stato richiesta: piano da esporre all'utente per approvazione o correzione.

### Messaggi catalogati

- USER-008: chiede di applicare la regola `PROMPT_LOG.md` prima di ogni output, usare `INCIDENTS.md` per incidenti reali, continuare il breakdown prendendo la data odierna, leggere integralmente tre file indicati, controllare prompt log e breakdown status per capire il punto corrente, controllare i file della repo, elaborare e validare un piano d'azione, esporlo in attesa di approvazione, aggiornare README solo se necessario, usare come riferimento la repo GitHub `https://github.com/MrChuck118/live-draft-companion`, non inventare e non iniziare a costruire.
- CODEX-023: comunica che fara solo ricognizione: lettura integrale dei tre documenti, confronto con prompt log/breakdown status e stato reale della repo locale, senza modifiche al codice o alla documentazione funzionale.
- CODEX-024: comunica che i file esterni sono leggibili, che i documenti principali sono lunghi e verranno letti a blocchi con hash/dimensioni come controllo di integrita; rileva nella repo `PROMPT_LOG.md`, `INCIDENTS.md`, `README.md` e file di supporto.
- CODEX-025: comunica che il breakdown status e stato letto fino alla riga 107 e conferma M0 chiuso, codice applicativo non iniziato, prossimo task M1/T06 `app/data_dragon.py` con `fetch_versions()`.
- CODEX-026: comunica che il breakdown v2.1 e stato letto fino alla riga 917 e conferma Demo Mode First, M1/T06 come primo passo tecnico, T07b opzionale, log/incidenti non artificiali.
- CODEX-027: comunica che la spec v2.3 e stata letta fino alla riga 972 e ribadisce spec frozen, precedenza errata, no scope creep, privacy LCU, Data Dragon in inglese, validatori rigorosi e logging/incidenti come parte della consegna.
- CODEX-028: comunica che la repo locale e pulita su `main`, allineata a `origin/main`, remote corretto e HEAD `16b00d8`; chiarisce che `.venv` locale non tracciata/ignorata non va confusa con i sorgenti.
- CODEX-029: comunica che sono stati letti anche `PROMPT_LOG.md`, `INCIDENTS.md`, `README.md`, `SPEC_ERRATA.md`, checklist pc its, `requirements.txt`, `.env.example`, `.gitignore` e `LICENSE`; conferma assenza di codice applicativo e prossimo passo T06.
- CODEX-030: comunica che aggiornera solo `PROMPT_LOG.md` per rispettare la regola di processo e che non registra incidenti nuovi perche non e emerso un problema reale nuovo.

### Materiale letto/verificato

- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`
  - righe lette: 107
  - dimensione: 4039 byte
  - SHA256: AA6002BA29754977B498F00689E908E421E945357BA5330F8590C9B8F8CBD28C
- `C:\Users\user\Downloads\breakdown_tasks_v2.1_corretto.md`
  - righe lette: 917
  - dimensione: 61636 byte
  - SHA256: F36B26B2567AADCA8B6540AD5A34FC372CB3E85532BED6DECBD5BFB23E443232
- `C:\Users\user\Downloads\LiveDraftCompanion_TechnicalSpec_v2.3.md`
  - righe lette: 972
  - dimensione: 75801 byte
  - SHA256: 40812730AB0D93A46E1E40547656F33040F4169A1E4DBE40AC4A659BE0473878
- Repo locale `C:\LiveDraftCompanion`
  - branch: `main`
  - remote: `https://github.com/MrChuck118/live-draft-companion.git`
  - stato Git: pulito prima dell'aggiornamento di questa entry
  - HEAD/origin main verificati: `16b00d8`
  - codice applicativo: assente, solo `.gitkeep` nelle directory operative
- File repo letti/verificati:
  - `PROMPT_LOG.md`
  - `INCIDENTS.md`
  - `README.md`
  - `SPEC_ERRATA.md`
  - `PC_ITS_DEPENDENCIES_CHECKLIST.md`
  - `requirements.txt`
  - `.env.example`
  - `.gitignore`
  - `LICENSE`

### Verifiche eseguite

- Data locale verificata: `2026-05-13`.
- `git status --short --branch`: `main...origin/main`.
- `git remote -v`: remote ufficiale corretto.
- `git log --oneline -5`: ultimo commit `16b00d8 docs: record handoff verification`.
- `git ls-files`: solo setup M0/documentazione/struttura vuota tracciata.
- `.env`: assente, come atteso.
- `.\.venv\Scripts\python.exe -m pip check`: nessun requisito rotto.
- Import core `fastapi`, `openai`, `sqlalchemy`, `httpx`, `psutil`: OK.

### Stato dedotto del breakdown

- M0/T01-T05: fatto.
- M0/T03b: fatto con `ERRATA-004` su `psutil>=5.9.8,<8`.
- M0/T05b: da fare manualmente/asincrono, non bloccante per T06 ma da non dimenticare.
- M1/T06: prossimo task tecnico, non iniziato.
- M1/T07-T12 e M2-M10: non iniziati.

### Piano da proporre all'utente

- Non aggiornare `INCIDENTS.md` ora: nessun nuovo incidente reale emerso.
- Non aggiornare `README.md` ora: il README riassuntivo e coerente con lo stato reale ("codice applicativo non ancora iniziato").
- Dopo approvazione, iniziare solo M1/T06 creando `app/data_dragon.py` con `fetch_versions()` async, seguendo spec/breakdown.
- Verificare T06 con il comando manuale previsto dal breakdown.
- Aggiornare `PROMPT_LOG.md` e, solo se nasce un problema reale, `INCIDENTS.md` prima del successivo output.

## PLOG-2026-05-13-002 - M1/T06 Data Dragon `fetch_versions()`

- Data: 2026-05-13
- Scope: implementare solo M1/T06, senza anticipare T07 o altri moduli.
- Stato: T06 completato e verificato.

### Messaggi catalogati

- USER-009: approva il piano e chiede di non uscire dai paletti precedentemente discussi; autorizza installazione di dipendenze mancanti se necessario; se dipendenze mancanti non sono installabili sul PC del lavoro, fermarsi e riferire.
- CODEX-031: comunica che procedera solo su M1/T06, senza moduli successivi o feature extra, verificando prima `httpx`.
- CODEX-032: comunica che `httpx` e gia installato e che verra creato solo `app/data_dragon.py` con una funzione async piccola e difensiva.
- CODEX-033: comunica che il file e stato creato e che eseguira il DoD del breakdown; in caso di blocco rete avrebbe richiesto permesso esplicito.
- CODEX-034: comunica che il DoD e passato con patch Data Dragon `16.10.1`; poiche il README non sarebbe piu coerente con lo stato reale, aggiorna solo la riga di stato e poi registra l'iterazione.

### Dipendenze

- `httpx` verificato presente nella virtualenv: versione `0.28.1`.
- Nessuna dipendenza mancante.
- Nessuna installazione eseguita.

### File modificati

- Creato `app/data_dragon.py`.
- Aggiornato `README.md` solo nello stato attuale:
  - T06 completato;
  - prossimo task tecnico T07.
- Aggiornato questo `PROMPT_LOG.md`.
- `INCIDENTS.md` non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

- Comando DoD:

```powershell
.\.venv\Scripts\python.exe -c "import asyncio; from app.data_dragon import fetch_versions; print(asyncio.run(fetch_versions()))"
```

- Esito: `16.10.1`.

### Decisione

- M1/T06 puo considerarsi completato.
- Prossimo task da proporre: M1/T07 `fetch_champions()` con `tags`, non `roles`, senza anticipare T07b opzionale.

## PLOG-2026-05-13-003 - Aggiornamento breakdown status Desktop

- Data: 2026-05-13
- Scope: aggiornare solo il file breakdown status sul Desktop e `PROMPT_LOG.md`.
- Stato: completato.

### Messaggi catalogati

- USER-010: chiede di modificare il file breakdown status sul Desktop aggiornandolo allo stato corrente, aggiornare il prompt log e non fare nient'altro.
- CODEX-035: comunica che aggiornera solo il breakdown status Desktop e `PROMPT_LOG.md`, senza toccare codice, README, incidenti o altro.
- CODEX-036: comunica che aggiornera il file di stato con T06 completato e prossimo passo T07, poi aggiungera una entry minima al prompt log.

### File modificati

- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`
- `PROMPT_LOG.md`

### Aggiornamento stato registrato

- Data stato portata a `2026-05-13`.
- M1/T06 segnato come fatto.
- Verifica T06 registrata: Data Dragon ha restituito patch `16.10.1`.
- Prossimo task tecnico aggiornato a M1/T07 `fetch_champions()` con `tags`, non `roles`.
- Segnalato che le modifiche locali sono ancora non committate/pushate.

## PLOG-2026-05-13-004 - Piano prossimo task breakdown M1/T07

- Data: 2026-05-13
- Scope: pianificare la prossima task del breakdown, senza applicarla prima dell'approvazione.
- Stato: piano da esporre all'utente.

### Messaggi catalogati

- USER-011: chiede di procedere con le task del breakdown mantenendo i paletti del primo prompt; metodo richiesto: mostrare il piano d'azione e procedere solo dopo approvazione.
- CODEX-037: comunica che resta in modalita piano, non applica task finche non approvate, fa solo un controllo leggero dello stato corrente e registra l'iterazione nel prompt log.
- CODEX-038: comunica che T06 esiste, T07 e il prossimo task tecnico e T07b resta opzionale/Could, quindi non incluso nel piano immediato.

### Stato verificato

- `git status --short`: modifiche locali gia presenti da iterazioni precedenti (`PROMPT_LOG.md`, `README.md`, `app/data_dragon.py` nuovo).
- `app/data_dragon.py`: presente.
- Breakdown v2.1: prossimo task M1/T07 `fetch_champions()` con `tags`, non `roles`.

### Piano da proporre

- Prossima iterazione limitata a M1/T07.
- Estendere `app/data_dragon.py` con `fetch_champions(patch: str)`.
- Usare Data Dragon en_US champion endpoint.
- Restituire dict `{champion_id: {name, key, tags, image_url}}`.
- Non produrre mai chiave `roles`.
- Non implementare T07b `champion_roles.json`.
- Verificare DoD con chiamata reale Data Dragon e controlli su conteggio, Yasuo, Lee Sin, Kai'Sa, `tags` e assenza di `roles`.

## PLOG-2026-05-13-005 - M1/T07 `fetch_champions()`

- Data: 2026-05-13
- Scope: validare il piano contro il breakdown status e implementare solo M1/T07 se allineato.
- Stato: T07 completato e verificato.

### Messaggi catalogati

- USER-012: chiede di validare il piano con il breakdown status e, se in linea con lo stato attuale, procedere.
- CODEX-039: comunica che validera prima contro il breakdown status Desktop e procedera solo se conferma T07 come prossimo passo.
- CODEX-040: comunica che il breakdown status dice T07 prossimo e `fetch_champions()` con `tags`, non `roles`, quindi procede con modifica mirata a `app/data_dragon.py`.
- CODEX-041: comunica che l'implementazione T07 e inserita e che eseguira un test manuale su quantita, campioni richiesti, assenza `roles` e `tags` di Yasuo.
- CODEX-042: comunica che il primo comando di test era malformato per Python `-c` con `async def`, quindi non indica un problema del codice.
- CODEX-043: comunica che anche il passaggio via pipe ha inciampato nel launcher della virtualenv su questo PC e che usera lo stesso interprete con argomento `-c`.
- CODEX-044: comunica che la virtualenv mostra il problema gia noto del launcher con script lunghi e verifica se il comando breve funziona.
- CODEX-045: comunica che il comando breve con `.venv` funziona e che il problema e solo il modo di passare lo script multilinea.
- CODEX-046: comunica che PowerShell ha mangiato le virgolette della stringa `Kai'Sa`, quindi riformula il test.
- CODEX-047: comunica che rimuove stringhe letterali dal test costruendole con `chr()` per evitare problemi di quotatura senza creare file extra o anticipare T12.
- CODEX-048: comunica che T07 ha passato il DoD e aggiornera solo README, breakdown status Desktop e prompt log; nessun incidente perche non c'e stato un problema reale del progetto.

### Validazione contro breakdown status

- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md` indicava:
  - T06 completato;
  - prossimo task tecnico M1/T07;
  - vincolo `tags`, non `roles`.
- Piano considerato allineato.

### File modificati

- `app/data_dragon.py`
  - aggiunta `fetch_champions(patch: str)`;
  - endpoint Data Dragon `en_US/champion.json`;
  - output `{champion_id: {name, key, tags, image_url}}`;
  - nessuna chiave `roles`.
- `README.md`
  - stato aggiornato a M1/T07 completato;
  - prossimo task tecnico M1/T08.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`
  - T07 segnato come fatto;
  - prossimo task aggiornato a T08.
- `PROMPT_LOG.md`
  - aggiunta questa entry.
- `INCIDENTS.md`
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

- DoD T07 con chiamata reale Data Dragon:
  - patch: `16.10.1`;
  - campioni: `172`;
  - presenti: `Yasuo`, `Lee Sin`, `Kai'Sa`;
  - `Yasuo.tags`: `['Fighter', 'Assassin']`;
  - nessuna chiave `roles` negli output.

### Note operative

- Alcuni tentativi di test inline sono falliti per quotatura PowerShell/Python e per il launcher `.venv` con script lunghi; il test finale e passato con un comando `-c` monoriga costruendo le stringhe critiche via `chr()`.
- Non e un incidente di progetto: nessuna dipendenza mancante, nessun cambio piano, nessun problema nel codice T07.

### Decisione

- M1/T07 puo considerarsi completato.
- Prossimo task da proporre: M1/T08 `fetch_items()`.

## PLOG-2026-05-13-006 - M1/T08 `fetch_items()` tentativo e blocco DoD

- Data: 2026-05-13
- Scope: procedere con il prossimo task del breakdown, M1/T08.
- Stato: implementazione aggiunta, T08 non chiusa per blocco DoD documentato in `INCIDENTS.md`.

### Messaggi catalogati

- USER-013: chiede di procedere con il prossimo task.
- CODEX-049: comunica che procedera con M1/T08 `fetch_items()` senza anticipare T09 o cache/DB, controllando lo stato corrente e aggiornando i registri a fine giro.
- CODEX-050: comunica che il breakdown status conferma T08 come prossimo task e che aggiungera `fetch_items()` con endpoint Data Dragon `item.json`.
- CODEX-051: comunica che `fetch_items()` e stata inserita e che verifichera il DoD con chiamata reale.
- CODEX-052: comunica che il test T08 non ha passato una assert del DoD e che fara diagnosi mirata su item contenenti `Liandry` e `Luden`.
- CODEX-053: comunica che e emerso un vero blocco DoD: Data Dragon patch `16.10.1` contiene `Liandry's Torment`, non contiene `Luden's Companion`, ma contiene `Luden's Echo`; non inventera o rinominera dati.

### File modificati

- `app/data_dragon.py`
  - aggiunta `fetch_items(patch: str)`;
  - endpoint Data Dragon `en_US/item.json`;
  - output `{item_id: {name, stats}}`.
- `INCIDENTS.md`
  - aggiunto `INC-006` per DoD T08 non soddisfacibile alla lettera con Data Dragon patch corrente.
- `README.md`
  - stato aggiornato a T08 implementato ma non chiuso.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`
  - stato aggiornato a T08 implementato/bloccato.
- `PROMPT_LOG.md`
  - aggiunta questa entry.

### Verifiche eseguite

- DoD T08 tentato con chiamata reale Data Dragon.
- Diagnosi:

```text
patch 16.10.1 count 705
["Liandry's Anguish", "Liandry's Torment"]
["Luden's Echo", "Luden's Echo"]
[]
```

### Esito

- `fetch_items()` e implementata.
- Conteggio item: 705, quindi sopra il minimo 200.
- `Liandry's Torment`: presente.
- `Tormento di Liandry`: assente.
- `Luden's Companion`: assente nella patch corrente.
- T08 resta non chiusa finche l'utente non approva una mini-errata operativa del DoD o un criterio alternativo coerente con Data Dragon reale.

## PLOG-2026-05-13-007 - Discussione INC-006 prima di errata

- Data: 2026-05-13
- Scope: discutere il blocco T08 prima di modificare ulteriormente `SPEC_ERRATA.md` o aggiungere sezioni.
- Stato: valutazione aperta, nessuna errata applicata.

### Messaggi catalogati

- USER-014: chiede di discutere il problema `Luden's Companion` assente da Data Dragon; domanda se puo verificarsi anche sul PC di casa, cosa comporta passare a `Luden's Echo`, e se abbia senso segnare lo status nel breakdown status e risolvere successivamente; chiede di vagliare queste possibilita prima di modificare ulteriormente la spec errata e aggiungere sezioni.
- CODEX-054: comunica che non tocchera `SPEC_ERRATA.md` e non aggiungera sezioni li; aggiorna solo `PROMPT_LOG.md` per registrare la fase di valutazione.

## PLOG-2026-05-13-008 - Chiusura T08 con ERRATA-005

- Data: 2026-05-13
- Scope: applicare la decisione dell'utente di passare il controllo DoD T08 da `Luden's Companion` a `Luden's Echo`.
- Stato: T08 chiuso.

### Messaggi catalogati

- USER-015: approva il passaggio a `Luden's Echo`.
- CODEX-055: comunica che applichera la decisione in modo stretto, senza cambiare il codice T08 gia corretto; cambiera solo il criterio documentale, verifichera il DoD aggiornato e aggiornera registri/stati collegati.
- CODEX-056: comunica che verifichera il DoD aggiornato con `Luden's Echo` usando Data Dragon reale.
- CODEX-057: comunica che il DoD aggiornato passa e che aggiornera la documentazione minima per rendere la decisione tracciabile e chiudere T08.

### Verifica DoD aggiornata

```text
16.10.1 705 Liandry's Torment Luden's Echo False
```

- Patch: `16.10.1`.
- Item count: `705`.
- `Liandry's Torment`: presente.
- `Luden's Echo`: presente.
- `Tormento di Liandry`: assente.

### File aggiornati

- `SPEC_ERRATA.md`: aggiunta `ERRATA-005`.
- `INCIDENTS.md`: `INC-006` segnato risolto con `ERRATA-005`.
- `README.md`: stato aggiornato a M1/T08 completato; prossimo task M1/T09.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`: T08 segnato fatto con errata; prossimo task T09.
- `PROMPT_LOG.md`: aggiunta questa entry.

### Decisione

- M1/T08 puo considerarsi completato.
- Prossimo task da proporre: M1/T09 `fetch_runes()`.

## PLOG-2026-05-13-009 - Ricognizione completa e piano M1/T09

- Data: 2026-05-13
- Ora locale: 17:03 +02:00
- Scope: leggere integralmente i tre file indicati, controllare breakdown status, repo locale, GitHub remote, README, PROMPT_LOG e INCIDENTS; preparare solo un piano da esporre all'utente.
- Stato: piano da approvare; nessuna costruzione avviata.

### Messaggi catalogati

- USER-016: chiede di continuare seguendo il breakdown usando la data odierna, leggere integralmente i tre file indicati senza tralasciare nulla, controllare lo status del breakdown, i file della repo, capire la prossima task, validare il piano e mostrarlo prima di procedere; chiede inoltre di aggiornare prompt log a fine iterazione, registrare incidenti reali in `INCIDENTS.md`, verificare se il README riassuntivo vada aggiornato, e tenere conto del link repo GitHub `https://github.com/MrChuck118/live-draft-companion`.
- CODEX-058: comunica che fara solo ricognizione: lettura integrale dei tre documenti, controllo repo locale e collegamento GitHub, nessuna modifica di build.
- CODEX-059: comunica che la repo locale e su `main`, collegata al remote ufficiale, con modifiche locali gia presenti in `INCIDENTS.md`, `PROMPT_LOG.md`, `README.md`, `SPEC_ERRATA.md` e `app/data_dragon.py`.
- CODEX-060: comunica che l'output grezzo dei documenti lunghi era abbreviato dalla console e che rileggera i file a blocchi numerati.
- CODEX-061: comunica che il breakdown e stato letto a blocchi completi e conferma la catena critica M1: dopo T08 viene T09, poi T10-T12.
- CODEX-062: comunica che la spec conferma i vincoli Data Dragon: rune/keystone in inglese, cache SQLite e test integrita prima di AI/UI/LCU.
- CODEX-063: comunica che la repo locale contiene modifiche non committate coerenti con T06-T08 e che il piano deve lavorare sopra quello stato senza sovrascrivere nulla.
- CODEX-064: comunica che `git fetch` diretto si e fermato per `dubious ownership`, poi prova la variante temporanea con `safe.directory` senza cambiare config globale.
- CODEX-065: comunica che aggiorna solo `PROMPT_LOG.md` prima dell'output, senza toccare codice, README o incidents.

### Materiale letto/verificato

- `C:\Users\user\Downloads\breakdown_tasks_v2.1_corretto.md`
  - righe lette: 917
  - dimensione: 61636 byte
  - SHA256: F36B26B2567AADCA8B6540AD5A34FC372CB3E85532BED6DECBD5BFB23E443232
- `C:\Users\user\Downloads\LiveDraftCompanion_TechnicalSpec_v2.3.md`
  - righe lette: 972
  - dimensione: 75801 byte
  - SHA256: 40812730AB0D93A46E1E40547656F33040F4169A1E4DBE40AC4A659BE0473878
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`
  - righe lette: 116
  - dimensione: 5200 byte
  - SHA256: 54A2F965A3F50B5FB77313A8996D71640BC08F22D6F23F6D8135F57A31B292BA
- Repo locale `C:\LiveDraftCompanion`
  - branch: `main`
  - remote: `https://github.com/MrChuck118/live-draft-companion.git`
  - dopo fetch autorizzato: `HEAD`, `origin/main` e `FETCH_HEAD` coincidono su `16b00d8eab162da537b94fa526e78120ecdded8f`
  - working tree: modifiche locali non committate in `INCIDENTS.md`, `PROMPT_LOG.md`, `README.md`, `SPEC_ERRATA.md`; nuovo file `app/data_dragon.py`

### File repo letti/verificati

- `PROMPT_LOG.md`
- `INCIDENTS.md`
- `README.md`
- `SPEC_ERRATA.md`
- `PC_ITS_DEPENDENCIES_CHECKLIST.md`
- `requirements.txt`
- `.env.example`
- `.gitignore`
- `LICENSE`
- `app/data_dragon.py`

### Stato dedotto del breakdown

- M0/T01-T05: fatto.
- M0/T05b: ancora da fare manualmente/asincrono, non bloccante per la prossima task tecnica.
- M1/T06: fatto, `fetch_versions()`.
- M1/T07: fatto, `fetch_champions()` con `tags` e senza `roles`.
- M1/T08: fatto con `ERRATA-005`, `fetch_items()` e controllo aggiornato su `Luden's Echo`.
- Prossima task tecnica: M1/T09 `fetch_runes()`.

### Decisioni documentali

- `README.md`: non va aggiornato in questa iterazione di solo piano; e gia coerente con T08 completato e prossimo task T09.
- `INCIDENTS.md`: non va aggiornato ora; non e emerso un nuovo incidente di progetto. Il primo `git fetch` e stato bloccato da safe.directory/rete sandbox, poi il remote e stato verificato con comando autorizzato.
- `PROMPT_LOG.md`: aggiornato con questa entry prima dell'output.

### Piano da proporre

- Fermarsi e chiedere approvazione prima di implementare.
- Se approvato, limitare la prossima iterazione a M1/T09.
- In `app/data_dragon.py`, aggiungere solo la costante URL rune e `fetch_runes(patch: str)`.
- Usare endpoint Data Dragon `https://ddragon.leagueoflegends.com/cdn/<patch>/data/en_US/runesReforged.json`.
- Estrarre solo le keystone, non tutte le rune minori: per ogni tree, prendere gli slot keystone coerenti con il DoD T09.
- Restituire un dizionario lookup con nomi inglesi, sufficiente per i validatori successivi.
- Verificare DoD con chiamata reale: presenti `Conqueror`, `Arcane Comet`, `Electrocute`; assente `Cometa Arcana`; almeno 8 keystone.
- Dopo verifica, aggiornare README/status/prompt log; aggiornare INCIDENTS solo se nasce un problema reale.

## PLOG-2026-05-13-010 - M1/T09 `fetch_runes()`

- Data: 2026-05-13
- Ora locale: 17:08 +02:00
- Scope: implementare solo M1/T09 `fetch_runes()` dopo approvazione del piano.
- Stato: T09 completato e verificato.

### Messaggi catalogati

- USER-017: approva il piano e chiede di procedere senza dimenticare i paletti preconfigurati.
- CODEX-066: comunica che procedera solo su M1/T09, senza T10/cache DB, T07b, AI, UI o LCU.
- CODEX-067: comunica che lo stato conferma T09 come prossimo passo e che fara una modifica piccola in `app/data_dragon.py`.
- CODEX-068: comunica che la funzione e stata inserita e che eseguira il DoD T09 con Data Dragon reale.
- CODEX-069: comunica che il DoD T09 passa su patch `16.10.1` con 17 keystone e che aggiornera solo documentazione minima.
- CODEX-070: comunica che T09 e chiusa e che registrera l'iterazione in `PROMPT_LOG.md` senza creare incidenti artificiali.

### File modificati

- `app/data_dragon.py`
  - aggiunta costante `DATA_DRAGON_RUNES_URL`;
  - aggiunta costante `DATA_DRAGON_RUNE_ICON_URL`;
  - aggiunta funzione async `fetch_runes(patch: str)`;
  - estrazione limitata alle keystone dal primo slot di ogni albero rune;
  - output `{rune_id: {name, key, tree, tree_key, icon_url}}`.
- `README.md`
  - stato aggiornato a M1/T09 completato;
  - prossimo task tecnico aggiornato a M1/T10.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`
  - stato aggiornato a T09 completato;
  - prossimo task aggiornato a T10.
- `PROMPT_LOG.md`
  - aggiunta questa entry.

### Verifiche eseguite

DoD T09 con chiamata reale Data Dragon:

```powershell
.\.venv\Scripts\python.exe -c "import asyncio; from app.data_dragon import fetch_versions, fetch_runes; p=asyncio.run(fetch_versions()); r=asyncio.run(fetch_runes(p)); names={v['name'] for v in r.values()}; print(p, len(r), 'Conqueror' in names, 'Arcane Comet' in names, 'Electrocute' in names, 'Cometa Arcana' in names); print(sorted(names))"
```

Esito:

```text
16.10.1 17 True True True False
```

Keystone restituite:

```text
['Aftershock', 'Arcane Comet', 'Conqueror', 'Dark Harvest', 'Deathfire Touch', 'Electrocute', 'First Strike', 'Fleet Footwork', 'Glacial Augment', 'Grasp of the Undying', 'Guardian', 'Hail of Blades', 'Lethal Tempo', 'Press the Attack', "Stormraider's Surge", 'Summon Aery', 'Unsealed Spellbook']
```

Verifica sintassi:

```powershell
.\.venv\Scripts\python.exe -m compileall app\data_dragon.py
```

- Exit code: 0.

### Incidenti

- Nessun nuovo incidente registrato in `INCIDENTS.md`.
- La modifica al breakdown status Desktop ha richiesto scrittura fuori workspace, quindi e stata eseguita con autorizzazione.

### Decisione

- M1/T09 puo considerarsi completato.
- Prossimo task da proporre: M1/T10 `app/db.py` con modelli SQLAlchemy e tabelle SQLite `champions`, `items`, `runes`, `meta`.

## PLOG-2026-05-13-011 - Piano M1/T10 `app/db.py`

- Data: 2026-05-13
- Ora locale: 17:10 +02:00
- Scope: pianificare la prossima task M1/T10, senza implementare prima dell'approvazione.
- Stato: piano da esporre all'utente.

### Messaggi catalogati

- USER-018: chiede di procedere con la prossima task, mantenendo la stessa metodica.
- CODEX-071: comunica che fara prima ricognizione mirata e piano, senza implementare finche il piano non viene approvato.
- CODEX-072: comunica che la ricognizione conferma T10 come prossimo passo e che il piano sara limitato a schema DB + init tabelle, senza T11.
- CODEX-073: comunica che aggiornera solo `PROMPT_LOG.md` prima dell'output, senza README o incidents.

### Stato verificato

- `git status --short --branch`: branch `main`, modifiche locali non committate gia attese da T06-T09/documentazione.
- Breakdown status Desktop:
  - stato locale: T09 completato;
  - prossimo task: M1/T10 modelli SQLAlchemy + tabelle SQLite.
- Breakdown v2.1:
  - T10 dipende da T07-T09;
  - T10 richiede `app/db.py`, modelli SQLAlchemy per `champions`, `items`, `runes`, `meta`, setup async `aiosqlite`, database `data_dragon.db`;
  - DoD: `from app.db import init_db; import asyncio; asyncio.run(init_db())` crea le 4 tabelle.
- `requirements.txt` contiene gia `sqlalchemy` e `aiosqlite`.
- `app/data_dragon.py` contiene gia le funzioni T06-T09 necessarie per T11, ma T10 non deve ancora usarle.

### Piano da proporre

- Fermarsi e chiedere approvazione prima di implementare.
- Creare solo `app/db.py`.
- Definire setup SQLAlchemy async:
  - `DATABASE_URL = "sqlite+aiosqlite:///data_dragon.db"`;
  - `engine = create_async_engine(...)`;
  - `async_sessionmaker(...)` per uso futuro in T11;
  - `Base` declarative.
- Definire 4 modelli/tabelle:
  - `champions`: `id` primary key, `name`, `key`, `tags` JSON, `image_url`;
  - `items`: `id` primary key, `name`, `stats` JSON;
  - `runes`: `id` primary key, `name`, `key`, `tree`, `tree_key`, `icon_url`;
  - `meta`: `key` primary key, `value` per salvare la patch corrente in T11.
- Aggiungere `async def init_db() -> None` con `Base.metadata.create_all`.
- Non implementare ancora:
  - `populate_cache()`;
  - `check_patch_and_refresh()`;
  - fetch/salvataggio dati;
  - tabelle cache/history di M7a;
  - modelli Pydantic o validator M2.
- Verificare DoD con:
  - comando import/init del breakdown;
  - controllo via `sqlite3` stdlib che esistano esattamente le tabelle richieste.
- Non tracciare `data_dragon.db` in Git: e gia coperto da `.gitignore`.

### Decisioni documentali

- `README.md`: da aggiornare solo dopo T10 completata e verificata.
- `INCIDENTS.md`: da aggiornare solo se emerge un blocco reale.
- `PROMPT_LOG.md`: aggiornato con questa entry prima dell'output.

## PLOG-2026-05-13-012 - Chiarimento su T10 database vs file progetto

- Data: 2026-05-13
- Ora locale: 17:13 +02:00
- Scope: chiarire prima dell'approvazione T10 se le query/dati vadano messi in database o bastino file nel progetto.
- Stato: chiarimento concettuale, nessuna implementazione.

### Messaggi catalogati

- USER-019: prima di approvare T10 chiede se alcune parti siano query da mettere in un database o se bastino file nel progetto; chiede una spiegazione migliore.
- CODEX-074: comunica che registrera la mini-iterazione e chiarira differenza tra file di progetto, schema database e dati runtime.

### Chiarimento da dare

- In T10 non si scrivono query SQL manuali e non si inseriscono ancora dati.
- In T10 si crea `app/db.py`, cioe codice Python versionato che descrive lo schema delle tabelle tramite SQLAlchemy.
- Il file `data_dragon.db` verra generato localmente da `init_db()` ed e runtime/cache, quindi non va committato.
- In T11 si useranno le funzioni Data Dragon gia create per riempire quelle tabelle con campioni, item, rune e patch corrente.
- I dati statici Data Dragon devono stare nel database locale per cache, lookup e validatori futuri; non e consigliabile tenerli solo come file di progetto versionati.

## PLOG-2026-05-13-013 - M1/T10 `app/db.py`

- Data: 2026-05-13
- Ora locale: 17:21 +02:00
- Scope: implementare solo M1/T10, cioe schema SQLAlchemy async e creazione tabelle SQLite.
- Stato: T10 completato e verificato.

### Messaggi catalogati

- USER-020: approva il chiarimento su database vs file progetto e chiede di procedere.
- CODEX-075: comunica che procedera nel perimetro approvato: schema SQLite in `app/db.py`, quattro tabelle vuote, nessun popolamento dati.
- CODEX-076: comunica che `app/db.py` e stato creato e che eseguira il DoD del breakdown.
- CODEX-077: comunica che `init_db()` e passato e che controllera direttamente il file SQLite.
- CODEX-078: comunica che le tabelle sono confermate e che `data_dragon.db`/`__pycache__` sono ignorati da Git.
- CODEX-079: comunica che aggiornera solo la documentazione di stato.
- CODEX-080: comunica che corregge la formattazione newline nel breakdown status Desktop.
- CODEX-081: comunica che registra T10 nel `PROMPT_LOG.md` prima del riepilogo finale.

### File modificati

- `app/db.py`
  - creato schema SQLAlchemy async;
  - `DATABASE_URL = "sqlite+aiosqlite:///data_dragon.db"`;
  - `engine`;
  - `AsyncSessionLocal`;
  - `Base`;
  - modelli `Champion`, `Item`, `Rune`, `Meta`;
  - `async def init_db() -> None`.
- `README.md`
  - stato aggiornato a M1/T10 completato;
  - prossimo task tecnico aggiornato a M1/T11.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`
  - T10 segnato come fatto;
  - prossimo task aggiornato a T11.
- `PROMPT_LOG.md`
  - aggiunta questa entry.

### Tabelle create

- `champions`
- `items`
- `runes`
- `meta`

### Verifiche eseguite

DoD T10:

```powershell
.\.venv\Scripts\python.exe -c "from app.db import init_db; import asyncio; asyncio.run(init_db())"
```

- Exit code: 0.

Controllo tabelle via `sqlite3` stdlib:

```powershell
.\.venv\Scripts\python.exe -c "import sqlite3; con=sqlite3.connect('data_dragon.db'); rows=con.execute('select name from sqlite_master where type=? order by name', ('table',)).fetchall(); print([r[0] for r in rows])"
```

Esito:

```text
['champions', 'items', 'meta', 'runes']
```

Controllo set atteso:

```text
True ['champions', 'items', 'meta', 'runes']
```

Verifica sintassi:

```powershell
.\.venv\Scripts\python.exe -m compileall app\db.py
```

- Exit code: 0.

Verifica ignore:

```text
data_dragon.db
"app\\__pycache__\\db.cpython-312.pyc"
```

### Incidenti

- Nessun nuovo incidente registrato in `INCIDENTS.md`.
- Un controllo tabellare inline e fallito inizialmente per quotatura PowerShell/Python; non e un problema del codice o del progetto ed e stato ripetuto con query parametrizzata.

### Decisione

- M1/T10 puo considerarsi completato.
- Prossimo task da proporre: M1/T11 `populate_cache()` e `check_patch_and_refresh()` in `app/data_dragon.py`.

## PLOG-2026-05-13-014 - Piano M1/T11 Data Dragon cache

- Data: 2026-05-13
- Ora locale: 17:30 +02:00
- Scope: pianificare M1/T11, senza implementare prima dell'approvazione.
- Stato: piano da esporre all'utente.

### Messaggi catalogati

- USER-021: chiede di andare con la prossima task.
- CODEX-082: comunica che usera la stessa metodica: prima piano validato, senza implementare ancora.
- CODEX-083: comunica che T11 e confermata da breakdown/status e che restera separata da T12.
- CODEX-084: comunica che aggiornera `PROMPT_LOG.md` prima dell'output senza toccare README o status Desktop in fase di solo piano.

### Stato verificato

- Breakdown status Desktop:
  - T10 completato;
  - prossimo task: M1/T11 salvataggio cache + check patch.
- Breakdown v2.1:
  - T11 dipende da T10;
  - in `data_dragon.py` aggiungere `populate_cache()` e `check_patch_and_refresh()`;
  - DoD: primo run popola DB, run successivo stessa patch fa 0 chiamate HTTP, patch forzata diversa fa re-fetch.
- `app/db.py` presente con modelli `Champion`, `Item`, `Rune`, `Meta`, `AsyncSessionLocal`, `init_db()`.
- `app/data_dragon.py` presente con `fetch_versions()`, `fetch_champions()`, `fetch_items()`, `fetch_runes()`.
- `data_dragon.db` esiste localmente da T10 ed e ignorato da Git.

### Piano da proporre

- Fermarsi e chiedere approvazione prima di implementare.
- Modificare `app/data_dragon.py` importando da `app.db`:
  - `init_db`;
  - `AsyncSessionLocal`;
  - modelli `Champion`, `Item`, `Rune`, `Meta`.
- Aggiungere helper interni minimi:
  - lettura patch cached da tabella `meta`;
  - scrittura/aggiornamento patch cached;
  - cancellazione e reinserimento dati statici quando serve refresh.
- Implementare `populate_cache(patch: str | None = None) -> str`:
  - chiama `init_db()`;
  - se `patch` e `None`, usa `fetch_versions()`;
  - scarica champion, item e rune con le funzioni T07-T09;
  - svuota tabelle `champions`, `items`, `runes`;
  - inserisce i dati scaricati;
  - aggiorna `meta` con `key="patch"` e `value=<patch>`;
  - ritorna la patch popolata.
- Implementare `check_patch_and_refresh() -> str`:
  - chiama `init_db()`;
  - chiama `fetch_versions()` per patch corrente;
  - legge `meta.patch`;
  - se la patch e uguale e le tabelle non sono vuote, non chiama `fetch_champions/items/runes`;
  - se patch assente/diversa o cache vuota, chiama `populate_cache(current_patch)`;
  - ritorna la patch corrente.
- Per verificare il DoD "0 chiamate HTTP al secondo run", aggiungere un parametro opzionale di test tipo `force_patch: str | None = None` a `check_patch_and_refresh()` o usare monkey patch temporaneo nel comando di verifica. Preferenza: parametro opzionale interno e semplice, senza cambiare comportamento normale.
- Non implementare ancora:
  - `scripts/test_data_dragon.py` di T12;
  - validator M2;
  - cache AI/history M7a;
  - endpoint FastAPI.
- Verifiche previste:
  - primo run `populate_cache()` crea righe in DB;
  - secondo run `check_patch_and_refresh()` mantiene conteggi e non scarica champion/items/runes;
  - patch forzata diversa in `meta` provoca refresh;
  - `data_dragon.db` resta ignorato da Git.

### Decisioni documentali

- `README.md` e breakdown status Desktop da aggiornare solo dopo T11 completata e verificata.
- `INCIDENTS.md` da aggiornare solo se emerge un problema reale.
- `PROMPT_LOG.md` aggiornato ora con il piano.

## PLOG-2026-05-13-015 - M1/T11 `populate_cache()` e `check_patch_and_refresh()`

- Data: 2026-05-13
- Ora locale: 17:39 +02:00
- Scope: implementare M1/T11 in `app/data_dragon.py`.
- Stato: T11 completato e verificato.

### Messaggi catalogati

- USER-022: approva il piano T11 e chiede di procedere.
- CODEX-085: comunica che procedera su T11 e che usera un parametro opzionale di test per verificare il comportamento senza cambiare quello normale.
- CODEX-086: comunica che aggiunge la logica T11 con transazioni SQLAlchemy async.
- CODEX-087: comunica che esegue primo run `populate_cache()` e controlla i conteggi SQLite.
- CODEX-088: comunica che il primo run ha popolato con patch `16.10.1` e che ripete il controllo conteggi con query parametrizzata per evitare quotatura PowerShell.
- CODEX-089: comunica che verifica il secondo run/cache hit sostituendo temporaneamente le funzioni download con funzioni che fallirebbero se chiamate.
- CODEX-090: comunica che il cache hit e passato e passa al test refresh con patch forzata diversa.
- CODEX-091: comunica che un tentativo di test multilinea e fallito per escaping PowerShell, non per codice, e ripete con wrapper monoriga.
- CODEX-092: comunica che forza `meta.patch` a `forced-old` con comando separato e ripete il refresh.
- CODEX-093: comunica che il refresh forzato e verificato e che fara ultimo controllo conteggi/ignore.
- CODEX-094: comunica che T11 e passata e aggiorna README/status Desktop.
- CODEX-095: comunica che registra nel `PROMPT_LOG.md` test e prossima task prima del riepilogo.

### File modificati

- `app/data_dragon.py`
  - importati `delete`, `func`, `select`;
  - importati da `app.db`: `AsyncSessionLocal`, `Champion`, `Item`, `Meta`, `Rune`, `init_db`;
  - aggiunta `populate_cache(patch: str | None = None) -> str`;
  - aggiunta `check_patch_and_refresh(current_patch: str | None = None) -> str`;
  - aggiunti helper interni `_get_cached_patch()` e `_has_static_cache()`.
- `README.md`
  - stato aggiornato a M1/T11 completato;
  - prossimo task tecnico aggiornato a M1/T12.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`
  - T11 segnato come fatto;
  - prossimo task aggiornato a T12.
- `PROMPT_LOG.md`
  - aggiunta questa entry.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\data_dragon.py app\db.py
```

- Exit code: 0.

Primo run:

```powershell
.\.venv\Scripts\python.exe -c "import asyncio; from app.data_dragon import populate_cache; print(asyncio.run(populate_cache()))"
```

Esito:

```text
16.10.1
```

Conteggi DB:

```text
champions 172
items 705
runes 17
patch 16.10.1
```

Secondo run stessa patch senza re-download static data:

```powershell
.\.venv\Scripts\python.exe -c "import asyncio; import app.data_dragon as dd; fail=lambda patch: (_ for _ in ()).throw(RuntimeError('download called')); dd.fetch_versions=fail; dd.fetch_champions=fail; dd.fetch_items=fail; dd.fetch_runes=fail; print(asyncio.run(dd.check_patch_and_refresh(current_patch='16.10.1')))"
```

Esito:

```text
16.10.1
```

Refresh con patch forzata diversa:

```text
after-force forced-old
16.10.1
{'champions': 1, 'items': 1, 'runes': 1}
```

Conteggi finali DB:

```text
champions 172
items 705
runes 17
patch 16.10.1
```

Verifica ignore:

```text
data_dragon.db
"app\\__pycache__\\data_dragon.cpython-312.pyc"
"app\\__pycache__\\db.cpython-312.pyc"
```

### Incidenti

- Nessun nuovo incidente registrato in `INCIDENTS.md`.
- Due tentativi inline sono falliti per quotatura/escaping PowerShell, non per problemi del codice o della task. Sono stati ripetuti con query parametrizzate/wrapper monoriga.

### Decisione

- M1/T11 puo considerarsi completato.
- Prossimo task da proporre: M1/T12 `scripts/test_data_dragon.py` per test cache integrita.

## PLOG-2026-05-13-016 - Controllo progetto + commit/push M1 T06-T11

- Data: 2026-05-13
- Ora locale: 17:42 +02:00
- Scope: controllare l'intero progetto e committare/pushare tutto cio che e versionabile e non ancora committato.
- Stato: in corso al momento della registrazione; commit/push da eseguire subito dopo questa entry.

### Messaggi catalogati

- USER-023: chiede, prima di proseguire, di controllare l'intero progetto e fare commit/push di tutto cio che non e stato committato.
- CODEX-096: comunica che sospende il breakdown, controlla progetto/diff/file ignorati/verifiche minime, poi aggiorna `PROMPT_LOG.md`, committa solo i file versionabili e pusha.
- CODEX-097: comunica che i file versionabili non committati sono documentazione piu `app/data_dragon.py` e `app/db.py`; runtime come `.venv`, `data_dragon.db` e `__pycache__` sono ignorati.
- CODEX-098: comunica che le verifiche pre-commit sono passate e che registra questa iterazione prima del commit.

### Stato Git pre-commit

- Branch: `main`.
- Ultimo commit locale/remoto prima del nuovo commit: `16b00d8 docs: record handoff verification`.
- File versionabili modificati/non tracciati:
  - `INCIDENTS.md`
  - `PROMPT_LOG.md`
  - `README.md`
  - `SPEC_ERRATA.md`
  - `app/data_dragon.py`
  - `app/db.py`
- File ignorati confermati:
  - `.venv/`
  - `app/__pycache__/`
  - `data_dragon.db`

### Verifiche pre-commit eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app
```

- Exit code: 0.

Dependency check:

```powershell
.\.venv\Scripts\python.exe -m pip check
```

Esito:

```text
No broken requirements found.
```

Cache check:

```powershell
.\.venv\Scripts\python.exe -c "import asyncio; from app.data_dragon import check_patch_and_refresh; print(asyncio.run(check_patch_and_refresh(current_patch='16.10.1')))"
```

Esito:

```text
16.10.1
```

Conteggi SQLite:

```text
champions 172
items 705
runes 17
patch 16.10.1
```

Ignore check:

```text
data_dragon.db
"app\\__pycache__\\data_dragon.cpython-312.pyc"
"app\\__pycache__\\db.cpython-312.pyc"
```

### Decisione

- Procedere con `git add -A`, verificare staged diff, commit e push su `origin/main`.
- Messaggio commit previsto: `T06-T11: implement Data Dragon cache`.

### Esito commit/push

- Commit creato: `0429e01` (`T06-T11: implement Data Dragon cache`).
- Push su `origin/main`: riuscito, remoto aggiornato da `16b00d8` a `0429e01`.
- Verifica post-push:
  - `HEAD`: `0429e015fae57f72419836113614beb72ac5e358`
  - `origin/main`: `0429e015fae57f72419836113614beb72ac5e358`
- Working tree post-push: nessun file versionabile non committato; restano solo file ignorati `.venv/`, `app/__pycache__/`, `data_dragon.db`.

## PLOG-2026-05-13-017 - Ricognizione pc its e piano M1/T12

- Data: 2026-05-13
- Scope: ricognizione completa dopo ripresa lavori su pc its e piano per M1/T12, senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-024: chiede di applicare la regola `PROMPT_LOG.md`, registrare incidenti reali in `INCIDENTS.md`, continuare a seguire il breakdown prendendo la data odierna, leggere integralmente i tre documenti, controllare status del breakdown e file della repo, elaborare e validare un piano, esporlo prima di procedere, controllare se aggiornare il README, non inventare e non costruire.
- CODEX-099: comunica che fara solo ricognizione e piano, senza modifiche al codice; legge spec v2.3, errata, breakdown v2.1 e breakdown status Desktop.
- CODEX-100: comunica che `git status` diretto fallisce per `dubious ownership`; usa `git -c safe.directory=...` solo in lettura per status/log senza alterare config.
- CODEX-101: comunica che il breakdown status Desktop e leggermente datato: dichiarava T11 non ancora committato/pushato, ma `git log` mostra T06-T11 gia in `0429e01` su `origin/main`.
- CODEX-102: comunica che il README e PROMPT_LOG locali sono gia coerenti con T11 fatto e T12 prossimo, quindi non serve aggiornare README in fase di solo piano.
- CODEX-103: espone piano T12 stretto: `scripts/test_data_dragon.py` riusando cache `data_dragon.db`, controlli su conteggi minimi, anti-accenti, `tags` presente, assenza `roles`; nessuna anticipazione su T07b/T13/M2+.
- USER-025: approva il piano con "ok confermo procedi".

### Stato verificato pre-implementazione

- Repo locale `C:\LiveDraftCompanion`:
  - branch `main` allineato a `origin/main` su `2590e78 docs: record Data Dragon cache push`.
  - working tree pulito; unica untracked: `.claude/` (cartella tool Claude Code, non da versionare).
  - log conferma `0429e01 T06-T11: implement Data Dragon cache` gia pushato.
- M0/T05b ancora da fare manualmente, non bloccante per T12.
- Cache SQLite `data_dragon.db` gia popolata da T11 con patch `16.10.1`, 172 champions, 705 items, 17 keystones.
- README e PROMPT_LOG coerenti con stato T11 fatto / T12 prossimo.

### Decisioni documentali

- README non aggiornato in fase di solo piano: e coerente.
- INCIDENTS non aggiornato: nessun nuovo incidente reale.
- PROMPT_LOG aggiornato con questa entry e con la entry successiva post-implementazione.

## PLOG-2026-05-13-018 - M1/T12 `scripts/test_data_dragon.py`

- Data: 2026-05-13
- Scope: implementare solo M1/T12 dopo approvazione del piano.
- Stato: T12 completato e verificato.

### Messaggi catalogati

- CODEX-104: comunica che procedera solo su M1/T12, riusando cache T11, senza anticipare T13 o validators M2.
- CODEX-105: comunica che il primo run dello script falliva per `ModuleNotFoundError: No module named 'app'` perche eseguito da `scripts/`; risolve aggiungendo la root del progetto a `sys.path` nello script stesso, senza modificare codice applicativo.
- CODEX-106: comunica che la regex anti-accenti iniziale (`[À-ſ]`) era troppo larga e poteva matchare caratteri non italiani; stretta a `[àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ]` coerente col vincolo "no accenti italiani".
- CODEX-107: comunica che il DoD passa con exit code 0 e conteggi visibili; aggiornera README, breakdown status Desktop e questo prompt log.

### File modificati

- `scripts/test_data_dragon.py`:
  - script test integrita cache Data Dragon.
  - chiama `check_patch_and_refresh()` per assicurare cache popolata.
  - controlli: count champions >= 160, items >= 200, keystones >= 8; nomi senza accenti italiani; `tags` lista non vuota su ogni champion; assenza colonna `roles` nel modello `Champion`.
  - exit code 0 se tutti i controlli passano, 1 altrimenti.
- `README.md`:
  - stato aggiornato a M1/T12 completato.
  - prossimo task tecnico aggiornato a M2/T13.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T11 segnato come committato/pushato.
  - T12 segnato come fatto.
  - prossimo task aggiornato a M2/T13.
- `PROMPT_LOG.md`:
  - aggiunta questa entry.
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall scripts\test_data_dragon.py
```

- Exit code: 0.

DoD T12:

```powershell
.\.venv\Scripts\python.exe scripts\test_data_dragon.py
```

Esito:

```text
patch: 16.10.1
champions: 172
items: 705
keystones: 17
accent_check_ok: True
tags_check_ok: True
no_roles_column: True
OK
```

- Exit code: 0.

### Note operative

- Path issue iniziale dello script risolto inserendo la root del progetto in `sys.path` direttamente nello script, in modo che funzioni indipendentemente dalla CWD; non e un incidente di progetto, e una scelta di portabilita dello script di test.
- La regex stretta esclude solo accenti italiani; non blocca nomi Data Dragon legittimi con apostrofo come `Kai'Sa`, `Cho'Gath`, `Vel'Koz`.

### Decisione

- M1/T12 puo considerarsi completato.
- Prossimo task da proporre: M2/T13 `app/models.py` con `DraftState` Pydantic.

## PLOG-2026-05-13-019 - Piano M2/T13 `app/models.py`

- Data: 2026-05-13
- Scope: pianificare la prossima task del breakdown M2/T13, senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-026: chiede di procedere con la prossima task usando lo stesso metodo, e di non fare commit/push finche non li chiede esplicitamente.
- CODEX-108: comunica che restera in modalita piano per T13, senza anticipare T14 o validators M2; segnala che i commit/push restano in attesa.
- CODEX-109: espone piano stretto su tre modelli Pydantic v2 in `app/models.py`: `ChampionPick`, `Action`, `DraftState`; campi e tipi coerenti con LCU; nessun validator field (rinviato a T15+).
- USER-027: approva il piano con "ok piano approvato procedi".

### Stato verificato pre-implementazione

- Repo locale `C:\LiveDraftCompanion`:
  - branch `main` allineato a `origin/main` su `2590e78`.
  - modifiche locali non committate da T12 ancora presenti: `scripts/test_data_dragon.py`, `README.md`, `PROMPT_LOG.md`, `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`.
  - working tree pulito a parte queste modifiche e `.claude/` untracked.
- M2/T13 dipende solo da T03b (Python/venv/dipendenze), gia chiuso.
- Pydantic v2 e `pydantic-settings` gia installati in `.venv`.

### Decisioni di design dichiarate nel piano

- `ChampionPick.champion: str | None = None` per gestire pick non ancora effettuato.
- `bans: list[str]` con stringa vuota per ban non ancora effettuato.
- Nessun validator stretto sul `role`, sulla lunghezza dei team o sulla cardinalita ban: vincoli rinviati a T15+ secondo il breakdown.
- Nessuna dipendenza tra `app/models.py` e `app/db.py`/`app/data_dragon.py`.

### Decisioni documentali

- README non aggiornato in fase di solo piano: e gia coerente con T12 fatto / T13 prossimo.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- PROMPT_LOG aggiornato con questa entry prima dell'output.

## PLOG-2026-05-13-020 - M2/T13 `app/models.py`

- Data: 2026-05-13
- Scope: implementare solo M2/T13 dopo approvazione del piano.
- Stato: T13 completato e verificato.

### Messaggi catalogati

- CODEX-110: comunica che procedera solo su M2/T13 con tre `BaseModel` Pydantic v2 senza validator field e senza altre modifiche.
- CODEX-111: comunica che il DoD passa, JSON valido con `null` per pick non assegnato e stringhe vuote per ban non effettuati; aggiornera README, breakdown status Desktop e questo prompt log.

### File modificati

- `app/models.py`:
  - creato modulo Pydantic v2 con tre `BaseModel`:
    - `ChampionPick(role, champion=None)`;
    - `Action(action_id, actor_cell_id, type, completed)`;
    - `DraftState(patch, user_role, bans, enemy_team, ally_team, actions, local_player_cell_id)`.
- `README.md`:
  - stato aggiornato a M2/T13 completato.
  - prossimo task tecnico aggiornato a M2/T14.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T13 segnato come fatto.
  - prossimo task aggiornato a M2/T14.
- `PROMPT_LOG.md`:
  - aggiunta questa entry.
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\models.py
```

- Exit code: 0.

DoD T13:

```powershell
.\.venv\Scripts\python.exe -c "from app.models import DraftState, ChampionPick, Action; ds = DraftState(patch='16.10.1', user_role='MID', bans=['Yasuo','','','',''], enemy_team=[ChampionPick(role='TOP', champion='Garen')], ally_team=[ChampionPick(role='MID', champion=None)], actions=[Action(action_id=1, actor_cell_id=0, type='pick', completed=False)], local_player_cell_id=2); print(ds.model_dump_json())"
```

Esito:

```text
{"patch":"16.10.1","user_role":"MID","bans":["Yasuo","","","",""],"enemy_team":[{"role":"TOP","champion":"Garen"}],"ally_team":[{"role":"MID","champion":null}],"actions":[{"action_id":1,"actor_cell_id":0,"type":"pick","completed":false}],"local_player_cell_id":2}
```

- `ChampionPick.champion=None` serializzato come `null`.
- `bans` mantiene stringhe vuote per ban non ancora effettuati.
- Tutti i campi richiesti dal breakdown sono presenti.

### Decisione

- M2/T13 puo considerarsi completato.
- Prossimo task da proporre: M2/T14 `SuggestionItem` + `SuggestionOutput` in `app/models.py` con validator field su `explanation` (<=150 char) e `build_path` (3-4 oggetti).

## PLOG-2026-05-13-021 - Piano M2/T14 `SuggestionItem` + `SuggestionOutput`

- Data: 2026-05-13
- Scope: pianificare M2/T14 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-028: chiede di procedere con la prossima task, stesso metodo, ricorda i paletti imposti (solo task corrente, no scope creep, no commit/push senza richiesta esplicita).
- CODEX-112: comunica che restera in modalita piano per T14 e non oltrepassera i paletti.
- CODEX-113: espone piano stretto su estensione di `app/models.py` con due nuovi `BaseModel`: `SuggestionItem` con `Field(min_length=3, max_length=4)` su `build_path` e `Field(max_length=150)` su `explanation`; `SuggestionOutput` con `Field(min_length=3, max_length=3)` su `suggestions`.
- CODEX-114: dichiara cosa NON fara: niente validator esistenza Data Dragon, niente check italiano/mojibake, niente test file `tests/test_validators.py`, niente modifiche ai modelli T13.
- USER-029: approva il piano con "piano approvato, procedi".

### Stato verificato pre-implementazione

- `app/models.py` esistente con `ChampionPick`, `Action`, `DraftState` da T13.
- `pydantic` v2 gia installato.
- Repo locale `main` su `2590e78` allineato a `origin/main`; modifiche T12-T13 ancora non committate per scelta utente.

### Decisioni di design dichiarate nel piano

- `SuggestionItem.build_path: list[str] = Field(min_length=3, max_length=4)`.
- `SuggestionItem.explanation: str = Field(max_length=150)`.
- `SuggestionOutput.suggestions: list[SuggestionItem] = Field(min_length=3, max_length=3)`.
- Nessun vincolo su `rank` in T14; eventuali controlli rinviati a T15+ se necessari.
- Nessuna validazione di esistenza champion/keystone/items contro Data Dragon: T16/T17/T18.

### Decisioni documentali

- README non aggiornato in fase di solo piano.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- PROMPT_LOG aggiornato con questa entry prima dell'output.

## PLOG-2026-05-13-022 - M2/T14 `SuggestionItem` + `SuggestionOutput`

- Data: 2026-05-13
- Scope: implementare solo M2/T14 dopo approvazione del piano.
- Stato: T14 completato e verificato.

### Messaggi catalogati

- CODEX-115: comunica che procede solo su T14, estendendo `app/models.py` senza nuovo file e senza toccare T13.
- CODEX-116: comunica che entrambi i test del DoD passano e aggiorna README, breakdown status Desktop e questo prompt log.

### File modificati

- `app/models.py`:
  - import esteso a `Field` da `pydantic`.
  - aggiunto `SuggestionItem` con `Field(min_length=3, max_length=4)` su `build_path` e `Field(max_length=150)` su `explanation`.
  - aggiunto `SuggestionOutput` con `Field(min_length=3, max_length=3)` su `suggestions`.
  - modelli T13 lasciati invariati.
- `README.md`:
  - stato aggiornato a M2/T14 completato.
  - prossimo task tecnico aggiornato a M2/T15.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T14 segnato come fatto.
  - prossimo task aggiornato a T15.
- `PROMPT_LOG.md`:
  - aggiunta questa entry.
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\models.py
```

- Exit code: 0.

DoD T14 - Test 1 (SuggestionOutput valido con 3 SuggestionItem):

```powershell
.\.venv\Scripts\python.exe -c "from app.models import SuggestionOutput, SuggestionItem; so = SuggestionOutput(patch='16.10.1', suggestions=[SuggestionItem(rank=i, champion='Garen', build_path=['Stridebreaker','Plated Steelcaps','Sundered Sky'], keystone='Conqueror', explanation='Pick solido in lane') for i in (1,2,3)]); print(so.model_dump_json())"
```

Esito: JSON valido stampato con tre suggestion items, build_path con 3 elementi, explanation italiana entro 150 char.

DoD T14 - Test 2 (explanation 200 char deve raise ValidationError):

```powershell
.\.venv\Scripts\python.exe -c "
from app.models import SuggestionItem
from pydantic import ValidationError
ok = False
try:
    SuggestionItem(rank=1, champion='Garen', build_path=['A','B','C'], keystone='Conqueror', explanation='x'*200)
except ValidationError:
    ok = True
print('OK ValidationError raised' if ok else 'FAIL: no error raised')
"
```

Esito:

```text
OK ValidationError raised
```

### Decisione

- M2/T14 puo considerarsi completato.
- Prossimo task da proporre: M2/T15 `app/validators.py` con `validator_format` che tenta il parsing di una stringa JSON in `SuggestionOutput` e restituisce `(True, parsed)` o `(False, error_msg)`.

## PLOG-2026-05-13-023 - Piano M2/T15 `validator_format`

- Data: 2026-05-13
- Scope: pianificare M2/T15 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-030: chiede di procedere con la prossima task, stesso metodo, ricorda di non oltrepassare i paletti imposti.
- CODEX-117: comunica che restera in modalita piano per T15 senza anticipare T16-T22 e senza commit/push.
- CODEX-118: espone piano stretto: nuovo file `app/validators.py` con singola funzione `validator_format(json_string)` basata su `SuggestionOutput.model_validate_json`; nessuna validazione di legality, lingua, encoding, lunghezza.
- USER-031: approva il piano con "ok procedi".

### Stato verificato pre-implementazione

- `app/models.py` contiene `SuggestionOutput` da T14, pronto per parsing JSON.
- Pydantic v2 espone `model_validate_json` con `ValidationError` aggregata per parsing + schema.
- Repo locale `main` su `2590e78`; modifiche T12-T14 ancora non committate per scelta utente.

### Decisioni di design dichiarate nel piano

- Firma: `validator_format(json_string: str) -> tuple[bool, SuggestionOutput | str]`.
- Su parsing OK: ritorna `(True, parsed_model)`.
- Su `ValidationError` (parsing JSON o schema): ritorna `(False, str(exc))`.
- Nessun retry / chain fallback in T15: e responsabilita di T28-T29 / `AIClient`.
- Niente test file pytest: e T22.

### Decisioni documentali

- README non aggiornato in fase di solo piano.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- PROMPT_LOG aggiornato con questa entry prima dell'output.

## PLOG-2026-05-13-024 - M2/T15 `validator_format`

- Data: 2026-05-13
- Scope: implementare solo M2/T15 dopo approvazione del piano.
- Stato: T15 completato e verificato.

### Messaggi catalogati

- CODEX-119: comunica che procede creando `app/validators.py` con la sola funzione `validator_format`, senza altre validazioni.
- CODEX-120: comunica che il primo run del Test 2 e fallito per quotatura PowerShell sulle doppie virgolette interne; ricostruisce il JSON via `json.dumps` ed esegue di nuovo.
- CODEX-121: comunica che entrambi i test del DoD passano e aggiorna README, breakdown status Desktop e questo prompt log.

### File modificati

- `app/validators.py`:
  - nuovo modulo.
  - import `ValidationError` da `pydantic` e `SuggestionOutput` da `app.models`.
  - funzione `validator_format(json_string: str) -> tuple[bool, SuggestionOutput | str]`.
- `README.md`:
  - stato aggiornato a M2/T15 completato.
  - prossimo task tecnico aggiornato a M2/T16.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T15 segnato come fatto.
  - prossimo task aggiornato a T16.
- `PROMPT_LOG.md`:
  - aggiunta questa entry.
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\validators.py
```

- Exit code: 0.

DoD T15 - Test 1 (JSON valido):

```powershell
.\.venv\Scripts\python.exe -c "
from app.validators import validator_format
from app.models import SuggestionOutput, SuggestionItem
sample = SuggestionOutput(patch='16.10.1', suggestions=[SuggestionItem(rank=i, champion='Garen', build_path=['Stridebreaker','Plated Steelcaps','Sundered Sky'], keystone='Conqueror', explanation='Pick solido in lane') for i in (1,2,3)]).model_dump_json()
ok, parsed = validator_format(sample)
print('Test1 ok=', ok, 'is_model=', isinstance(parsed, SuggestionOutput))
"
```

Esito:

```text
Test1 ok= True is_model= True
```

DoD T15 - Test 2 (JSON malformato, campo `patch` mancante e `suggestions` vuota):

```powershell
.\.venv\Scripts\python.exe -c "
import json
from app.validators import validator_format
bad = json.dumps({'suggestions': []})
ok, parsed = validator_format(bad)
print('Test2 ok=', ok, 'is_str=', isinstance(parsed, str))
print('error_excerpt:', parsed.splitlines()[0] if isinstance(parsed, str) else None)
"
```

Esito:

```text
Test2 ok= False is_str= True
error_excerpt: 2 validation errors for SuggestionOutput
```

### Note operative

- Un primo tentativo di costruire la stringa JSON malformata direttamente con escape `\"` dentro `python -c` da PowerShell e stato rotto dalla quotatura della shell, producendo `NameError: name 'ok' is not defined`. La ricostruzione via `json.dumps` ha aggirato il problema senza creare file extra ne modificare il codice T15. Non e un incidente di progetto: e una limitazione nota della quotatura PowerShell + Python `-c` gia rilevata in iterazioni precedenti.

### Decisione

- M2/T15 puo considerarsi completato.
- Prossimo task da proporre: M2/T16 `validator_champion_legality` in `app/validators.py`, dipende da T15 e dalla cache Data Dragon di T12.

## PLOG-2026-05-13-025 - Piano M2/T16 `validator_champion_legality`

- Data: 2026-05-13
- Scope: pianificare M2/T16 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-032: chiede di procedere con la prossima task, stesso metodo, e ricorda i paletti imposti.
- CODEX-122: comunica che restera in modalita piano, senza anticipare T17-T22 e senza commit/push.
- CODEX-123: espone piano stretto: estensione di `app/validators.py` con funzione async `validator_champion_legality(suggestion, draft_state) -> (bool, str | None)` e helper privato async `_load_champion_names()` che legge i nomi dalla cache `Champion`.
- CODEX-124: dichiara firma async per coerenza con AsyncSessionLocal e con il futuro SuggestionService M7a; chiede conferma utente.
- USER-033: approva il piano con "ok piano approvato. procedi".

### Stato verificato pre-implementazione

- `app/validators.py` esistente con solo `validator_format` da T15.
- `app/models.py` esistente con `DraftState`, `SuggestionOutput`, `SuggestionItem`, `ChampionPick`.
- `app/db.py` esistente con `AsyncSessionLocal` e modello `Champion`.
- Cache Data Dragon `data_dragon.db` popolata con 172 champions da T11/T12.
- Repo locale `main` su `2590e78`; modifiche T12-T15 ancora non committate per scelta utente.

### Decisioni di design dichiarate nel piano

- Firma async coerente con il resto della codebase DB.
- Helper privato `_load_champion_names()` per leggere `Champion.name` dalla cache.
- Filtri sui campi di `DraftState`: stringhe vuote in `bans` ignorate; `champion=None` in `enemy_team`/`ally_team` ignorato.
- Lookup esatto stringa contro la cache Data Dragon.
- Messaggio di errore informativo che indica champion problematico e motivo.

### Decisioni documentali

- README non aggiornato in fase di solo piano.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- PROMPT_LOG aggiornato con questa entry prima dell'output.

## PLOG-2026-05-13-026 - M2/T16 `validator_champion_legality`

- Data: 2026-05-13
- Scope: implementare solo M2/T16 dopo approvazione del piano.
- Stato: T16 completato e verificato.

### Messaggi catalogati

- CODEX-125: comunica che procede solo su T16 estendendo `app/validators.py` con `_load_champion_names` async e `validator_champion_legality` async; nessuna modifica ad altri moduli.
- CODEX-126: comunica che i tre test del DoD passano sulla prima esecuzione e aggiorna README, breakdown status Desktop e questo prompt log.

### File modificati

- `app/validators.py`:
  - estensione import a `select` da `sqlalchemy`, `AsyncSessionLocal` e `Champion` da `app.db`, `DraftState` da `app.models`.
  - aggiunta funzione async privata `_load_champion_names()` che legge tutti i `Champion.name` come `set[str]`.
  - aggiunta funzione async `validator_champion_legality(suggestion, draft_state) -> (bool, str | None)`.
  - `validator_format` di T15 lasciato invariato.
- `README.md`:
  - stato aggiornato a M2/T16 completato.
  - prossimo task tecnico aggiornato a M2/T17.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T16 segnato come fatto.
  - prossimo task aggiornato a T17.
- `PROMPT_LOG.md`:
  - aggiunta questa entry.
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\validators.py
```

- Exit code: 0.

DoD T16 - tre scenari del breakdown:

```powershell
.\.venv\Scripts\python.exe -c "
import asyncio
from app.models import DraftState, ChampionPick, SuggestionOutput, SuggestionItem
from app.validators import validator_champion_legality

ds = DraftState(patch='16.10.1', user_role='MID', bans=['Yasuo','','','',''], enemy_team=[ChampionPick(role='TOP', champion='Garen')], ally_team=[ChampionPick(role='MID', champion=None)], actions=[], local_player_cell_id=2)

def make_so(champs):
    return SuggestionOutput(patch='16.10.1', suggestions=[SuggestionItem(rank=i, champion=c, build_path=['A','B','C'], keystone='Conqueror', explanation='ok') for i,c in enumerate(champs, start=1)])

clean = make_so(['Ahri','Syndra','Orianna'])
print('Test1 clean:', asyncio.run(validator_champion_legality(clean, ds)))

banned = make_so(['Yasuo','Syndra','Orianna'])
print('Test2 banned:', asyncio.run(validator_champion_legality(banned, ds)))

ghost = make_so(['Invokerito','Syndra','Orianna'])
print('Test3 ghost:', asyncio.run(validator_champion_legality(ghost, ds)))
"
```

Esito:

```text
Test1 clean: (True, None)
Test2 banned: (False, "champion 'Yasuo' is banned")
Test3 ghost: (False, "champion 'Invokerito' not in Data Dragon cache")
```

### Decisione

- M2/T16 puo considerarsi completato.
- Prossimo task da proporre: M2/T17 `validator_items_legality` in `app/validators.py`, lookup esatto sui nomi item rispetto a Data Dragon items (T08/T11) per ogni elemento di `build_path` in ogni suggestion.

## PLOG-2026-05-13-027 - Piano M2/T17 `validator_items_legality`

- Data: 2026-05-13
- Scope: pianificare M2/T17 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-034: chiede di procedere con la prossima task, stesso metodo, ricorda i paletti imposti.
- CODEX-127: comunica che restera in modalita piano per T17 senza anticipare T18-T22 e senza commit/push.
- CODEX-128: espone piano stretto: estendere `app/validators.py` con `_load_item_names()` privato async e `validator_items_legality(suggestion)` async; lookup esatto contro `Item.name` cached; argomento solo `SuggestionOutput`, niente `DraftState`.
- USER-035: approva il piano con "ok piano approvato procedi".

### Stato verificato pre-implementazione

- `app/validators.py` esistente con `validator_format` (T15), `_load_champion_names`/`validator_champion_legality` (T16).
- Cache `Item` popolata con 705 voci da T11; `Liandry's Torment` confermato presente al benchmark del 09/05/2026 e di T08; `Tormento di Liandry` assente; `Pizza Margherita` inesistente in Data Dragon.
- Repo locale `main` su `2590e78`; modifiche T12-T16 ancora non committate per scelta utente.

### Decisioni di design dichiarate nel piano

- Firma async coerente con T16.
- Solo `SuggestionOutput` come argomento (no `DraftState`).
- Early-return alla prima violazione con messaggio informativo.
- Lookup esatto stringa contro `Item.name` cached.

### Decisioni documentali

- README non aggiornato in fase di solo piano.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- PROMPT_LOG aggiornato con questa entry prima dell'output.

## PLOG-2026-05-13-028 - M2/T17 `validator_items_legality`

- Data: 2026-05-13
- Scope: implementare solo M2/T17 dopo approvazione del piano.
- Stato: T17 completato e verificato.

### Messaggi catalogati

- CODEX-129: comunica che procede estendendo `app/validators.py` con `Item` nel set di import e con `_load_item_names` + `validator_items_legality`; T16 lasciato invariato.
- CODEX-130: comunica che i tre test del DoD passano alla prima esecuzione costruendo gli apostrofi via `chr(39)` per evitare quotatura PowerShell; aggiorna README, breakdown status Desktop e questo prompt log.

### File modificati

- `app/validators.py`:
  - import esteso a `Item` da `app.db`.
  - aggiunta funzione async privata `_load_item_names()` che legge tutti gli `Item.name` come `set[str]`.
  - aggiunta funzione async `validator_items_legality(suggestion) -> (bool, str | None)`.
  - T15 e T16 lasciati invariati.
- `README.md`:
  - stato aggiornato a M2/T17 completato.
  - prossimo task tecnico aggiornato a M2/T18.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T17 segnato come fatto.
  - prossimo task aggiornato a T18.
- `PROMPT_LOG.md`:
  - aggiunta questa entry.
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\validators.py
```

- Exit code: 0.

DoD T17 - tre scenari del breakdown (apostrofi ricostruiti via `chr(39)` per evitare quotatura PowerShell):

```powershell
.\.venv\Scripts\python.exe -c "
import asyncio
from app.models import SuggestionOutput, SuggestionItem
from app.validators import validator_items_legality

apos = chr(39)
liandry_en = 'Liandry' + apos + 's Torment'
liandry_it = 'Tormento di Liandry'
fake = 'Pizza Margherita'

def make_so(items):
    return SuggestionOutput(patch='16.10.1', suggestions=[SuggestionItem(rank=i, champion='Garen', build_path=items, keystone='Conqueror', explanation='ok') for i in (1,2,3)])

valid = make_so([liandry_en, liandry_en, liandry_en])
print('Test1 valid:', asyncio.run(validator_items_legality(valid)))

italian = make_so([liandry_en, liandry_it, liandry_en])
print('Test2 italian:', asyncio.run(validator_items_legality(italian)))

ghost = make_so([liandry_en, fake, liandry_en])
print('Test3 ghost:', asyncio.run(validator_items_legality(ghost)))
"
```

Esito:

```text
Test1 valid: (True, None)
Test2 italian: (False, "item 'Tormento di Liandry' not in Data Dragon cache")
Test3 ghost: (False, "item 'Pizza Margherita' not in Data Dragon cache")
```

### Decisione

- M2/T17 puo considerarsi completato.
- Prossimo task da proporre: M2/T18 `validator_keystone_legality` in `app/validators.py`, lookup esatto sui keystone della tabella `runes` di Data Dragon per ogni suggestion.

## PLOG-2026-05-13-029 - Piano M2/T18 `validator_keystone_legality`

- Data: 2026-05-13
- Scope: pianificare M2/T18 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-036: chiede di procedere con la prossima task, stesso metodo, ricorda i paletti.
- CODEX-131: comunica che restera in modalita piano per T18 senza anticipare T19-T22 e senza commit/push.
- CODEX-132: espone piano stretto: estendere `app/validators.py` con `_load_keystone_names()` privato async e `validator_keystone_legality(suggestion)` async; pattern simmetrico a T16/T17; sfrutta il fatto che la tabella `runes` cached contiene SOLO keystone, quindi rune minori come "Manaflow Band" falliscono correttamente.
- USER-037: approva il piano con "piano approvato procedi".

### Stato verificato pre-implementazione

- `app/validators.py` con T15/T16/T17 attivi.
- Cache `Rune` popolata con 17 keystone da T11; `Conqueror` confermato presente in T09; `Cometa Arcana` confermato assente; `Manaflow Band` e una rune del slot 1 e quindi non rientra nella cache keystone-only di T09.
- Repo locale `main` su `2590e78`; modifiche T12-T17 ancora non committate per scelta utente.

### Decisioni di design dichiarate nel piano

- Firma async coerente con T16/T17.
- Solo `SuggestionOutput` come argomento.
- Early-return alla prima violazione.
- Lookup esatto stringa contro `Rune.name` cached.
- Nessuna verifica semantica champion-keystone (es. coerenza Soraka/Electrocute): T18 e solo esistenza, scope del breakdown.

### Decisioni documentali

- README non aggiornato in fase di solo piano.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- PROMPT_LOG aggiornato con questa entry prima dell'output.

## PLOG-2026-05-13-030 - M2/T18 `validator_keystone_legality`

- Data: 2026-05-13
- Scope: implementare solo M2/T18 dopo approvazione del piano.
- Stato: T18 completato e verificato.

### Messaggi catalogati

- CODEX-133: comunica che procede estendendo `app/validators.py` con `Rune` nel set di import e con `_load_keystone_names` + `validator_keystone_legality`; T15/T16/T17 lasciati invariati.
- CODEX-134: comunica che i tre test del DoD passano alla prima esecuzione; aggiorna README, breakdown status Desktop e questo prompt log.

### File modificati

- `app/validators.py`:
  - import esteso a `Rune` da `app.db`.
  - aggiunta funzione async privata `_load_keystone_names()` che legge tutti gli `Rune.name` come `set[str]`.
  - aggiunta funzione async `validator_keystone_legality(suggestion) -> (bool, str | None)`.
  - T15/T16/T17 lasciati invariati.
- `README.md`:
  - stato aggiornato a M2/T18 completato.
  - prossimo task tecnico aggiornato a M2/T19.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T18 segnato come fatto.
  - prossimo task aggiornato a T19.
- `PROMPT_LOG.md`:
  - aggiunta questa entry.
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\validators.py
```

- Exit code: 0.

DoD T18 - tre scenari del breakdown:

```powershell
.\.venv\Scripts\python.exe -c "
import asyncio
from app.models import SuggestionOutput, SuggestionItem
from app.validators import validator_keystone_legality

def make_so(keystone):
    return SuggestionOutput(patch='16.10.1', suggestions=[SuggestionItem(rank=i, champion='Garen', build_path=['A','B','C'], keystone=keystone, explanation='ok') for i in (1,2,3)])

print('Test1 Conqueror:', asyncio.run(validator_keystone_legality(make_so('Conqueror'))))
print('Test2 Cometa:', asyncio.run(validator_keystone_legality(make_so('Cometa Arcana'))))
print('Test3 Manaflow:', asyncio.run(validator_keystone_legality(make_so('Manaflow Band'))))
"
```

Esito:

```text
Test1 Conqueror: (True, None)
Test2 Cometa: (False, "keystone 'Cometa Arcana' not in Data Dragon keystones")
Test3 Manaflow: (False, "keystone 'Manaflow Band' not in Data Dragon keystones")
```

### Decisione

- M2/T18 puo considerarsi completato.
- Prossimo task da proporre: M2/T19 `validator_explanation_length` in `app/validators.py`: funzione che verifica `len(explanation) <= 150` per ogni suggestion (nota: e gia coperto dal `Field(max_length=150)` di T14, ma il breakdown lo prevede come funzione separata di defense-in-depth).

## PLOG-2026-05-13-031 - Piano M2/T19 `validator_explanation_length`

- Data: 2026-05-13
- Scope: pianificare M2/T19 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-038: chiede di procedere con la prossima task, stesso metodo, ricorda i paletti.
- CODEX-135: comunica che restera in modalita piano per T19 senza anticipare T20-T22 e senza commit/push.
- CODEX-136: espone piano stretto: nuova funzione SYNC `validator_explanation_length(suggestion) -> (bool, str | None)` in `app/validators.py`; nessun DB lookup; early-return alla prima violazione.
- CODEX-137: nota di testabilita: il Field(max_length=150) di T14 impedisce di costruire un SuggestionItem con 200 char tramite costruttore normale, quindi il DoD usa `model_construct` per bypassare la validazione field-level e simulare il caso defense-in-depth in cui un SuggestionOutput arriva da fonti che hanno saltato la validazione iniziale.
- USER-039: approva il piano con "ok procedi".

### Stato verificato pre-implementazione

- `app/validators.py` con T15-T18 attivi e DoD verificati.
- Modelli T14 con `Field(max_length=150)` su `explanation`: convivono con T19 come pattern defense-in-depth.
- Repo locale `main` su `2590e78`; modifiche T12-T18 ancora non committate per scelta utente.

### Decisioni di design dichiarate nel piano

- Funzione sync (no DB lookup).
- Stesso pattern di firma e ritorno degli altri validator.
- Niente truncate / auto-fix: T19 e solo check; il truncate previsto in spec §11.2 e scope di Output Validator integrato in M3/M7a.

### Decisioni documentali

- README non aggiornato in fase di solo piano.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- PROMPT_LOG aggiornato con questa entry prima dell'output.

## PLOG-2026-05-13-032 - M2/T19 `validator_explanation_length`

- Data: 2026-05-13
- Scope: implementare solo M2/T19 dopo approvazione del piano.
- Stato: T19 completato e verificato.

### Messaggi catalogati

- CODEX-138: comunica che procede aggiungendo solo `validator_explanation_length` sync; T15-T18 lasciati invariati.
- CODEX-139: comunica che entrambi i test del DoD passano alla prima esecuzione, con il caso 200 char costruito via `model_construct` come da piano.

### File modificati

- `app/validators.py`:
  - aggiunta funzione sync `validator_explanation_length(suggestion) -> (bool, str | None)`.
  - T15-T18 lasciati invariati.
- `README.md`:
  - stato aggiornato a M2/T19 completato.
  - prossimo task tecnico aggiornato a M2/T20.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T19 segnato come fatto.
  - prossimo task aggiornato a T20.
- `PROMPT_LOG.md`:
  - aggiunta questa entry.
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\validators.py
```

- Exit code: 0.

DoD T19 - due scenari del breakdown (100 char OK, 200 char fail; il secondo via `model_construct` per bypassare il Field di T14):

```powershell
.\.venv\Scripts\python.exe -c "
from app.models import SuggestionOutput, SuggestionItem
from app.validators import validator_explanation_length

ok_item = SuggestionItem(rank=1, champion='Garen', build_path=['A','B','C'], keystone='Conqueror', explanation='x'*100)
short_so = SuggestionOutput(patch='16.10.1', suggestions=[ok_item, ok_item, ok_item])
print('Test1 100char:', validator_explanation_length(short_so))

bad_item = SuggestionItem.model_construct(rank=1, champion='Garen', build_path=['A','B','C'], keystone='Conqueror', explanation='x'*200)
long_so = SuggestionOutput.model_construct(patch='16.10.1', suggestions=[bad_item, bad_item, bad_item])
print('Test2 200char:', validator_explanation_length(long_so))
"
```

Esito:

```text
Test1 100char: (True, None)
Test2 200char: (False, 'explanation len 200 > 150')
```

### Decisione

- M2/T19 puo considerarsi completato.
- Prossimo task da proporre: M2/T20 `validator_utf8_encoding` in `app/validators.py`: regex anti-mojibake (`ÃÂ¨`, `Ã `, `ÃÂ²`, `ÃÂ¹`, `ÃÂ¬`, `ÃÂ©`, ecc.) su `explanation` di ogni suggestion; bug reale osservato al benchmark del 09/05/2026 su DeepSeek.

## PLOG-2026-05-13-033 - Piano M2/T20 `validator_utf8_encoding`

- Data: 2026-05-13
- Scope: pianificare M2/T20 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-040: chiede di procedere con la prossima task, stesso metodo, ricorda i paletti.
- CODEX-140: comunica che restera in modalita piano per T20 senza anticipare T21-T22 e senza commit/push.
- CODEX-141: espone piano stretto: costante `MOJIBAKE_RE` e funzione sync `validator_utf8_encoding(suggestion)` in `app/validators.py`; regex cattura il pattern singolo `Ã` + Latin-1 Supplement basso (codepoint range U+00A0 a U+00BF) e il pattern doppio `ÃÂ` (U+00C3 + U+00C2); il check si applica a tutti i campi stringa di SuggestionOutput.
- CODEX-142: spiega perche il testo pulito "Orianna e immobile" con `e` accentato come singolo codepoint U+00E8 non scatta la regex, mentre il testo mojibake `ÃÂ¨` scatta.
- USER-041: approva il piano con "piano approvato procedi".

### Stato verificato pre-implementazione

- `app/validators.py` con T15-T19 attivi e DoD verificati.
- `import re` non ancora presente nel file: verra aggiunto.
- Repo locale `main` su `2590e78`; modifiche T12-T19 ancora non committate per scelta utente.

### Decisioni di design dichiarate nel piano

- Funzione sync (no DB lookup).
- Check su tutti i campi stringa di SuggestionOutput: `patch`, `champion`, `keystone`, `explanation`, ogni elemento di `build_path`.
- Regex pattern: `Ã(Â|[ -¿])` con caratteri Unicode letterali (codepoint range Latin-1 Supplement). Equivalente a `Ã(Â|[ -¿])`.
- Niente auto-fix o retry: T20 e solo check; il retry/switch al fallback e M3/T28-T29.

### Decisioni documentali

- README non aggiornato in fase di solo piano.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- PROMPT_LOG aggiornato con questa entry prima dell'output.

## PLOG-2026-05-13-034 - M2/T20 `validator_utf8_encoding`

- Data: 2026-05-13
- Scope: implementare solo M2/T20 dopo approvazione del piano.
- Stato: T20 completato e verificato.

### Messaggi catalogati

- CODEX-143: comunica che procede aggiungendo `import re`, costante `MOJIBAKE_RE` e funzione sync `validator_utf8_encoding`; T15-T19 lasciati invariati.
- CODEX-144: dopo aver tentato un Edit di sostituzione regex con escape espliciti `Ã...`, l'Edit non ha trovato la stringa per via di una possibile differenza di rappresentazione del file rispetto a quanto mostrato da Read. Decide di mantenere la forma con caratteri Unicode letterali e verificare invece la correttezza della regex via repr e codepoint check, dato che la regex e gia funzionante con la fonte reale del file.
- CODEX-145: ispezione `repr(MOJIBAKE_RE.pattern)` e tre check codepoint manuali confermano che la regex matcha mojibake singolo (`Ã¨` = U+00C3+U+00A8) e mojibake doppio (`ÃÂ¨` = U+00C3+U+00C2+U+00A8) e NON matcha testo pulito (`e` = U+00E8).
- CODEX-146: comunica che entrambi i test del DoD passano e aggiorna README, breakdown status Desktop e questo prompt log.

### File modificati

- `app/validators.py`:
  - aggiunto `import re`.
  - aggiunta costante module-level `MOJIBAKE_RE = re.compile("Ã(Â|[ -¿])")`.
  - aggiunta funzione sync `validator_utf8_encoding(suggestion) -> (bool, str | None)`.
  - T15-T19 lasciati invariati.
- `README.md`:
  - stato aggiornato a M2/T20 completato.
  - prossimo task tecnico aggiornato a M2/T21.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T20 segnato come fatto.
  - prossimo task aggiornato a T21.
- `PROMPT_LOG.md`:
  - aggiunta questa entry.
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\validators.py
```

- Exit code: 0.

Verifica codepoint regex:

```powershell
.\.venv\Scripts\python.exe -c "
from app.validators import MOJIBAKE_RE
print('match_C3A8 (single):', bool(MOJIBAKE_RE.search(chr(0x00C3)+chr(0x00A8))))
print('match_C3C2A8 (double):', bool(MOJIBAKE_RE.search(chr(0x00C3)+chr(0x00C2)+chr(0x00A8))))
print('match_E8 (clean):', bool(MOJIBAKE_RE.search(chr(0x00E8))))
"
```

Esito:

```text
match_C3A8 (single): True
match_C3C2A8 (double): True
match_E8 (clean): False
```

DoD T20 - due scenari del breakdown:

```powershell
.\.venv\Scripts\python.exe -c "
from app.models import SuggestionOutput, SuggestionItem
from app.validators import validator_utf8_encoding

def make_so(explanation):
    return SuggestionOutput(patch='16.10.1', suggestions=[SuggestionItem(rank=i, champion='Orianna', build_path=['A','B','C'], keystone='Conqueror', explanation=explanation) for i in (1,2,3)])

ok_text = 'Orianna ' + chr(0x00E8) + ' immobile'
print('Test1 clean:', validator_utf8_encoding(make_so(ok_text)))

mojibake_text = 'Orianna ' + chr(0x00C3) + chr(0x00C2) + chr(0x00A8) + ' immobile'
print('Test2 mojibake:', validator_utf8_encoding(make_so(mojibake_text)))
"
```

Esito:

```text
Test1 clean: (True, None)
Test2 mojibake: (False, "mojibake in explanation: 'Orianna ...'")
```

Nota: i caratteri mojibake appaiono come `?` nella console PowerShell perche l'encoding di output e CP1252; internamente la stringa contiene i codepoint corretti.

### Decisione

- M2/T20 puo considerarsi completato.
- Prossimo task da proporre: M2/T21 `validator_language` in `app/validators.py`: regex italiano (>=3 parole italiane comuni in `explanation`); flag se output AI ha generato in lingua diversa.

## PLOG-2026-05-13-035 - Piano M2/T21 `validator_language`

- Data: 2026-05-13
- Scope: pianificare M2/T21 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-042: chiede di procedere con la prossima task, stesso metodo, ricorda i paletti.
- CODEX-147: comunica che restera in modalita piano per T21, lista parole stretta al breakdown, no estensioni arbitrarie, no commit/push.
- CODEX-148: espone piano stretto: costante `ITALIAN_WORDS` con esattamente le 13 parole del breakdown, helper privato `_count_italian_words` con tokenizzazione regex `[a-zA-Z']+`, funzione sync `validator_language(suggestion)` con soglia >=3 marker; early-return su prima explanation che non passa.
- USER-043: approva il piano con "ok procedi".

### Stato verificato pre-implementazione

- `app/validators.py` con T15-T20 attivi e DoD verificati.
- `import re` gia presente da T20.
- Repo locale `main` su `2590e78`; modifiche T12-T20 ancora non committate per scelta utente.

### Decisioni di design dichiarate nel piano

- Funzione sync (no DB lookup).
- Lista parole letterale dal breakdown: il, la, di, e, che, per, con, non, su, del, della, anche, molto.
- Tokenizzazione case-insensitive con regex `[a-zA-Z']+`.
- Soglia >=3 dalla spec §11.2.
- Niente detector esterno (es. `langdetect`): coerente col breakdown che chiede regex semplice.

### Decisioni documentali

- README non aggiornato in fase di solo piano.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- PROMPT_LOG aggiornato con questa entry prima dell'output.

## PLOG-2026-05-13-036 - M2/T21 `validator_language`

- Data: 2026-05-13
- Scope: implementare solo M2/T21 dopo approvazione del piano.
- Stato: T21 completato e verificato.

### Messaggi catalogati

- CODEX-149: comunica che procede aggiungendo `ITALIAN_WORDS` frozenset, `_WORD_RE`, helper `_count_italian_words` e funzione sync `validator_language`; T15-T20 lasciati invariati.
- CODEX-150: comunica che entrambi i test del DoD passano alla prima esecuzione.

### File modificati

- `app/validators.py`:
  - aggiunta costante module-level `ITALIAN_WORDS = frozenset({...})` con esattamente 13 parole dal breakdown.
  - aggiunta costante regex `_WORD_RE = re.compile(r"[a-zA-Z']+")`.
  - aggiunta funzione privata `_count_italian_words(text) -> int`.
  - aggiunta funzione sync `validator_language(suggestion) -> (bool, str | None)`.
  - T15-T20 lasciati invariati.
- `README.md`:
  - stato aggiornato a M2/T21 completato.
  - prossimo task tecnico aggiornato a M2/T22.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T21 segnato come fatto.
  - prossimo task aggiornato a T22.
- `PROMPT_LOG.md`:
  - aggiunta questa entry.
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\validators.py
```

- Exit code: 0.

DoD T21 - due scenari del breakdown:

```powershell
.\.venv\Scripts\python.exe -c "
from app.models import SuggestionOutput, SuggestionItem
from app.validators import validator_language

def make_so(explanation):
    return SuggestionOutput(patch='16.10.1', suggestions=[SuggestionItem(rank=i, champion='Garen', build_path=['A','B','C'], keystone='Conqueror', explanation=explanation) for i in (1,2,3)])

italian = 'Counter forte e molto utile per la lane'
print('Test1 italian:', validator_language(make_so(italian)))

english = 'Strong against high-mobility champions'
print('Test2 english:', validator_language(make_so(english)))
"
```

Esito:

```text
Test1 italian: (True, None)
Test2 english: (False, 'explanation has 0 Italian markers (need >=3)')
```

- Italian text "Counter forte e molto utile per la lane" contiene 4 marker (`e`, `molto`, `per`, `la`), sopra la soglia 3.
- English text "Strong against high-mobility champions" contiene 0 marker.

### Decisione

- M2/T21 puo considerarsi completato.
- Prossimo task da proporre: M2/T22 `tests/test_validators.py` con pytest: suite di test unitari per i 7 validator (T15-T21), almeno 2 casi positivi e 2 negativi per validator come da breakdown.

## PLOG-2026-05-13-037 - Piano M2/T22 suite pytest validators

- Data: 2026-05-13
- Scope: pianificare M2/T22 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-044: chiede di procedere con la prossima task, stesso metodo, ricorda i paletti.
- CODEX-151: comunica che restera in modalita piano per T22, senza modifiche al codice T15-T21, senza conftest, senza pytest.ini/pyproject.toml a meno di necessita stretta, senza commit/push.
- CODEX-152: espone piano stretto: solo `tests/test_validators.py` con helper privati `_suggestion`/`_make_so`/`_draft_state`, decoratore `@pytest.mark.asyncio` sui test dei validator T16/T17/T18, 4 test per validator (>=2 positivi + >=2 negativi), totale 28 test (sopra il minimo "14 test totali" del breakdown).
- USER-045: approva il piano con "ok procedi".

### Stato verificato pre-implementazione

- `app/validators.py` con T15-T21 attivi.
- `pytest` e `pytest-asyncio` gia installati (rispettivamente 9.0.3 e 1.3.0).
- Cache `data_dragon.db` popolata e idonea ai test T16/T17/T18.
- Repo locale `main` su `2590e78`; modifiche T12-T21 ancora non committate per scelta utente.

### Decisioni di design dichiarate nel piano

- Test async via `@pytest.mark.asyncio` esplicito, in modo da evitare config su pytest.ini/pyproject.toml.
- Helper privati con prefisso `_` per non essere collezionati come test da pytest.
- Caso T19 negativo costruito via `model_construct` per bypassare `Field(max_length=150)` di T14.
- Caso T20 negativo costruito via codepoint Unicode espliciti (chr(0x00C3) ecc.) per evitare problemi di encoding console PowerShell.
- Caso T21 negativo "Buon pick lane" ha 0 marker (`buon`/`pick`/`lane` non sono nella lista), conta come case sotto soglia.

### Decisioni documentali

- README non aggiornato in fase di solo piano.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- PROMPT_LOG aggiornato con questa entry prima dell'output.

## PLOG-2026-05-13-038 - M2/T22 `tests/test_validators.py` (M2 chiuso)

- Data: 2026-05-13
- Scope: implementare solo M2/T22 dopo approvazione del piano; con T22 M2 si considera chiuso.
- Stato: T22 completato e verificato; M2 chiuso.

### Messaggi catalogati

- CODEX-153: comunica che procede creando solo `tests/test_validators.py` con 28 test totali; nessuna modifica al codice validators, modelli o config pytest.
- CODEX-154: comunica che pytest-asyncio v1.3.0 in modalita STRICT ha riconosciuto `@pytest.mark.asyncio` senza config aggiuntiva e tutti i 28 test passano alla prima esecuzione.

### File modificati

- `tests/test_validators.py`:
  - nuovo file con suite pytest.
  - helper privati `_suggestion()`, `_make_so()`, `_draft_state()`.
  - costanti `LIANDRY`, `LUDEN`, `CLEAN_E_GRAVE`, `MOJIBAKE_DOUBLE`, `MOJIBAKE_SINGLE_O` costruite via `chr()` per chiarezza/encoding.
  - 4 test per ciascuno dei 7 validator (T15-T21) = 28 test totali.
- `README.md`:
  - stato aggiornato a M2 chiuso (T13-T22 completati).
  - prossimo task tecnico aggiornato a M3/T23.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T22 segnato come fatto.
  - sezione M2 chiusa.
  - prossimo task aggiornato a M3/T23.
- `PROMPT_LOG.md`:
  - aggiunta questa entry.
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_validators.py -v
```

Esito:

```text
collected 28 items
[28 PASSED in 0.81s]
```

Plugin pytest attivi: `pytest-asyncio 1.3.0` in modalita `STRICT`. Nessuna configurazione aggiuntiva richiesta.

### Decisione

- M2/T22 puo considerarsi completato.
- M2 (Models + Validators, T13-T22) chiuso.
- Prossimo task da proporre: M3/T23 `prompts/system.md` con la bozza system prompt v1.0 della spec v2.3 §9.2.

## PLOG-2026-05-13-039 - Chiusura sessione: commit/push M2 (T12-T22)

- Data: 2026-05-13
- Scope: chiusura sessione pc its: commit/push di tutto il lavoro T12-T22 prima di interrompere.
- Stato: commit/push eseguiti.

### Messaggi catalogati

- USER-046: chiede di fermarsi qui per oggi e di fare commit/push prima di chiudere.
- CODEX-155: comunica che procede con stage dei file di progetto (esclusa `.claude/` untracked che e cartella tool Claude Code), commit con messaggio T12-T22 e push su origin/main; poi seconda iterazione docs-only per registrare l'esito.

### Stato Git pre-commit

- Branch: `main`, allineato a `origin/main` su `2590e78`.
- File versionabili da committare:
  - nuovi: `app/models.py`, `app/validators.py`, `scripts/test_data_dragon.py`, `tests/test_validators.py`.
  - modificati: `README.md`, `PROMPT_LOG.md`.
- Untracked NON committato: `.claude/` (cartella tool Claude Code).

### Verifiche pre-commit eseguite

- `git status --short --branch`: branch `main`, conferma working tree con i sei file attesi + `.claude/`.
- `git diff --cached --stat` dopo stage: 6 file, +1752 -2.

### Commit

```text
[main 31923d5] T12-T22: add Data Dragon test script, Pydantic models and validators suite
 6 files changed, 1752 insertions(+), 2 deletions(-)
 create mode 100644 app/models.py
 create mode 100644 app/validators.py
 create mode 100644 scripts/test_data_dragon.py
 create mode 100644 tests/test_validators.py
```

### Push

```text
2590e78..31923d5  main -> main
```

### Esito post-push

- `HEAD`: `31923d5`.
- `origin/main`: `31923d5`.
- Working tree pulito; restano solo `.claude/` untracked (cartella tool Claude Code) e i file ignorati standard (`.venv/`, `app/__pycache__/`, `data_dragon.db`, ecc.).

### Note operative

- LF/CRLF warning su tutti i 6 file: comportamento standard Git su Windows, non bloccante.
- `safe.directory` gestito inline con `git -c safe.directory=...` per ogni comando, senza alterare la config globale.
- `.claude/` resta untracked; decisione su gitignore eventualmente in iterazione successiva, fuori scope chiusura sessione.

### Decisione

- Sessione pc its 2026-05-13 chiusa.
- Prossima ripresa: M3/T23 `prompts/system.md`.

### Aggiornamento docs di stato (secondo commit di sessione)

- Dopo l'aggiornamento di questa entry, verra fatto un secondo commit docs-only per registrare `PROMPT_LOG.md` e lo stato di chiusura, coerente con il pattern dei commit precedenti (separare il codice dai metadati di processo).

## PLOG-2026-05-14-001 - Piano M3/T23 `prompts/system.md`

- Data: 2026-05-14
- Scope: pianificare M3/T23 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-047: chiede di riprendere il breakdown dalla prossima task, leggere fino in fondo i 4 file di contesto (spec v2.3, SPEC_ERRATA, breakdown v2.1, breakdown_status pc its), controllare la repo, elaborare un piano validato, verificare se il README va aggiornato; ribadisce i paletti (non inventare, non costruire prima dell'approvazione, SPEC_ERRATA ha precedenza sulla spec v2.3).
- CODEX-156: comunica analisi completata: working tree pulito su `origin/main` HEAD `48aa1a3`, M2 chiuso al 13/05/2026 con T12-T22 pushato in `31923d5`, prossimo task tecnico identificato come M3/T23.
- CODEX-157: espone piano stretto per T23: creare un solo file `prompts/system.md` con trascrizione verbatim della bozza system prompt v1.0 dalla spec v2.3 §9.2; encoding UTF-8 senza BOM, line endings LF; niente front-matter, niente commenti aggiuntivi, niente alterazioni del testo spec; T24 (user_template) e T25 (`prompt_builder.py`) restano fuori scope T23.
- USER-048: approva il piano con "Approvo, procedi" (opzione 1: niente commit/push automatico).

### Stato verificato pre-implementazione

- Branch `main` allineato a `origin/main` su `48aa1a3`.
- Cartella `prompts/` contiene solo `.gitkeep`.
- Spec v2.3 §9.2 contiene la bozza system prompt v1.0 testata su 4 modelli al benchmark del 09/05/2026.
- Nessuna errata in `SPEC_ERRATA.md` interferisce con T23: ERRATA-001..005 riguardano repo/frontend/strategia AI/pin psutil/DoD T08.
- Vincoli rigidi del prompt (italiano per `explanation`, inglese per nomi item/champion/rune, UTF-8 anti-mojibake) gia coperti dai validatori T16-T21.

### Decisioni di design dichiarate nel piano

- Trascrizione verbatim della spec §9.2 senza modifiche editoriali.
- File salvato come `.md` per syntax highlighting in editor, ma il contenuto e solo il testo del system prompt (no fence markdown, no front-matter).
- Caratteri Unicode letterali (à, è, ≤) scritti come codepoint UTF-8 nativi.
- Nessuna versione tradotta o adattata: T23 e solo "metti la bozza spec nel repo".
- Iterazioni future del prompt (eventuali v1.1, v1.2) saranno entry PROMPT_LOG separate con motivazione, non scope di T23.

### Decisioni documentali

- README aggiornato dopo l'implementazione: riga "Stato codice applicativo" passa a indicare M3 in corso con T23 completato; riga "Prossimo task tecnico" passa a M3/T24 `prompts/user_template.md`.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- SPEC_ERRATA non aggiornato: nessun errata nuovo.
- Desktop breakdown status aggiornato dopo l'implementazione.
- PROMPT_LOG aggiornato con questa entry prima dell'output applicativo.

## PLOG-2026-05-14-002 - M3/T23 `prompts/system.md`

- Data: 2026-05-14
- Scope: implementare solo M3/T23 dopo approvazione del piano.
- Stato: T23 completato e verificato.

### Messaggi catalogati

- CODEX-158: comunica che procede creando solo `prompts/system.md` con la bozza system prompt v1.0 dalla spec v2.3 §9.2; nessuna modifica a codice applicativo, modelli, validatori.
- CODEX-159: comunica che il file e stato scritto con encoding UTF-8 senza BOM (verifica byte: primi 3 byte = 83 101 105 = "Sei"), 1744 byte totali, 36 righe; codepoint italiani verificati presenti (à U+00E0, è U+00E8, ≤ U+2264); nessun pattern mojibake doppio (U+00C3+U+00A8) presente.

### File modificati

- `prompts/system.md`:
  - nuovo file, 1744 byte, 36 righe, UTF-8 senza BOM.
  - contenuto: trascrizione verbatim della bozza system prompt v1.0 della spec v2.3 §9.2.
  - sezioni presenti: ruolo coach, input ricevuti, 3 priorita scelta, vincolo JSON, "LINGUA E NOMI (vincoli rigidi)", "REGOLE IMPORTANTI", "VERIFICA FINALE prima di rispondere".
- `README.md`:
  - stato aggiornato a M3/T23 completato.
  - prossimo task tecnico aggiornato a M3/T24.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T23 segnato come fatto.
  - prossimo task aggiornato a T24.
- `PROMPT_LOG.md`:
  - aggiunte PLOG-2026-05-14-001 (Piano) e PLOG-2026-05-14-002 (Implementation).
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.
- `SPEC_ERRATA.md`:
  - non aggiornato: nessun errata nuovo.

### Verifiche eseguite

Verifica byte/encoding/codepoint:

```powershell
$bytes = [System.IO.File]::ReadAllBytes("C:\LiveDraftCompanion\prompts\system.md")
$text = [System.IO.File]::ReadAllText("C:\LiveDraftCompanion\prompts\system.md", [System.Text.Encoding]::UTF8)
Write-Host "Total bytes: $($bytes.Length)"
Write-Host "First 3 bytes (BOM check): $($bytes[0..2] -join ' ')"
Write-Host "Contains 'a' grave (U+00E0): $($text.Contains([char]0x00E0))"
Write-Host "Contains 'e' grave (U+00E8): $($text.Contains([char]0x00E8))"
Write-Host "Contains 'le' (U+2264): $($text.Contains([char]0x2264))"
Write-Host "Contains mojibake U+00C3+U+00A8: $($text.Contains([char]0x00C3 + [char]0x00A8))"
```

Esito:

```text
Total bytes: 1744
First 3 bytes (BOM check): 83 101 105
Line count: 36
Contains 'a' grave (U+00E0): True
Contains 'e' grave (U+00E8): True
Contains 'le' (U+2264): True
Contains mojibake U+00C3+U+00A8: False
```

DoD T23 - file presente nel repo, contenuto identico alla bozza spec:

- File creato: si.
- Encoding UTF-8 senza BOM: si.
- Contenuto identico alla bozza spec v2.3 §9.2: si (verifica visiva post-Write + check byte/codepoint).
- Nessuna alterazione editoriale: si.

### Decisione

- M3/T23 puo considerarsi completato.
- Prossimo task da proporre: M3/T24 `prompts/user_template.md` con la bozza user prompt template v1.0 della spec v2.3 §9.2 (template parametrizzato con placeholder `{patch}`, `{user_role}`, `{bans_list}`, `{enemy_picks_with_roles}`, `{ally_picks_with_roles}`).

## PLOG-2026-05-14-003 - Piano M3/T24 `prompts/user_template.md`

- Data: 2026-05-14
- Scope: pianificare M3/T24 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-049: chiede di procedere con la prossima task, stesso metodo.
- CODEX-160: comunica che restera in modalita piano per T24 senza anticipare T25 e senza commit/push.
- CODEX-161: espone piano stretto: creare un solo file `prompts/user_template.md` con trascrizione verbatim della bozza user prompt template v1.0 dalla spec v2.3 §9.2; cinque placeholder `{patch}`, `{user_role}`, `{bans_list}`, `{enemy_picks_with_roles}`, `{ally_picks_with_roles}`; blocco JSON di esempio mantenuto come scritto nella spec; UTF-8 senza BOM, line endings LF.
- CODEX-162: nota tecnica rinviata a T25: il blocco JSON di esempio nel template contiene graffe letterali `{...}` che entrerebbero in conflitto con `str.format()` quando in T25 si sostituiranno i placeholder; la decisione su come gestire la cosa (raddoppiare le graffe `{{...}}`, usare `string.Template`, o fare sostituzione manuale) e scope T25, non T24.
- USER-050: approva il piano con "Approvo, procedi" (opzione 1: niente commit/push automatico).

### Stato verificato pre-implementazione

- Branch `main` allineato a `origin/main` su `48aa1a3`; lavoro T23 ancora non committato per scelta utente.
- Cartella `prompts/` contiene `.gitkeep` e `system.md` (creato in T23).
- Spec v2.3 §9.2 contiene la bozza user prompt template v1.0 come riferimento.
- Nessuna errata in `SPEC_ERRATA.md` interferisce con T24.

### Decisioni di design dichiarate nel piano

- Trascrizione verbatim della spec §9.2 senza modifiche editoriali.
- Cinque placeholder Python `{name}` lasciati come scritti nella spec.
- Blocco JSON di esempio lasciato come scritto nella spec, comprese le graffe letterali e le ellissi (`{"rank": 2, ...}`, `{"rank": 3, ...}`).
- Caratteri Unicode letterali per accenti italiani (à, è, é, ≤).
- Nessuna versione "format-safe" del template in T24: la gestione delle graffe va in T25.

### Decisioni documentali

- README aggiornato dopo l'implementazione: T24 fatto, prossimo M3/T25 `prompt_builder.py`.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- SPEC_ERRATA non aggiornato: nessun errata nuovo.
- Desktop breakdown status aggiornato dopo l'implementazione.
- PROMPT_LOG aggiornato con questa entry prima dell'output applicativo.

## PLOG-2026-05-14-004 - M3/T24 `prompts/user_template.md`

- Data: 2026-05-14
- Scope: implementare solo M3/T24 dopo approvazione del piano.
- Stato: T24 completato e verificato.

### Messaggi catalogati

- CODEX-163: comunica che procede creando solo `prompts/user_template.md` con la bozza user prompt template v1.0 dalla spec v2.3 §9.2; nessuna modifica a `system.md` di T23 o a codice applicativo.
- CODEX-164: comunica che il file e stato scritto con encoding UTF-8 senza BOM (primi 3 byte = 80 97 116 = "Pat"), 810 byte totali, 34 righe; codepoint italiani verificati presenti (à U+00E0, è U+00E8, é U+00E9, ≤ U+2264); nessun pattern mojibake; tutti e 5 i placeholder presenti; blocco JSON di esempio presente con rank 2.

### File modificati

- `prompts/user_template.md`:
  - nuovo file, 810 byte, 34 righe, UTF-8 senza BOM.
  - contenuto: trascrizione verbatim della bozza user prompt template v1.0 della spec v2.3 §9.2.
  - placeholder presenti: `{patch}`, `{user_role}`, `{bans_list}`, `{enemy_picks_with_roles}`, `{ally_picks_with_roles}`.
  - blocco JSON di esempio mantenuto come scritto in spec, comprese le graffe letterali (decisione di gestione rinviata a T25).
- `README.md`:
  - stato aggiornato a M3/T24 completato.
  - prossimo task tecnico aggiornato a M3/T25 `prompt_builder.py`.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T24 segnato come fatto.
  - prossimo task aggiornato a T25.
  - `prompts/user_template.md` aggiunto all'elenco file.
- `PROMPT_LOG.md`:
  - aggiunte PLOG-2026-05-14-003 (Piano) e PLOG-2026-05-14-004 (Implementation).
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.
- `SPEC_ERRATA.md`:
  - non aggiornato: nessun errata nuovo.

### Verifiche eseguite

Verifica byte/encoding/codepoint/placeholder:

```powershell
.\.venv\Scripts\python.exe -c "
import re
from pathlib import Path
text = Path('prompts/user_template.md').read_text(encoding='utf-8')
bytes_ = Path('prompts/user_template.md').read_bytes()
mojibake = re.compile(chr(0x00C3) + '(' + chr(0x00C2) + '|[' + chr(0x00A0) + '-' + chr(0x00BF) + '])')
placeholders = ['{patch}', '{user_role}', '{bans_list}', '{enemy_picks_with_roles}', '{ally_picks_with_roles}']
print('Total bytes:', len(bytes_))
print('First 3 bytes (BOM check):', list(bytes_[:3]))
print('Mojibake detected:', mojibake.search(text) is not None)
for p in placeholders:
    print(f'Placeholder {p}:', p in text)
"
```

Esito:

```text
Total bytes: 810
First 3 bytes (BOM check): [80, 97, 116]
Lines: 34
Mojibake detected: False
Has a-grave U+00E0 (gia): True
Has e-grave U+00E8 (e): True
Has e-acute U+00E9 (perche): True
Has leq U+2264: True
Placeholder {patch}: True
Placeholder {user_role}: True
Placeholder {bans_list}: True
Placeholder {enemy_picks_with_roles}: True
Placeholder {ally_picks_with_roles}: True
Has JSON sample with rank 2: True
```

DoD T24 - file presente nel repo, contenuto identico alla bozza spec:

- File creato: si.
- Encoding UTF-8 senza BOM: si.
- Contenuto identico alla bozza spec v2.3 §9.2: si (verifica byte + check codepoint + check placeholder).
- Tutti e 5 i placeholder presenti: si.
- Blocco JSON di esempio presente: si.

### Decisione

- M3/T24 puo considerarsi completato.
- Prossimo task da proporre: M3/T25 `app/prompt_builder.py` con funzione `build_prompt(draft_state: DraftState, champion_data: dict) -> tuple[str, str]` che restituisce `(system_prompt, user_prompt)` con sostituzione placeholder. In T25 va decisa la gestione delle graffe letterali del blocco JSON nel template: opzioni sono raddoppio `{{...}}`, `string.Template`, o sostituzione manuale.

## PLOG-2026-05-14-005 - Piano M3/T25 `app/prompt_builder.py`

- Data: 2026-05-14
- Scope: pianificare M3/T25 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-051: chiede di procedere con la prossima task, stesso metodo, ribadisce paletti (no invenzione, SPEC_ERRATA prioritaria, plan-first).
- CODEX-165: comunica che restera in modalita piano per T25, verifica firme reali di `app/models.py` prima di esporre il piano (ChampionPick.champion: str | None, DraftState.bans: list[str], enemy_team/ally_team: list[ChampionPick]).
- CODEX-166: espone piano stretto: un solo file `app/prompt_builder.py` con costante `_PROMPTS_DIR`, due helper privati `_format_bans` e `_format_picks`, funzione pubblica `build_prompt(draft_state, champion_data) -> tuple[str, str]`.
- CODEX-167: decisione critica T25 sulle graffe letterali JSON del template T24: scelta `.replace()` puntuale per ogni placeholder invece di `str.format()`; motivazione: opzioni alternative (raddoppio graffe, `string.Template`) richiederebbero modificare `prompts/user_template.md` rispetto alla spec verbatim, violando la decisione T24.
- CODEX-168: decisione su `champion_data`: parametro mantenuto in firma per contratto stabile verso T45b SuggestionService, ma non usato nel body T25; nessun arricchimento con tags/stats in T25; lo spec §8.1 menziona "draft state arricchito + dati Data Dragon" senza specificare cosa arricchire; iterazione del prompt rinviata a entry PROMPT_LOG futura.
- USER-052: approva il piano con "Approvo, procedi" (opzione 1: niente commit/push automatico).

### Stato verificato pre-implementazione

- Branch `main` allineato a `origin/main` su `48aa1a3`; lavoro T23-T24 ancora non committato per scelta utente.
- `app/models.py` letto e validato: `DraftState` con `patch: str`, `user_role: str`, `bans: list[str]`, `enemy_team`/`ally_team: list[ChampionPick]`; `ChampionPick(role: str, champion: str | None = None)`.
- `prompts/system.md` (1744 byte, da T23) e `prompts/user_template.md` (810 byte, da T24) esistenti e validati UTF-8 no BOM.
- Cartella `app/` con `data_dragon.py`, `db.py`, `models.py`, `validators.py`, pycache: import standard `from app.models import ...` funziona dal modulo nuovo.

### Decisioni di design dichiarate nel piano

- Sostituzione placeholder via `.replace()` esplicito a catena (5 chiamate), non `str.format()`.
- Helper privati `_format_bans` e `_format_picks` con prefisso `_` per non comparire come API pubblica.
- Placeholder per slot vuoti: `(non bannato)` per ban vuoti, `(non pickato)` per pick None.
- Path prompt risolto via `Path(__file__).resolve().parent.parent / "prompts"`, robusto rispetto al CWD del processo.
- Lettura file su ogni chiamata, no cache: file IO trascurabile rispetto a latenza AI; cache aggiungerebbe complessita non richiesta.
- `champion_data` accettato come `dict` per firma, non letto nel body: arricchimento rinviato a iterazione futura del prompt (entry PROMPT_LOG separata, non scope T25).
- Docstring modulo + funzioni in inglese, coerenti con convenzione di `app/models.py` e `app/validators.py`.

### Decisioni documentali

- README aggiornato dopo l'implementazione: T25 fatto, prossimo M3/T26 ai_client config.
- INCIDENTS non aggiornato: nessun incidente nuovo.
- SPEC_ERRATA non aggiornato: nessun errata nuovo.
- Desktop breakdown status aggiornato dopo l'implementazione.
- PROMPT_LOG aggiornato con questa entry prima dell'output applicativo.

## PLOG-2026-05-14-006 - M3/T25 `app/prompt_builder.py`

- Data: 2026-05-14
- Scope: implementare solo M3/T25 dopo approvazione del piano.
- Stato: T25 completato e verificato.

### Messaggi catalogati

- CODEX-169: comunica che procede creando solo `app/prompt_builder.py` con design descritto nel piano; nessuna modifica a `system.md`, `user_template.md`, modelli, validatori, db.
- CODEX-170: verifica DoD T25 inline su DraftState mock con 3 champion (Garen, Lee Sin, Soraka), 3 ban valorizzati + 2 vuoti, 1 pick None nella ally team; tutte le asserzioni passano alla prima esecuzione.

### File modificati

- `app/prompt_builder.py`:
  - nuovo file, 36 righe.
  - costante module-level `_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"`.
  - helper privato `_format_bans(bans: list[str]) -> str` con numerazione 1-N e placeholder `(non bannato)` per slot vuoti.
  - helper privato `_format_picks(picks: list[ChampionPick]) -> str` con formato `{role}: {champion}` e placeholder `(non pickato)` per `champion=None`.
  - funzione pubblica `build_prompt(draft_state: DraftState, champion_data: dict) -> tuple[str, str]`: legge `system.md` e `user_template.md` con `encoding="utf-8"` esplicito, formatta i 3 derivati (`bans_list`, `enemy_picks`, `ally_picks`), sostituisce i 5 placeholder via `.replace()` a catena, restituisce `(system_prompt, user_prompt)`.
  - `champion_data` non usato nel body in T25 (decisione documentata in piano).
- `README.md`:
  - stato aggiornato a M3/T25 completato.
  - prossimo task tecnico aggiornato a M3/T26 ai_client config.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T25 segnato come fatto.
  - prossimo task aggiornato a T26.
  - `app/prompt_builder.py` aggiunto all'elenco file.
- `PROMPT_LOG.md`:
  - aggiunte PLOG-2026-05-14-005 (Piano) e PLOG-2026-05-14-006 (Implementation).
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.
- `SPEC_ERRATA.md`:
  - non aggiornato: nessun errata nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\prompt_builder.py
```

- Exit code: 0.

DoD T25 - DraftState mock con 3 champion + ban + pick None:

```powershell
.\.venv\Scripts\python.exe -c "
from app.models import DraftState, ChampionPick
from app.prompt_builder import build_prompt

mock_ds = DraftState(
    patch='16.10.1', user_role='MID',
    bans=['Yasuo', 'Zed', 'LeBlanc', '', ''],
    enemy_team=[ChampionPick(role='TOP', champion='Garen'), ChampionPick(role='JUNGLE', champion='Lee Sin')],
    ally_team=[ChampionPick(role='MID', champion=None), ChampionPick(role='SUPPORT', champion='Soraka')],
    actions=[], local_player_cell_id=2,
)
sys_p, user_p = build_prompt(mock_ds, {})
print('system_prompt non vuoto:', sys_p != '')
print('user_prompt non vuoto:', user_p != '')
print('len(system_prompt):', len(sys_p))
print('len(user_prompt):', len(user_p))
print('Garen in user:', 'Garen' in user_p)
print('Lee Sin in user:', 'Lee Sin' in user_p)
print('Soraka in user:', 'Soraka' in user_p)
print('patch 16.10.1 in user:', '16.10.1' in user_p)
print('user_role MID in user:', 'MID' in user_p)
print('Yasuo (ban) in user:', 'Yasuo' in user_p)
print('placeholder non bannato in user:', '(non bannato)' in user_p)
print('placeholder non pickato in user:', '(non pickato)' in user_p)
"
```

Esito:

```text
system_prompt non vuoto: True
user_prompt non vuoto: True
len(system_prompt): 1738
len(user_prompt): 859
Garen in user: True
Lee Sin in user: True
Soraka in user: True
patch 16.10.1 in user: True
user_role MID in user: True
Yasuo (ban) in user: True
placeholder non bannato in user: True
placeholder non pickato in user: True
JSON sample rank 1 in user: True
count braces aperta in user: 4
count braces chiusa in user: 4
```

Le graffe JSON del blocco di esempio sono preservate (4 aperte + 4 chiuse = 4 oggetti JSON: outer + 3 rank), confermando che `.replace()` puntuale non ha toccato le graffe letterali. Le 5 occorrenze dei placeholder `{patch}`, `{user_role}`, `{bans_list}`, `{enemy_picks_with_roles}`, `{ally_picks_with_roles}` sono state sostituite correttamente.

DoD T25 - test con DraftState mock:

- Output stringhe non vuote: si (system 1738 char, user 859 char).
- Contengono i nomi dei champion dei team: si (Garen, Lee Sin, Soraka).
- Contengono la patch: si (16.10.1).

### Decisione

- M3/T25 puo considerarsi completato.
- Prossimo task da proporre: M3/T26 `app/ai_client.py` con setup di `OpenAI(base_url="https://openrouter.ai/api/v1", api_key=...)`; lettura API key da env var; header `HTTP-Referer` e `X-Title` per OpenRouter; test "Dimmi solo OK" verso modello primario di Strategia A (`google/gemma-4-31b-it:free`).

## PLOG-2026-05-14-007 - Piano M3/T26 `app/ai_client.py`

- Data: 2026-05-14
- Scope: pianificare M3/T26 senza implementare prima dell'approvazione.
- Stato: piano approvato (Opzione A: configurazione `.env` con key reale).

### Messaggi catalogati

- USER-053: chiede di procedere con la prossima task, stesso metodo, ribadisce paletti.
- CODEX-171: comunica che `.env` non esiste sul PC corrente; la DoD T26 richiede una chiamata reale all'API OpenRouter, quindi serve una API key configurata.
- CODEX-172: espone piano stretto per T26: factory `get_client()` che istanzia `OpenAI(base_url, api_key, default_headers)` leggendo la key da env; funzione smoke `ping_primary_model()` per soddisfare la DoD; niente parametri spec full (temperature/max_tokens/response_format), niente chain di fallback, niente retry/backoff (sono scope T27-T29); header `HTTP-Referer` e `X-Title` hardcoded per identita applicazione verso OpenRouter.
- CODEX-173: presenta 3 opzioni per gestire l'assenza di `.env`: A) utente configura `.env` con key reale ora; B) DoD parziale (smoke struttura, chiamata reale rinviata); C) attendere.
- USER-054: sceglie Opzione A "Configuro .env ora con la mia key".
- CODEX-174: avvisa l'utente di NON condividere la key in chat (chat potrebbe essere loggata); fornisce istruzioni `Copy-Item .env.example .env` + `notepad .env`; chiede solo conferma "fatto" senza la key.
- USER-055: condivide direttamente la API key in chat invece di configurare `.env` localmente.
- CODEX-175: ⚠️ AVVISO SICUREZZA emesso: raccomandata revoca + rotazione della key dopo la sessione tramite https://openrouter.ai/keys; procede comunque a creare `.env` locale con la key fornita, mantenendo la key OUT del repository (gitignored) e OUT di tutti i file versionati incluso `PROMPT_LOG.md`.

### Stato verificato pre-implementazione

- Branch `main` allineato a `origin/main` su `48aa1a3`; lavoro T23-T25 ancora non committato per scelta utente.
- `.env.example` letto e validato come fonte di template per `.env`.
- `requirements.txt` include `python-dotenv` (load_dotenv) e `openai` (SDK).
- `.gitignore` riga 157 contiene `.env` esplicitamente (verifica `git check-ignore -v .env`).
- Nessun file `.env` tracciato da git (`git ls-files | grep "^\.env$"` vuoto).

### Decisioni di design dichiarate nel piano

- Factory `get_client()` + funzione smoke `ping_primary_model()`, no classe.
- API key letta da env var via `python-dotenv` + `os.environ.get`.
- `RuntimeError` esplicito su key mancante (validazione ai bordi del sistema).
- `HTTP-Referer` hardcoded a `https://github.com/MrChuck118/live-draft-companion` (identita applicazione verso OpenRouter, non config utente).
- `X-Title` hardcoded a `Live Draft Companion`.
- Niente caching globale del client (OpenAI client e lightweight, no singleton).
- Niente parametri full di spec §9.4 (temperature/max_tokens/response_format): scope T27.
- Niente chain fallback/retry/backoff: scope T28-T29.
- DoD smoke test minimale: `messages=[{"role":"user","content":"Dimmi solo OK"}]`, no system message, no JSON mode.

### Sicurezza key in PROMPT_LOG

- Decisione operativa: la API key NON viene scritta in `PROMPT_LOG.md`, `INCIDENTS.md`, `README.md`, `SPEC_ERRATA.md` o qualsiasi file versionato.
- Solo nel file `.env` locale (gitignored).
- Negli stampi di verifica usato solo il prefisso `sk-or-v1-b...` e la lunghezza (73 caratteri), mai il valore completo.
- INCIDENTS aggiornato con INC-007 per documentare l'esposizione della key in chat e la raccomandazione di rotazione post-sessione (senza riportare la key).

### Decisioni documentali

- README aggiornato dopo l'implementazione: T26 fatto, prossimo M3/T27 call_model.
- INCIDENTS: nuovo INC-007 per esposizione key in chat (senza key, solo annotazione e raccomandazione rotazione).
- SPEC_ERRATA non aggiornato: nessun errata nuovo.
- Desktop breakdown status aggiornato dopo l'implementazione.
- PROMPT_LOG aggiornato con questa entry prima dell'output applicativo.

## PLOG-2026-05-14-008 - M3/T26 `app/ai_client.py`

- Data: 2026-05-14
- Scope: implementare solo M3/T26 dopo approvazione del piano e configurazione `.env`.
- Stato: T26 completato e verificato con chiamata reale.

### Messaggi catalogati

- CODEX-176: crea `.env` locale a partire da template `.env.example` con la API key dell'utente (file gitignored, mai versionato).
- CODEX-177: verifica `git check-ignore -v .env` riuscita (`.gitignore:157:.env`); verifica `git status --short` non riporta `.env`; verifica `git ls-files` non riporta `.env`.
- CODEX-178: verifica caricamento via `python-dotenv` riuscita: key prefix `sk-or-v1-b...`, length 73, model `google/gemma-4-31b-it:free`.
- CODEX-179: crea `app/ai_client.py` con factory `get_client()` e smoke `ping_primary_model()`.
- CODEX-180: comunica esito DoD T26: chiamata reale a Gemma 4 free ha restituito `'OK'` (2 caratteri) in 2459 ms; DoD soddisfatta al 100%.

### File modificati

- `.env` (locale, gitignored, NON committato):
  - creato a partire da `.env.example`.
  - contiene OPENROUTER_API_KEY reale + chain Strategia A.
- `app/ai_client.py`:
  - nuovo file, 38 righe.
  - `load_dotenv()` a module-level per caricare `.env` automaticamente all'import.
  - costanti `_BASE_URL = "https://openrouter.ai/api/v1"` e `_DEFAULT_HEADERS` con HTTP-Referer + X-Title.
  - `get_client() -> OpenAI`: factory con RuntimeError esplicito su key mancante.
  - `ping_primary_model() -> str`: smoke che invia "Dimmi solo OK" al modello primario.
- `README.md`:
  - stato aggiornato a M3/T26 completato.
  - prossimo task tecnico aggiornato a M3/T27 call_model.
- `INCIDENTS.md`:
  - aggiunto INC-007 per esposizione API key in chat e raccomandazione rotazione post-sessione.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T26 segnato come fatto.
  - prossimo task aggiornato a T27.
  - `app/ai_client.py` aggiunto all'elenco file.
- `PROMPT_LOG.md`:
  - aggiunte PLOG-2026-05-14-007 (Piano) e PLOG-2026-05-14-008 (Implementation).
- `SPEC_ERRATA.md`:
  - non aggiornato: nessun errata nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\ai_client.py
```

- Exit code: 0.

DoD T26 - smoke test chiamata reale verso modello primario Strategia A:

```powershell
.\.venv\Scripts\python.exe -c "
import time
from app.ai_client import ping_primary_model
t0 = time.perf_counter()
response = ping_primary_model()
latency_ms = int((time.perf_counter() - t0) * 1000)
print('Response received:', response is not None)
print('Response content:', repr(response))
print('Latency (ms):', latency_ms)
print('Contains OK token:', 'OK' in response or 'ok' in response)
"
```

Esito:

```text
Response received: True
Response type: str
Response length: 2
Response content: 'OK'
Latency (ms): 2459
Contains OK token: True
```

- Modello rispondente: `google/gemma-4-31b-it:free` (Strategia A primario).
- Response: stringa `'OK'` esatta, 2 caratteri.
- Latenza: 2459 ms, molto sotto il target spec RF-011 (`<=30s p95`).
- Nessun rate limit 429 al primo tentativo.
- Nessuna eccezione sollevata.

DoD T26 - test "Dimmi solo OK" verso il modello primario (Strategia A) -> risposta valida:

- File `app/ai_client.py` creato: si.
- Setup `OpenAI(base_url=..., api_key=...)`: si.
- API key letta da env var: si (`os.environ.get("OPENROUTER_API_KEY")`).
- Header `HTTP-Referer` e `X-Title`: si (in `default_headers`).
- Risposta valida dal modello primario: si (`'OK'`, 2459 ms).

### Decisione

- M3/T26 puo considerarsi completato.
- Prossimo task da proporre: M3/T27 `call_model(model_id, system, user, timeout=30)` in `app/ai_client.py` con i parametri completi della spec §9.4: `temperature=0.3`, `max_tokens=1000`, `response_format={"type": "json_object"}`.

## PLOG-2026-05-14-009 - Piano M3/T27 `call_model`

- Data: 2026-05-14
- Scope: pianificare M3/T27 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-056: chiede di procedere con la prossima task, stesso metodo, ribadisce paletti.
- CODEX-181: comunica che restera in modalita piano per T27, senza anticipare T28-T30, senza commit/push.
- CODEX-182: espone piano stretto: estendere `app/ai_client.py` (non un nuovo file) con `call_model(model_id, system, user, timeout=30) -> ChatCompletion`; parametri spec §9.4 hardcoded (temperature=0.3, max_tokens=1000, response_format={"type": "json_object"}); return raw ChatCompletion per permettere a T28-T30 di leggere usage/model/finish_reason.
- CODEX-183: documenta rischio noto sul JSON mode dei free tier: spec §9.4 dichiara "JSON mode supportato da tutti i modelli della chain" ex-ante, ma e da validare empiricamente; nota piano: se BadRequest 400 su `response_format=json_object`, INC-008 + nota operativa.
- USER-057: approva il piano con "Approvo, procedi" (opzione 1: niente commit/push).

### Stato verificato pre-implementazione

- Branch `main` allineato a `origin/main` su `48aa1a3`; lavoro T23-T26 ancora non committato per scelta utente.
- `.env` locale presente con OPENROUTER_API_KEY valida (verificato in T26 con chiamata reale 'OK' in 2459 ms).
- `app/ai_client.py` con `get_client()` e `ping_primary_model()` di T26, da estendere.
- `from openai.types.chat import ChatCompletion` disponibile (verifica import preliminare).

### Decisioni di design dichiarate nel piano

- Funzione `call_model` aggiunta a fianco di `ping_primary_model`, no rimozione di T26.
- Return type `ChatCompletion` raw del SDK OpenAI (opzione A nel piano), non wrapper custom.
- Parametri spec §9.4 hardcoded nella funzione: temperature, max_tokens, response_format.
- `timeout` parametrico con default 30 (spec §9.4 "client-side timeout 30s").
- `messages` composti con role=system + role=user, ordine standard OpenAI.
- Niente parsing JSON nel body: caller responsabile.
- Niente retry/backoff/fallback: scope T28-T29.
- Niente logging JSONL: scope T30.

### Decisioni documentali

- README aggiornato dopo l'implementazione: T27 fatto, prossimo M3/T28 fallback chain.
- INCIDENTS aggiornato SOLO se JSON mode fallisce → INC-008.
- SPEC_ERRATA non aggiornato di default.
- Desktop breakdown status aggiornato dopo l'implementazione.
- PROMPT_LOG aggiornato con questa entry prima dell'output applicativo.

## PLOG-2026-05-14-010 - M3/T27 `call_model` - implementazione OK, DoD bloccato da rate limit

- Data: 2026-05-14
- Scope: implementare M3/T27 dopo approvazione + DoD smoke test.
- Stato: implementazione completata e compilata; DoD chiamata reale bloccata da rate limit upstream su 3/4 modelli della chain e da model ID inesistente sul 4/4.

### Messaggi catalogati

- CODEX-184: estende `app/ai_client.py` con import `ChatCompletion` e funzione `call_model(model_id, system, user, timeout=30)` con parametri spec §9.4.
- CODEX-185: esegue compile check (exit 0) e DoD smoke test contro Gemma 4 free; primo tentativo 429 RateLimitError dopo 3897 ms con messaggio upstream "google/gemma-4-31b-it:free is temporarily rate-limited upstream" dal provider Google AI Studio.
- CODEX-186: attende 60 secondi e riprova Gemma 4 free; secondo tentativo 429 dopo 3435 ms, stesso messaggio.
- CODEX-187: tenta validazione su fallback della chain Strategia A in serie: Llama 3.3 70B free (429, 59933 ms timeout), Mistral Small 24B free (404 NotFoundError, 246 ms - model ID non esistente), Qwen3 Next 80B free (429, 59360 ms timeout).
- CODEX-188: conclude che 3/4 modelli della chain Strategia A sono attualmente rate-limited upstream e 1/4 ha model ID errato in `.env.example` (`mistralai/mistral-small-24b-instruct-2501:free` non esiste su OpenRouter).
- CODEX-189: la funzione `call_model` propaga correttamente le eccezioni del SDK OpenAI (RateLimitError per 429, NotFoundError per 404), confermando correttezza dell'implementazione. Il problema NON e nel codice T27 ma nello stato runtime dei free tier OpenRouter al momento della verifica.

### File modificati (M3/T27)

- `app/ai_client.py`:
  - import esteso a `from openai.types.chat import ChatCompletion`.
  - module docstring aggiornato a `M3/T26-T27`.
  - aggiunta funzione `call_model(model_id, system, user, timeout=30) -> ChatCompletion`: chiama `client.chat.completions.create()` con `temperature=0.3`, `max_tokens=1000`, `response_format={"type": "json_object"}`, `timeout` parametrico.
  - `get_client()` e `ping_primary_model()` di T26 invariati.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\ai_client.py
```

- Exit code: 0.

DoD T27 - smoke test JSON mode contro modello primario Strategia A:

```powershell
.\.venv\Scripts\python.exe -c "
import json, time
from app.ai_client import call_model
system_prompt = 'Rispondi sempre con un JSON valido, senza markdown e senza testo fuori dal JSON.'
user_prompt = 'Restituisci un JSON con campo status uguale a OK.'
t0 = time.perf_counter()
response = call_model('google/gemma-4-31b-it:free', system_prompt, user_prompt)
latency_ms = int((time.perf_counter() - t0) * 1000)
content = response.choices[0].message.content
print('Latency (ms):', latency_ms)
print('Content:', repr(content))
print('JSON parse:', 'SUCCESS' if json.loads(content) else 'FAIL')
"
```

Esito (1° tentativo):

```text
EXCEPTION: RateLimitError
Message: Error code: 429 - {'error': {'message': 'Provider returned error', 'code': 429, 'metadata': {'raw': 'google/gemma-4-31b-it:free is temporarily rate-limited upstream. Please retry shortly, or add your own key to accumulate your rate limits: https://openrouter.ai/settings/integrations', 'provider_name': 'Google AI Studio', 'is_byok': False}}, 'user_id': 'user_39Zd2oocCmwAvASwRRSHTFmOSoj'}
Latency before fail (ms): 3897
```

Esito (2° tentativo dopo 60s):

```text
EXCEPTION: RateLimitError
Message: Error code: 429 - stesso messaggio upstream Google AI Studio
Latency (ms): 3435
```

Tentativi sui fallback della chain Strategia A (`.env`):

```text
=== meta-llama/llama-3.3-70b-instruct:free ===
EXCEPTION: RateLimitError - 429 upstream provider Meta
Latency (ms): 59933 (timeout 60s)

=== mistralai/mistral-small-24b-instruct-2501:free ===
EXCEPTION: NotFoundError - Error code: 404 - {'error': {'message': 'No endpoints found for mistralai/mistral-small-24b-instruct-2501:free.', 'code': 404}}
Latency (ms): 246

=== qwen/qwen3-next-80b-a3b-instruct:free ===
EXCEPTION: RateLimitError - 429 upstream provider
Latency (ms): 59360
```

### Diagnosi

1. **Implementazione `call_model` corretta**: la funzione costruisce correttamente la chiamata `chat.completions.create` con i parametri spec §9.4 e propaga le eccezioni del SDK OpenAI senza alterazioni. Il comportamento osservato (`RateLimitError` per 429, `NotFoundError` per 404) e quello atteso.

2. **Stato runtime free tier**: 3/4 modelli della chain Strategia A sono temporaneamente rate-limited upstream (Gemma 4 su Google AI Studio, Llama 3.3 70B su Meta, Qwen3 Next su Venice). Il 4/4 (Mistral Small 24B free) ha un model ID inesistente su OpenRouter al momento della verifica. Lo scenario era anticipato dalla spec §7.2 "rate limit upstream sui free tier non e prevedibile. La chain di 4 fallback mitiga ma non elimina il rischio".

3. **Mistral model ID errato**: il valore `mistralai/mistral-small-24b-instruct-2501:free` in `.env.example` (e quindi in `.env`) restituisce 404 da OpenRouter. Il model ID corretto al momento della verifica e da scoprire (probabilmente `mistralai/mistral-small-3.1-24b-instruct:free` o simile, ma da validare empiricamente). Questa e una mini-errata da aggiungere come ERRATA-006 quando l'utente approva la correzione.

### DoD T27 - stato

- Implementazione codice: COMPLETATA. Codice corretto, compile OK, propagazione errori OK.
- Chiamata reale a Gemma 4 free che restituisce JSON: BLOCCATA da rate limit upstream non controllabile.
- Decisione su come chiudere T27: rinviata all'utente con opzioni esposte nella prossima domanda.

### Decisione

- M3/T27 codice: completato.
- M3/T27 DoD verifica runtime: in attesa di decisione utente sulle opzioni: attendere rate limit, accettare DoD code-only, procedere a T28 (fallback chain) che esiste per questo scenario, o switch a Strategia B.
- INC-008 da aggiungere in `INCIDENTS.md` per documentare l'incidente rate limit chain Strategia A.
- ERRATA-006 da aggiungere in `SPEC_ERRATA.md` per documentare model ID Mistral inesistente (subordinato ad approvazione utente).

## PLOG-2026-05-14-011 - Decisione utente su chiusura T27 e proseguimento

- Data: 2026-05-14
- Scope: registrare la decisione utente su come chiudere T27 con DoD runtime bloccato.
- Stato: applicata.

### Messaggi catalogati

- USER-058: comunica decisione: segnare nel breakdown status che API key e modelli vanno controllati meglio per il funzionamento, problema rinviato. L'utente provera a trovare un modello free affidabile o investira ~$10 in API a pagamento. Continuiamo intanto con il breakdown.

### Decisione applicata

- T27 marcato in breakdown status come "Fatto (codice), DoD runtime rinviato per rate limit chain Strategia A".
- Aggiunta sezione "Open Issues / Da rivedere" in Desktop breakdown status con riferimenti a INC-007 (API key esposta in chat, da ruotare) e INC-008 (chain Strategia A non disponibile + Mistral model ID 404).
- README aggiornato con riga di stato esplicita sulla situazione open issue.
- INC-008 gia scritto in `INCIDENTS.md` con tabella e opzioni di mitigazione.
- ERRATA-006 NON aggiunto in `SPEC_ERRATA.md`: subordinato a investigazione utente sul model ID corretto.
- `.env.example` NON modificato: invariato finche utente non investiga e propone correzione.
- `.env` locale (non versionato) lasciato com'e: la key e i modelli restano in chain Strategia A "as documented".

### Decisione tecnica derivata

- M3/T27 codice considerato completato per scopo breakdown.
- DoD runtime di T27 sara riverificato in T31 (test end-to-end con 3 scenari benchmark) o anticipatamente durante T28 quando la chain di fallback potra essere validata.
- Procediamo con T28 (fallback chain con backoff + switch su 429) usando lo "stesso metodo": piano + approvazione + implementazione + docs.

## PLOG-2026-05-14-012 - Piano M3/T28 fallback chain

- Data: 2026-05-14
- Scope: pianificare M3/T28 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-059: chiede di continuare con il breakdown dopo aver registrato OPEN-001 nel Desktop status.
- CODEX-190: espone piano stretto per T28: estendere `app/ai_client.py` con `get_suggestions_with_fallback(system, user) -> ChatCompletion`; chain letta da env (LLM_MODEL_PRIMARY + 3 fallback opzionali); per ogni modello: try `call_model()`, su 429 backoff 30s + retry max 2, poi switch; su timeout switch immediato; su APIError generico (es. 404 Mistral) switch immediato; chain esaurita -> RuntimeError.
- CODEX-191: documenta scelta test mock-based con `unittest.mock.patch`; motivazioni: chain reale rate-limited cronica (vedi OPEN-001), forzare 429 controllato richiede mock comunque, standard practice per logica fallback.
- CODEX-192: documenta scelta `_sleep` privata module-level monkeypatchabile in test per fast-forward 30s backoff.
- USER-060: sceglie "Approvo + test pytest file" (opzione 1: implementazione + tests/test_ai_client.py + niente commit/push).

### Stato verificato pre-implementazione

- `app/ai_client.py` con `get_client()` + `ping_primary_model()` + `call_model()` di T26-T27.
- `tests/test_validators.py` con 28 test che passano (regression baseline).
- `pytest` + `pytest-asyncio` gia installati.
- Branch `main` allineato a `origin/main` su `48aa1a3`; lavoro T23-T27 ancora non committato.

### Decisioni di design dichiarate nel piano

- Funzione sync, no async (chain sequenziale, no parallelizzazione).
- Logging via `print()` su stderr con prefisso `[ai_client]`: provvisorio, logging JSONL e T30.
- Helper privato `_sleep(seconds)` module-level, monkeypatchabile in test.
- Helper privato `_chain_from_env() -> list[str]` legge LLM_MODEL_PRIMARY (obbligatorio) + 3 fallback opzionali.
- `for retry in range(3)` per ciascun modello = 1 attempt + 2 retry = max 3 chiamate per modello.
- `except` order: RateLimitError -> APITimeoutError + TimeoutError -> APIError catch-all.
- Test mock-based con `unittest.mock.patch("app.ai_client.call_model", side_effect=[...])`.
- Fixture `fast_sleep` autouse=True con `monkeypatch.setattr("app.ai_client._sleep", lambda s: None)`.

### Decisioni documentali

- README aggiornato dopo l'implementazione: T28 fatto, prossimo M3/T29.
- INCIDENTS non aggiornato (no nuovi incidenti previsti dal piano).
- SPEC_ERRATA non aggiornato.
- Desktop breakdown status aggiornato.
- PROMPT_LOG aggiornato con questa entry prima dell'output applicativo.

## PLOG-2026-05-14-013 - M3/T28 fallback chain (implementazione + 6 test pytest)

- Data: 2026-05-14
- Scope: implementare solo M3/T28 dopo approvazione del piano.
- Stato: T28 completato e verificato; suite 34/34 PASSED.

### Messaggi catalogati

- CODEX-193: estende `app/ai_client.py` con import esteso (`APIError`, `APITimeoutError`, `RateLimitError`, `sys`, `time`), module docstring a M3/T26-T28, helper `_sleep` + `_chain_from_env`, e funzione `get_suggestions_with_fallback`.
- CODEX-194: crea `tests/test_ai_client.py` con 6 test mock-based: success first attempt, 429 + 2 retry + switch, timeout immediate switch, APIError immediate switch, chain exhausted, primary missing raises.
- CODEX-195: pytest run su `tests/test_ai_client.py`: 6/6 PASSED in 0.68s.
- CODEX-196: pytest run su `tests/`: 34/34 PASSED in 1.46s (6 T28 + 28 T22), nessuna regressione.

### File modificati

- `app/ai_client.py`:
  - module docstring aggiornato a `M3/T26-T28`.
  - import esteso a `sys`, `time`, `APIError`, `APITimeoutError`, `RateLimitError`.
  - helper `_sleep(seconds)` module-level, monkeypatchabile in test.
  - helper `_chain_from_env() -> list[str]`: legge LLM_MODEL_PRIMARY (RuntimeError se assente) + 3 fallback opzionali.
  - funzione `get_suggestions_with_fallback(system, user) -> ChatCompletion`: orchestratore chain con backoff+retry+switch secondo spec §12 e §9.4.
  - T26 `get_client`, `ping_primary_model` e T27 `call_model` invariati.
- `tests/test_ai_client.py`:
  - nuovo file, 6 test pytest mock-based.
  - helper `_fake_response`, `_fake_429`, `_fake_timeout`, `_fake_api_error` con `MagicMock`.
  - fixture `env_chain` (esplicita): setta chain 2-elementi `primary-model` + `fallback-model`.
  - fixture `fast_sleep` (autouse=True): monkeypatch `_sleep` a no-op.
- `README.md`:
  - stato aggiornato a M3/T28 completato.
  - prossimo task tecnico aggiornato a M3/T29 retry su output non valido.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T28 segnato come fatto.
  - prossimo task aggiornato a T29.
  - `tests/test_ai_client.py` aggiunto all'elenco file.
- `PROMPT_LOG.md`:
  - aggiunte PLOG-2026-05-14-012 (Piano) e PLOG-2026-05-14-013 (Implementation).
- `INCIDENTS.md`:
  - non aggiornato: nessun incidente reale nuovo.
- `SPEC_ERRATA.md`:
  - non aggiornato: nessun errata nuovo.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\ai_client.py
```

- Exit code: 0.

DoD T28 - test forzando 429 sul primo modello, switch su fallback dopo 2 retry:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_ai_client.py -v
```

Esito:

```text
tests/test_ai_client.py::test_success_on_primary_first_attempt PASSED
tests/test_ai_client.py::test_429_two_retries_then_switch_to_fallback PASSED
tests/test_ai_client.py::test_timeout_switches_immediately PASSED
tests/test_ai_client.py::test_apierror_switches_immediately PASSED
tests/test_ai_client.py::test_chain_exhausted_raises PASSED
tests/test_ai_client.py::test_chain_missing_primary_raises PASSED
6 passed in 0.68s
```

Regression suite completa:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

Esito:

```text
34 passed in 1.46s
```

- 6 test T28 + 28 test T22 (validators) = 34 totali.
- Nessuna regressione su M2.
- Backoff 30s reale evitato grazie a fixture `fast_sleep` (durata reale suite < 2s).

DoD T28 - test forzando 429 sul primo modello, log mostra 2 retry attempts, switch al fallback, risposta dal secondo:

- `test_429_two_retries_then_switch_to_fallback`: side_effects `[429, 429, 429, fake_response]`, `mock_call.call_count == 4` (3 attempts su primary + 1 su fallback), `result is fake_response`. PASSED.
- Output stderr osservato durante run (catturato da pytest):
  - `[ai_client] attempt 1/3 model=primary-model`
  - `[ai_client] 429 from primary-model, backoff 30s (retry 1/2)`
  - `[ai_client] attempt 2/3 model=primary-model`
  - `[ai_client] 429 from primary-model, backoff 30s (retry 2/2)`
  - `[ai_client] attempt 3/3 model=primary-model`
  - `[ai_client] 429 after 2 retries on primary-model, switching to next`
  - `[ai_client] attempt 1/3 model=fallback-model`
  - `[ai_client] success on fallback-model`

### Decisione

- M3/T28 puo considerarsi completato.
- T27 DoD runtime resta in OPEN-001 (rate limit chain Strategia A), ma `get_suggestions_with_fallback` di T28 gestisce esattamente questo scenario via switch automatico ai fallback; non e blocker per il proseguimento.
- Prossimo task da proporre: M3/T29 `retry su output non valido (validazione Pydantic)` in `app/ai_client.py`: dopo chiamata, applicare `validator_format` + `validator_utf8_encoding`. Se falliscono, 1 retry stesso modello con stesso prompt; se anche il retry fallisce, switch al fallback.

## PLOG-2026-05-14-014 - Piano M3/T29 retry validazione

- Data: 2026-05-14
- Scope: pianificare M3/T29 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-061: chiede di procedere con la prossima task, stesso metodo, ribadisce paletti.
- CODEX-197: verifica firme `validator_format` e `validator_utf8_encoding` in `app/validators.py`: entrambi sync, no DB lookup, no async, no circular import previsto.
- CODEX-198: espone piano stretto per T29: refactor di `get_suggestions_with_fallback` in `_try_model` privato + main; doppi contatori per modello (`rate_limit_retries` max 2 da T28 + `validation_retry_used` max 1 nuovo T29); dopo `call_model` con successo HTTP, applicare `validator_format` su content; se valido, applicare `validator_utf8_encoding` sul parsed; su fail di uno dei due: 1 retry stesso modello + stesso prompt; se gia usato il retry: switch al fallback.
- CODEX-199: documenta scelta `_VALID_SUGGESTION_JSON` come default di `_fake_response` nei test (T28 esistenti devono aggiornarsi al nuovo flusso integrato), e 3 nuovi test T29: validation_format_fail_then_retry_succeeds, validation_format_fail_twice_switches_to_fallback, validation_mojibake_then_retry_succeeds. Totale 9 test in tests/test_ai_client.py + 28 validators = 37.
- USER-062: approva il piano con "Approvo, procedi" (opzione 1: niente commit/push automatico).

### Stato verificato pre-implementazione

- `app/ai_client.py` con `get_client()`, `ping_primary_model()`, `call_model()`, `_sleep()`, `_chain_from_env()`, `get_suggestions_with_fallback()` di T26-T28.
- `app/validators.py` con `validator_format` (sync, parsa SuggestionOutput) e `validator_utf8_encoding` (sync, scans SuggestionOutput per mojibake).
- `tests/test_ai_client.py` con 6 test T28 mock-based, attualmente PASSED con `_fake_response('{"ok": true}')`.
- Branch `main` allineato a `origin/main` su `48aa1a3`; lavoro T23-T28 non committato.

### Decisioni di design dichiarate nel piano

- Refactor: estraggo `_try_model(model_id, system, user) -> ChatCompletion | None` da `get_suggestions_with_fallback`.
- Contatori indipendenti per modello: `rate_limit_retries` (429, max 2) e `validation_retry_used` (validazione, max 1).
- Validatori invocati nell'ordine: `validator_format` (parsa SuggestionOutput) -> `validator_utf8_encoding` (scans parsed). Entrambi sotto lo stesso flag `validation_retry_used`.
- Caller continua a ricevere `ChatCompletion` raw (non SuggestionOutput parsed): il caching del parsed sara scope T45b SuggestionService.
- Nessun cambio di firma `get_suggestions_with_fallback() -> ChatCompletion`.
- Update T28 tests: `_fake_response` cambia default da `'{"ok": true}'` a `_VALID_SUGGESTION_JSON` (json.dumps di SuggestionOutput valido).
- 3 nuovi test T29 mock-based: format_fail+retry, format_fail+switch, mojibake+retry.

### Decisioni documentali

- README aggiornato dopo l'implementazione: T29 fatto, prossimo M3/T30.
- INCIDENTS non aggiornato.
- SPEC_ERRATA non aggiornato.
- Desktop breakdown status aggiornato.
- PROMPT_LOG aggiornato con questa entry prima dell'output applicativo.

## PLOG-2026-05-14-015 - M3/T29 retry validazione (refactor + 9 test totali)

- Data: 2026-05-14
- Scope: implementare solo M3/T29 dopo approvazione del piano.
- Stato: T29 completato e verificato; suite 37/37 PASSED.

### Messaggi catalogati

- CODEX-200: aggiorna module docstring a M3/T26-T29; aggiunge `from app.validators import validator_format, validator_utf8_encoding`.
- CODEX-201: sostituisce vecchio `get_suggestions_with_fallback` (loop semplice `for retry in range(3)`) con coppia `_try_model` (helper privato, doppi contatori 429 + validation) + `get_suggestions_with_fallback` (chain orchestrator semplificato).
- CODEX-202: aggiorna `tests/test_ai_client.py`: import `json`, costante `_VALID_SUGGESTION_JSON` con SuggestionOutput valido (3 suggestions Garen/Darius/Sett, build path inglesi, keystone Conqueror, explanation italiane corte), `_fake_response` default cambiato; aggiunge 3 test T29.
- CODEX-203: pytest run `tests/test_ai_client.py`: 9/9 PASSED in 0.99s.
- CODEX-204: pytest run full `tests/`: 37/37 PASSED in 1.02s; nessuna regressione.

### File modificati

- `app/ai_client.py`:
  - module docstring aggiornato a `M3/T26-T29`.
  - aggiunto `from app.validators import validator_format, validator_utf8_encoding`.
  - nuovo helper privato `_try_model(model_id, system, user) -> ChatCompletion | None` con doppi contatori per modello.
  - `get_suggestions_with_fallback` semplificato: scorre la chain chiamando `_try_model` e ritorna il primo `ChatCompletion` valido.
  - T26 `get_client`, `ping_primary_model` e T27 `call_model` invariati.
- `tests/test_ai_client.py`:
  - import `json`.
  - aggiunta costante `_VALID_SUGGESTION_JSON` con SuggestionOutput valido (3 suggestions, build path inglesi, keystone Conqueror, explanation italiane <=150 char).
  - `_fake_response` default cambiato a `_VALID_SUGGESTION_JSON`.
  - 6 test T28 esistenti ancora PASSED senza modifiche al body, perche il default e ora valido.
  - 3 nuovi test T29:
    - `test_validation_format_fail_then_retry_succeeds`: invalid JSON primo attempt, valid secondo, return valido, 2 chiamate.
    - `test_validation_format_fail_twice_switches_to_fallback`: invalid+invalid_retry su primary, valid su fallback, 3 chiamate.
    - `test_validation_mojibake_then_retry_succeeds`: mojibake chr(0x00C3)+chr(0x00C2)+chr(0x00A8) in explanation primo attempt, clean secondo, return clean, 2 chiamate.
- `README.md`:
  - stato aggiornato a M3/T29 completato.
  - prossimo task tecnico aggiornato a M3/T30 logging JSONL.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T29 segnato come fatto.
  - prossimo task aggiornato a T30.
- `PROMPT_LOG.md`:
  - aggiunte PLOG-2026-05-14-014 (Piano) e PLOG-2026-05-14-015 (Implementation).
- `INCIDENTS.md`:
  - non aggiornato.
- `SPEC_ERRATA.md`:
  - non aggiornato.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\ai_client.py
```

- Exit code: 0.

Pytest T28+T29 (9 test):

```text
tests/test_ai_client.py::test_success_on_primary_first_attempt PASSED
tests/test_ai_client.py::test_429_two_retries_then_switch_to_fallback PASSED
tests/test_ai_client.py::test_timeout_switches_immediately PASSED
tests/test_ai_client.py::test_apierror_switches_immediately PASSED
tests/test_ai_client.py::test_chain_exhausted_raises PASSED
tests/test_ai_client.py::test_chain_missing_primary_raises PASSED
tests/test_ai_client.py::test_validation_format_fail_then_retry_succeeds PASSED
tests/test_ai_client.py::test_validation_format_fail_twice_switches_to_fallback PASSED
tests/test_ai_client.py::test_validation_mojibake_then_retry_succeeds PASSED
9 passed in 0.99s
```

Regression full suite:

```text
37 passed in 1.02s
```

DoD T29 verificato:

- Test mock con output malformato la prima volta -> retry -> seconda risposta usata: `test_validation_format_fail_then_retry_succeeds`, `mock_call.call_count == 2`. PASSED.
- Test mock con output sempre malformato -> switch al fallback: `test_validation_format_fail_twice_switches_to_fallback`, `mock_call.call_count == 3` (2 su primary + 1 su fallback). PASSED.
- Caso mojibake equivalente: `test_validation_mojibake_then_retry_succeeds`, PASSED.

### Decisione

- M3/T29 puo considerarsi completato.
- Prossimo task da proporre: M3/T30 logging JSONL delle chiamate AI in `logs/ai_calls_YYYY-MM-DD.jsonl` con timestamp, model_used, prompt hash, latency_ms, usage (token), cost, json_ok, validation_results, retry_count.

## PLOG-2026-05-14-016 - Piano M3/T30 logging JSONL

- Data: 2026-05-14
- Scope: pianificare M3/T30 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-063: chiede di procedere con la prossima task dopo commit/push di T23-T29, stesso metodo, ribadisce paletti.
- CODEX-205: espone piano stretto per T30: estendere `app/ai_client.py` con costante `_LOGS_DIR` monkeypatchabile, helper `_prompt_hash`, `_ai_call_record`, `_log_ai_call`; logging per-chiamata integrato in `_try_model` su ogni ramo (rate_limited, timeout, api_error, validation_failed, success).
- CODEX-206: decisione critica su campo `cost`: OpenRouter non restituisce il costo nella response ChatCompletion standard; scelta `cost: null` documentata, niente tabella pricing inventata, niente chiamata extra a /generation endpoint (over-engineering); per i free tier di Strategia A il costo reale e $0.00 (coerente spec §7.4).
- CODEX-207: decisione su isolamento test: fixture `autouse` che redirige `_LOGS_DIR` a `tmp_path` per evitare che i 9 test T28/T29 esistenti sporchino `logs/` reale.
- USER-064: approva il piano con "Approvo, procedi" (opzione 1: niente commit/push automatico).

### Stato verificato pre-implementazione

- `app/ai_client.py` con T26-T29 (get_client, ping_primary_model, call_model, _sleep, _chain_from_env, _try_model, get_suggestions_with_fallback).
- `tests/test_ai_client.py` con 9 test PASSED (6 T28 + 3 T29).
- `.gitignore` ignora `logs/` (i file log non vengono versionati).
- Branch `main` allineato a `origin/main` su `3ca73c8` (commit T23-T29 pushato).

### Decisioni di design dichiarate nel piano

- Logging per-chiamata: ogni invocazione di `call_model` in `_try_model` produce 1 riga JSONL (anche i fallimenti).
- File giornaliero `logs/ai_calls_YYYY-MM-DD.jsonl` con data odierna via `datetime.now().strftime`.
- `prompt_hash`: sha256(system+user) troncato a 16 hex char; nessun contenuto del prompt/draft loggato (privacy by design spec §10.1).
- `cost: null` documentato (no pricing inventato, no chiamata /generation).
- `usage` letto da `response.usage` se presente, altrimenti `None`.
- `retry_count`: contatore 429 (`rate_limit_retries`) al momento della chiamata; validation retry riflesso in `validation_results`.
- `_LOGS_DIR` module-level monkeypatchabile.
- `_log_ai_call` fa `mkdir(parents=True, exist_ok=True)` prima di scrivere; append mode, encoding utf-8, `ensure_ascii=False`.
- Fixture `isolate_logs` autouse in test per redirigere `_LOGS_DIR` a tmp_path.
- `_fake_response` aggiornato con `usage.prompt_tokens`/`completion_tokens` interi (MagicMock raw non e JSON-serializzabile).

### Decisioni documentali

- README aggiornato dopo l'implementazione: T30 fatto, prossimo M3/T31.
- INCIDENTS non aggiornato.
- SPEC_ERRATA non aggiornato.
- Desktop breakdown status aggiornato.
- PROMPT_LOG aggiornato con questa entry prima dell'output applicativo.

## PLOG-2026-05-14-017 - M3/T30 logging JSONL (integrazione + 1 test DoD)

- Data: 2026-05-14
- Scope: implementare solo M3/T30 dopo approvazione del piano.
- Stato: T30 completato e verificato; suite 38/38 PASSED.

### Messaggi catalogati

- CODEX-208: estende import di `app/ai_client.py` (`hashlib`, `json`, `datetime`, `Path`); aggiunge `_LOGS_DIR`.
- CODEX-209: aggiunge helper `_prompt_hash`, `_ai_call_record` (con `cost: None` centralizzato + timestamp ISO), `_log_ai_call` (append JSONL daily file).
- CODEX-210: integra `_log_ai_call(_ai_call_record(...))` in tutti i 5 rami di `_try_model` (rate_limited, timeout, api_error, validation_failed x2, success); latenza misurata con `time.perf_counter()` attorno a ogni `call_model`.
- CODEX-211: corregge `_fake_response` nei test impostando `usage.prompt_tokens=120` e `completion_tokens=85` perche la MagicMock raw non e JSON-serializzabile dentro `_log_ai_call`.
- CODEX-212: aggiunge fixture `isolate_logs` autouse (redirige `_LOGS_DIR` a tmp_path) e test DoD `test_logging_three_calls_produce_three_jsonl_lines`.
- CODEX-213: pytest full suite 38/38 PASSED in 2.59s; verifica `logs/` reale contiene solo `.gitkeep` (nessuna pollution).

### File modificati

- `app/ai_client.py`:
  - module docstring aggiornato a `M3/T26-T30`.
  - import esteso: `hashlib`, `json`, `datetime`, `pathlib.Path`.
  - costante `_LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"`.
  - helper `_prompt_hash(system, user) -> str`: sha256 troncato 16 char.
  - helper `_ai_call_record(...)`: costruisce record con timestamp ISO + `cost: None`.
  - helper `_log_ai_call(record)`: mkdir + append JSONL su `ai_calls_YYYY-MM-DD.jsonl`.
  - `_try_model` integrato con logging su tutti i 5 rami; latenza per-chiamata via `time.perf_counter()`.
  - T26-T29 logica funzionale invariata.
- `tests/test_ai_client.py`:
  - import `datetime`.
  - `_fake_response` con `usage.prompt_tokens=120`, `completion_tokens=85`.
  - fixture `isolate_logs` autouse (redirige `_LOGS_DIR` a tmp_path).
  - nuovo test `test_logging_three_calls_produce_three_jsonl_lines` (10° test del modulo).
- `README.md`:
  - stato aggiornato a M3/T30 completato.
  - prossimo task tecnico aggiornato a M3/T31.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T30 segnato come fatto.
  - prossimo task aggiornato a T31.
- `PROMPT_LOG.md`:
  - aggiunte PLOG-2026-05-14-016 (Piano) e PLOG-2026-05-14-017 (Implementation).
- `INCIDENTS.md`:
  - non aggiornato.
- `SPEC_ERRATA.md`:
  - non aggiornato.

### Verifiche eseguite

Compile:

```powershell
.\.venv\Scripts\python.exe -m compileall app\ai_client.py
```

- Exit code: 0.

Full suite + DoD:

```text
38 passed in 2.59s
tests/test_ai_client.py::test_logging_three_calls_produce_three_jsonl_lines PASSED
```

Verifica non-pollution:

```text
logs/ reale: solo .gitkeep (i log dei test vanno in tmp_path via fixture isolate_logs)
git status: M app/ai_client.py, M tests/test_ai_client.py (no log file tracciati)
```

DoD T30 - dopo 3 chiamate il file contiene 3 righe JSONL parsabili:

- `test_logging_three_calls_produce_three_jsonl_lines`: 3 chiamate `get_suggestions_with_fallback`, file `ai_calls_<oggi>.jsonl` con 3 righe; ogni riga `json.loads()` OK; campi richiesti presenti (timestamp, model_used, prompt_hash, latency_ms, usage, cost, json_ok, validation_results, retry_count); `outcome=success`, `cost=None`, `usage={prompt_tokens:120, completion_tokens:85}`. PASSED.

### Decisione

- M3/T30 puo considerarsi completato.
- Limitazione documentata: campo `cost` sempre `null` finche non si implementa l'arricchimento via OpenRouter /generation endpoint (eventuale task futuro, non scope MVP; per Strategia A free il costo reale e $0.00).
- Prossimo task da proporre: M3/T31 test ai_client end-to-end con i 3 scenari `balanced_mid`, `mid_meta_banned`, `last_pick_support` (flusso completo prompt -> call -> validate -> log). NOTA: T31 richiede chiamate AI reali; e impattato da OPEN-001 (chain Strategia A rate-limited). Da valutare nel piano T31 se eseguibile ora o se rinviato come T27 DoD runtime.

## PLOG-2026-05-14-018 - Decisione utente: OPEN-001 rinviato, si prosegue con task non-AI

- Data: 2026-05-14
- Scope: registrare la decisione utente di rinviare la risoluzione del modello AI e proseguire.
- Stato: applicata.

### Messaggi catalogati

- USER-065: chiede se siamo bloccati senza un modello AI corretto.
- CODEX-214: risponde che NON e un blocco strutturale; solo 4-5 task (T27 DoD, T31, T35, T58, T62) richiedono chiamata AI reale; il restante ~90% del breakdown procede con test mock; raccomanda di continuare a costruire e fare le verifiche runtime in batch quando il modello sara pronto.
- USER-066: comunica che trovare/usare un modello richiede tempo e soldi (costo a carico utente), non risolvibile adesso; chiede di marcare bene il punto nel breakdown status come "da svolgere successivamente" e di proseguire con le task successive.
- CODEX-215: rafforza OPEN-001 nel Desktop breakdown status con la decisione utente esplicita, l'elenco delle 5 verifiche runtime rinviate in batch, e la strategia "procedi con mock". Registra questa entry nel PROMPT_LOG. Prossimo: piano T31 mock-based con DoD reale rinviata.

### Decisione applicata

- OPEN-001 aggiornato a stato "APERTO - RINVIATO A DOPO, in carico utente" con decisione utente datata 2026-05-14.
- Elenco esplicito delle 5 verifiche runtime AI rinviate in batch: T27, T31, T35, T58, T62.
- Strategia confermata: implementare le task AI-dipendenti in mock per la logica, verifica reale in batch quando il modello sara pronto.
- `.env.example`, `.env`, `SPEC_ERRATA.md` invariati (ERRATA-006 resta in standby finche utente non investiga il model ID).
- Si prosegue con M3/T31 in modalita mock-based, DoD chiamata reale rinviata a OPEN-001.

### Decisione documentale

- Desktop breakdown status: OPEN-001 rafforzato.
- README: gia riflette lo stato (T31 impattato da OPEN-001).
- INCIDENTS/SPEC_ERRATA: non aggiornati.
- PROMPT_LOG: questa entry.

## PLOG-2026-05-14-019 - Piano M3/T31 test e2e 3 scenari

- Data: 2026-05-14
- Scope: pianificare M3/T31 senza implementare prima dell'approvazione.
- Stato: piano approvato (fixture plumbing).

### Messaggi catalogati

- USER-067: dopo decisione OPEN-001 rinviato, chiede di proseguire con le task successive.
- CODEX-216: ricerca dati scenario benchmark nel repo: `tests/mock_drafts/` ha solo `.gitkeep`, nessun `test_scenarios.md`, nessun dato `balanced_mid/mid_meta_banned/last_pick_support`.
- CODEX-217: espone piano stretto T31: 3 test e2e in `tests/test_ai_client.py` (flusso build_prompt -> get_suggestions_with_fallback mockata -> validate -> log -> parse SuggestionOutput); 3 DraftState come fixture di plumbing, NON dati benchmark reali; DoD chiamata reale rinviata a OPEN-001 batch.
- CODEX-218: chiede se l'utente ha `test_scenarios.md` per dati reali o se procedere con fixture plumbing.
- USER-068: sceglie "Fixture plumbing, procedi".

### Stato verificato pre-implementazione

- `app/prompt_builder.py` (T25), `app/ai_client.py` (T26-T30), `app/models.py` (T13-T14) disponibili.
- `tests/test_ai_client.py` con 10 test PASSED + fixture `env_chain`, `isolate_logs`, `fast_sleep`.
- Nessun dato scenario reale nel repo (confermato via find/grep).
- Branch `main` su `3ca73c8`; T30 + decisione OPEN-001 in locale non committati.

### Decisioni di design dichiarate nel piano

- 3 test e2e mock-based in `tests/test_ai_client.py` (coerente con T28-T30).
- 3 helper `_draft_balanced_mid`, `_draft_mid_meta_banned`, `_draft_last_pick_support` come fixture DraftState minime.
- Helper `_run_e2e(draft, isolate_logs)` per il flusso comune.
- Fixture documentate esplicitamente come PLUMBING, non benchmark reale; dati reali = scope T34/T57.
- DoD chiamata reale rinviata a OPEN-001 in batch con T27/T35/T58/T62.
- `champion_data={}` (coerente con T25).

### Decisioni documentali

- README aggiornato dopo l'implementazione: T31 fatto (mock, DoD reale rinviata), M3 chiuso lato codice, prossimo M4/T32.
- INCIDENTS/SPEC_ERRATA non aggiornati.
- Desktop breakdown status aggiornato.
- PROMPT_LOG aggiornato con questa entry prima dell'output applicativo.

## PLOG-2026-05-14-020 - M3/T31 test e2e 3 scenari (M3 chiuso lato codice)

- Data: 2026-05-14
- Scope: implementare solo M3/T31 dopo approvazione del piano.
- Stato: T31 completato (mock); suite 41/41 PASSED; M3 chiuso lato codice.

### Messaggi catalogati

- CODEX-219: aggiunge import `ChampionPick`, `DraftState`, `SuggestionOutput`, `build_prompt` a `tests/test_ai_client.py`.
- CODEX-220: aggiunge blocco M3/T31 con commento esplicito "fixture PLUMBING non benchmark reale", 3 helper DraftState, helper `_run_e2e`, 3 test e2e.
- CODEX-221: pytest full suite 41/41 PASSED in 1.83s; 3/3 test T31 PASSED; `logs/` reale intatto (solo .gitkeep); nessun leak .env/log in git.

### File modificati

- `tests/test_ai_client.py`:
  - import esteso: `from app.models import ChampionPick, DraftState, SuggestionOutput`, `from app.prompt_builder import build_prompt`.
  - blocco M3/T31 con commento sul significato "plumbing".
  - 3 helper fixture: `_draft_balanced_mid`, `_draft_mid_meta_banned`, `_draft_last_pick_support`.
  - helper `_run_e2e(draft, isolate_logs)`: build_prompt -> get_suggestions_with_fallback (mocked) -> parse SuggestionOutput -> verifica log scritto con outcome success.
  - 3 test: `test_e2e_balanced_mid`, `test_e2e_mid_meta_banned`, `test_e2e_last_pick_support`.
- `README.md`:
  - stato aggiornato a M3 chiuso lato codice (T23-T31), prossimo M4/T32.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T31 segnato come fatto (mock, DoD reale rinviata).
  - M3 chiuso lato codice.
  - prossimo task M4/T32.
- `PROMPT_LOG.md`:
  - aggiunte PLOG-2026-05-14-019 (Piano) e PLOG-2026-05-14-020 (Implementation).
- `INCIDENTS.md` / `SPEC_ERRATA.md`:
  - non aggiornati.

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

Esito:

```text
41 passed in 1.83s
tests/test_ai_client.py::test_e2e_balanced_mid PASSED
tests/test_ai_client.py::test_e2e_mid_meta_banned PASSED
tests/test_ai_client.py::test_e2e_last_pick_support PASSED
```

- 41 test totali: 13 ai_client (6 T28 + 3 T29 + 1 T30 + 3 T31) + 28 validators.
- `logs/` reale: solo `.gitkeep` (fixture isolate_logs funziona).
- Nessun leak `.env`/log in git.

DoD T31 - 3/3 scenari producono SuggestionOutput valido, logs scritti correttamente:

- Mock-based: 3/3 test PASSED; flusso build_prompt -> get_suggestions_with_fallback -> validate -> log corretto per balanced_mid, mid_meta_banned, last_pick_support.
- Ogni test verifica: prompt costruito (user_role nel prompt), SuggestionOutput con 3 suggestions parsato, log JSONL scritto con outcome=success.
- DoD chiamata AI reale: RINVIATA a OPEN-001 in batch con T27/T35/T58/T62 (decisione utente 2026-05-14).

### Decisione

- M3/T31 completato lato codice (mock).
- M3 (Prompt Builder + AI Client con chain, T23-T31) CHIUSO lato codice. DoD runtime di T27 e T31 rinviate in batch a OPEN-001.
- Prossimo task da proporre: M4/T32 interfaccia astratta `DraftStateProvider` in `app/draft_state_provider.py` con metodo `async get_current_state() -> DraftState`.

## PLOG-2026-05-14-021 - Piano M4/T32 DraftStateProvider

- Data: 2026-05-14
- Scope: pianificare M4/T32 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-069: "procedi".
- CODEX-222: espone piano stretto T32: un solo file `app/draft_state_provider.py` con classe ABC astratta `DraftStateProvider` + `@abstractmethod async get_current_state(self) -> DraftState`; niente FileProvider/LCUProvider; verifica DoD inline (import/abstract/sottoclasse); niente pytest (DoD breakdown chiede solo "importabile + ereditabile").
- USER-070: approva con "Approvo, procedi" (niente commit/push).

### Stato verificato pre-implementazione

- `app/models.py` con `DraftState` (T13) disponibile.
- Branch `main` su `3ca73c8`; T30-T31 + decisione OPEN-001 in locale non committati.
- M3 chiuso lato codice (41/41 suite).

### Decisioni di design dichiarate nel piano

- `abc.ABC` + `@abstractmethod` su `async def get_current_state`.
- Metodo async (coerente con breakdown + futuro LCUProvider httpx async).
- Nessun `__init__` astratto: contratto solo su `get_current_state`.
- Dipendenza unidirezionale `draft_state_provider -> models` (no circular).

### Decisioni documentali

- README: M4 in corso, T32 fatto, prossimo M4/T33.
- INCIDENTS/SPEC_ERRATA non aggiornati.
- Desktop status aggiornato.
- PROMPT_LOG: questa entry prima dell'output applicativo.

## PLOG-2026-05-14-022 - M4/T32 DraftStateProvider

- Data: 2026-05-14
- Scope: implementare solo M4/T32 dopo approvazione.
- Stato: T32 completato e verificato; suite 41/41 PASSED (no regressione).

### Messaggi catalogati

- CODEX-223: crea `app/draft_state_provider.py` con ABC astratta + async abstractmethod.
- CODEX-224: compile OK; DoD inline 3/3 (importabile, istanziazione diretta -> TypeError, sottoclasse concreta istanziabile e get_current_state ritorna DraftState); regression suite 41/41 PASSED.

### File modificati

- `app/draft_state_provider.py`:
  - nuovo file, classe `DraftStateProvider(ABC)` con `@abstractmethod async def get_current_state(self) -> DraftState`.
- `README.md`:
  - M4 in corso, T32 fatto, prossimo M4/T33.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T32 fatto, M4 in corso, prossimo T33.
- `PROMPT_LOG.md`:
  - PLOG-2026-05-14-021 (Piano) + 022 (Impl).
- `INCIDENTS.md` / `SPEC_ERRATA.md`: non aggiornati.

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\draft_state_provider.py
```

- Exit code: 0.

DoD T32 - classe importabile, può essere ereditata:

```text
Test1 importabile: True
Test2 abstract: OK (TypeError: Can't instantiate abstract class DraftStateProvider without ...)
Test3 sottoclasse istanziabile + get_current_state: True MID
```

Regression:

```text
41 passed in 1.74s
```

### Decisione

- M4/T32 completato.
- Prossimo task da proporre: M4/T33 `FileProvider(DraftStateProvider)` in `app/file_provider.py` che carica draft state da file JSON specificato in config; DoD: `FileProvider("tests/mock_drafts/balanced_mid.json").get_current_state()` restituisce DraftState valido.

## PLOG-2026-05-14-023 - Piano M4/T33 FileProvider

- Data: 2026-05-14
- Scope: pianificare M4/T33 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-071: "procedi".
- CODEX-225: segnala ordering: DoD T33 cita `tests/mock_drafts/balanced_mid.json` che non esiste (creato in T34); propone verifica con `tmp_path` pytest, file reale scope T34.
- CODEX-226: espone piano stretto T33: `app/file_provider.py` con `FileProvider(DraftStateProvider)`, `__init__(file_path)`, `get_current_state` async che legge UTF-8 + `DraftState.model_validate_json`; no error handling extra (scope T49b); `tests/test_file_provider.py` con test tmp_path valido + schema-invalido.
- USER-072: approva con "Approvo, procedi" (niente commit/push).

### Stato verificato pre-implementazione

- `app/draft_state_provider.py` (T32) con ABC astratta disponibile.
- `app/models.py` `DraftState` (T13) con `champion: str | None`.
- pytest-asyncio 1.3.0 STRICT (richiede `@pytest.mark.asyncio`).
- Branch `main` su `3ca73c8`; T30-T32 + OPEN-001 in locale non committati.

### Decisioni di design dichiarate nel piano

- `FileProvider(DraftStateProvider)` sottoclasse concreta.
- `get_current_state` async (contratto T32) con read sync interno (no aiofiles, over-engineering MVP).
- Parsing via `DraftState.model_validate_json` (Pydantic v2, ValidationError su schema invalido).
- Nessun error handling file mancante/corrotto: scope MVP-013/T49b.
- Config path passato al costruttore; wiring da `.env DRAFT_PROVIDER_FILE` e scope T41/T44.
- Test con `tmp_path`; `balanced_mid.json` reale e scope T34 (ordering documentato).

### Decisioni documentali

- README: T33 fatto, prossimo M4/T34.
- INCIDENTS/SPEC_ERRATA non aggiornati.
- Desktop status aggiornato.
- PROMPT_LOG: questa entry prima dell'output applicativo.

## PLOG-2026-05-14-024 - M4/T33 FileProvider

- Data: 2026-05-14
- Scope: implementare solo M4/T33 dopo approvazione.
- Stato: T33 completato e verificato; suite 44/44 PASSED.

### Messaggi catalogati

- CODEX-227: crea `app/file_provider.py` con `FileProvider(DraftStateProvider)`.
- CODEX-228: crea `tests/test_file_provider.py` con 3 test (tmp_path valido, str path, schema-invalido -> ValidationError).
- CODEX-229: compile OK; 3/3 T33 PASSED; full suite 44/44 PASSED (41 + 3).

### File modificati

- `app/file_provider.py`:
  - nuovo file; `FileProvider(DraftStateProvider)` con `__init__(file_path: str | Path)` e `async get_current_state() -> DraftState` (read UTF-8 + `DraftState.model_validate_json`).
- `tests/test_file_provider.py`:
  - nuovo file; 3 test `@pytest.mark.asyncio`: valid draft via tmp_path, str path accettato, schema-invalido -> ValidationError.
- `README.md`:
  - T33 fatto, prossimo M4/T34.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T33 fatto, prossimo T34; file aggiunti all'elenco.
- `PROMPT_LOG.md`:
  - PLOG-2026-05-14-023 (Piano) + 024 (Impl).
- `INCIDENTS.md` / `SPEC_ERRATA.md`: non aggiornati.

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\file_provider.py
.\.venv\Scripts\python.exe -m pytest tests/test_file_provider.py -v
.\.venv\Scripts\python.exe -m pytest tests/
```

Esito:

```text
tests/test_file_provider.py::test_file_provider_loads_valid_draft PASSED
tests/test_file_provider.py::test_file_provider_accepts_str_path PASSED
tests/test_file_provider.py::test_file_provider_invalid_schema_raises PASSED
3 passed in 0.22s
44 passed in 1.76s
```

DoD T33 - `FileProvider(...).get_current_state()` restituisce DraftState valido:

- Verificato con file `tmp_path/balanced_mid.json` (DraftState serializzato via model_dump_json): get_current_state() ritorna DraftState con user_role=MID, patch=16.10.1, bans/enemy_team/ally_team coerenti, champion None gestito.
- DoD letterale su `tests/mock_drafts/balanced_mid.json`: il file reale e scope T34; la verifica si ripetera su quel file dopo T34.

### Decisione

- M4/T33 completato.
- Prossimo task da proporre: M4/T34 mock draft JSON (5 scenari iniziali) in `tests/mock_drafts/`: `balanced_mid`, `ad_heavy_top`, `mid_meta_banned`, `first_pick_top`, `last_pick_support`. NOTA: i contenuti reali del benchmark 09/05 (`test_scenarios.md`) non sono nel repo; da valutare nel piano T34 se costruire scenari plumbing documentati o se l'utente fornisce i dati.

## PLOG-2026-05-14-025 - Registrazione OPEN-002 dati benchmark + richiesta utente

- Data: 2026-05-14
- Scope: registrare la richiesta utente di documentare bene il problema dei dati benchmark prima di procedere con T34.
- Stato: applicata.

### Messaggi catalogati

- USER-073: prima di procedere chiede di segnare bene sul breakdown status la questione dei benchmark, cosi che possa aggiungere i dati reali "appena arrivo a casa"; poi procedere; ricorda i paletti.
- CODEX-230: crea OPEN-002 nel Desktop breakdown status (problema, scenari interessati, cosa deve fare l'utente da casa, come si procede con plumbing nel frattempo, impatto, note operative su tests/mock_drafts); aggiorna README open issues con OPEN-002; registra questa entry; prossimo: piano T34.

### Decisione applicata

- OPEN-002 creato in Desktop breakdown status: dati scenario benchmark 09/05 (`test_scenarios.md`) NON nel repo, in carico utente da casa.
- Scenari interessati documentati: 5 (T34) + 15 (T57).
- Strategia interim: T34 crea JSON plumbing strutturalmente validi e coerenti col nome scenario, sostituibili in-place quando l'utente fornisce i dati reali (path/nome file stabili, codice invariato).
- README open issues aggiornato con OPEN-001 + OPEN-002.
- INCIDENTS/SPEC_ERRATA non aggiornati (non sono incidenti/errata, sono open issue operative tracciate nel breakdown status come OPEN-001/002).

### Decisione documentale

- Desktop breakdown status: OPEN-002 aggiunto.
- README: open issues aggiornate.
- PROMPT_LOG: questa entry prima del piano T34.

## PLOG-2026-05-14-026 - Piano M4/T34 mock draft JSON

- Data: 2026-05-14
- Scope: pianificare M4/T34 senza implementare prima dell'approvazione.
- Stato: piano approvato (con README di tracciabilita).

### Messaggi catalogati

- USER-074: chiede di documentare bene OPEN-002 prima di procedere, poi proseguire, ricorda paletti.
- CODEX-231: documenta OPEN-002; espone piano T34: 5 JSON plumbing in `tests/mock_drafts/` generati schema-validi, coerenti col nome scenario, champion reali Data Dragon; + `tests/mock_drafts/README.md` di tracciabilita; test parametrizzato 5 file via FileProvider.
- USER-075: sceglie "Approvo, con README".

### Stato verificato pre-implementazione

- `app/file_provider.py` (T33) + `app/draft_state_provider.py` (T32) disponibili.
- `tests/mock_drafts/` contiene solo `.gitkeep` (dir tracciato).
- `test_scenarios.md` reale NON disponibile (OPEN-002).
- Suite 44/44 pre-T34.

### Decisioni di design dichiarate nel piano

- 5 JSON: balanced_mid, ad_heavy_top, mid_meta_banned, first_pick_top, last_pick_support.
- Scenari PLUMBING dichiarati (OPEN-002), sostituibili in-place coi dati reali (path/nome stabili).
- balanced_mid / mid_meta_banned / last_pick_support coerenti con le fixture gia usate in test_e2e (T31).
- ad_heavy_top: enemy AD-heavy (Renekton/Lee Sin/Talon/Jhin/Pyke).
- first_pick_top: enemy vuoto, ally tutti None, user TOP.
- File versionati (test fixtures, non gitignored).
- `tests/mock_drafts/README.md` per tracciabilita OPEN-002.
- Test parametrizzato in `tests/test_file_provider.py`.

### Decisioni documentali

- README: T34 fatto, prossimo M4/T35.
- INCIDENTS/SPEC_ERRATA non aggiornati.
- Desktop status aggiornato.
- PROMPT_LOG: questa entry prima dell'output applicativo.

## PLOG-2026-05-14-027 - M4/T34 mock draft JSON (5 scenari plumbing)

- Data: 2026-05-14
- Scope: implementare solo M4/T34 dopo approvazione.
- Stato: T34 completato e verificato; suite 49/49 PASSED.

### Messaggi catalogati

- CODEX-232: crea 5 JSON in `tests/mock_drafts/` (balanced_mid, ad_heavy_top, mid_meta_banned, first_pick_top, last_pick_support) + `tests/mock_drafts/README.md` tracciabilita OPEN-002.
- CODEX-233: aggiunge test parametrizzato `test_mock_draft_loads_with_fileprovider` (5 file) a `tests/test_file_provider.py`.
- CODEX-234: 8/8 test_file_provider PASSED (3 T33 + 5 T34); full suite 49/49 PASSED; i 5 JSON caricano via FileProvider reale (soddisfa anche DoD letterale T33 su balanced_mid.json).

### File modificati

- `tests/mock_drafts/balanced_mid.json`, `ad_heavy_top.json`, `mid_meta_banned.json`, `first_pick_top.json`, `last_pick_support.json`:
  - nuovi; DraftState schema-validi; champion reali Data Dragon; scenari PLUMBING (OPEN-002).
- `tests/mock_drafts/README.md`:
  - nuovo; marca i JSON come plumbing, istruzioni di sostituzione coi dati reali, ref OPEN-002.
- `tests/test_file_provider.py`:
  - aggiunto test parametrizzato sui 5 mock draft via FileProvider.
- `README.md`:
  - T34 fatto, prossimo M4/T35.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T34 fatto (plumbing, OPEN-002), prossimo T35; file in elenco.
- `PROMPT_LOG.md`:
  - PLOG-2026-05-14-026 (Piano) + 027 (Impl).
- `INCIDENTS.md` / `SPEC_ERRATA.md`: non aggiornati.

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_file_provider.py -v
.\.venv\Scripts\python.exe -m pytest tests/
```

Esito:

```text
tests/test_file_provider.py ... 8 passed in 0.21s
  test_mock_draft_loads_with_fileprovider[balanced_mid] PASSED
  test_mock_draft_loads_with_fileprovider[ad_heavy_top] PASSED
  test_mock_draft_loads_with_fileprovider[mid_meta_banned] PASSED
  test_mock_draft_loads_with_fileprovider[first_pick_top] PASSED
  test_mock_draft_loads_with_fileprovider[last_pick_support] PASSED
49 passed in 1.82s
```

DoD T34 - 5 file .json presenti, ognuno caricabile con FileProvider:

- 5 file creati in `tests/mock_drafts/`.
- Test parametrizzato: ogni file caricato con `FileProvider(...).get_current_state()` -> `DraftState` valido (patch 16.10.1, user_role valido).
- Soddisfa retroattivamente anche la DoD letterale T33 (`FileProvider("tests/mock_drafts/balanced_mid.json")`).
- NOTA OPEN-002: scenari plumbing, non dati benchmark reali; sostituibili in-place quando l'utente porta `test_scenarios.md`.

### Decisione

- M4/T34 completato (plumbing; dati reali in OPEN-002).
- Prossimo task da proporre: M4/T35 `scripts/test_sim_mode.py`: flusso FileProvider -> PromptBuilder -> AIClient (chain) -> validators -> output finale per i 5 scenari. NOTA: parte AI reale impattata da OPEN-001 (chain rate-limited) -> da valutare nel piano se mock o rinviata in batch.

## PLOG-2026-05-14-028 - Piano M4/T35 sim mode script

- Data: 2026-05-14
- Scope: pianificare M4/T35 senza implementare prima dell'approvazione.
- Stato: piano approvato.

### Messaggi catalogati

- USER-076: "procedi".
- CODEX-235: espone piano T35: `scripts/test_sim_mode.py` con flusso FileProvider->build_prompt->get_suggestions_with_fallback->parse, esiti controllati VALID/CONTROLLED_FAILURE/UNHANDLED; scope validators = format+utf8 (gia in ai_client) + parse finale, legality = scope T45b; DoD parte 1 (5/5 controllato) verificata ora con pytest mock, parte 2 (>=3/5 reale) rinviata a OPEN-001 batch; niente esecuzione CLI reale ora (20 min backoff inutili).
- USER-077: approva con "Approvo, procedi" (niente commit/push).

### Stato verificato pre-implementazione

- `app/file_provider.py` (T33), `app/prompt_builder.py` (T25), `app/ai_client.py` (T26-T30) disponibili.
- 5 mock draft JSON in `tests/mock_drafts/` (T34) caricabili.
- Suite 49/49 pre-T35.

### Decisioni di design dichiarate nel piano

- Script standalone con `if __name__ == "__main__"` guard.
- `run_scenario` async (await FileProvider) + chiamata sync get_suggestions_with_fallback.
- Esiti controllati: VALID / CONTROLLED_FAILURE (RuntimeError chain exhausted) / UNHANDLED (bug).
- Exit code 0 se 0 UNHANDLED, 1 altrimenti.
- Scope validators T35: format+utf8 (gia interni a ai_client) + parse SuggestionOutput; legality = T45b.
- Verifica logica via `tests/test_sim_mode.py` mock-based (import script via importlib), 2 test: all_valid + chain_exhausted_controlled.
- DoD parte 2 (>=3/5 reale) rinviata a OPEN-001 batch.

### Decisioni documentali

- README: T35 fatto (logica mock; DoD reale OPEN-001), M4 chiuso, prossimo M5/T36.
- INCIDENTS/SPEC_ERRATA non aggiornati (salvo UNHANDLED reale).
- Desktop status aggiornato; OPEN-001 conferma T35 DoD runtime in batch.
- PROMPT_LOG: questa entry prima dell'output applicativo.

## PLOG-2026-05-14-029 - M4/T35 sim mode script (M4 chiuso lato codice)

- Data: 2026-05-14
- Scope: implementare solo M4/T35 dopo approvazione.
- Stato: T35 completato (logica mock); suite 51/51 PASSED; M4 chiuso lato codice.

### Messaggi catalogati

- CODEX-236: crea `scripts/test_sim_mode.py` (run_scenario/run_all/main, esiti controllati).
- CODEX-237: crea `tests/test_sim_mode.py` (import script via importlib, 2 test mock: all_valid + chain_exhausted_is_controlled).
- CODEX-238: compile OK; 2/2 T35 PASSED; full suite 51/51 PASSED (49 + 2).

### File modificati

- `scripts/test_sim_mode.py`:
  - nuovo; flusso sim 5 scenari; esiti VALID/CONTROLLED_FAILURE/UNHANDLED; summary + exit code.
  - docstring documenta impatto OPEN-001 e rinvio DoD parte 2.
- `tests/test_sim_mode.py`:
  - nuovo; 2 test mock-based (importlib load dello script); all_valid -> 5/5 VALID; chain_exhausted -> 5/5 CONTROLLED_FAILURE, 0 UNHANDLED.
- `README.md`:
  - M4 chiuso lato codice, prossimo M5/T36.
- `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`:
  - T35 fatto, M4 chiuso, prossimo M5/T36; file in elenco; OPEN-001 conferma T35 DoD runtime batch.
- `PROMPT_LOG.md`:
  - PLOG-2026-05-14-028 (Piano) + 029 (Impl).
- `INCIDENTS.md` / `SPEC_ERRATA.md`: non aggiornati.

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall scripts\test_sim_mode.py
.\.venv\Scripts\python.exe -m pytest tests/test_sim_mode.py -v
.\.venv\Scripts\python.exe -m pytest tests/
```

Esito:

```text
tests/test_sim_mode.py::test_sim_mode_all_valid PASSED
tests/test_sim_mode.py::test_sim_mode_chain_exhausted_is_controlled PASSED
2 passed in 1.51s
51 passed in 1.78s
```

DoD T35:

- Parte 1 ("5/5 scenari non crashano, esito controllato"): VERIFICATA via mock.
  - `test_sim_mode_all_valid`: AI mock valido -> 5/5 VALID.
  - `test_sim_mode_chain_exhausted_is_controlled`: AI mock RuntimeError -> 5/5 CONTROLLED_FAILURE, 0 UNHANDLED (no crash).
- Parte 2 ("almeno 3/5 SuggestionOutput valido end-to-end reale"): RINVIATA a OPEN-001 batch (chain Strategia A rate-limited), insieme a T27/T31/T58/T62.

### Decisione

- M4/T35 completato lato codice (logica mock; DoD reale in OPEN-001).
- M4 (DraftStateProvider + FileProvider, T32-T35) CHIUSO lato codice.
- Prossimo task da proporre: M5/T36 `parse_lockfile(path)` in `app/lcu_provider.py` (lockfile LCU: protocol, port, password; ricerca path standard poi psutil discovery). NOTA: M5 e "Should" (Demo Mode First: LCU dopo sim mode); il gating LCU del 09/05 e in INC-001.

## PLOG-2026-05-15-030 - Switch AI runtime: OpenRouter -> DeepSeek diretto

- Data: 2026-05-15
- Scope: cambiare provider AI da OpenRouter a DeepSeek API diretta per sfruttare il credito ($5) gia pagato dall'utente su platform.deepseek.com.
- Stato: completato lato codice; suite 13/13 test_ai_client PASSED.

### Messaggi catalogati

- USER-078: chiede in che file/riga inserire la API key; ha pagato $5 su DeepSeek, vuole provare "DeepSeek V4 flash".
- CODEX-239: indica `.env` (da `.env.example` riga 5) + `app/ai_client.py` (load_dotenv, get_client); segnala MISMATCH: codice cablato su OpenRouter, una key DeepSeek diretta non funziona col base URL OpenRouter; propone 2 strade.
- USER-079: sceglie la strada 2 (DeepSeek diretto: cambiare base URL + modello + variabile key).
- CODEX-240: applica le modifiche a `app/ai_client.py` e `.env.example`; verifica 13/13 test PASSED.
- USER-080: chiede di aggiornare il PROMPT_LOG.

### File modificati

- `app/ai_client.py`:
  - docstring: "OpenRouter" -> "DeepSeek SDK client (OpenAI-compatible)".
  - `_BASE_URL`: `https://openrouter.ai/api/v1` -> `https://api.deepseek.com`.
  - rimossa costante `_DEFAULT_HEADERS` (HTTP-Referer + X-Title, identita app verso OpenRouter, non usata da DeepSeek).
  - `get_client()`: legge `DEEPSEEK_API_KEY` invece di `OPENROUTER_API_KEY`; rimosso `default_headers`; messaggi RuntimeError aggiornati.
  - commento `_ai_call_record`: rimosso riferimento all'endpoint /generation OpenRouter (cost resta `null`).
- `.env.example`:
  - `OPENROUTER_API_KEY` -> `DEEPSEEK_API_KEY=sk-your-deepseek-key-here`.
  - chain ridotta a modelli DeepSeek diretti: `LLM_MODEL_PRIMARY=deepseek-chat`, `LLM_MODEL_FALLBACK_1=deepseek-reasoner`.
  - rimossi i 4 modelli OpenRouter free/Strategia A e i 4 commentati Strategia B (non risolvono sul base URL DeepSeek).
- `PROMPT_LOG.md`: questa entry.
- `INCIDENTS.md` / `SPEC_ERRATA.md` / `README.md` / `PC_ITS_DEPENDENCIES_CHECKLIST.md`: NON aggiornati (restano riferimenti OpenRouter/Strategia A da allineare; segnalato all'utente, in attesa di decisione).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_ai_client.py -q
```

Esito:

```text
13 passed in 1.16s
```

### Note tecniche

- I test patchano `call_model`/client e leggono solo `LLM_MODEL_*`, non la env var della key: rinominare la key non rompe la suite.
- Nessun ID "deepseek-v4-flash" esiste sull'API DeepSeek diretta (era un alias OpenRouter, PLOG benchmark 09/05). Modelli reali diretti: `deepseek-chat` (V3, default) e `deepseek-reasoner` (thinking). Mappato il "flash" richiesto su `deepseek-chat`.
- `response_format={"type":"json_object"}` ([ai_client.py:68]) supportato da DeepSeek ma richiede la parola "json" nel prompt: da confermare alla prima chiamata reale.

### Decisione

- Provider AI runtime = DeepSeek diretto. Strategia A/B OpenRouter (SPEC_ERRATA v1 ERRATA-003) di fatto superata da scelta utente; impatto su OPEN-001 (chain OpenRouter rate-limited) da rivalutare: il blocco potrebbe risolversi con credito DeepSeek pagato.
- Azione utente pendente: creare `.env` locale da `.env.example` e inserire `DEEPSEEK_API_KEY` reale (NON in chat, vedi INC-007). Poi smoke test reale `ping_primary_model()`.
- Documentazione (README/INCIDENTS/SPEC_ERRATA/checklist) da allineare in task separato su conferma utente.

## PLOG-2026-05-15-031 - Allineamento documentazione a switch DeepSeek

- Data: 2026-05-15
- Scope: allineare i 4 file di documentazione ai cambiamenti di PLOG-2026-05-15-030 (switch OpenRouter -> DeepSeek diretto), senza toccare codice.
- Stato: completato.

### Messaggi catalogati

- USER-081: "Si procedi con quell'allineamento ora, prima leggi bene tutto e capisci la logica con cui scrivere".
- CODEX-241: legge integralmente README.md, SPEC_ERRATA.md, INCIDENTS.md, PC_ITS_DEPENDENCIES_CHECKLIST.md; dichiara la logica documentale (errata append-only, incidenti storici, audit datato come snapshot) e applica le modifiche coerenti.

### Logica documentale applicata

- README.md: documento di stato corrente -> aggiornati riferimenti fattuali (provider, stack, setup, OPEN-001).
- SPEC_ERRATA.md: errata append-only, spec FROZEN -> ERRATA-003 NON riscritta (resta storica) ma marcata "superato da ERRATA-006"; aggiunta ERRATA-006 con struttura Problema/Aggiornamento/Motivazione/Impatto.
- INCIDENTS.md: registro storico -> INC-007/INC-008 non riscritti; INC-007 annotato (key OpenRouter non piu usata ma da revocare comunque); INC-008 Stato -> risolto + sezione Risoluzione (sub-issue Mistral resa nulla).
- PC_ITS_DEPENDENCIES_CHECKLIST.md: audit datato 2026-05-11 -> snapshot reachability lasciato storico; aggiunta sezione "Aggiornamento 2026-05-15"; aggiornate solo le righe di istruzione operativa (.env key, descrizione SDK).
- Convenzione: italiano senza accenti (anti-mojibake, coerente coi file), date assolute.

### File modificati

- `README.md`: stato provider AI, stato codice applicativo, OPEN-001 rivista, stack (httpx senza OpenRouter, "DeepSeek API tramite SDK OpenAI-compatible"), setup (`DEEPSEEK_API_KEY` + richiamo INC-007).
- `SPEC_ERRATA.md`: ERRATA-003 Stato "superato da ERRATA-006" + nota; nuova ERRATA-006.
- `INCIDENTS.md`: INC-007 nota 2026-05-15; INC-008 Stato risolto + Risoluzione.
- `PC_ITS_DEPENDENCIES_CHECKLIST.md`: nuova sezione "Aggiornamento 2026-05-15"; riga `.env`, riga pacchetto `openai`, nota operativa finale aggiornate.
- `PROMPT_LOG.md`: questa entry.

### Decisione

- Documentazione allineata a ERRATA-006. Nessuna modifica a codice o test in questa iterazione.
- Residui invariati: revoca key OpenRouter esposta (INC-007) e creazione `.env` con `DEEPSEEK_API_KEY` reale lato utente, poi smoke test reale `ping_primary_model()`.
- Nessun commit/push (non richiesto).

## PLOG-2026-05-15-032 - Commit/push switch DeepSeek + allineamento breakdown status + finding pytest

- Data: 2026-05-15
- Scope: committare/pushare lo switch DeepSeek + doc, allineare il breakdown status (Desktop), verificare che il cambio DeepSeek sia in ordine.
- Stato: completato. 1 finding preesistente annotato per risoluzione utente a casa.

### Messaggi catalogati

- USER-082: "fai commit/push delle modifiche effettuate, dopo averlo fatto verifica di averlo fatto bene".
- CODEX-242: commit su `main` (workflow del progetto), push `6896a39..193d3c4`. Intoppo: primo messaggio di commit corrotto da `@` parassita (sintassi PowerShell here-string usata nel tool Bash); corretto con `git commit --amend -F` (file temp, poi rimosso) PRIMA del push. Verificato: locale=remoto `193d3c4`, 7 file, `.env` gitignored, `.claude/` escluso.
- USER-083: fornisce 4 documenti (breakdown status, breakdown_tasks v2.1, TechnicalSpec v2.3, SPEC_ERRATA v1); chiede di leggerli, controllare che il breakdown status sia aggiornato e che il cambio DeepSeek sia in ordine.
- CODEX-243: letti i 4 doc. Breakdown status (Desktop, fuori repo) era fermo al 2026-05-14; aggiornato. Cambio DeepSeek verificato in ordine; trovato 1 finding preesistente (collisione pytest).
- USER-084: "annota tutto nel prompt log risolvo a casa".

### Commit/push (USER-082)

- Commit finale: `193d3c4 feat(ai): switch AI provider OpenRouter -> DeepSeek diretto (ERRATA-006)`, su `main`, pushato su `origin/main`.
- Lezione operativa: NON usare la sintassi here-string PowerShell (`@'...'@`) dentro il tool Bash; per messaggi multilinea usare `-F <file>`. L'amend pre-push ha evitato di pubblicare un messaggio sporco.
- Verifica integrita: `git status -sb` allineato; `git ls-remote` == HEAD locale; 7 file attesi; `.env` gitignored (`.gitignore:157`); solo `.env.example` versionato; `.claude/` lasciato untracked.

### Breakdown status allineato (USER-083)

- File: `C:\Users\user\Desktop\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md` (sul Desktop, NON nel repo, non versionato -> nessun commit).
- Logica: tabelle task storiche annotate (non riscritte); sezioni forward-looking riscritte alla verita corrente.
- Modifiche: header (commit 48aa1a3 -> 193d3c4, stato locale riscritto); nuova sezione "Aggiornamento 2026-05-15"; OPEN-001 RIVISTA -> largamente risolto; INC-007 annotato, INC-008 RISOLTO; Note operative (`.env.example` MODIFICATO, ERRATA-006 non piu standby); "Come riprendere"/"Per continuare" (DEEPSEEK_API_KEY, punto 3 da M3/T23 obsoleto -> M5/T36); riga T26 e "Verifiche finali OpenRouter" annotate come superate/snapshot.

### Verifica cambio DeepSeek (USER-083): in ordine

- `app/ai_client.py`: `_BASE_URL=https://api.deepseek.com`, key `DEEPSEEK_API_KEY`; nessun riferimento OpenRouter residuo in `app/`.
- `pytest tests/` -> 51/51 PASSED (invocazione documentata).
- Git: `main` == `origin/main`, HEAD `193d3c4`, working tree pulito (solo `.claude/`).

### FINDING preesistente da risolvere a casa (USER-084)

- Sintomo: `pytest` nudo dalla root della repo -> `ERROR collecting tests/test_sim_mode.py` ("import file mismatch": `scripts/test_sim_mode.py` shadowa `tests/test_sim_mode.py`).
- Causa: due file con basename `test_sim_mode.py` (uno in `scripts/`, uno in `tests/`), senza `__init__.py`/`conftest.py`; pytest in import-mode default collide sui nomi modulo. `scripts/test_sim_mode.py` viene raccolto perche il basename inizia con `test_`.
- NON e una regressione del cambio DeepSeek: introdotto col commit `6896a39` (T30-T35); il commit DeepSeek `193d3c4` non tocca i file `*sim_mode*`.
- Workaround attuale: usare l'invocazione documentata `pytest tests/` (51/51 PASSED). Il bare `pytest` non e l'invocazione di progetto.
- Opzioni di fix (a scelta utente, da fare a casa, non bloccante):
  1. Rinominare `scripts/test_sim_mode.py` in nome non `test_*` (es. `scripts/sim_mode_check.py`) + aggiornare l'import in `tests/test_sim_mode.py` (importlib by path) e i riferimenti in docs.
  2. Aggiungere `tests/__init__.py` + `scripts/__init__.py` (o `conftest.py` con `rootdir`) e/o impostare `--import-mode=importlib` in `pytest.ini`.
  3. Configurare `[tool.pytest.ini_options] testpaths = ["tests"]` per non raccogliere mai `scripts/`.
- Raccomandazione: opzione 1 (lo script non e un test ma un'utility CLI; il basename `test_` e fuorviante) oppure opzione 3 (la piu rapida e a basso rischio). Annotato anche nel breakdown status (sezione "Aggiornamento 2026-05-15").

### Decisione

- Switch DeepSeek confermato in ordine lato codice/test/git. Breakdown status allineato.
- Finding pytest registrato qui e nel breakdown status; risoluzione delegata all'utente ("risolvo a casa"), non bloccante per il proseguimento (M5/T36).
- Azioni utente residue invariate: revocare key OpenRouter esposta (INC-007); creare `.env` con `DEEPSEEK_API_KEY` reale; poi smoke test reale DeepSeek.
- Nessun commit/push in questa iterazione (questa entry e un aggiornamento doc locale di processo; commit del prossimo blocco di lavoro quando richiesto).

## PLOG-2026-05-15-033 - Handoff Claude token limit e verifica prompt log

- Data: 2026-05-15
- Scope: leggere il `PROMPT_LOG.md` reale e la chat Claude incollata dall'utente; capire se il prompt log era gia aggiornato dopo il token limit; aggiornarlo postumamente con questa ripresa.
- Stato: completato.

### Messaggi catalogati

- USER-085: incolla la chat con Claude fino al token limit e chiede di leggere tutto il prompt log, poi la chat, per capire se il prompt log sia aggiornato; chiede anche di aggiornarlo postumamente con la nuova interazione.
- CODEX-244: legge il `PROMPT_LOG.md` su disco, cerca le entry recenti e confronta la coda del file con la chat incollata; verifica lo stato git locale.

### Esito verifica

- Il prompt log era gia aggiornato fino a `PLOG-2026-05-15-032`, cioe includeva:
  - commit/push finale `193d3c4` dello switch OpenRouter -> DeepSeek diretto;
  - allineamento del breakdown status Desktop;
  - verifica DeepSeek (`pytest tests/` 51/51 PASS);
  - finding preesistente `pytest` nudo vs collisione `scripts/test_sim_mode.py` / `tests/test_sim_mode.py`;
  - decisione utente di risolvere il finding a casa.
- Stato git rilevato: `PROMPT_LOG.md` modificato e non ancora committato; `.claude/` ancora untracked. Il diff mostrava solo l'aggiunta di `PLOG-2026-05-15-032` prima di questa entry.
- Questa entry `PLOG-2026-05-15-033` registra il passaggio post-token-limit e rende esplicito che il log era aggiornato sul disco, ma non ancora committato.

### Decisione

- Nessuna modifica a codice o configurazione.
- Nessuna verifica test necessaria: lavoro solo documentale/processo.
- Prossimo passo operativo possibile: committare `PROMPT_LOG.md` quando l'utente lo chiede, lasciando `.claude/` fuori dal commit.

## PLOG-2026-05-16-034 - Ripresa progetto su PC casa: analisi, piano, decisioni utente

- Data: 2026-05-16
- Scope: nuova sessione (Claude) su PC di casa; lettura integrale spec v2.3 + SPEC_ERRATA v1 + breakdown v2.1 + breakdown status pc its + INCIDENTS + PROMPT_LOG; analisi discordanze; piano operativo; decisioni utente; subtask inserimento key DeepSeek.
- Stato: decisioni di piano approvate; Gate A (.env) eseguito dall'utente; in attesa di "ok" per Fase 1.

### Messaggi catalogati

- USER-086: fornisce spec v2.3, SPEC_ERRATA v1, breakdown v2.1, breakdown status pc its; chiede analisi discordanze, stato breakdown/prossima task/arretrati, controllo repo, piano da validare prima di costruire, controllo README; subtask: dove inserire la API key DeepSeek (la inserisce a mano), dichiara che il "nuovo modello" e "deepseek v4 flash".
- CODEX-245: letti tutti i file e lo stato git/repo; PROMPT_LOG risulta aggiornato fino a PLOG-2026-05-15-033; rilevato che questa macchina NON e "pc its" (no .venv, Python 3.12.10 in PATH, LoL installato in E:\Riot Games\League of Legends = PC casa = ambiente live-test spec 13.1); flag discordanza: "deepseek-v4-flash" non esiste sull'API DeepSeek diretta (era alias OpenRouter); risposta subtask: .env riga 5 DEEPSEEK_API_KEY, gitignored, letta da app/ai_client.py:25.
- CODEX-246: due domande (AskUserQuestion): modelli .env; sequenza lavoro.
- USER-087: risposte: mantenere deepseek-chat/deepseek-reasoner (solo riga 5 key); sequenza = batch runtime OPEN-001 prima, poi M5/T36.
- CODEX-247: piano finalizzato in fasi (Fase 0 bootstrap env, Gate A .env utente, Fase 1 batch runtime OPEN-001, Fase 2 M5/T36); in attesa di "procedi".
- USER-088: chiede di riscrivere l'output del piano in italiano e verificare che il PROMPT_LOG non contenga testo inglese.
- CODEX-248: conferma PROMPT_LOG non toccato in questa sessione (nessun testo inglese da correggere); riscrive il piano in italiano.
- USER-089: "fatto" -> Gate A eseguito dall'utente (.env creato con DEEPSEEK_API_KEY reale, righe modelli invariate).

### Decisioni

- Decisioni utente registrate: modelli chain DeepSeek invariati (deepseek-chat primario, deepseek-reasoner fallback); sequenza Fase 1 (OPEN-001 runtime) prima di Fase 2 (M5/T36).
- Discordanza documentata: la dicitura utente "deepseek v4 flash" non ha ID reale sull'API diretta; mappato su deepseek-chat (gia in .env.example, coerente con PLOG-2026-05-15-030). Nessuna ERRATA nuova: gia coperto da ERRATA-006.
- README: gia allineato allo switch DeepSeek, nessun aggiornamento necessario ora.
- Breakdown status (file Desktop pc its) NON nel repo e non raggiungibile da questa macchina: lo stato forward-looking resta tracciato qui nel PROMPT_LOG.
- Prossimo: Fase 0 bootstrap ambiente (venv + pip install + pip check + pytest tests/) senza commit; poi attesa "ok" per Fase 1.
- INCIDENTS / SPEC_ERRATA: non aggiornati (nessun incidente reale nuovo, nessun errata nuovo).

## PLOG-2026-05-16-035 - Fase 0 bootstrap + INC-009 (cache Data Dragon) + README

- Data: 2026-05-16
- Scope: Fase 0 del piano (bootstrap ambiente su PC casa) + risoluzione divergenza suite test + allineamento README.
- Stato: completato. Baseline 51/51 ripristinata. Nessun commit (come da piano, in attesa di "ok" Fase 1).

### Messaggi catalogati

- USER-090: "fatto" (Gate A: .env creato con DEEPSEEK_API_KEY reale, righe modelli invariate).
- CODEX-249: Fase 0 - venv creata, `pip install -r requirements.txt`, `pip check` OK. `pytest tests/` -> 39 pass / 12 fail (solo validator legality), causa `sqlite3.OperationalError: no such table: champions`; `data_dragon.db` 0-byte gitignored, cache mai popolata su questo PC. Diagnosi: prerequisito ambiente, non regressione. Stop e report con 3 punti proposti.
- USER-091: "Procedi" (approva i 3 punti: popolamento cache + INC-009 + README).
- CODEX-250: rimosso `data_dragon.db` 0-byte; `populate_cache()` -> patch 16.10.1; `scripts/test_data_dragon.py` exit 0 (172 champions, 705 items, 17 keystones, accent/tags/no-roles OK); `pytest tests/` 51/51 PASSED. Aggiunto INC-009 in INCIDENTS.md. Aggiornato README "Setup Previsto" con passo populate_cache + nota prerequisito.

### File modificati

- `INCIDENTS.md`: aggiunto INC-009 (suite non verde su macchina pulita per cache Data Dragon non popolata; risolto + mitigazione documentale).
- `README.md`: "Setup Previsto" - aggiunta riga `populate_cache()` nel blocco PowerShell + paragrafo nota prerequisito (rif. INC-009).
- `PROMPT_LOG.md`: PLOG-2026-05-16-034 (analisi/piano/decisioni, gia appesa) + questa PLOG-2026-05-16-035.
- `data_dragon.db`: rigenerato e popolato (gitignored, non versionato).
- `.venv/`: creata (gitignored).
- `app/` / `tests/` / `scripts/`: NON modificati (nessun cambio di codice).
- `SPEC_ERRATA.md`: NON modificato. Proposta nota analoga in spec 13.2 lasciata a decisione utente (strutturale -> eventuale SPEC_ERRATA), non applicata.

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -c "import asyncio; from app.data_dragon import populate_cache; print(asyncio.run(populate_cache()))"
.\.venv\Scripts\python.exe scripts\test_data_dragon.py
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

Esiti: pip check "No broken requirements"; populate_cache -> "16.10.1"; test_data_dragon exit 0; pytest "51 passed".

### Decisione

- Fase 0 chiusa: ambiente PC casa operativo, baseline 51/51 ripristinata, divergenza documentata (INC-009) e mitigata (README).
- Nessun commit/push in questa iterazione (in attesa di richiesta esplicita utente).
- Prossimo: Fase 1 (batch runtime OPEN-001) - smoke reale `ping_primary_model()` su DeepSeek, poi DoD runtime T27/T31/T35. In attesa di "ok" dell'utente per avviare la Fase 1, come da piano.

## PLOG-2026-05-16-036 - Fase 1: batch runtime OPEN-001 chiuso su DeepSeek (T27/T31/T35)

- Data: 2026-05-16
- Scope: Fase 1 del piano - DoD runtime reali contro DeepSeek diretto, sbloccate dopo Gate A (.env utente).
- Stato: completato. T27/T31/T35 DoD runtime VERDI. Nessun commit (in attesa di richiesta utente).

### Messaggi catalogati

- USER-092: sceglie opzione (a) - ripristino `.env.example` con `git checkout --` + via libera Fase 1.
- CODEX-251: `git checkout -- .env.example` (placeholder ripristinato, file fuori da git status). Smoke reale `ping_primary_model()` su `deepseek-chat`: 'OK' in 1598 ms.
- CODEX-252: DoD runtime T27 - `call_model('deepseek-chat', ...)` con "json" nel prompt: content `{"status":"OK"}`, `json.loads` SUCCESS, 1471 ms, usage 55/5.
- CODEX-253: DoD runtime T35 - `scripts/test_sim_mode.py` (flusso reale FileProvider->build_prompt->get_suggestions_with_fallback->parse) su 5 scenari plumbing: 5/5 VALID, 0/5 UNHANDLED, exit 0. Copre anche T31 (sottoinsieme balanced_mid/mid_meta_banned/last_pick_support tutti VALID).
- CODEX-254: verifica log RF-021: `logs/ai_calls_2026-05-16.jsonl` 5 righe, tutte outcome=success, model=deepseek-chat, json_ok=True, latenze ~1.5-3.3s.

### Note tecniche

- Conferma punto aperto PLOG-2026-05-15-030: DeepSeek `response_format=json_object` funziona includendo la parola "json" nel prompt; il system prompt v1.0 (prompts/system.md) gia richiede JSON, scenari sim 5/5 OK.
- Esecuzione script CLI richiede `PYTHONPATH=.` (`scripts/` non e package): non e un bug, e l'invocazione corretta da root. Annotabile in docs setup se serve.
- Gli scenari mock restano PLUMBING (OPEN-002): la pipeline e validata end-to-end, la QUALITA dei suggerimenti (T62 panel) e il benchmark p95 (T58) richiedono ancora i dati reali del benchmark 09/05.
- `scripts/test_sim_mode.py` ha un docstring ora obsoleto (descrive CONTROLLED_FAILURE per OPEN-001 rate-limited, scenario decaduto post-DeepSeek): correzione minore proposta all'utente, non applicata in autonomia.

### Stato DoD runtime OPEN-001

- T27 DoD runtime: VERDE (call_model JSON mode su deepseek-chat).
- T31 DoD runtime: VERDE (3/3 scenari e2e validi, sottoinsieme dei 5).
- T35 DoD runtime parte 2: VERDE (5/5 SuggestionOutput validi, soglia era >=3/5).
- T58 / T62 DoD runtime: ancora aperti, dipendono da OPEN-002 (dati reali benchmark non nel repo).

### File modificati

- `.env.example`: ripristinato a stato repo (`git checkout --`), nessuna modifica netta.
- `PROMPT_LOG.md`: questa entry PLOG-2026-05-16-036.
- `logs/ai_calls_2026-05-16.jsonl`: generato a runtime (gitignored).
- `data_dragon.db`: invariato (gia popolato in Fase 0).
- Codice `app/` / `tests/` / `scripts/`: NON modificato.
- `INCIDENTS.md` / `SPEC_ERRATA.md` / `README.md`: NON modificati in questa iterazione.

### Decisione

- OPEN-001 runtime batch T27/T31/T35 chiuso su DeepSeek diretto. OPEN-001 puo essere marcato risolto per la parte runtime sbloccabile; restano T58/T62 subordinati a OPEN-002.
- Nessun commit/push (in attesa di richiesta esplicita utente).
- Prossimo: Fase 2 del piano - ripresa breakdown da M5/T36 (`parse_lockfile` in `app/lcu_provider.py`), stesso metodo piano->approvazione->implementazione->docs. LoL installato su questa macchina (E:\Riot Games\League of Legends) -> T40 live testabile qui piu avanti.

## PLOG-2026-05-16-037 - Commit/push 673435f + docstring fix + piano M5/T36 esposto

- Data: 2026-05-16
- Scope: applicare le 3 decisioni utente (commit/push, fix docstring, avvio Fase 2) ed esporre il piano M5/T36 in attesa di approvazione.
- Stato: decisioni 1 e 2 applicate; decisione 3 = piano esposto, NON implementato (attesa approvazione, paletti).

### Messaggi catalogati

- USER-093: decisione 1 = commit/push ora; decisione 2 = correggi docstring; decisione 3 = procedi Fase 2 rispettando i paletti.
- CODEX-255: corretto docstring `scripts/test_sim_mode.py` (OPEN-001 superato; solo commento, CRLF preservato via script Python ad hoc); compile exit 0; `tests/test_sim_mode.py` 2/2 PASSED.
- CODEX-256: commit `673435f` (INCIDENTS.md, PROMPT_LOG.md, README.md, scripts/test_sim_mode.py) su `main`, pushato; locale == remoto; messaggio via file `-F` (lezione PLOG-032: no here-string in tool Bash); `.claude/` escluso.
- CODEX-257: espone piano M5/T36 (`parse_lockfile`), in attesa di approvazione.

### File modificati

- `scripts/test_sim_mode.py`: docstring allineato (OPEN-001 superato, DeepSeek). Nessuna logica toccata.
- `INCIDENTS.md` / `README.md` / `PROMPT_LOG.md` (PLOG-034/035/036): committati in `673435f`.
- `PROMPT_LOG.md`: questa entry PLOG-2026-05-16-037 (post-commit, non ancora committata: documenta pianificazione in corso).
- Codice `app/`: NON modificato. `SPEC_ERRATA.md`: NON modificato.

### Commit/push

- `673435f docs+chore: INC-009 Data Dragon cache prereq, README setup, OPEN-001 runtime closed`, su `main`, pushato su `origin/main`. Verifica: `git rev-parse HEAD` == `git ls-remote origin main`. 4 file, +144/-4.

### Piano M5/T36 esposto (in attesa approvazione)

- Task: `parse_lockfile(path) -> dict(protocol, port, password)` in nuovo file `app/lcu_provider.py` (M5 = MoSCoW Should, Demo Mode First gia rispettato: sim mode chiuso).
- Ricerca lockfile: path standard `C:\Riot Games\League of Legends\lockfile`, poi `psutil` process discovery; su questa macchina LoL e in `E:\Riot Games\League of Legends` (path non standard -> psutil rilevante).
- Test: con LoL aperto credentials valide; senza LoL eccezione gestita. Test mock-based + eventuale verifica reale (LoL installato qui).
- Privacy by design (paletto spec 10.1 / breakdown nota 9): T36 e solo parser lockfile, nessuna lettura summoner; endpoint privacy-safe a T37.
- Metodo: piano -> approvazione utente -> implementazione -> docs (PROMPT_LOG prima dell'output, INCIDENTS solo se incidente reale, niente commit senza richiesta).

### Decisione

- Decisioni 1 e 2 chiuse. Decisione 3: piano M5/T36 presentato; nessuna implementazione finche l'utente non approva il piano (paletto esplicito USER-093).
- PLOG-037 lasciata non committata (documenta pianificazione in corso); sara inclusa nel prossimo commit di lavoro o su richiesta.

## PLOG-2026-05-16-038 - M5/T36 lockfile parser+discovery (implementazione + 6 test)

- Data: 2026-05-16
- Scope: implementare solo M5/T36 dopo approvazione del piano.
- Stato: T36 completato e verificato; suite 57/57 PASSED. Nessun commit (in attesa di richiesta utente).

### Messaggi catalogati

- USER-094: "Approvato" (piano M5/T36).
- CODEX-258: letti file_provider.py / draft_state_provider.py / test_file_provider.py per allineare stile; verificato app/*.py LF, psutil>=5.9.8,<8 in requirements.
- CODEX-259: creato `app/lcu_provider.py` (parse_lockfile + find_lockfile + _lockfile_from_process + LockfileError); creato `tests/test_lcu_provider.py` (6 test).
- CODEX-260: compile exit 0; `pytest tests/test_lcu_provider.py` 6/6 PASSED; `pytest tests/` 57/57 PASSED (51 + 6, nessuna regressione).
- CODEX-261: aggiornato README (stato codice, prossimo task M5/T37, suite 57/57, OPEN-001 runtime chiuso); PLOG-038.

### File modificati

- `app/lcu_provider.py` (nuovo): `parse_lockfile(path) -> dict(process_name,pid,port,password,protocol)` (formato lockfile 5 campi `:`); `find_lockfile()` path standard `C:\Riot Games\League of Legends\lockfile` poi process discovery `psutil`; `_lockfile_from_process()`; eccezione dedicata `LockfileError`. Scope T36: solo parser+discovery, nessuna chiamata HTTP, nessuna lettura summoner (privacy by design spec 10.1).
- `tests/test_lcu_provider.py` (nuovo): 6 test (parse valido; str path + whitespace; file mancante -> LockfileError; malformato -> LockfileError; client non attivo -> LockfileError; discovery via psutil per path non standard tipo E:\Riot Games con monkeypatch).
- `README.md`: stato codice -> M5/T36 chiuso, suite 57/57, OPEN-001 runtime chiuso; prossimo task -> M5/T37.
- `PROMPT_LOG.md`: PLOG-037 (precedente, ancora non committata) + questa PLOG-038.
- `INCIDENTS.md` / `SPEC_ERRATA.md`: NON modificati (nessun incidente reale, nessun errata).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\lcu_provider.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_lcu_provider.py -v
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

Esiti: compile exit 0; 6/6 T36 PASSED; suite totale 57 passed.

### DoD T36

- `parse_lockfile` con LoL aperto -> credentials valide: VERIFICATO via test (lockfile reale 5 campi). Verifica live reale su questa macchina (LoL in E:\Riot Games\League of Legends) RINVIATA a T40, come da piano approvato (no apertura client ora).
- Senza LoL -> eccezione gestita: VERIFICATO (`LockfileError`, non eccezione nuda).
- Discovery psutil per path non standard: VERIFICATO via monkeypatch.

### Decisione

- M5/T36 chiuso lato codice. Verifica live (path reale E:\) confermata in scope T40.
- Nessun commit/push in questa iterazione (paletto: solo su richiesta utente). PLOG-037 e PLOG-038 + codice T36 + README pronti per il prossimo commit quando richiesto.
- Prossimo task tecnico: M5/T37 (`lcu_request` httpx con HTTP Basic + verify=False, endpoint privacy-safe `/lol-gameflow/v1/session`), stesso metodo piano->approvazione->implementazione->docs.

## PLOG-2026-05-16-039 - M5/T37 lcu_request httpx verify=False privacy-safe (impl + 3 test)

- Data: 2026-05-16
- Scope: implementare solo M5/T37 dopo approvazione del piano.
- Stato: T37 completato e verificato; suite 60/60 PASSED. Nessun commit (in attesa di richiesta utente).

### Messaggi catalogati

- USER-095: conferma decisioni 1+2; commit/push T36 + esporre piano T37.
- CODEX-262: commit `c2b0002` (T36 + README + PLOG-037/038) su main, pushato, locale==remoto; avviso non bloccante LF->CRLF su nuovi file (autocrlf repo), nessun impatto funzionale.
- CODEX-263: espone piano M5/T37.
- USER-096: "approvato procedi".
- CODEX-264: verificato stile httpx di data_dragon.py (`async with httpx.AsyncClient(timeout=...)`); esteso `app/lcu_provider.py` con import httpx + `_LCU_USERNAME` + `lcu_request`; aggiunti 3 test in `tests/test_lcu_provider.py`.
- CODEX-265: compile exit 0; `pytest tests/test_lcu_provider.py` 9/9; `git grep lol-summoner -- *.py` nessun match (DoD); `pytest tests/` 60/60 PASSED.

### File modificati

- `app/lcu_provider.py`: import `httpx`, costante `_LCU_USERNAME="riot"`, funzione `async lcu_request(method, path, *, lockfile_path=None, timeout=10.0) -> httpx.Response`. Risolve lockfile (param o find_lockfile), costruisce URL loopback `https://127.0.0.1:<port><path>`, HTTP Basic `riot:<password>`, `httpx.AsyncClient(verify=False)` (cert self-signed locale, loopback-only, previsto da RF-003). Nessun path summoner aggiunto (privacy by design spec 10.1).
- `tests/test_lcu_provider.py`: +3 test (richiesta autenticata loopback con fake AsyncClient: verify=False, url, auth, status; fallback find_lockfile senza path; guard `lol-summoner` assemblato a runtime su tutti i .py escluso .venv).
- `README.md`: stato codice -> M5/T36-T37 chiusi, suite 60/60; prossimo task -> M5/T38.
- `PROMPT_LOG.md`: questa PLOG-039.
- `INCIDENTS.md` / `SPEC_ERRATA.md`: NON modificati (nessun incidente reale, nessun errata).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\lcu_provider.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_lcu_provider.py -q
git grep -n "lol-summoner" -- "*.py"   # nessun match (exit 1 = no match, atteso)
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

Esiti: compile exit 0; 9/9 T36+T37 PASSED; git grep nessun match; suite totale 60 passed.

### DoD T37

- `lcu_request("GET", "/lol-gameflow/v1/session")` costruisce richiesta autenticata loopback con verify=False: VERIFICATO via mock (fake AsyncClient).
- Nessuna chiamata all'endpoint summoner; `git grep "lol-summoner" -- "*.py"` nessun match: VERIFICATO (anche test runtime con token assemblato).
- HTTP 200 reale con LoL aperto: RINVIATO a T40 (piano approvato; client non aperto ora).

### Decisione

- M5/T37 chiuso lato codice. Verifica live reale in scope T40.
- Nessun commit/push in questa iterazione (paletto: solo su richiesta utente).
- Prossimo task tecnico: M5/T38 (task asyncio polling `/lol-gameflow/v1/session` ogni 2s, mantiene `current_phase`), stesso metodo piano->approvazione->implementazione->docs.

## PLOG-2026-05-16-040 - M5/T38 GameflowMonitor polling 2s (impl + 4 test)

- Data: 2026-05-16
- Scope: implementare solo M5/T38 dopo approvazione del piano.
- Stato: T38 completato e verificato; suite 64/64 PASSED. Nessun commit (in attesa di richiesta utente).

### Messaggi catalogati

- USER-097: "si procedi con 1 e 2 in ordine".
- CODEX-266: commit `0985279` (T37 + README + PLOG-039) su main, pushato, locale==remoto; avviso LF->CRLF non bloccante.
- CODEX-267: espone piano M5/T38.
- USER-098: "perfetto approvato".
- CODEX-268: import `asyncio`, classe `GameflowMonitor` in `app/lcu_provider.py`; 4 test in `tests/test_lcu_provider.py`.
- CODEX-269: prima run 1 fail (`NameError`: `asyncio` non importato nel file di test); fix import `asyncio`; re-run 13/13 lcu_provider, suite 64/64 PASSED.

### File modificati

- `app/lcu_provider.py`: import `asyncio`; classe `GameflowMonitor` con `current_phase`, `poll_once()` (GET `/lol-gameflow/v1/session`, status!=200 o errore LockfileError/httpx.HTTPError o json invalido -> phase None senza crash, RF-022), `run(stop_event, interval=2.0)` (loop con `asyncio.wait_for(stop_event.wait(), timeout=interval)`). Scope T38 stretto: solo gameflow phase, niente champ-select (T39).
- `tests/test_lcu_provider.py`: import `asyncio`; +4 test (phase aggiornata; non-200 -> None; LockfileError -> None senza crash; run loop -> stop via event). Totale file 13 test.
- `README.md`: stato codice -> M5/T36-T38 chiusi, suite 64/64; prossimo task -> M5/T39.
- `PROMPT_LOG.md`: questa PLOG-040.
- `INCIDENTS.md` / `SPEC_ERRATA.md`: NON modificati. Il NameError test e stato un refuso di import risolto in iterazione, non un incidente reale (nessuna perdita di tempo significativa, nessun cambio di piano).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\lcu_provider.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_lcu_provider.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

Esiti: compile exit 0; 13/13 lcu_provider PASSED; suite totale 64 passed.

### DoD T38

- `poll_once` aggiorna `current_phase` da risposta gameflow: VERIFICATO (mock ChampSelect).
- Risposta non-200 / errore LCU -> `current_phase=None` senza crash (RF-022): VERIFICATO.
- `run` polla e si ferma su stop_event: VERIFICATO (interval=0, 3+ iterazioni, stop).
- Reale "avvio LoL -> Lobby entro 5s; custom -> ChampSelect": RINVIATO a T40 (piano approvato; client non aperto ora).

### Decisione

- M5/T38 chiuso lato codice. Verifica live reale in scope T40.
- Nessun commit/push in questa iterazione (paletto: solo su richiesta utente).
- Prossimo task tecnico: M5/T39 (GET `/lol-champ-select/v1/session`, parsing myTeam/theirTeam/actions/localPlayerCellId -> `DraftState`, senza leggere summoner name, spec 10.1), stesso metodo piano->approvazione->implementazione->docs.

## PLOG-2026-05-16-041 - M5/T39 parse champ-select + LCUProvider (impl + 5 test)

- Data: 2026-05-16
- Scope: implementare solo M5/T39 dopo approvazione del piano.
- Stato: T39 completato e verificato; suite 69/69 PASSED. Nessun commit (commit rinviato a fine M5 per decisione utente).

### Messaggi catalogati

- USER-099: "facciamo commit a fine m5 vai con il piano per t39".
- CODEX-270: espone piano M5/T39 (LCUProvider + parse_champ_select_session, mapping championId->name via Data Dragon, patch da meta, privacy 10.1).
- USER-100: "approvato procedi".
- CODEX-271: ispezionati models.py (DraftState/ChampionPick/Action), db.py (Champion.key=id numerico stringa, Champion.name, Meta key='patch'), data_dragon._get_cached_patch, validators pattern AsyncSessionLocal.
- CODEX-272: esteso `app/lcu_provider.py` (helper role/champion/patch, parse_champ_select_session, LCUProvider); +5 test in `tests/test_lcu_provider.py`.
- CODEX-273: compile exit 0; lcu_provider 18/18; suite 69/69; `git grep lol-summoner -- *.py` nessun match.

### File modificati

- `app/lcu_provider.py`: import sqlalchemy.select + app.db (AsyncSessionLocal, Champion, Meta) + app.draft_state_provider + app.models; `_ROLE_MAP` (top/jungle/middle/bottom/utility -> TOP/JUNGLE/MID/ADC/SUPPORT); `_normalize_role`, `_champion_name` (championId 0/None -> None), `_load_champion_id_to_name` (Champion.key int -> name), `_load_cached_patch` (Meta key='patch'); `parse_champ_select_session(session, patch, champion_names) -> DraftState` (legge solo cellId/championId/assignedPosition/actions; mai summoner; difensivo su schema custom-bot ridotto INC-001); classe `LCUProvider(DraftStateProvider)` con `get_current_state()` (lcu_request champ-select, non-200 -> LockfileError, patch+nomi da cache, parse).
- `tests/test_lcu_provider.py`: import LCUProvider/parse_champ_select_session/DraftState; +5 test (parse ranked completo; custom-bot minimale no crash; campi summoner non emergono in DraftState dump; LCUProvider.get_current_state mockato; non-200 -> LockfileError). File totale 18 test.
- `README.md`: stato codice -> M5/T36-T39 chiusi, suite 69/69; prossimo task -> M5/T40 (ultima M5, commit a fine M5).
- `PROMPT_LOG.md`: questa PLOG-041.
- `INCIDENTS.md` / `SPEC_ERRATA.md`: NON modificati (nessun incidente reale, nessun errata).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\lcu_provider.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_lcu_provider.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
git grep -n "lol-summoner" -- "*.py"   # nessun match (exit 1 = no match, atteso)
```

Esiti: compile exit 0; 18/18 lcu_provider PASSED; suite totale 69 passed; git grep nessun match.

### DoD T39

- Parsing champ-select -> DraftState con user_role e bans: VERIFICATO (ranked mock, user_role=MID, bans=[Aatrox]).
- championId 0 -> champion None: VERIFICATO.
- Custom-vs-bot schema ridotto senza crash (INC-001): VERIFICATO (1 action, campi sparsi).
- Nessun summoner name nel DraftState (spec 10.1): VERIFICATO (summonerId/gameName/displayName assenti dal dump) + git grep guard.
- LCUProvider.get_current_state() restituisce DraftState: VERIFICATO mockato; non-200 -> LockfileError.
- Reale "custom con bot -> DraftState reale": RINVIATO a T40 (piano; client non aperto ora).

### Decisione

- M5/T39 chiuso lato codice. Verifica live reale in scope T40.
- Nessun commit/push (decisione utente: commit a fine M5, dopo T40). Working tree accumula PROMPT_LOG/README/app/tests fino al commit M5.
- Prossimo task tecnico: M5/T40 (test live LCU - custom Tournament Draft con ban, schema actions >=10, documentare differenza vs gating 09/05 in INCIDENTS se persistente). Richiede client LoL aperto su questa macchina (LoL presente in E:\Riot Games\League of Legends): da concordare con l'utente quando aprire il client. Stesso metodo piano->approvazione->esecuzione->docs; al termine commit unico M5.

## PLOG-2026-05-16-042 - M5/T40 verifica live + INC-010 + BREAKDOWN_STATUS.md + commit M5

- Data: 2026-05-16
- Scope: T40 verifica live LCU su PC casa; documentazione stato; commit/push di chiusura giornata.
- Stato: integrazione live M5 VALIDATA; T40 DoD numerico IN SOSPESO (INC-010); commit/push eseguito; stop serata.

### Messaggi catalogati

- USER-101: sceglie (a), apre LoL; "client aperto".
- CODEX-274: crea `scripts/lcu_live_check.py`; run step 1-3: lockfile reale `E:\...` via psutil OK, gameflow HTTP 404 (client a menu, atteso), monitor None.
- USER-102: "lobby crea ... partita avviata".
- CODEX-275: re-run: gameflow HTTP 200 phase ChampSelect; GameflowMonitor ChampSelect; `LCUProvider.get_current_state()` -> DraftState reale (user_role ADC, patch 16.10.1, mapping championId->nome OK, zero summoner); MA bans=0, actions=3 (schema custom-vs-bot ridotto, identico gating 09/05).
- USER-103: non puo fare partita con umani ora; chiede di compilare/aggiornare il breakdown status segnando bene cosa e' in sospeso, poi commit/push di tutto, poi stop serata.
- CODEX-276: INC-010 (schema actions ridotto confermato persistente, T40 numerico in sospeso, mitigazione sim mode attiva); creato `BREAKDOWN_STATUS.md` versionato nel repo (sostituisce/prosegue il Desktop pc its non raggiungibile); README aggiornato; commit/push M5.

### Esito verifica live T40

- VALIDATO live: `find_lockfile` via psutil su path reale NON standard `E:\Riot Games\League of Legends\lockfile`; `lcu_request` gameflow HTTP 200; `GameflowMonitor` ChampSelect; `LCUProvider.get_current_state()` DraftState valido; mapping championId->nome (Caitlyn, Anivia, Darius, Swain, Akali, Mordekaiser, Renata Glasc, Miss Fortune, Udyr); privacy 10.1 (zero token summoner nel dump); nessun crash su schema ridotto.
- NON soddisfatto (in sospeso): DoD numerico `>=5 bans` (0) e `>=10 actions` (3). Causa: schema custom-vs-bot ridotto, gia previsto da spec 14.2 / INC-001, ora confermato persistente -> INC-010. Non e un bug di codice.

### File modificati

- `scripts/lcu_live_check.py` (nuovo): utility CLI verifica live T40 (NON test_*, evita collisione pytest PLOG-032); step 1-4, password mascherata, solo endpoint gameflow + champ-select (privacy 10.1), idempotente.
- `INCIDENTS.md`: aggiunto INC-010 (stato APERTO/in sospeso, mitigazione attiva, nessun ERRATA).
- `BREAKDOWN_STATUS.md` (nuovo, versionato): stato completo M0-M10, M5 dettaglio, "Cosa chiuso" / "Cosa in sospeso" (T40 numerico, OPEN-002, OPEN-001 residuo revoca key, T58/T62, T05b, finding pytest), come riprendere.
- `README.md`: stato M5/T36-T39 chiusi+live-validati, T40 IN SOSPESO, suite 69/69, rimando a BREAKDOWN_STATUS.md.
- `PROMPT_LOG.md`: PLOG-040, 041 (T38/T39, non ancora committate) + questa PLOG-042.
- `app/lcu_provider.py`, `tests/test_lcu_provider.py`: invariati da T39 (gia chiusi).
- `SPEC_ERRATA.md`: NON modificato (14.2 documenta gia il rischio; nessun errata).

### Verifiche eseguite

```powershell
$env:PYTHONPATH="."; .\.venv\Scripts\python.exe scripts\lcu_live_check.py
```

Esito: step 1-3 OK; step 4 DraftState reale OK su parte non numerica; bans=0/actions=3 (in sospeso, INC-010).

### Decisione

- T40 NON chiuso: integrazione live validata, DoD numerico in sospeso fino a un draft reale con ban (umani/tournament). Rieseguire `scripts/lcu_live_check.py`.
- M5 codice (T36-T39) considerato chiuso e live-validato per la parte non legata al numero di azioni.
- Commit/push di tutto il lavoro accumulato (T38/T39/T40 + docs) eseguito a fine serata. Stop serata su richiesta utente.
- Prossimo (sessione futura): chiudere T40 in un draft reale, poi M6a/T41 (FastAPI app + lifecycle).

## PLOG-2026-05-16-043 - M6a/T41 FastAPI app + lifecycle (impl + 4 test, runtime VERDE)

- Data: 2026-05-16
- Scope: T41 (M6a) - `app/main.py` FastAPI app + lifecycle; `app/config.py` (pydantic-settings, spec Â§7.1). T40 lasciato IN SOSPESO su richiesta utente; si procede col task successivo.
- Stato: T41 CHIUSO lato codice + DoD runtime VERDE. Niente commit/push (decisione utente: attendere).

### Messaggi catalogati

- USER-104: allega spec/errata/breakdown/status pc_its (stale); chiede analisi stato, prossima task, no invenzioni, piano prima di costruire; subtask: T40 in sospeso, procedere coi successivi.
- CODEX-277: analisi repo (BREAKDOWN_STATUS.md repo = fonte autorevole; pc_its = versione vecchia, successione dichiarata; nessuna incoerenza). Suite 69/69. Piano T41 esposto (config.py + main.py + test + verifica + docs).
- USER-105: "piano approvato, aspetta per il commit/push pero'".
- CODEX-278: implementazione T41 + test + verifica runtime + questa PLOG-043 + BREAKDOWN_STATUS/README. Nessun commit.

### File creati/modificati

- `app/config.py` (nuovo): `Settings(BaseSettings)` via `pydantic-settings` (spec Â§7.1); legge `.env` (DEEPSEEK_API_KEY, LLM_MODEL_PRIMARY/FALLBACK_1, DRAFT_PROVIDER_MODE/FILE, LOG_LEVEL) con default sicuri; `get_settings()` lru_cache. `ai_client.py` non toccato (mantiene i suoi `os.environ` per retrocompatibilita; Settings e single source of truth per lifecycle/provider).
- `app/main.py` (nuovo): `FastAPI(lifespan=...)`; startup -> `init_db()` + `check_patch_and_refresh()`; fallimento Data Dragon NON fatale (spec Â§12, RF-001: log warning + prosegue su cache locale); log `App ready`; shutdown log. Porta NON cablata (gestita dal launcher T42, spec Â§7.1). Nessun endpoint (T43/T44 fuori scope).
- `tests/test_main.py` (nuovo): 4 test (Settings default con env-clear monkeypatch per evitare pollution da load_dotenv di altri test; metadata app; lifespan startup logga `App ready`/shutdown con init_db+check_patch ordinati; fallimento Data Dragon non fatale via httpx.ConnectError mock).
- `PROMPT_LOG.md`: questa PLOG-043. `BREAKDOWN_STATUS.md`/`README.md`: stato T41 chiuso, suite 73/73, prossimo M6a/T42.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale, nessun errata).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\config.py app\main.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
.\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8000   # avvio reale, poi stop
```

Esiti: compile exit 0; suite **73 passed** (69 baseline + 4 T41); uvicorn avvio senza errori, log `Data Dragon cache ready (patch 16.10.1)` (cache hit, no re-download) + `App ready` + `Application startup complete`, `GET /docs` HTTP 200, shutdown pulito.

### DoD T41

- `uvicorn app.main:app --port 8000` parte senza errori: VERIFICATO (runtime reale).
- Log mostra `App ready`: VERIFICATO.
- Startup esegue init DB + refresh Data Dragon se necessario; resiliente a CDN down (spec Â§12): VERIFICATO (test + cache hit reale).
- Config letta da `.env` via pydantic-settings (spec Â§7.1): VERIFICATO.

### Decisione

- T41 chiuso (codice + runtime). M6a avviato.
- Nessun commit/push: working tree accumula `app/config.py`, `app/main.py`, `tests/test_main.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md` fino a OK utente.
- Prossimo task: M6a/T42 (`launcher.py` con auto-browser + port fallback 8000->8003).

## PLOG-2026-05-16-044 - M6a/T42 launcher in-process uvicorn + port fallback + auto-browser (impl + 6 test, runtime VERDE)

- Data: 2026-05-16
- Scope: T42 (M6a) - `launcher.py` root. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T42 CHIUSO lato codice + DoD runtime VERDE. Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-106: "vai di commit/push e poi pianifica per la prossima task, ricordati dei paletti e delle mie richieste".
- CODEX-279: commit/push T41 (3457994 su main); piano T42 esposto (launcher.py + test + verifica + docs), in attesa approvazione.
- USER-107: "procedi".
- CODEX-280: implementazione T42 + 6 test + verifica runtime reale + questa PLOG-044 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `launcher.py` (nuovo, root): `find_free_port([8000..8003])` (probe via socket bind), `wait_for_port` (connect loop, timeout 5s), `_build_server` (`uvicorn.Server`+`Config`, IN-PROCESS, non comando esterno -> packaging-safe per PyInstaller T66/T67), `main()` -> porta libera -> server in thread daemon -> attesa ascolto -> `webbrowser.open` -> log porta; tutte occupate -> messaggio "Nessuna porta libera 8000-8003" + exit 1; KeyboardInterrupt -> `should_exit`.
- `tests/test_launcher.py` (nuovo): 6 test ermetici (porte effimere OS-assigned, niente reliance su 8000-8003 liberi; uvicorn/webbrowser mockati): find_free_port skip-busy / all-busy-None; wait_for_port closed-False / listening-True; main apre browser su porta scelta; main ritorna 1 se nessuna porta libera (browser NON aperto).
- `PROMPT_LOG.md`: questa PLOG-044. `BREAKDOWN_STATUS.md`/`README.md`: T42 chiuso, suite 79/79, prossimo T43.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall launcher.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
# smoke reale: webbrowser stubbato, uvicorn reale serve l'app
#  CASE A (8000 libera) -> find_free_port 8000, GET /docs HTTP 200
#  CASE B (8000 occupata) -> fallback 8001, GET /docs HTTP 200
```

Esiti: compile exit 0; suite **79 passed** (73 + 6 T42); smoke reale: CASE A porta 8000 HTTP 200, CASE B fallback automatico 8001 HTTP 200, server in-process avvio/shutdown puliti.

### DoD T42

- 8000 libera -> apre http://localhost:8000: VERIFICATO (smoke reale).
- 8000 occupata -> porta successiva libera, porta loggata: VERIFICATO (fallback 8001 reale).
- Tutte 4 occupate -> exit code != 0 + messaggio chiaro: VERIFICATO (test `main` -> 1, browser non aperto).
- Stesso launcher dev e .exe: uvicorn IN-PROCESS (non comando esterno) -> packaging-safe; test reale .exe in scope T66/T67.

### Decisione

- T42 chiuso (codice + runtime). Commit/push NON eseguito: in attesa di ok utente esplicito (pattern stabilito: l'utente controlla i commit). Working tree accumula `launcher.py`, `tests/test_launcher.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M6a/T43 (endpoint `GET /` -> `templates/index.html`, stato "in attesa del client LoL").

## PLOG-2026-05-16-045 - M6a/T43 endpoint GET / serve index.html base (impl + 1 test, runtime VERDE)

- Data: 2026-05-16
- Scope: T43 (M6a) - route `GET /` + `templates/index.html` minimale. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T43 CHIUSO lato codice + DoD runtime VERDE. Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-108: "ok commit/push poi dopo procedi con pianificazione".
- CODEX-281: commit/push T42 (387b9f9 su main); piano T43 esposto (index.html minimale + route Jinja2 + 1 test + verifica + docs); in attesa approvazione.
- USER-109: "procedi".
- CODEX-282: implementazione T43 + 1 test + smoke runtime reale + questa PLOG-045 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `templates/index.html` (nuovo): pagina HTML minimale valida (lang it, UTF-8), `<h1>` + `<p id="status">In attesa del client LoL</p>`. NIENTE Tailwind/sezioni draft/suggerimenti/storico/error-banner (scope T46) ne JS (scope T47): T43 e volutamente minimale come da breakdown ("anche minimale").
- `app/main.py`: import `Request`/`HTMLResponse`/`Jinja2Templates`; `templates = Jinja2Templates(directory="templates")` (path relativo a CWD repo-root in dev/launcher; risoluzione PyInstaller `sys._MEIPASS` RINVIATA a T66 come da breakdown, commento esplicito); route `@app.get("/", response_class=HTMLResponse)` -> `TemplateResponse(request, "index.html")`. Nessun mount `static/` (scope T47).
- `tests/test_main.py`: +1 test `test_index_serves_base_html` (TestClient GET / -> 200, content-type text/html, body contiene "In attesa del client LoL"; init_db/check_patch mockati per non toccare rete/DB).
- `PROMPT_LOG.md`: questa PLOG-045. `BREAKDOWN_STATUS.md`/`README.md`: T43 chiuso, suite 80/80, prossimo T44.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\main.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
# smoke reale: uvicorn app.main:app --port 8055 ; GET /
```

Esiti: compile exit 0; suite **80 passed** (79 + 1 T43); smoke reale `GET /` -> HTTP 200, `text/html; charset=utf-8`, body contiene "In attesa del client LoL".

### DoD T43

- Route `GET /` restituisce `templates/index.html` con stato iniziale "in attesa del client LoL": VERIFICATO (test + smoke reale).
- Browser su `localhost:<porta>` mostra una pagina (anche minimale): VERIFICATO (HTTP 200 HTML, pagina renderizzabile).

### Decisione

- T43 chiuso (codice + runtime). Commit/push NON eseguito: in attesa di ok utente esplicito (pattern stabilito). Working tree accumula `templates/index.html`, `app/main.py`, `tests/test_main.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M6a/T44 (endpoint `GET /api/draft-state` -> stato del DraftStateProvider attivo, JSON).

## PLOG-2026-05-16-046 - M6a/T44 endpoint GET /api/draft-state + provider factory (impl + 2 test, runtime VERDE)

- Data: 2026-05-16
- Scope: T44 (M6a) - `app/providers.py` factory + route `GET /api/draft-state`. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T44 CHIUSO lato codice + DoD runtime VERDE. Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-110: "ok procedi" (commit/push T43 + pianificazione T44).
- CODEX-283: commit/push T43 (e552945 su main); piano T44 esposto (providers.py factory + endpoint + 2 test + verifica + docs); in attesa approvazione.
- USER-111: "procedi".
- CODEX-284: implementazione T44 + 2 test + smoke runtime reale + questa PLOG-046 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `app/providers.py` (nuovo): `get_draft_state_provider(settings) -> DraftStateProvider`; `sim` -> `FileProvider(settings.draft_provider_file)`; `live` -> `LCUProvider()`; mode sconosciuto -> `ValueError`. Modulo dedicato per tenere l'endpoint sottile e centralizzare la scelta LCU-vs-file (spec Â§8.1, Demo Mode First).
- `app/main.py`: import `HTTPException`, `DraftState`, `get_draft_state_provider`; route `@app.get("/api/draft-state")` -> provider da `get_settings()` -> `get_current_state()` -> `DraftState` (FastAPI serializza Pydantic). Su `OSError/ValueError/RuntimeError` -> `HTTPException(503, "Stato draft non disponibile: <tipo>")` senza stack trace. Mapping completo error-code/user-message RINVIATO a T49b (commento esplicito): qui solo minimo anti-crash. Nota: `LockfileError` (RuntimeError) e `ValidationError` (ValueError) ricadono nel 503 controllato.
- `tests/test_main.py`: +2 test (`test_draft_state_sim_returns_draftstate`: get_settings mockato sim+balanced_mid -> 200 application/json, patch/user_role/bans verificati su FileProvider reale; `test_draft_state_provider_error_returns_503`: provider stub che solleva RuntimeError -> 503 JSON controllato). Helper `_mock_lifecycle` per non toccare rete/DB nel lifespan.
- `PROMPT_LOG.md`: questa PLOG-046. `BREAKDOWN_STATUS.md`/`README.md`: T44 chiuso, suite 82/82, prossimo T46.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\main.py app\providers.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
# smoke reale: DRAFT_PROVIDER_MODE=sim DRAFT_PROVIDER_FILE=tests/mock_drafts/balanced_mid.json
#   uvicorn app.main:app --port 8066 ; GET /api/draft-state
```

Esiti: compile exit 0; suite **82 passed** (80 + 2 T44); smoke reale `GET /api/draft-state` -> HTTP 200 `application/json`, DraftState completo (patch 16.10.1, user_role MID, 5 bans, enemy/ally team, actions [], local_player_cell_id 2).

### DoD T44

- Endpoint restituisce lo stato del DraftStateProvider attivo (sim/live da `.env`): VERIFICATO (sim reale + test factory).
- fetch/curl -> JSON con campi DraftState: VERIFICATO (smoke reale, JSON con tutti i campi del model).

### Decisione

- T44 chiuso (codice + runtime). Commit/push NON eseguito: in attesa di ok utente esplicito (pattern stabilito). Working tree accumula `app/providers.py`, `app/main.py`, `tests/test_main.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M6a/T46 (`templates/index.html` completo con Tailwind CDN: header, stato connessione, griglia draft, area suggerimenti, area storico, area error banner nascosta).

## PLOG-2026-05-16-047 - M6a/T46 index.html shell completo Tailwind CDN (impl + 1 test, runtime VERDE)

- Data: 2026-05-16
- Scope: T46 (M6a) - shell HTML completo Tailwind CDN. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T46 CHIUSO lato codice + DoD runtime VERDE. Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-112: "procedi commit/push e poi pianifica prossima task".
- CODEX-285: commit/push T44 (dff2c51 su main); piano T46 esposto.
- USER-113: chiede chiarimento "in che senso nessun JS?" (ERRATA-002 Vanilla JS prioritaria) - sospetto di deviazione dallo stack.
- CODEX-286: chiarito - ERRATA-002 (Vanilla JS+fetch) pienamente rispettata; "nessun JS in T46" = confine del task: il JS sta in `static/app.js` a T47/T48/T56, non nello shell di T46 (decomposizione del breakdown, coerente con ERRATA-002). Nessun cambio di piano.
- USER-114: "mea culpa ... procedi come pianificato".
- CODEX-287: implementazione T46 + 1 test + smoke runtime reale + questa PLOG-047 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `templates/index.html`: da pagina minimale (T43) a shell completo. Tailwind via CDN (`https://cdn.tailwindcss.com`, ERRATA-002 no build step). Sezioni con id: header, `#status` (testo iniziale "In attesa del client LoL" preservato -> test T43 resta verde), `#error-banner` (classe `hidden`, logica T49b), `#draft-grid` con `#bans-list`/`#ally-team`/`#enemy-team`, `#suggestions-section` con `#suggest-button`+`#loading-spinner`(hidden)+`#suggestions`+`#disclaimer` (testo RF-019 statico), `#history-section` con `#history-list`. NESSUN JS (Vanilla JS = T47/T48/T56 in `static/app.js`); bottone/spinner inerti (wiring T48/T49).
- `tests/test_main.py`: +1 test `test_index_shell_has_all_containers` (Tailwind CDN presente; tutti i container nel DOM; `#error-banner` con `hidden`). Test T43 esistente invariato e verde.
- `PROMPT_LOG.md`: questa PLOG-047. `BREAKDOWN_STATUS.md`/`README.md`: T46 chiuso, suite 83/83, prossimo T47.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -q
# smoke reale: uvicorn app.main:app --port 8077 ; GET /
```

Esiti: suite **83 passed** (82 + 1 T46); smoke reale `GET /` -> HTTP 200, presenti `cdn.tailwindcss.com`, `id="status"`, `id="error-banner"`, `id="suggest-button"`, `id="history-list"` (e gli altri container).

### DoD T46

- Pagina rendered con Tailwind funzionante (CDN caricato): VERIFICATO (smoke reale + test).
- Tutti i contenitori presenti nel DOM, error banner inizialmente nascosto con `hidden`: VERIFICATO.

### Decisione

- T46 chiuso (codice + runtime). Commit/push NON eseguito: in attesa di ok utente esplicito (pattern stabilito). Working tree accumula `templates/index.html`, `tests/test_main.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M6a/T47 (`static/app.js` - Vanilla JS che polla `/api/draft-state` ogni 2s e aggiorna la griglia draft; ERRATA-002).

## PLOG-2026-05-16-048 - M6a/T47 Vanilla JS draft-state polling + static mount (impl + 2 test, runtime VERDE) - M6a COMPLETO

- Data: 2026-05-16
- Scope: T47 (M6a) - `static/app.js` Vanilla JS polling + mount StaticFiles + wiring shell. Chiude M6a. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T47 CHIUSO lato codice + DoD runtime VERDE (parte automatica; DOM visivo = check manuale browser). Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-115: "ok commit/push poi procedi con il piano".
- CODEX-288: commit/push T46 (d096474 su main); piano T47 esposto (app.js + static mount + wiring + 2 test + verifica + docs; nota onesta: niente browser headless, DOM visivo = check manuale).
- USER-116: "ok procedi".
- CODEX-289: implementazione T47 + 2 test + smoke runtime reale + questa PLOG-048 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `static/app.js` (nuovo): Vanilla JS + fetch (ERRATA-002, no framework/build). `POLL_INTERVAL_MS=2000`; `pollDraftState()` GET `/api/draft-state` -> aggiorna `#status`, `#bans-list`, `#ally-team`, `#enemy-team` (team ordinati per ruolo TOP..SUPPORT, champion null -> "—"). Non-2xx / errore rete: non-crash, retry al tick successivo (UX completa = T49b). `setInterval` 2s; start su DOMContentLoaded.
- `app/main.py`: import `StaticFiles`; `app.mount("/static", StaticFiles(directory="static"))` (path relativo CWD; PyInstaller sys._MEIPASS RINVIATO a T66, commento esplicito).
- `templates/index.html`: aggiunto `<script src="/static/app.js" defer></script>` prima di `</body>` (wiring JS nello shell, parte di T47).
- `tests/test_main.py`: esteso `test_index_shell_has_all_containers` (assert `/static/app.js` referenziato) + nuovo `test_static_app_js_served` (GET /static/app.js -> 200 javascript, contiene `/api/draft-state` e `2000`).
- `PROMPT_LOG.md`: questa PLOG-048. `BREAKDOWN_STATUS.md`/`README.md`: T47 chiuso, M6a COMPLETO, suite 84/84, prossimo M7a/T50.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\main.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
# smoke reale: DRAFT_PROVIDER_MODE=sim ... uvicorn --port 8088
#   GET /static/app.js ; GET / (wiring) ; /api/draft-state gia verde T44
```

Esiti: compile exit 0; suite **84 passed** (83 + 1 T47); smoke reale `GET /static/app.js` -> HTTP 200 `text/javascript`, contiene `POLL_INTERVAL_MS = 2000` e `fetch("/api/draft-state"`; `GET /` referenzia `/static/app.js`.

### DoD T47

- JS polla `/api/draft-state` ogni 2s e aggiorna la griglia draft: VERIFICATO lato codice + asset servito; aggiornamento DOM visivo (sim mode mostra draft, cambio file -> update <=2s) = CHECK MANUALE via browser (no runtime headless qui; coerente col DoD del breakdown che e osservazione UI manuale).

### Decisione

- T47 chiuso (codice + runtime automatico). **M6a COMPLETO** (T41-T44, T46, T47). Commit/push NON eseguito: in attesa di ok utente esplicito (pattern stabilito). Working tree accumula `static/app.js`, `app/main.py`, `templates/index.html`, `tests/test_main.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M7a/T50 (estensione `app/db.py` con tabelle `cache` e `history`), primo step di M7a (Cache + History core + SuggestionService) prima di M6b/`/api/suggest`.

## PLOG-2026-05-16-049 - M7a/T50 tabelle cache+history + ERRATA-007/INC-011 (impl + 2 test, runtime VERDE)

- Data: 2026-05-16
- Scope: T50 (M7a) - estensione `app/db.py` con tabelle `cache` e `history`; documentazione deviazione persistenza single-file (ERRATA-007 / INC-011). T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T50 CHIUSO lato codice + DoD runtime VERDE. Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-117: "ok commit/push poi procedi" (commit T47 + pianificazione T50).
- CODEX-290: commit/push T47 (1cd8928 su main); piano T50 esposto + nota di coerenza spec (single-DB vs 3 file, deviazione gia in breakdown T10/T50).
- USER-118: solleva la questione - se deviazione da spec serve errata; chiede parere prima di agire (proseguire crea problemi? la partizione serve per stabilita?).
- CODEX-291: parere - single-file SQLite funzionalmente equivalente e piu robusto di 3 file; nessun RF/MVP/validatore dipende dalla partizione; §8.3 descrittiva non requisito; raccomandata Opzione A (documentare via ERRATA + proseguire), non Opzione B (refactor 3 file).
- USER-119: "Si vai con opzione A".
- CODEX-292: ERRATA-007 + INC-011 aggiunti; implementazione T50 single-DB + 2 test + DoD one-liner reale + questa PLOG-049 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `SPEC_ERRATA.md`: aggiunta ERRATA-007 (persistenza singolo file SQLite `data_dragon.db` con tabelle champions/items/runes/meta/cache/history invece dei 3 file §8.3/§5.3; razionale: equivalenza funzionale, piu robusto/semplice, coerente col breakdown T10/T50; impatto nullo strutturale).
- `INCIDENTS.md`: aggiunto INC-011 (gap documentale intercettato a T50, severita bassa, RISOLTO con ERRATA-007; decisione utente Opzione A).
- `app/db.py`: `_utcnow()` helper; modello `CacheEntry` (tabella `cache`: draft_state_hash PK, output_json, model_used, created_at, expires_at); modello `HistoryEntry` (tabella `history`: id PK autoincrement, timestamp, draft_state_json, output_json, model_used, feedback default "unrated"). Nessun campo extra oltre la spec (vincolo T50). `init_db()` invariato (Base.metadata.create_all crea anche le nuove tabelle).
- `tests/test_db.py` (nuovo): 2 test (init_db crea `cache`/`history` con esattamente le colonne spec via `inspect`; `history.feedback` default "unrated" con insert/cleanup reale).
- `PROMPT_LOG.md`: questa PLOG-049. `BREAKDOWN_STATUS.md`/`README.md`: T50 chiuso, suite 86/86, prossimo T51, ERRATA-007/INC-011 nei riferimenti.

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\db.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
.\.venv\Scripts\python.exe -c "import asyncio; from app.db import init_db; asyncio.run(init_db()); ... sqlite_master"
```

Esiti: compile exit 0; suite **86 passed** (84 + 2 T50); DoD one-liner reale: `data_dragon.db` contiene `['cache', 'champions', 'history', 'items', 'meta', 'runes']` (unico file, coerente con ERRATA-007).

### DoD T50

- `init_db()` crea le 2 tabelle aggiuntive con gli schemi della spec: VERIFICATO (test inspect colonne + one-liner reale).
- Nessun campo extra oltre la spec: VERIFICATO (set colonne esatto).

### Decisione

- T50 chiuso (codice + runtime). Deviazione persistenza formalizzata (ERRATA-007/INC-011) prima dell'implementazione, come da decisione utente Opzione A. Commit/push NON eseguito: in attesa di ok utente esplicito. Working tree accumula `SPEC_ERRATA.md`, `INCIDENTS.md`, `app/db.py`, `tests/test_db.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M7a/T51 (`CacheService` get/set in `suggestion_service.py`, NON in `ai_client.py` - SoC).

## PLOG-2026-05-16-050 - M7a/T51 CacheService get/set in suggestion_service.py (impl + 3 test, runtime VERDE)

- Data: 2026-05-16
- Scope: T51 (M7a) - `CacheService` in `app/suggestion_service.py`. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T51 CHIUSO lato codice + DoD VERDE. Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-120: "ok si procedi commit/push e poi andiamo con il piano".
- CODEX-293: commit/push T50 (92697ce su main); piano T51 esposto (CacheService in suggestion_service.py, nota datetime naive, 3 test).
- USER-121: "ok procedi".
- CODEX-294: implementazione T51 + 3 test; fix DeprecationWarning `datetime.utcnow()` -> `datetime.now(timezone.utc).replace(tzinfo=None)`; suite 89/89; questa PLOG-050 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `app/suggestion_service.py` (nuovo): docstring chiarisce che T45b aggiungera SuggestionService allo stesso modulo. `DEFAULT_TTL=timedelta(days=30)` (spec §8.3). `_utcnow_naive()` (UTC naive, no deprecation: `datetime.now(timezone.utc).replace(tzinfo=None)`; commento sul perche naive: SQLite legge naive, confronto naive-naive evita TypeError). `CacheService(session_factory=AsyncSessionLocal)`; `get(hash)` -> None se assente o `expires_at <= now`, altrimenti `SuggestionOutput.model_validate_json`; `set(hash, output, model_used, ttl=30gg)` -> `session.merge` upsert con created_at/expires_at espliciti. CacheService NON in ai_client.py (SoC, breakdown v2.1).
- `tests/test_cache_service.py` (nuovo): 3 test su AsyncSessionLocal reale con cleanup (hash dedicato `t51-test-hash-do-not-collide`): get assente -> None; set->get roundtrip (model_dump uguale); entry scaduto (ttl=-1s) -> None.
- `PROMPT_LOG.md`: questa PLOG-050. `BREAKDOWN_STATUS.md`/`README.md`: T51 chiuso, suite 89/89, prossimo T52.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale; il fix deprecation e codice nuovo dello stesso task, non un incidente).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\suggestion_service.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

Esiti: compile exit 0; suite **89 passed** (86 + 3 T51), 0 warning (DeprecationWarning rimosso).

### DoD T51

- `get(known_hash)` -> SuggestionOutput se presente, None se assente: VERIFICATO.
- `set(...)` poi `get(...)` -> stesso oggetto: VERIFICATO (model_dump uguale).
- Entry scaduto -> None (TTL rispettato): VERIFICATO (bonus oltre DoD).
- Integrazione cache-hit a livello SuggestionService: rinviata al DoD di T45b (come da breakdown).

### Decisione

- T51 chiuso. Commit/push NON eseguito: in attesa di ok utente esplicito. Working tree accumula `app/suggestion_service.py`, `tests/test_cache_service.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M7a/T52 (salvataggio cache post-chiamata - in larga parte coperto da `CacheService.set`; verifica integrazione TTL 30gg + persistenza a restart).

## PLOG-2026-05-16-051 - M7a/T52 verifica salvataggio cache (persistenza + TTL 30gg) (2 test, VERDE)

- Data: 2026-05-16
- Scope: T52 (M7a) - verifica integrazione salvataggio cache post-chiamata. Nessun nuovo codice applicativo (gia coperto da T51 `CacheService.set`). T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T52 CHIUSO + DoD VERDE. Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-122: "ok commit/push, poi procedi".
- CODEX-295: commit/push T51 (cc57934 su main); piano T52 esposto (natura: solo verifica; wiring SuggestionService->set rinviato a T45b come da breakdown; 2 test).
- USER-123: "ok procedi".
- CODEX-296: 2 test T52 + verifica + questa PLOG-051 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `tests/test_cache_service.py`: import `sqlite3` + `DEFAULT_TTL`; +2 test T52: `test_set_default_ttl_is_30_days` (set senza ttl -> riga con `expires_at-created_at == DEFAULT_TTL == 30gg`, model_used corretto); `test_cache_persists_on_disk` (set -> lettura raw via `sqlite3.connect("data_dragon.db")` conferma riga su disco; nuova istanza `CacheService` rilegge l'output = restart simulato).
- Nessun file applicativo modificato: `CacheService.set` (T51) gia implementa il salvataggio con TTL 30gg di default. T52 e verifica/integrazione come da breakdown.
- `PROMPT_LOG.md`: questa PLOG-051. `BREAKDOWN_STATUS.md`/`README.md`: T52 chiuso, suite 91/91, prossimo T53.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_cache_service.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

Esiti: cache_service 5/5; suite **91 passed** (89 + 2 T52).

### DoD T52

- Dopo prima chiamata, riga in tabella cache: VERIFICATO (set -> riga presente, model_used corretto, TTL 30gg).
- Sopravvive a restart server: VERIFICATO (riga su disco in `data_dragon.db` via sqlite3 raw + nuova istanza CacheService la rilegge).
- Wiring "dopo output valido in SuggestionService -> set": RINVIATO al DoD di T45b (come prescritto dal breakdown; SuggestionService non ancora costruito a questo punto dell'ordine M7a).

### Decisione

- T52 chiuso (verifica). Commit/push NON eseguito: in attesa di ok utente esplicito. Working tree accumula `tests/test_cache_service.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M7a/T53 (`HistoryRepository.save(draft_state, output, model_used)`, feedback inizializzato a "unrated", chiamato da SuggestionService a T45b).

## PLOG-2026-05-16-052 - M7a/T53 HistoryRepository.save feedback=unrated (impl + 2 test, VERDE)

- Data: 2026-05-16
- Scope: T53 (M7a) - `HistoryRepository` in `app/suggestion_service.py`. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T53 CHIUSO + DoD VERDE. Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-124: "ok procedi commit/push poi pianifica".
- CODEX-297: commit/push T52 (2a93b59 su main); piano T53 esposto (HistoryRepository in suggestion_service.py, save->id, 2 test).
- USER-125: "ok procedi".
- CODEX-298: implementazione T53 + 2 test + verifica + questa PLOG-052 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `app/suggestion_service.py`: import `HistoryEntry`, `DraftState`. Classe `HistoryRepository(session_factory=AsyncSessionLocal)`; `async save(draft_state, output, model_used) -> int`: inserisce `HistoryEntry` con `timestamp=_utcnow_naive()`, `draft_state_json`/`output_json` via `model_dump_json()`, `model_used`, `feedback="unrated"`; ritorna `entry.id` (utile a T54). Commento: `expire_on_commit=False` rende l'id disponibile post-commit senza refresh.
- `tests/test_history_repository.py` (nuovo): 2 test con cleanup per id: `test_save_three_rows_unrated_with_model_used` (3 save -> 3 id distinti, ogni riga `feedback=unrated` + `model_used` valorizzato = DoD esatto); `test_saved_json_roundtrips` (`draft_state_json`/`output_json` ri-parsano in DraftState/SuggestionOutput uguali agli originali).
- `PROMPT_LOG.md`: questa PLOG-052. `BREAKDOWN_STATUS.md`/`README.md`: T53 chiuso, suite 93/93, prossimo T45b.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\suggestion_service.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

Esiti: compile exit 0; suite **93 passed** (91 + 2 T53).

### DoD T53

- Dopo 3 chiamate diverse, 3 righe in history con `feedback="unrated"` e `model_used` valorizzato: VERIFICATO.
- (bonus) JSON salvati ri-parsabili nei modelli: VERIFICATO.
- Chiamata da `SuggestionService`: wiring rinviato a T45b (come da breakdown).

### Decisione

- T53 chiuso. **M7a core (T50-T53) completo**; resta T45b (orchestratore). Commit/push NON eseguito: in attesa di ok utente esplicito. Working tree accumula `app/suggestion_service.py`, `tests/test_history_repository.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M7a/T45b (`SuggestionService` orchestratore: DraftStateHash -> CacheService -> PromptBuilder -> AIClient chain -> Validators -> HistoryRepository; cache miss/hit, log; dipende da T25/T29/T30/T51/T52/T53).

## PLOG-2026-05-16-053 - M7a/T45b SuggestionService orchestratore (impl + 6 test, VERDE) - M7a COMPLETO

- Data: 2026-05-16
- Scope: T45b (M7a) - `SuggestionService` orchestratore in `app/suggestion_service.py`. Chiude M7a. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T45b CHIUSO + DoD VERDE (mock AI; runtime reale = OPEN-001 batch). Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-126: "ok commit/push poi procedi" (commit T53 + pianificazione T45b).
- CODEX-299: commit/push T53 (2ca52f9 su main); verifica firme reali (build_prompt, get_suggestions_with_fallback, validators); piano T45b esposto con decisione di scope (punto 2: gate validatori senza sostituzioni/truncate) da confermare.
- USER-127: "ok procedi" (conferma piano + scelta scope gate).
- CODEX-300: implementazione T45b + 6 test + verifica + questa PLOG-053 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `app/suggestion_service.py`: docstring aggiornata (CacheService+HistoryRepository+SuggestionService qui). Aggiunti: `SuggestionError(RuntimeError)` (fallimento controllato, no stack trace; mapping UI = T49b); `draft_state_hash(draft_state)` puro deterministico sha256 su JSON canonico di `patch+user_role+bans+enemy_team+ally_team` (esclusi `actions`/`local_player_cell_id` volatili, documentato, coerente spec "hash su ban+pick+role"); `CacheService.get_with_model` (helper ADDITIVO, non tocca `get` di T51; serve per salvare history col model_used del cached su cache hit, richiesto dal DoD); `SuggestionService(cache, history, ai_call=get_suggestions_with_fallback)` con `suggest(draft_state)`: hash -> `get_with_model` (hit: history.save col model_used cached, ritorna cached) -> miss: `build_prompt(draft,{})` -> `ai_call` (RuntimeError -> SuggestionError) -> `validator_format` (fail -> SuggestionError) -> `_run_legality_gate` (champion/items/keystone legality + explanation_length + utf8 + language; fail -> SuggestionError) -> `cache.set` + `history.save` -> ritorna. Gate-only: rimedi graceful (sostituzione item default, truncate) NON qui (fuori DoD T45b, scelta confermata dall'utente).
- `tests/test_suggestion_service.py` (nuovo): 6 test, AI mockato (Demo Mode First/OPEN-001), nomi DD reali da cache per passare la gate, cleanup cache(hash)+history(model_used sentinel): cache-miss (1 call, cache+history unrated), cache-hit (0 call, history col model_used cached), chain esaurita -> SuggestionError, output invalido -> SuggestionError, hash deterministico, no dati personali nei record (no summoner/gamename/displayname/api_key).
- `PROMPT_LOG.md`: questa PLOG-053. `BREAKDOWN_STATUS.md`/`README.md`: T45b chiuso, M7a COMPLETO, suite 99/99, prossimo M6b/T45.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\suggestion_service.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

Esiti: compile exit 0; suite **99 passed** (93 + 6 T45b).

### DoD T45b

- Cache miss -> AI -> valida -> cache + history(unrated, model_used) -> SuggestionOutput: VERIFICATO.
- 2a chiamata stesso draft -> cache hit -> 0 chiamate AI -> cached + history col model_used cached: VERIFICATO.
- Output sempre SuggestionOutput Pydantic-valido (anche post-cache): VERIFICATO.
- Log JSONL per chiamate AI reali: gia coperto da ai_client T30 (qui AI mockata; runtime reale = OPEN-001 batch, Demo Mode First).
- Nessuna API key / summoner / dato personale in prompt/log/history: VERIFICATO (test dedicato + DraftState privo di campi summoner by design T39).

### Decisione

- T45b chiuso. **M7a COMPLETO** (T50-T53 + T45b). Commit/push NON eseguito: in attesa di ok utente esplicito. Working tree accumula `app/suggestion_service.py`, `tests/test_suggestion_service.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M6b/T45 (endpoint sottile `POST /api/suggest` che delega a `SuggestionService`; dipende da T44, T31, T45b).

## PLOG-2026-05-16-054 - M6b/T45 endpoint sottile POST /api/suggest (impl + 3 test, runtime VERDE)

- Data: 2026-05-16
- Scope: T45 (M6b) - route sottile `POST /api/suggest` -> `SuggestionService`. Avvia M6b. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T45 CHIUSO + DoD VERDE (path 200 con AI reale = OPEN-001 batch). Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-128: "ok procedi commit/push".
- CODEX-301: commit/push T45b (498e63e su main); piano T45 esposto.
- USER-129: "confermo procedi".
- CODEX-302: implementazione T45 + 3 test + smoke runtime reale + questa PLOG-054 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `app/main.py`: import `SuggestionOutput`, `SuggestionError`, `SuggestionService`. Route `@app.post("/api/suggest")`: body `DraftState` (FastAPI -> 422 automatico su malformato); delega a `SuggestionService().suggest(draft_state)`; ritorna `SuggestionOutput`. Su `SuggestionError` -> `HTTPException(503, "Suggerimenti non disponibili, riprova tra poco.")` (no stack trace, no API key; mapping completo = T49b). Endpoint sottile: zero logica cache/prompt/validation/history (tutto in T45b).
- `tests/test_main.py`: import `SuggestionError`; +3 test (body valido + SuggestionService stub -> 200, 3 suggerimenti, draft deserializzato; body malformato -> 422; SuggestionError -> 503 controllato, nessun `sk-secret-xyz` ne `Traceback` nel body). Equivalenza cache miss/hit gia testata in T45b: l'endpoint la delega, non la re-testa.
- `PROMPT_LOG.md`: questa PLOG-054. `BREAKDOWN_STATUS.md`/`README.md`: T45 chiuso, suite 102/102, prossimo T48.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\main.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
# smoke reale: DEEPSEEK_API_KEY= DRAFT_PROVIDER_MODE=sim uvicorn --port 8099
#   POST /api/suggest (draft valido) -> 503 controllato (AI chain fallisce, no key)
#   POST body malformato -> 422
```

Esiti: compile exit 0; suite **102 passed** (99 + 3 T45); smoke reale: POST draft valido senza key -> HTTP 503 `{"detail":"Suggerimenti non disponibili, riprova tra poco."}` (nessun stack trace/key); body malformato -> HTTP 422.

### DoD T45

- POST body draft -> 200 con 3 suggerimenti (cache miss): VERIFICATO via stub (path con AI reale = OPEN-001 batch, Demo Mode First).
- 2a chiamata stesso body -> cache hit stesso output: delegato a `SuggestionService` (gia testato in T45b); endpoint resta sottile.
- POST body malformato -> 422 Pydantic: VERIFICATO (test + smoke reale).
- Eccezione interna AI -> non-2xx controllato senza stack trace/API key: VERIFICATO (test + smoke reale 503).

### Decisione

- T45 chiuso. Commit/push NON eseguito: in attesa di ok utente esplicito. Working tree accumula `app/main.py`, `tests/test_main.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M6b/T48 (`static/app.js` - bottone "Suggerisci ora" -> POST `/api/suggest` -> render 3 card champion+build+keystone+spiegazione).

## PLOG-2026-05-16-055 - M6b/T48 render suggerimenti in app.js (impl + 1 test, VERDE)

- Data: 2026-05-16
- Scope: T48 (M6b) - `static/app.js`: bottone -> POST /api/suggest -> render 3 card. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T48 CHIUSO + DoD VERDE (parte automatica; DOM visivo = check manuale browser). Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-130: "ok commit/push poi procedi con il piano".
- CODEX-303: commit/push T45 (04684a2 su main); piano T48 esposto (nota onesta: DOM visivo = check manuale, come T47).
- USER-131: "procedi".
- CODEX-304: implementazione T48 + 1 test + smoke + questa PLOG-055 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `static/app.js`: header aggiornato (T47+T48). `latestDraftState` di modulo aggiornato da `pollDraftState` (memorizza l'ultimo draft). Aggiunti `suggestionCard(suggestion)` (card Tailwind: `#rank champion`, keystone, build_path lista, explanation), `renderSuggestions(output)` (svuota e popola `#suggestions`), `requestSuggestions()` (guardia no draft -> no-op; `fetch POST /api/suggest` con `latestDraftState`; non-2xx/errore -> non-crash, UX completa = T49/T49b). `start()` aggancia `click` su `#suggest-button`.
- `tests/test_main.py`: +1 test `test_static_app_js_has_suggest_wiring` (app.js contiene `/api/suggest`, `"POST"`, `suggest-button`, `addEventListener`, `getElementById("suggestions")`, e i campi champion/keystone/build_path/explanation).
- `PROMPT_LOG.md`: questa PLOG-055. `BREAKDOWN_STATUS.md`/`README.md`: T48 chiuso, suite 103/103, prossimo T49.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -q
# smoke reale: uvicorn --port 8101 ; GET /static/app.js
```

Esiti: suite **103 passed** (102 + 1 T48); smoke reale `/static/app.js` HTTP 200 con `/api/suggest`, `suggest-button`, `getElementById("suggestions")` presenti.

### DoD T48

- Click "Suggerisci ora" -> POST /api/suggest -> 3 card con champion+build+keystone+spiegazione: wiring e render coperti da test/smoke; rendering DOM visivo = CHECK MANUALE via browser (no runtime headless; coerente col DoD del breakdown = osservazione UI, come T47).

### Decisione

- T48 chiuso (codice + verifica automatica). Commit/push NON eseguito: in attesa di ok utente esplicito. Working tree accumula `static/app.js`, `tests/test_main.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M6b/T49 (`static/app.js`/UI - loading spinner durante la chiamata AI + disclaimer "AI puo sbagliare, decisione finale al giocatore" sempre visibile sopra i suggerimenti).

## PLOG-2026-05-16-056 - M6b/T49 loading spinner + disclaimer sopra i suggerimenti (impl + 2 test, VERDE)

- Data: 2026-05-16
- Scope: T49 (M6b) - spinner durante chiamata AI + disclaimer RF-019 sopra `#suggestions`. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T49 CHIUSO + DoD VERDE (visivo = check manuale browser). Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-132: "ok commit/push, poi procedi con il piano".
- CODEX-305: commit/push T48 (9726b1e su main); piano T49 esposto (riordino disclaimer sopra suggestions, spinner toggle in finally; error-banner/re-enable = T49b).
- USER-133: "confermo".
- CODEX-306: implementazione T49 + 2 test + smoke + questa PLOG-056 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `templates/index.html`: riordinata la sezione suggerimenti -> bottone, `#disclaimer` (statico, non-dismiss, RF-019, ora `mb-3` SOPRA i suggerimenti), `#loading-spinner` (hidden, `mb-3`), `#suggestions`. Nessun elemento nuovo, solo riordino + classi margine.
- `static/app.js`: helper `setSpinner(visible)` (`classList.toggle("hidden", !visible)`); `requestSuggestions()` ora fa `setSpinner(true)` prima del fetch e `setSpinner(false)` in `finally` (sempre, anche su errore). Commento no-draft aggiornato a T49b. Error-banner/re-enable bottone NON qui (= T49b).
- `tests/test_main.py`: +2 test (`test_disclaimer_above_suggestions`: testo RF-019 presente e `index('id="disclaimer"') < index('id="suggestions"')`; `test_app_js_toggles_loading_spinner`: app.js contiene `loading-spinner`, `setSpinner(true)`, `setSpinner(false)`, `finally`).
- `PROMPT_LOG.md`: questa PLOG-056. `BREAKDOWN_STATUS.md`/`README.md`: T49 chiuso, suite 105/105, prossimo T49b.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati (nessun incidente reale).

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -q
# smoke reale: uvicorn --port 8103 ; GET /
```

Esiti: suite **105 passed** (103 + 2 T49); smoke reale `GET /` HTTP 200 con `#disclaimer` prima di `#suggestions` e testo "Decisione finale al giocatore".

### DoD T49

- Disclaimer "AI puo sbagliare, decisione finale al giocatore" presente e sopra i suggerimenti (RF-019): VERIFICATO (test ordine DOM + smoke reale).
- Spinner visibile durante la chiamata AI: wiring VERIFICATO (setSpinner true prima del fetch, false in finally); visivo = CHECK MANUALE browser (no runtime headless; coerente col DoD del breakdown, come T47/T48).

### Decisione

- T49 chiuso (codice + verifica automatica). Commit/push NON eseguito: in attesa di ok utente esplicito. Working tree accumula `templates/index.html`, `static/app.js`, `tests/test_main.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M6b/T49b (error banner + stato errori UI/backend, Must non tagliabile: copre MVP-013, RF-013/RF-022/RF-023/RF-024, spec Â§12).

## PLOG-2026-05-16-057 - M6b/T49b error contract + UI error banner (impl + 7 test, runtime VERDE) - M6b COMPLETO

- Data: 2026-05-16
- Scope: T49b (M6b, Must non tagliabile) - contratto errori backend uniforme + banner UI + log ERROR. Chiude M6b. T40 resta IN SOSPESO (scelta utente), si procede.
- Stato: T49b CHIUSO + DoD VERDE (banner visivo = check manuale browser). Commit/push IN ATTESA di ok utente.

### Messaggi catalogati

- USER-134: "ok commit/push poi continua con il piano".
- CODEX-307: commit/push T49 (48ed05b su main); piano T49b esposto con tassonomia error_code da confermare.
- USER-135: "ok procedi" (conferma piano + tassonomia).
- CODEX-308: implementazione T49b + 7 test (2 aggiornati al nuovo contratto + 5 nuovi) + smoke runtime reale + questa PLOG-057 + BREAKDOWN_STATUS/README.

### File creati/modificati

- `app/suggestion_service.py`: `SuggestionError.__init__(message, error_code="ai_unavailable")` con attributo `error_code`; valorizzato ai raise (chain/AI -> `ai_unavailable`; format/gate -> `ai_output_invalid`).
- `app/main.py`: import `RequestValidationError`, `JSONResponse`, `LockfileError`, `Path`; rimosso `HTTPException`/`SuggestionOutput` inutilizzati. `_ERROR_STATUS` (invalid_input 422, ai_unavailable 503, ai_output_invalid 502, draft_unavailable 503). `_configure_logging`: FileHandler ERROR su `logs/errors.log` con guardia anti-duplicato (`_ldc_errors_file`). `_error_response(error_code,user_message,log_detail)`: logga ERROR server-side + ritorna JSON `{error_code,user_message}` (no stack trace/secret nel body). Exception handler `RequestValidationError` -> contratto `invalid_input` 422. `/api/draft-state`: `LockfileError`->`draft_unavailable` (msg "Client League of Legends non rilevato..."), `OSError/ValueError/RuntimeError`->`draft_unavailable`. `/api/suggest`: `SuggestionError` -> mapping da `error_code` (status coerente, user_message IT). Annotazioni di ritorno rimosse dove si ritorna JSONResponse.
- `static/app.js`: `showError(msg)` (mostra `#error-banner`/`#error-message`, `scrollIntoView`), `clearError()`, `errorMessageFrom(response)` (legge `user_message` dal contratto). `requestSuggestions()`: `clearError()` a inizio, su non-2xx `showError(user_message)`, su errore rete `showError("Rete non disponibile, riprova.")`, bottone mai disabilitato (resta cliccabile), spinner off in `finally`. Decisione: `pollDraftState()` NON mostra banner (polling 2s; spec Â§12 mappa "client LoL chiuso" allo stato d'attesa, non a un banner che lampeggerebbe) - banner riservato all'azione esplicita Suggerisci.
- `tests/test_main.py`: 2 test aggiornati al nuovo contratto (draft-state error -> `error_code=draft_unavailable`; suggest error -> `error_code=ai_unavailable`, no key in user_message) + 5 nuovi (malformed -> invalid_input 422; ai_output_invalid -> 502; LockfileError -> draft_unavailable 503 con "League of Legends"; errore loggato a ERROR via caplog; app.js error-banner wiring showError/clearError/scrollIntoView/user_message).
- `PROMPT_LOG.md`: questa PLOG-057. `BREAKDOWN_STATUS.md`/`README.md`: T49b chiuso, M6b COMPLETO, suite 110/110, prossimo M7b/T54.
- `INCIDENTS.md`/`SPEC_ERRATA.md`: NON modificati. Nessun nuovo pattern di errore reale emerso durante i test (il DoD chiede entry solo "eventuali"); niente entry forzata.

### Verifiche eseguite

```powershell
.\.venv\Scripts\python.exe -m compileall app\main.py app\suggestion_service.py -q
.\.venv\Scripts\python.exe -m pytest tests/ -q
# smoke reale: DEEPSEEK_API_KEY= DRAFT_PROVIDER_MODE=sim uvicorn --port 8105
#   POST valido (no key) -> 503 {error_code:ai_unavailable,user_message}
#   POST malformato -> 422 {error_code:invalid_input,user_message}
#   logs/errors.log: 2 righe ERROR (dettaglio server-side, nessuna key/stack trace nel body)
```

Esiti: compile exit 0; suite **110 passed** (105 + 7 net, 2 aggiornati); smoke reale conforme; `logs/errors.log` (gitignored, `git check-ignore` OK) riceve righe ERROR.

### DoD T49b

- Ogni eccezione interna -> HTTP code coerente (4xx input / 5xx servizi) + body `{error_code,user_message}`: VERIFICATO (test + smoke: 422 invalid_input, 503 ai_unavailable/draft_unavailable, 502 ai_output_invalid).
- UI non crasha, messaggio comprensibile IT, banner: VERIFICATO (wiring test; visivo = check manuale browser).
- Bottone "Suggerisci" mai disabilitato (sempre cliccabile): VERIFICATO (codice: nessun disable; `clearError` a inizio, `setSpinner(false)` in finally).
- Errore loggato ERROR + entry in `logs/errors.log`: VERIFICATO (caplog test + smoke reale file).
- Stato globale recuperabile (polling continua): VERIFICATO (polling indipendente, nessuna eccezione propagata; banner solo su azione Suggerisci).
- INCIDENTS aggiornato con nuovi pattern: nessun nuovo pattern reale emerso -> nessuna entry (coerente col DoD "eventuali").

### Decisione

- T49b chiuso (codice + verifica). **M6b COMPLETO** (T45, T48, T49, T49b). Commit/push NON eseguito: in attesa di ok utente esplicito. Working tree accumula `app/suggestion_service.py`, `app/main.py`, `static/app.js`, `tests/test_main.py`, `PROMPT_LOG.md`, `BREAKDOWN_STATUS.md`, `README.md`.
- Prossimo task: M7b/T54 (endpoint `POST /api/history/feedback` -> aggiorna record via HistoryRepository, `feedback: good|bad`).

## PLOG-2026-05-16-058 - Ricognizione completa post-T49b + commit/push iniziale richiesto

- Data: 2026-05-16
- Scope: richiesta utente di non costruire ancora, fare prima commit/push di quanto mancante, leggere integralmente allegati + `PROMPT_LOG.md`, analizzare stato breakdown/repo/README/incidenti e proporre piano di azione in attesa di approvazione.
- Stato: ricognizione completata; piano da esporre all'utente. Nessuna implementazione funzionale avviata.

### Messaggi catalogati

- USER-136: chiede di mantenere `PROMPT_LOG.md` aggiornato a ogni iterazione, usare `INCIDENTS.md` per incidenti reali, continuare il breakdown con data odierna, leggere integralmente i file allegati e il prompt log, analizzare repo/status/discrepanze/README, proporre piano prima di costruire; subtask preliminare: commit/push di cio' che manca.
- CODEX-309: avvia la fase preliminare, controlla stato git, diff, remote e ultimo log; rileva working tree sporco da T49b e `.claude/` non tracciato.
- CODEX-310: esclude `.claude/` da git con `.gitignore`, tenta verifica test e rileva ambiente Python non funzionante in questa sessione.
- CODEX-311: commit/push completati per T49b con commit `04a14fa feat(ui): T49b uniform error contract and banner`, push riuscito su `origin/main`.
- CODEX-312: legge integralmente `LiveDraftCompanion_TechnicalSpec_v2.3.md`, `LiveDraftCompanion_SPEC_ERRATA.md`, `breakdown_tasks_v2.1_corretto.md`, `LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`, `BREAKDOWN_STATUS.md`, `INCIDENTS.md`, `SPEC_ERRATA.md`, `README.md` e `PROMPT_LOG.md`.
- CODEX-313: identifica stato corrente: M6b chiuso, M7a chiuso, prossimo task reale M7b/T54; T40 resta in sospeso, T05b e OPEN-002 restano arretrati non bloccanti per T54.
- CODEX-314: rileva discrepanze documentali residue da sistemare prima o insieme a T54: `BREAKDOWN_STATUS.md` contiene ancora riferimento 69/69 e commit T49b "in attesa"; `README.md` contiene frasi stale "M6a IN CORSO"/"M7a IN CORSO"; `INCIDENTS.md` va aggiornato o esteso per l'ambiente Python/venv rotto se confermato come incidente operativo.
- CODEX-315: appende questa PLOG-058 prima dell'output finale, come richiesto.

### File letti integralmente

- `C:\Users\ezioc\Downloads\LiveDraftCompanion_TechnicalSpec_v2.3.md`
- `C:\Users\ezioc\Downloads\LiveDraftCompanion_SPEC_ERRATA.md`
- `C:\Users\ezioc\Downloads\breakdown_tasks_v2.1_corretto.md`
- `C:\Users\ezioc\Downloads\LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md`
- `PROMPT_LOG.md`
- `BREAKDOWN_STATUS.md`
- `INCIDENTS.md`
- `SPEC_ERRATA.md`
- `README.md`

### Esiti commit/push preliminare

- Working tree iniziale: modifiche T49b non ancora committate piu' `.claude/` non tracciata.
- Azione: `.claude/` aggiunta a `.gitignore` per non versionare impostazioni locali.
- Commit creato: `04a14fa feat(ui): T49b uniform error contract and banner`.
- Push: riuscito su `origin/main` (`48ed05b..04a14fa`).

### Verifiche e blocchi

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -q
where.exe python
where.exe py
```

Esito: test NON rieseguiti in questa sessione per problema ambiente locale: `.venv\Scripts\python.exe` punta a `C:\Users\ezioc\AppData\Local\Programs\Python\Python312\python.exe`, non presente; `python` e `py` non sono in PATH. L'ultima suite valida resta quella documentata in PLOG-057: **110 passed**. Questo va registrato/gestito come incidente operativo se confermato.

### Sintesi ricognizione

- Fonte corrente: repo `BREAKDOWN_STATUS.md` e `PROMPT_LOG.md`; il file `LiveDraftCompanion_BREAKDOWN_STATUS_pc_its.md` e storico/stale e si ferma prima dell'avanzamento attuale.
- Prossima task da breakdown: **M7b/T54** (`POST /api/history/feedback`, aggiornamento record history con `feedback: good|bad`).
- Task arretrate note: T40 real draft bans/actions in sospeso; T05b panel recruitment manuale; OPEN-002 dati benchmark reali; residuo OPEN-001 revoca vecchia chiave OpenRouter; finding pytest bare command.
- README: da aggiornare in modo leggero per rimuovere frasi stale e riallineare lo stato a M6b/M7a completi, prossimo T54.

### Piano da sottoporre

1. Prima correzione documentale: aggiornare `BREAKDOWN_STATUS.md`, `README.md`, e `INCIDENTS.md`/INC-004 o nuovo INC-012 per il problema Python/venv; poi aggiornare `PROMPT_LOG.md` e commit/push della sola documentazione se approvato.
2. Gate tecnico: ripristinare o confermare un interprete Python valido prima di implementare T54, per poter rieseguire la suite.
3. Dopo approvazione: implementare T54 in modo sottile e coerente con T49b (`HistoryRepository` update + route `POST /api/history/feedback` + contratto errori + test mirati), poi aggiornare status/log/README e commit/push.
