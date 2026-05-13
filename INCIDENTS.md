# INCIDENTS.md

Registro degli incidenti, dei rischi emersi durante lo sviluppo e delle decisioni tecniche cambiate a causa di evidenza pratica.

Regola operativa: registrare qui problemi reali che fanno perdere tempo, cambiano il piano, richiedono mitigazioni, oppure documentano scope creep evitato. Non creare incidenti artificiali.

## INC-001 - Gating LCU del 09/05/2026

- Data rilevazione: 2026-05-09
- Fase: pre-build / validazione tecnica v2.3
- Severita: rischio tecnico validato
- Stato: mitigato nella spec v2.3
- Fonte: `LiveDraftCompanion_TechnicalSpec_v2.3.md`, sezioni 7.1, 11.3, 14.2 e registro versioni.

### Descrizione

Il gating test LCU ha confermato che l'integrazione diretta con `httpx` + lockfile funziona sul PC di casa: client rilevato, fase `ChampSelect` catturata, draft state leggibile. Il wrapper `lcu-driver` e stato scartato come dipendenza primaria.

Nel test custom con bot del 09/05/2026 e stata pero osservata una differenza pratica nello schema delle `actions`: custom con bot ha mostrato `actions count: 3`, mentre una draft ranked/tournament tipica dovrebbe esporre molte piu azioni di ban/pick.

### Impatto

La scelta tecnica LCU e confermata, ma il parser live va testato di nuovo in custom Tournament Draft con ban attivati prima di considerare chiusa la modalita live.

### Mitigazione

- Seguire il principio Demo Mode First.
- Costruire prima `FileProvider`.
- Integrare `LCUProvider` solo dopo sim end-to-end.
- In T40 verificare schema actions live e documentare eventuali differenze.

## INC-002 - Workspace locale non allineata alla repo GitHub

- Data rilevazione: 2026-05-11
- Fase: pre-build / orientamento M0
- Severita: setup blocker leggero
- Stato: risolto

### Descrizione

La cartella aperta `C:\LiveDraftCompanion` non era una repository Git: `git status` restituiva `fatal: not a git repository`. La cartella conteneva solo due file vuoti iniziali, `prompt_log` e `incidents`, poi compilati come registri locali.

Il repository remoto indicato nella spec e dall'utente esiste ed e raggiungibile:

- URL: `https://github.com/MrChuck118/live-draft-companion`
- Branch: `main`
- Commit remoto verificato: `0ca1767cf18ca55aea0f5c3047fa7126f8158d15`
- File remoti iniziali: `README.md`, `LICENSE`, `.gitignore`

### Impatto

Senza riallineamento, iniziare T02-T04 dentro `C:\LiveDraftCompanion` avrebbe creato una workspace diversa dalla repo ufficiale, con rischio di perdere tracciabilita dei commit.

### Mitigazione

La cartella `C:\LiveDraftCompanion` e stata agganciata a `origin/main` preservando i registri locali e normalizzandoli in `PROMPT_LOG.md` e `INCIDENTS.md`.

## INC-003 - `psutil<5.7.0` non installabile su Python 3.12.10

- Data rilevazione: 2026-05-11
- Fase: M0 / T03b
- Severita: setup blocker
- Stato: risolto con ERRATA-004

### Descrizione

Durante `pip install -r requirements.txt`, il vincolo originale `psutil<5.7.0` ha scaricato `psutil-5.6.7.tar.gz` e ha tentato la compilazione locale su Python 3.12.10. La build della wheel e fallita con errore:

```text
Microsoft Visual C++ 14.0 or greater is required.
```

Questo conferma il rischio gia previsto in T03b del breakdown: il pin vecchio non offre wheel compatibile per CPython 3.12 su Windows e richiede toolchain C++ locale.

### Impatto

T03 non puo chiudersi con il pin originale. Senza correzione, l'ambiente non e replicabile su PC Academy o su una macchina Windows pulita.

### Mitigazione

- Aggiunta `ERRATA-004` in `SPEC_ERRATA.md`.
- Aggiornato `requirements.txt` a `psutil>=5.9.8,<8`, come previsto dal fallback T03b.
- Nuovo `pip install -r requirements.txt` completato con successo.
- Verifica T03b completata: `import psutil` funziona e riporta versione `7.2.2`.

## INC-004 - `python` e `py` non presenti nel PATH della sessione

- Data rilevazione: 2026-05-11
- Fase: M0 / T03
- Severita: setup friction
- Stato: mitigato

### Descrizione

I comandi `where.exe python py`, `python --version` e `py --version` non trovano interpreti nella sessione corrente. Python 3.12.10 e pero installato e funzionante al percorso:

```text
C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe
```

### Impatto

La procedura standard della spec (`python -m venv .venv`) non funziona letteralmente in questa sessione se il PATH non viene corretto. La creazione della virtualenv richiede l'uso del percorso assoluto.

### Mitigazione

- Creata `.venv` usando il percorso assoluto di Python 3.12.10.
- Le verifiche successive usano `.\.venv\Scripts\python.exe`.
- Da considerare per README/setup finale: indicare fallback con percorso assoluto o chiedere all'utente di aggiungere Python al PATH.

## INC-005 - Output `pip show` rumoroso per encoding console CP1252

- Data rilevazione: 2026-05-11
- Fase: audit dipendenze pc its
- Severita: bassa
- Stato: mitigato

### Descrizione

Durante `pip show` su piu pacchetti, la console Windows in encoding CP1252 ha generato `UnicodeEncodeError` su metadati autore contenenti caratteri non ASCII.

### Impatto

Nessun impatto sull'installazione o sugli import. `pip check`, `pip list`, `pip install -r requirements.txt` e gli import Python hanno funzionato correttamente.

### Mitigazione

Per le verifiche operative usare:

```powershell
.\.venv\Scripts\python.exe -m pip list --format=freeze
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -c "import ..."
```

Evitare `pip show` multipacchetto come fonte primaria in questa console.

## INC-006 - DoD T08 cita item non presente in Data Dragon patch corrente

- Data rilevazione: 2026-05-13
- Fase: M1 / T08
- Severita: DoD blocker
- Stato: risolto con ERRATA-005

### Descrizione

Durante la verifica di `fetch_items()` su Data Dragon patch `16.10.1`, l'endpoint `item.json` ha restituito 705 item. Il dataset contiene `Liandry's Torment` e non contiene il nome italiano `Tormento di Liandry`, ma non contiene `Luden's Companion`, richiesto letteralmente dal DoD T08 del breakdown.

La diagnosi sui nomi item contenenti `Luden` ha restituito:

```text
["Luden's Echo", "Luden's Echo"]
```

### Impatto

La funzione `fetch_items()` puo essere implementata correttamente contro Data Dragon, ma T08 non puo essere chiusa rispettando alla lettera il DoD senza inventare o rinominare un item non presente nella patch corrente.

### Mitigazione proposta

- Non alterare i dati Data Dragon.
- Non sostituire artificialmente `Luden's Echo` con `Luden's Companion`.
- Fermare la chiusura di T08 e chiedere conferma su una mini-errata operativa del DoD: sostituire il controllo di esempio `Luden's Companion` con un item realmente presente nella patch corrente, ad esempio `Luden's Echo`, mantenendo invariati scopo e formato della task.

### Risoluzione

L'utente ha approvato il passaggio del controllo DoD da `Luden's Companion` a `Luden's Echo`. Aggiunta `ERRATA-005` in `SPEC_ERRATA.md`. T08 verificato con Data Dragon patch `16.10.1`: 705 item, `Liandry's Torment` presente, `Luden's Echo` presente, `Tormento di Liandry` assente.
