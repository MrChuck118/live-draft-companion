# Live Draft Companion - SPEC_ERRATA.md

Documento complementare a `LiveDraftCompanion_TechnicalSpec_v2.3.md`.

La spec v2.3 resta FROZEN. Questo file registra aggiornamenti di stato e correzioni operative non strutturali emerse durante la build.

## ERRATA-001 - Repository GitHub operativo

- Data: 2026-05-11
- Stato: confermato
- Sintesi: il repository `https://github.com/MrChuck118/live-draft-companion` e operativo, pubblico, su branch `main`, con README placeholder, LICENSE MIT e `.gitignore` Python.

## ERRATA-002 - Frontend stack chiuso su Vanilla JS + fetch

- Data: 2026-05-11
- Stato: confermato
- Sintesi: il frontend MVP usa HTML, Tailwind CDN e Vanilla JS + fetch. HTMX resta fuori dal MVP.

## ERRATA-003 - Strategia AI default chiusa su Strategia A free-only

- Data: 2026-05-11
- Stato: superato da ERRATA-006 (2026-05-15)
- Sintesi: la configurazione default del MVP parte da Strategia A free-only via OpenRouter. Strategia B resta piano di emergenza attivabile via `.env` solo dopo rate limit cronico documentato.
- Nota 2026-05-15: superato da ERRATA-006. Il provider AI non e piu OpenRouter (ne Strategia A ne B) ma DeepSeek API diretta. Questa errata resta come registro storico della decisione originale.

## ERRATA-004 - Aggiornamento pin `psutil` per Python 3.12.10

- Data: 2026-05-11
- Sezione spec interessata: 7.3, 13.2
- Tipo: correzione operativa di dipendenza
- Stato: applicato in `requirements.txt`

### Problema

La spec v2.3 indicava `psutil<5.7.0` per ridurre il rischio di `AccessDenied` su Windows durante process discovery LCU. Durante T03b, su Python 3.12.10, `pip install -r requirements.txt` ha tentato di compilare `psutil-5.6.7` da sorgente e ha fallito per assenza di Microsoft C++ Build Tools.

### Aggiornamento

Il vincolo operativo viene aggiornato a:

```text
psutil>=5.9.8,<8
```

### Motivazione

Le versioni moderne di `psutil` hanno wheel Windows per Python 3.12, rendendo l'ambiente replicabile senza installare una toolchain C++ esterna. Il rischio `AccessDenied` andra gestito nel codice LCU con eccezioni controllate e fallback al lockfile, non bloccando l'installazione.

### Impatto

Nessun cambiamento strutturale a MVP, RF, architettura o flusso dati. Cambia solo il vincolo di dipendenza per rendere T03 completabile su Python 3.12.10.

## ERRATA-005 - Correzione DoD T08 item Data Dragon

- Data: 2026-05-13
- Sezione interessata: breakdown operativo v2.1, M1/T08
- Tipo: correzione operativa di criterio di test
- Stato: applicato nella verifica T08

### Problema

Il DoD T08 del breakdown cita `Luden's Companion` come item da verificare in Data Dragon. Sulla patch corrente `16.10.1`, Data Dragon `item.json` non contiene `Luden's Companion`, ma contiene `Luden's Echo`.

### Aggiornamento

Per T08, il controllo di esempio viene aggiornato da:

```text
Luden's Companion
```

a:

```text
Luden's Echo
```

### Motivazione

Il task T08 deve verificare che `fetch_items()` restituisca item reali dalla patch corrente con nomi inglesi Data Dragon. Non bisogna inventare o rinominare item non presenti nel dataset reale.

### Impatto

Nessun cambiamento a MVP, RF, architettura o codice applicativo. Cambia solo l'esempio usato nel DoD per allineare il test ai dati reali di Data Dragon.

## ERRATA-006 - Provider AI cambiato da OpenRouter a DeepSeek API diretta

- Data: 2026-05-15
- Sezione spec interessata: 7.2, 7.4, 9.4 (provider e chain modelli AI)
- Tipo: cambio operativo di provider AI runtime
- Stato: applicato in `app/ai_client.py` e `.env.example`
- Supera: ERRATA-003 (Strategia A/B OpenRouter). Rende non necessaria la prevista errata di correzione del model ID Mistral (INC-008 sub-issue).

### Problema

La chain Strategia A free-only via OpenRouter (ERRATA-003) si e rivelata non utilizzabile per le DoD runtime: 3/4 modelli rate-limited upstream e 1/4 con model ID inesistente (INC-008). Lo switch a Strategia B richiedeva un top-up su OpenRouter. L'utente ha invece gia acquistato credito ($5) direttamente su `platform.deepseek.com` e ha scelto di andare diretto su DeepSeek anziche passare per OpenRouter.

### Aggiornamento

Il provider AI runtime passa da:

```text
OpenRouter (base_url https://openrouter.ai/api/v1, OPENROUTER_API_KEY,
chain Strategia A free + Strategia B fallback)
```

a:

```text
DeepSeek API diretta (base_url https://api.deepseek.com, DEEPSEEK_API_KEY,
LLM_MODEL_PRIMARY=deepseek-chat, LLM_MODEL_FALLBACK_1=deepseek-reasoner)
```

Modifiche applicate: `app/ai_client.py` (base URL, env var della key, rimozione header OpenRouter-specifici) e `.env.example` (variabile key e chain modelli). Dettaglio in `PROMPT_LOG.md` PLOG-2026-05-15-030.

### Motivazione

DeepSeek espone un'API OpenAI-compatible: il client SDK esistente funziona cambiando solo `base_url` e nome variabile della key, senza riscrivere la logica di chain/retry/validazione. Usare il credito gia pagato su DeepSeek evita un secondo top-up su OpenRouter e rimuove la dipendenza dai free tier rate-limited. Non esiste un model ID "deepseek-v4-flash" sull'API diretta (era un alias OpenRouter): il modello "flash" richiesto e mappato su `deepseek-chat` (DeepSeek-V3).

### Impatto

Nessun cambiamento strutturale a MVP, RF, architettura, flusso dati o logica di fallback/validazione: cambiano solo endpoint, credenziale e ID modelli. Le DoD runtime AI reali (T27/T31/T35/T58/T62) vanno rieseguite contro DeepSeek dopo che l'utente configura `.env` con `DEEPSEEK_API_KEY`. Il vincolo JSON mode (`response_format=json_object`) e supportato da DeepSeek ma richiede la parola "json" nel prompt: da confermare al primo smoke test reale.

## ERRATA-007 - Persistenza locale su singolo file SQLite invece di tre file separati

- Data: 2026-05-16
- Sezione spec interessata: 8.3 (tabella "Dati salvati"), 5.3 (riferimento `history.db`), 8.1 (Cache Layer / History Layer)
- Tipo: scelta operativa di persistenza non strutturale
- Stato: applicato in `app/db.py` (T10 per Data Dragon; formalizzato a T50 per cache+history)
- Tracciabilita: INC-011

### Problema

La spec v2.3 §8.3 e §5.3 descrivono tre file SQLite separati:

```text
datadragon.db   (champions, items, runes, meta)
cache.db        (cache output AI, chiave hash draft state)
history.db      (storico consigli + feedback + model_used)
```

L'implementazione adotta invece un **singolo file SQLite** `data_dragon.db` con un unico engine SQLAlchemy e tutte le tabelle (`champions`, `items`, `runes`, `meta`, e da T50 `cache`, `history`). La scelta era gia implicita nel breakdown operativo v2.1 (T10 fissa "Database file: `data_dragon.db`"; T50 chiede di "**aggiungere** le tabelle a `db.py`", stesso engine), ma a T10 la divergenza non era ancora materiale perche esistevano solo le tabelle Data Dragon. Diventa concreta a T50 con l'aggiunta di `cache` e `history`: questo e il momento corretto per documentarla.

### Aggiornamento

La tabella §8.3 va letta come segue per l'implementazione:

```text
File unico: data_dragon.db (un solo engine SQLAlchemy async + aiosqlite)
  - tabelle champions / items / runes / meta   (cache statica Data Dragon)
  - tabella cache                              (output AI per hash draft state, TTL)
  - tabella history                            (storico consigli + feedback + model_used)
```

I nomi logici `cache.db` / `history.db` della spec si intendono come le **tabelle** `cache` / `history` dentro l'unico file.

### Motivazione

SQLite gestisce nativamente piu tabelle in un unico file: e funzionalmente equivalente a tre file (stessa durabilita, integrita e query) ed e piu robusto e semplice di tre engine separati (in SQLite non esistono JOIN cross-database senza `ATTACH`, e tre connessioni aumentano la complessita di lifecycle). Nessun RF, MVP, validatore o criterio di accettazione dipende dalla partizione in file: la §8.3 e una tabella descrittiva, non un requisito. La scelta e inoltre coerente con il breakdown operativo v2.1 (T10/T50), che e l'autorita implementativa.

### Impatto

Nessun cambiamento strutturale a MVP, RF, architettura logica, flusso dati o validatori. Cambia solo il numero di file fisici di persistenza (uno invece di tre), trasparente all'utente e ai consumatori delle tabelle. Lo split in tre file resta possibile in futuro senza impatto sul dominio se mai dovesse servire (non previsto). `.gitignore` gia esclude `*.db`.
