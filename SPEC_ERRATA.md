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
- Stato: confermato
- Sintesi: la configurazione default del MVP parte da Strategia A free-only via OpenRouter. Strategia B resta piano di emergenza attivabile via `.env` solo dopo rate limit cronico documentato.

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
