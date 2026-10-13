# ⚽ Football Player Performance Analytics Dashboard

> **Synthetic Data Notice:** All statistics in this dashboard are entirely synthetic and generated for
> demonstration purposes. They do not represent real-world football results, clubs, or players.

A portfolio-quality interactive football analytics dashboard built with Python and Streamlit,
featuring player comparison, team-level aggregation, position breakdown, and downloadable filtered data.

---

## Features

| Page | What you get |
|---|---|
| **Overview** | 5 KPI cards (players, goals, assists, minutes, rating) + top-10 charts |
| **Player Analysis** | Radar comparison, Goals vs Assists scatter, Shots vs Goals scatter with trendline |
| **Team Analysis** | Grouped goals/assists bar, squad composition stacked bar, team summary table |
| **Position Analysis** | Rating box plot, avg goals bar, GK/DEF/MID/FWD sub-sections |
| **All pages** | Sidebar filters (season, team, position, player search) + CSV download |

---

## Project Structure

```
football analysis/
├── app.py                    # Main Streamlit application (530 lines)
├── generate_data.py          # Reproducible synthetic dataset generator
├── football_players.csv      # Generated dataset (185 rows, 80 players, 3 seasons)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .streamlit/
    └── config.toml           # Dark green pitch theme
```

---

## Quick Start (Local)

### 1. Prerequisites

- Python 3.9 or newer
- pip

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate the dataset (only needed once)

```bash
python generate_data.py
```

This writes `football_players.csv` to the project root.

### 5. Run the dashboard

```bash
streamlit run app.py
```

Streamlit will open the dashboard automatically at `http://localhost:8501`.

---

## Deploy to Streamlit Community Cloud

1. Push the repository to GitHub (include `app.py`, `football_players.csv`, `requirements.txt`, and `.streamlit/config.toml`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select your repository and branch, set **Main file path** to `app.py`.
4. Click **Deploy** — the app will be live within a minute.

> The CSV is committed to the repo, so `generate_data.py` does **not** need to run on the cloud.

---

## Dataset Schema

| Column | Type | Description |
|---|---|---|
| player_id | int | Unique row identifier |
| player_name | str | Synthetic full name |
| age | int | Player age (17–38) |
| nationality | str | Synthetic nationality |
| team | str | Synthetic club (10 clubs) |
| position | str | Goalkeeper / Defender / Midfielder / Forward |
| season | str | 2021-22 / 2022-23 / 2023-24 |
| appearances | int | Matches played |
| goals | int | Goals scored (position-realistic) |
| assists | int | Goal assists |
| shots | int | Total shots |
| shots_on_target | int | On-target shots |
| minutes_played | int | Total minutes |
| pass_accuracy | float | Pass accuracy % |
| rating | float | Match rating (5.0–9.5) |
| yellow_cards | int | Yellow cards |
| red_cards | int | Red cards |
| clean_sheets | int | Clean sheets (GK/DEF only) |

---

## KPI Calculations

All KPIs are recalculated dynamically from the filtered dataframe — nothing is hardcoded.

| KPI | Formula |
|---|---|
| Total Players | `df['player_name'].nunique()` |
| Total Goals | `df['goals'].sum()` |
| Total Assists | `df['assists'].sum()` |
| Total Minutes Played | `df['minutes_played'].sum()` |
| Average Player Rating | `df['rating'].mean()` |

---

## Technology Stack

- **Python 3.9+**
- **Streamlit ≥ 1.32** — UI framework
- **Pandas ≥ 2.0** — data manipulation
- **NumPy ≥ 1.26** — numeric operations and trendline
- **Plotly ≥ 5.20** — interactive charts

---

## Regenerating the Dataset

To regenerate with different parameters, edit `generate_data.py` (e.g. change `NUM_PLAYERS` or stat ranges) and re-run:

```bash
python generate_data.py
```

The seed `numpy.random.seed(42)` ensures identical output each time with the same parameters.

---

*Built as a portfolio demonstration project. All data is synthetic.*
