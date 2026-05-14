Patch corrente: {patch}

Mio ruolo: {user_role}

Ban (5):
{bans_list}

Enemy team:
{enemy_picks_with_roles}

Ally team (in ordine di pick già fatti):
{ally_picks_with_roles}

Suggerisci i Top 3 campioni per il mio ruolo con build essenziale (3-4 oggetti core),
keystone rune e una breve spiegazione (max 1-2 frasi in italiano, ≤150 caratteri) del
perché ognuno è una buona scelta in questo specifico draft.

Rispondi nel seguente formato JSON:

{
  "patch": "string",
  "suggestions": [
    {
      "rank": 1,
      "champion": "string (nome esatto del campione in inglese)",
      "build_path": ["item1", "item2", "item3"],
      "keystone": "string (es. 'Conqueror', 'Arcane Comet')",
      "explanation": "string (max 150 caratteri in italiano)"
    },
    {"rank": 2, ...},
    {"rank": 3, ...}
  ]
}
