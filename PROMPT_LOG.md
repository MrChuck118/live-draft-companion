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
