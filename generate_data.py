"""
generate_data.py
Generates a reproducible synthetic football (soccer) player dataset.
NOTE: All data is entirely synthetic and does not represent real-world results.
Run: python generate_data.py  ->  writes football_players.csv
"""

import numpy as np
import pandas as pd

np.random.seed(42)

# ── Reference pools ────────────────────────────────────────────────────────────
FIRST_NAMES = [
    "Luca", "Marco", "Diego", "Carlos", "James", "Kevin", "Raheem",
    "Pierre", "Antoine", "Gabriel", "Bruno", "Toni", "Kai", "Mason",
    "Bukayo", "Erling", "Vinicius", "Pedri", "Gavi", "Jamal",
    "Federico", "Alessandro", "Roberto", "Sergio", "Ivan", "Nikola",
    "Patrick", "Leroy", "Sadio", "Riyad", "Ilkay", "Phil", "Jack",
    "Declan", "Jordan", "Marcus", "Rasmus", "Cody", "Viktor", "Ollie",
]
LAST_NAMES = [
    "Rossi", "Hernandez", "Mueller", "Salah", "Mane", "Silva", "Pereira",
    "Garcia", "Martinez", "Diaz", "Fernandez", "Santos", "Lopez", "Gomez",
    "Rodrigues", "Costa", "Moreno", "Torres", "Jimenez", "Alvarez",
    "Andersen", "Eriksen", "Nielsen", "Hansen", "Jensen", "Pedersen",
    "Schmidt", "Becker", "Wagner", "Richter", "Koch", "Klein",
    "Dubois", "Bernard", "Leroy", "Moreau", "Simon", "Laurent",
]
TEAMS = [
    "Atletico United", "City Blues", "Riverside FC", "Northern Star",
    "Capital Rovers", "Eastside FC", "Golden Eagles", "Silver Wolves",
    "Harbor City", "Redstone Athletic",
]
NATIONALITIES = [
    "Brazil", "France", "Germany", "Spain", "England",
    "Argentina", "Portugal", "Italy", "Netherlands", "Belgium",
]
POSITIONS = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
SEASONS = ["2021-22", "2022-23", "2023-24"]

# Position-based stat ranges  (min, max)
STAT_RANGES = {
    #                goals  assists  shots  sot    minutes   pass_acc  rating
    "Goalkeeper":  ((0,1), (0,2),  (0,3), (0,1), (1200,3420), (55,80), (6.0,8.5)),
    "Defender":    ((0,5), (0,7),  (0,20),(0,8), (900,3420),  (65,88), (6.0,8.5)),
    "Midfielder":  ((1,12),(2,15), (10,60),(4,28),(900,3420), (72,93), (6.2,9.0)),
    "Forward":     ((5,30),(2,15), (30,120),(12,55),(900,3240),(60,85),(6.5,9.5)),
}

# ── Build player roster ────────────────────────────────────────────────────────
NUM_PLAYERS = 80          # unique players; with 3 seasons -> 180+ rows total
player_names = []
seen = set()
while len(player_names) < NUM_PLAYERS:
    name = f"{np.random.choice(FIRST_NAMES)} {np.random.choice(LAST_NAMES)}"
    if name not in seen:
        seen.add(name)
        player_names.append(name)

player_teams       = np.random.choice(TEAMS, size=NUM_PLAYERS)
player_positions   = np.random.choice(POSITIONS, size=NUM_PLAYERS,
                                       p=[0.10, 0.30, 0.35, 0.25])
player_ages        = np.random.randint(17, 39, size=NUM_PLAYERS)
player_nationals   = np.random.choice(NATIONALITIES, size=NUM_PLAYERS)

# ── Generate season rows ───────────────────────────────────────────────────────
rows = []
player_id_counter = 1

for pid in range(NUM_PLAYERS):
    name      = player_names[pid]
    team      = player_teams[pid]
    pos       = player_positions[pid]
    age_base  = player_ages[pid]
    nat       = player_nationals[pid]
    ranges    = STAT_RANGES[pos]

    # Each player appears in 1, 2 or 3 seasons (random)
    num_seasons = np.random.choice([1, 2, 3], p=[0.2, 0.3, 0.5])
    chosen_seasons = np.random.choice(SEASONS, size=num_seasons, replace=False)

    for season_idx, season in enumerate(sorted(chosen_seasons)):
        age = age_base + season_idx

        goals          = int(np.random.randint(*ranges[0]))
        assists        = int(np.random.randint(*ranges[1]))
        shots          = int(np.random.randint(*ranges[2]))
        shots_on_tgt   = int(min(shots, np.random.randint(max(0, ranges[3][0]), max(1, ranges[3][1]))))
        minutes_played = int(np.random.randint(*ranges[4]))
        pass_accuracy  = round(float(np.random.uniform(*ranges[5])), 1)
        rating         = round(float(np.random.uniform(*ranges[6])), 2)
        yellow_cards   = int(np.random.randint(0, 10))
        red_cards      = int(np.random.randint(0, 3))
        appearances    = int(minutes_played // np.random.randint(50, 91))
        clean_sheets   = (int(np.random.randint(0, 18))
                          if pos in ("Goalkeeper", "Defender") else 0)

        rows.append({
            "player_id":       player_id_counter,
            "player_name":     name,
            "age":             age,
            "nationality":     nat,
            "team":            team,
            "position":        pos,
            "season":          season,
            "appearances":     appearances,
            "goals":           goals,
            "assists":         assists,
            "shots":           shots,
            "shots_on_target": shots_on_tgt,
            "minutes_played":  minutes_played,
            "pass_accuracy":   pass_accuracy,
            "rating":          rating,
            "yellow_cards":    yellow_cards,
            "red_cards":       red_cards,
            "clean_sheets":    clean_sheets,
        })
        player_id_counter += 1

df = pd.DataFrame(rows)
df.to_csv("football_players.csv", index=False)
print(f"Generated football_players.csv  — {len(df)} rows, {df['player_name'].nunique()} unique players.")
