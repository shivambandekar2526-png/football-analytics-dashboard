# ⚽ Football Analytics Pro — Tactical & Performance Intelligence Platform

> **Synthetic Data Notice:** All statistics and metrics in this platform are entirely synthetic and generated for demonstration purposes. They do not represent real-world football results, clubs, or players.

A portfolio-grade, professional interactive football analytics platform built with Python, Streamlit, and Plotly. Redesigned from scratch with an ultra-modern dark glassmorphism aesthetic, tactical pitch board, EA FC style player scouting dossiers, head-to-head combat duels, advanced per-90 metrics, and club power rankings.

---

## 🌟 Key Features & Views

| View / Module | Capabilities & Highlights |
|---|---|
| **🏠 Overview & Pulse** | 6 high-impact KPI cards (Players, Goals, Assists, Goal Contrib, Minutes, Rating) · Top-10 Scorers (position colored) · Top-10 Highest Rated · Top-10 Playmakers (Assists) · Season-over-season output trajectory line chart · Interactive player table. |
| **⚽ Tactical Pitch & Best XI** | **[NEW]** Regulation football pitch visualization with authentic markings · Custom tactical formation switch (4-3-3 Attack, 4-4-2 Classic, 4-2-3-1 Modern, 3-5-2 Fluid) · Algorithmic Best XI Dream Team selector · Glowing player badges, ratings, and on-pitch hover telemetry · Squad statistics & Starting XI roster. |
| **🌟 Scouting Dossier** | **[NEW]** EA Sports FC / FIFA Ultimate Team inspired player scouting cards · 6 core FIFA attributes (Shooting, Passing, Playmaking, Stamina, Defending, Rating) · Dynamic radar comparison against positional cohort benchmarks · Career form trajectory across seasons. |
| **🔍 Player Comparison & Duel** | **[NEW] 1v1 Combat Duel Arena** with dual-track progress bars and automatic category winner detection · Multi-player normalized radar comparison (2–5 players) · Goals vs Assists scatter · Shots vs Goals with efficiency regression trendline · **[NEW] Finishing Efficiency Quadrant Matrix** (Volume vs Conversion) · Pass accuracy vs Rating scatter. |
| **🏟️ Team Analytics & Standings** | Club KPI cards · Grouped goals & assists bar chart · Squad composition stacked bar · Club average rating leaderboard · **[NEW] Attacking vs Defending Dominance Matrix** (Goals vs Clean Sheets) · **[NEW] Fair Play & Disciplinary Leaderboard** · Comprehensive club standings table. |
| **📐 Positional Deep-Dive** | Position KPI cards (GK, DEF, MID, FWD) · Rating distribution box plot with jitter · Avg goals & avg assists comparison · **[NEW] Positional attribute benchmark radar** · 4 specialized spotlight cards (GK Clean Sheets, DEF Pass Accuracy, MID Assists, FWD Conversion %). |
| **⚡ Global Controls & Filters** | Metric mode switch (Raw Totals vs Per 90 Minutes) · Quick preset filters (Wonderkids, Prime Stars, Veterans, Elite Tier, Goal Machines) · Season, Club, Position multiselects · Age range slider · Min minutes slider · Player name search · Dual export hub (CSV & JSON). |

---

## 🏗️ Project Architecture

```
football analysis/
├── app.py                      # Main Streamlit application and view router
├── modules/
│   ├── ui_theme.py             # Design system, CSS styling, constants, Plotly polish
│   ├── pitch_board.py          # Regulation football pitch renderer & Best XI selector
│   ├── scouting.py             # EA FC style player dossier & 1v1 duel engine
│   └── analytics.py            # Advanced per-90 metrics, efficiency matrices, power rankings
├── generate_data.py            # Reproducible synthetic dataset generator
├── football_players.csv        # Generated dataset (185 rows, 80 players, 3 seasons)
├── requirements.txt            # Python dependencies
├── README.md                   # Platform documentation
└── .streamlit/
    └── config.toml             # Streamlit dark theme configuration
```

---

## 🚀 Quick Start (Local)

### 1. Prerequisites
- Python 3.9 or newer
- pip

### 2. Activate Environment & Install Dependencies

```bash
# Optional virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Generate Data (if not present)

```bash
python generate_data.py
```

### 4. Launch the Platform

```bash
streamlit run app.py
```

The application will launch automatically at `http://localhost:8501`.

---

## 📊 Advanced Metrics Calculated

- **Goals / 90 min**: `(Goals / Minutes Played) * 90`
- **Assists / 90 min**: `(Assists / Minutes Played) * 90`
- **Goal Contributions (G+A)**: `Goals + Assists`
- **Shot Accuracy %**: `(Shots on Target / Total Shots) * 100`
- **Shot Conversion Rate %**: `(Goals / Total Shots) * 100`
- **Minutes per Goal Contribution**: `Minutes Played / (Goals + Assists)`
- **Disciplinary Penalty Index**: `(Yellow Cards * 1) + (Red Cards * 3)`
- **Attack Index**: `(Total Goals * 1.5) + (Total Assists * 1.0)`

---

## 🎨 Design Philosophy

- **Dark Pitch Aesthetic**: Deep midnight slate (`#0A0E17`) paired with pitch neon green (`#00FF87`), electric cyan (`#00D2FF`), royal purple (`#8B5CF6`), and gold (`#F59E0B`).
- **Glassmorphic Depth**: Subtle 1px translucent borders, glowing accents, and smooth hover elevation.
- **Visual Telemetry**: Interactive Plotly charts with custom dark backgrounds, unified gridlines, and clean typography.
