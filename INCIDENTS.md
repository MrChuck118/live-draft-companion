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

## INC-007 - API key OpenRouter esposta in chat durante setup T26

- Data rilevazione: 2026-05-14
- Fase: M3 / T26
- Severita: media (rischio esposizione credenziali)
- Stato: mitigato in repo, raccomandazione rotazione comunicata all'utente
- Nota 2026-05-15: dopo ERRATA-006 il codice non usa piu `OPENROUTER_API_KEY` (provider = DeepSeek diretto). La raccomandazione di REVOCARE la key OpenRouter esposta (`...e26d34`) resta comunque valida e pendente: una key esposta va revocata anche se non piu usata dal progetto.

### Descrizione

Durante il setup di `.env` per la DoD T26 (chiamata reale a OpenRouter per smoke test "Dimmi solo OK"), l'utente ha condiviso la propria `OPENROUTER_API_KEY` come messaggio diretto in chat invece di configurare il file `.env` localmente come suggerito.

Il flusso atteso era:

1. Utente copia `.env.example` in `.env` localmente.
2. Utente edita `.env` con la propria key.
3. Utente conferma "fatto" senza esporre la key.

Il flusso effettivo:

1. Utente ha pubblicato la key in chat.
2. Codex ha emesso AVVISO SICUREZZA raccomandando di non condividere la key in canali loggabili.
3. Codex ha proceduto a creare `.env` con la key ricevuta, mantenendo la key OUT del repository.

### Impatto

- Nessuna esposizione della key in file versionati del repo: `.env` e gitignored (`.gitignore:157`), verificato con `git check-ignore -v .env` e `git status --short`.
- Nessuna scrittura della key in `PROMPT_LOG.md`, `INCIDENTS.md`, `README.md`, `SPEC_ERRATA.md` o qualsiasi altro file versionato.
- Negli stampi di verifica usato solo prefix `sk-or-v1-b...` e lunghezza, mai il valore completo.
- Tuttavia: la chat tra utente e Codex potrebbe essere loggata/cacheata lato sistema. La key e quindi potenzialmente esposta al di fuori del controllo dell'utente.

### Mitigazione

- AVVISO SICUREZZA emesso in chat con raccomandazione di:
  - revocare la key esposta da https://openrouter.ai/keys (key che termina in `...e26d34`).
  - generare una nuova key.
  - aggiornare `.env` locale con la nuova key.
- Per le iterazioni future: NON condividere mai credenziali in chat, configurare i file `.env` direttamente in locale.
- Documentazione futura su `README.md` di buona pratica: spiegare che le key vanno scritte solo in `.env` locale, mai in chat o in file versionati.

## INC-008 - Chain Strategia A interamente non disponibile durante DoD T27 (429 upstream + 404 model ID)

- Data rilevazione: 2026-05-14
- Fase: M3 / T27 (DoD smoke test JSON mode)
- Severita: media (blocca DoD runtime, non l'implementazione)
- Stato: risolto 2026-05-15 - switch a DeepSeek diretto (ERRATA-006)

### Descrizione

Durante la verifica DoD T27 (smoke test JSON mode contro modello primario Strategia A), 3/4 modelli della chain configurata in `.env` sono risultati rate-limited upstream e 1/4 ha restituito 404 per model ID inesistente:

| Model | Esito | Latency | Provider | Note |
|---|---|---|---|---|
| google/gemma-4-31b-it:free | 429 (2 tentativi a 60s di distanza) | 3897 ms / 3435 ms | Google AI Studio | Rate limit upstream |
| meta-llama/llama-3.3-70b-instruct:free | 429 | 59933 ms (timeout 60s) | Meta | Rate limit upstream |
| mistralai/mistral-small-24b-instruct-2501:free | 404 NotFoundError | 246 ms | (n/a) | Model ID inesistente su OpenRouter |
| qwen/qwen3-next-80b-a3b-instruct:free | 429 | 59360 ms (timeout 60s) | Venice | Rate limit upstream |

Tutti i tentativi sono stati fatti dopo il successo di T26 (`ping_primary_model` con Gemma 4 free che ha restituito 'OK' in 2459 ms). Quindi tra T26 (success) e T27 (429) il rate limit Gemma 4 free e stato esaurito; e le altre opzioni della chain sono anch'esse rate-limited o non valide.

### Impatto

- DoD T27 chiamata reale BLOCCATA al momento della verifica.
- Implementazione `call_model()` corretta e compilata, non rotta dall'incidente.
- Scenario anticipato dalla spec §7.2 "rate limit upstream sui free tier non e prevedibile. La chain di 4 fallback mitiga ma non elimina il rischio. Mitigazione critica: modalita simulazione (MVP-015) sempre disponibile come piano C per la demo".
- Soglia di switch a Strategia B (`SPEC_ERRATA.md` ERRATA-003): "rate limit upstream sui free tier registrato in `INCIDENTS.md` in >=3 sessioni di sviluppo consecutive". Al momento questa e 1 sessione: NON ancora soglia di switch.

### Mitigazione - opzioni proposte all'utente

1. Attendere 10-30 minuti e ritentare la DoD su Gemma 4 free (i rate limit Google AI Studio free tier sono spesso per finestra di tempo).
2. Accettare T27 DoD come "code-only" (codice corretto, runtime rinviato a iterazione futura quando la chain torna disponibile o quando si esegue T28 fallback chain).
3. Saltare la DoD runtime di T27 e procedere a T28 (fallback chain), che esiste specificamente per gestire questo scenario di 429 cronico e che usera la stessa funzione `call_model`.
4. Switch a Strategia B (richiede top-up OpenRouter ~$10 da utente per sbloccare modelli paid + alzare rate limit free a 1000/giorno).

### Sub-issue: Mistral model ID inesistente

Indipendentemente dal rate limit, il model ID `mistralai/mistral-small-24b-instruct-2501:free` configurato in `.env.example` e `.env` non esiste su OpenRouter al momento della verifica (404). Mistral Small 3 e citato nella spec §7.2 e nel breakdown come fallback Strategia A, ma con un ID che oggi non risolve.

Per correggere serve:

- Identificare il model ID corretto di Mistral Small free su OpenRouter al momento (probabili candidati: `mistralai/mistral-small-3.1-24b-instruct:free`, `mistralai/mistral-small-3.2-24b-instruct:free`, da validare con OpenRouter API listing).
- Aggiungere ERRATA-006 in `SPEC_ERRATA.md` con la correzione del model ID.
- Aggiornare `.env.example` e `.env` con il nuovo ID corretto.

Questa correzione e subordinata ad approvazione utente: non si tocca `.env.example` (committato) senza decisione esplicita.

### Risoluzione

- Data: 2026-05-15
- L'utente ha acquistato credito ($5) direttamente su `platform.deepseek.com` e ha scelto di abbandonare OpenRouter (sia Strategia A free sia Strategia B paid) per andare diretto su DeepSeek API.
- Applicata ERRATA-006: `app/ai_client.py` e `.env.example` ora puntano a `https://api.deepseek.com` con `DEEPSEEK_API_KEY` e chain `deepseek-chat` / `deepseek-reasoner`.
- Effetti su questo incidente:
  - La chain OpenRouter rate-limited non e piu nel percorso runtime: la causa radice (free tier 429 + scelta tra attesa/top-up) decade.
  - La sub-issue del model ID Mistral inesistente diventa nulla: i modelli OpenRouter sono stati rimossi da `.env.example`. La prevista ERRATA-006 di correzione model ID NON serve piu (il numero ERRATA-006 e stato usato per lo switch DeepSeek).
- Residuo aperto: le DoD runtime reali (T27/T31/T35/T58/T62) restano da eseguire, ma ora contro DeepSeek, dopo che l'utente crea `.env` locale con `DEEPSEEK_API_KEY`. Non e piu un blocco da rate limit ma una semplice azione di configurazione utente.
- Dettaglio decisione in `PROMPT_LOG.md` PLOG-2026-05-15-030.

## INC-009 - Suite test non verde su macchina pulita: cache Data Dragon non popolata

- Data rilevazione: 2026-05-16
- Fase: ripresa progetto su PC casa / Fase 0 bootstrap ambiente
- Severita: bassa (prerequisito ambiente, nessuna regressione di codice)
- Stato: risolto + mitigazione documentale

### Descrizione

Su PC di casa (macchina diversa da "pc its", senza `.venv` ne cache locali), dopo bootstrap ambiente (`venv` + `pip install -r requirements.txt`, `pip check` OK) la suite ha dato 39 pass / 12 fail invece della baseline 51/51 documentata.

I 12 fallimenti erano esclusivamente i validator di legality (`test_champion_legality`, `test_items_legality`, `test_keystone_legality`, 4 test ciascuno). Errore reale: `sqlite3.OperationalError: no such table: champions`. `data_dragon.db` presente ma 0 byte e gitignored (non viene dal repo): la cache Data Dragon non era mai stata popolata su questo PC.

Non e una regressione: i validator T16-T18 leggono champion/item/keystone da `data_dragon.db`. La baseline 51/51 su "pc its" era valida perche T11/T12 vi erano gia stati eseguiti.

### Impatto

Su qualsiasi macchina pulita (incluso potenzialmente il PC Academy) la suite fallisce in modo identico finche la cache Data Dragon non viene popolata. Il README "Setup Previsto" e lo spec 13.2 non elencavano questo passo come prerequisito ai test.

### Mitigazione

- Rimosso `data_dragon.db` 0-byte; eseguito `populate_cache()` (scarica da Data Dragon CDN, `init_db()` incluso): patch 16.10.1.
- Verifica `scripts/test_data_dragon.py` (T12): exit 0, 172 champions, 705 items, 17 keystones, accent/tags/no-roles check OK.
- `pytest tests/`: 51/51 PASSED ripristinato.
- README "Setup Previsto" aggiornato con il passo di popolamento cache Data Dragon come prerequisito ai test. Proposta di nota analoga in spec 13.2 lasciata a decisione utente (modifica strutturale -> eventuale SPEC_ERRATA, non applicata qui).

## INC-010 - Schema actions LCU ridotto in custom-vs-bot: confermato persistente (T40)

- Data rilevazione: 2026-05-16
- Fase: M5 / T40 (test live LCU su PC casa)
- Severita: bassa (limite ambiente di test previsto da spec 14.2, nessun bug di codice)
- Stato: APERTO - in sospeso verifica con draft reale (umani/tournament). Mitigazione gia attiva.

### Descrizione

Verifica live T40 su PC di casa (LoL in `E:\Riot Games\League of Legends`, client aperto, custom con bot in champion select). Catena M5 validata end-to-end:

- `find_lockfile()` ha risolto il path reale NON standard `E:\Riot Games\League of Legends\lockfile` via `psutil` (ramo mai testabile su pc its): OK.
- `lcu_request("GET", "/lol-gameflow/v1/session")`: HTTP 200, phase `ChampSelect`: OK.
- `GameflowMonitor.poll_once()`: `ChampSelect`: OK.
- `LCUProvider.get_current_state()`: `DraftState` valido, `user_role=ADC`, patch `16.10.1` da cache, mapping championId->nome corretto (Caitlyn, Anivia, Darius, Swain, Akali, Mordekaiser, Renata Glasc, Miss Fortune, Udyr), nessun token summoner nel dump (privacy 10.1 OK), nessun crash su schema ridotto.

Tuttavia il DoD numerico di T40 (`>=5 bans`, `>=10 actions`) NON e soddisfatto: `bans=0`, `actions=3` (`ban` non completato del giocatore locale, `ten_bans_reveal`, `pick` non completato), `enemy_team` con ruoli vuoti. Identico al gating del 09/05/2026 (3 actions).

### Impatto

Conferma il rischio gia previsto nella spec 14.2 ("Schema actions LCU diverso in ranked vs custom", probabilita Media) e in INC-001. Il custom-vs-bot espone solo le azioni del giocatore locale, non le 15+ di un draft completo. Il criterio numerico `>=10 actions / >=5 bans` e raggiungibile solo in un draft reale (ranked o tournament con umani), non in custom-vs-bot. Non e un difetto del codice: `LCUProvider`/`parse_champ_select_session` parsano correttamente e in modo difensivo quanto LCU espone.

### Mitigazione

- Mitigazione gia prevista dalla spec e GIA IMPLEMENTATA E VERDE: modalita simulazione (`FileProvider`, MVP-015) 5/5 VALID su DeepSeek (PLOG-2026-05-16-036). La demo Academy non dipende dal draft live.
- Codice M5 (T36-T39) validato live per tutta la parte non legata al numero di azioni: lockfile/psutil, auth, gameflow, champ-select parsing, mapping, privacy.

### Residuo (in sospeso)

- Verifica DoD numerico T40 (`>=5 bans`, `>=10 actions`) rinviata a un draft reale con ban effettivi (umani o tournament draft completo). Da rieseguire `scripts/lcu_live_check.py` in quella sessione.
- Nessuna modifica strutturale di spec: 14.2 documenta gia il rischio; questa e la sua conferma empirica, non una variazione di perimetro. Nessun ERRATA necessario.
