# Mock draft scenarios (M4/T34)

I file `.json` in questa cartella sono **scenari PLUMBING**, non i dati reali del
benchmark del 09/05/2026.

## Stato (OPEN-002)

I dati reali del benchmark (`test_scenarios.md` del corso) NON sono nel
repository. Questi 5 JSON sono strutturalmente validi (`DraftState` schema),
usano champion reali Data Dragon e sono coerenti col nome dello scenario, ma i
pick/ban specifici **non** sono quelli testati il 09/05/2026.

Quando i dati reali saranno disponibili (l'utente li porta da casa):

1. Sostituire il contenuto di ciascun file mantenendo **stesso path e nome**.
2. Lo schema resta identico (`DraftState`), cambia solo il contenuto.
3. Il codice (`FileProvider`, test) non va modificato.
4. Rilanciare `pytest tests/test_file_provider.py` per ri-verificare.

Riferimento: `OPEN-002` nel breakdown status, `PROMPT_LOG.md`.

## Scenari

| File | Ruolo utente | Situazione |
|---|---|---|
| `balanced_mid.json` | MID | enemy comp bilanciata |
| `ad_heavy_top.json` | TOP | enemy AD-heavy |
| `mid_meta_banned.json` | MID | meta mid bannati |
| `first_pick_top.json` | TOP | first pick, nessun pick fatto |
| `last_pick_support.json` | SUPPORT | last pick, enemy 5/5 + ally 4/5 |
