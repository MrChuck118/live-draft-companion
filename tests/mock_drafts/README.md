# Mock draft scenarios (M4/T34, M8/T57)

I file `.json` in questa cartella sono **scenari PLUMBING**, non i dati reali del
benchmark del 09/05/2026.

## Stato (OPEN-002)

I dati reali del benchmark (`test_scenarios.md` del corso) NON sono nel
repository. Questi 15 JSON sono strutturalmente validi (`DraftState` schema),
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
| `split_damage_top.json` | TOP | enemy split-damage / mixed threats |
| `ap_heavy_jungle.json` | JUNGLE | enemy AP-heavy |
| `balanced_jungle.json` | JUNGLE | enemy comp bilanciata |
| `early_pick_jungle.json` | JUNGLE | pick iniziale con poche info |
| `ap_heavy_adc.json` | ADC | enemy AP-heavy con botlane mage |
| `balanced_adc.json` | ADC | enemy comp bilanciata |
| `aggressive_bans_adc.json` | ADC | ban list aggressiva su marksman |
| `ap_heavy_support.json` | SUPPORT | enemy AP-heavy / poke |
| `balanced_support.json` | SUPPORT | enemy comp bilanciata |
| `meta_picks_out_mid.json` | MID | meta pick mid bannati o gia occupati |
