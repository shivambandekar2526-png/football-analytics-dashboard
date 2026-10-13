# Football Player Performance Analytics Dashboard — Implementation Plan

## Top-Level Overview

Build a self-contained, portfolio-quality Streamlit web application that lets users explore, filter and compare synthetic football (soccer) player statistics. The project produces four files: `football_players.csv` (synthetic dataset), `app.py` (Streamlit application), `requirements.txt` (Python dependencies), and `README.md` (run & deploy guide). All KPIs and charts are derived dynamically from the filtered data. The UI uses a dark, football-inspired green-pitch theme applied via Streamlit's config and inline CSS.

---

## Dataset Schema

File: `football_players.csv`

| Column | Type | Description |
|---|---|---|
| player_id | int | Unique player identifier (1–100+) |
| player_name | str | Full name (synthetic) |
| age | int | Player age (17–38) |
| nationality | str | Country name (synthetic) |
| team | str | Club name (8–10 synthetic clubs) |
| position | str | One of: Goalkeeper, Defender, Midfielder, Forward |
| season | str | One of: 2021-22, 2022-23, 2023-24 |
| appearances | int | Matches played |
| goals | int | Goals scored (position-realistic ranges) |
| assists | int | Assists (position-realistic ranges) |
| shots | int | Total shots (position-realistic) |
| shots_on_target | int | Subset of shots |
| minutes_played | int | Total minutes |
| pass_accuracy | float | Percentage 0–100 |
| rating | float | Average match rating 5.0–9.5 |
| yellow_cards | int | Yellow cards received |
| red_cards | int | Red cards received |
| clean_sheets | int | Goalkeeper/Defender only; 0 for others |

**Generation rules:**
- At least 100 rows; players appear once per season (up to 3 rows per player across seasons).
- Goals/assists/shots are seeded with `numpy.random.seed(42)` for full reproducibility.
- A header comment in the CSV and a visible banner in the app clearly state: *"Data is entirely synthetic and does not represent real-world football results."*

---

## KPI Calculations

All KPIs are recalculated every time filters change (no hardcoded values).

| KPI Card | Formula |
|---|---|
| Total Players | `df['player_name'].nunique()` |
| Total Goals | `df['goals'].sum()` |
| Total Assists | `df['assists'].sum()` |
| Total Minutes Played | `df['minutes_played'].sum()` |
| Average Player Rating | `df['rating'].mean()` rounded to 2 dp |

---

## Page & Feature Structure

### Sidebar Filters (all pages)
- Season multiselect (default: all)
- Team multiselect (default: all)
- Position multiselect (default: all)
- Player search text input (filters player name by substring)
- "Download filtered data as CSV" button

### Page 1 — Overview
- Synthetic data disclaimer banner
- 5 KPI metric cards in a single row
- Top-10 players by goals bar chart (horizontal)
- Top-10 players by rating bar chart (horizontal)

### Page 2 — Player Analysis
- Player multi-select for head-to-head comparison (up to 5 players)
- Radar chart comparing selected players across 6 normalised stats: goals, assists, pass_accuracy, rating, shots_on_target, minutes_played
- Goals vs Assists scatter plot (colour = position, size = rating)
- Shots vs Goals scatter plot (colour = team, trendline via numpy polyfit)

### Page 3 — Team Analysis
- Grouped bar chart: goals and assists per team
- Stacked bar chart: player count per team broken down by position
- Team summary table (sortable): team, total goals, total assists, avg rating, player count

### Page 4 — Position Analysis
- KPI row filtered to each position group
- Box plot of rating distribution by position
- Bar chart of average goals by position
- Goalkeeper sub-section: clean sheets leaderboard
- Defender sub-section: avg pass accuracy
- Midfielder sub-section: avg assists
- Forward sub-section: goals-per-shot ratio (goals / shots, shots > 0)

### Player Statistics Table (all pages, below charts)
- Searchable via sidebar player filter
- Sortable columns via `st.dataframe`
- Pagination handled automatically by Streamlit

---

## Chart Choices & Rationale

| Chart | Library | Reason |
|---|---|---|
| KPI cards | `st.metric` | Native Streamlit, no extra code |
| Horizontal bar (top-10) | Plotly Express `bar` | Clear ranking, easy label |
| Radar / spider | Plotly Graph Objects `Scatterpolar` | Multi-stat player comparison |
| Scatter (goals vs assists) | Plotly Express `scatter` | Reveals player archetypes |
| Scatter (shots vs goals) | Plotly Express `scatter` + numpy trendline | Shows efficiency |
| Grouped bar (team goals/assists) | Plotly Express `bar` with `barmode='group'` | Side-by-side team view |
| Stacked bar (team composition) | Plotly Express `bar` with `barmode='stack'` | Position breakdown |
| Box plot (rating by position) | Plotly Express `box` | Distribution insight |
| Bar (avg goals by position) | Plotly Express `bar` | Simple comparison |

All charts use a shared dark theme template (`plotly_dark`) with green accent colour `#00FF87` to match the pitch theme.

---

## UI Theme

Applied via `.streamlit/config.toml`:
```
[theme]
base = "dark"
primaryColor = "#00FF87"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#1a1f2e"
textColor = "#ffffff"
font = "sans serif"
```

Additional CSS injected via `st.markdown(unsafe_allow_html=True)` for:
- KPI card styling (rounded dark tiles with green border)
- Disclaimer banner (amber highlight)
- Page title with football emoji branding

---

## Project File Structure

```
football analysis/
├── app.py                     # Main Streamlit application
├── football_players.csv       # Synthetic dataset
├── requirements.txt           # Python dependencies
├── README.md                  # Setup and deploy guide
└── .streamlit/
    └── config.toml            # Dark green theme config
```

---

## Module Layout inside `app.py`

```
app.py
├── SECTION 1: Imports & page config
├── SECTION 2: Theme / CSS injection
├── SECTION 3: Data loading & caching (@st.cache_data)
├── SECTION 4: Sidebar filters & download button
├── SECTION 5: Page router (st.sidebar radio)
├── SECTION 6: render_overview(df)
├── SECTION 7: render_player_analysis(df)
├── SECTION 8: render_team_analysis(df)
└── SECTION 9: render_position_analysis(df)
```

Each `render_*` function receives the already-filtered dataframe. Input validation (empty dataframe after filtering) is handled inside each render function with a clear `st.warning` message.

---

## Error & Validation Handling

| Scenario | Handling |
|---|---|
| No rows after filtering | `st.warning("No players match the current filters.")` |
| Radar chart with < 2 players selected | `st.info("Select at least 2 players to compare.")` |
| Division by zero in goals-per-shot | Filter `shots > 0` before calculating |
| Missing values in CSV | `df.fillna(0)` for numeric, `df.fillna('Unknown')` for string columns on load |

---

## requirements.txt Contents

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.26.0
plotly>=5.20.0
```

---

## Sub-Tasks

---

### Sub-Task 1 — Generate the Synthetic Dataset

**Intent:** Create a reproducible CSV with at least 100 rows of realistic synthetic player data. This is the foundation for every other sub-task.

**Expected Outcomes:**
- `football_players.csv` exists in the project root.
- Contains all 18 columns described in the schema.
- At least 100 rows covering 4 positions, 8–10 teams, and 3 seasons.
- Seeded with `numpy.random.seed(42)` so every regeneration produces identical data.
- First line comment (or README note) disclaims synthetic nature.

**Todo List:**
1. Write a standalone Python script (or inline generation) using `numpy` and `pandas`.
2. Define player name pool (first names + last names list, combine randomly).
3. Define team list (8 clubs) and nationality list (10 countries).
4. Assign position-realistic stat ranges: GK low goals, FW high goals/shots, etc.
5. Generate 3 seasons of data; not every player appears every season.
6. Save to `football_players.csv`.

**Relevant Context:** Schema table and generation rules in the Dataset Schema section above.

**Status:** [ ] pending

---

### Sub-Task 2 — Streamlit Theme & Project Scaffolding

**Intent:** Set up the `.streamlit/config.toml` theme and the skeleton of `app.py` (imports, page config, CSS, data loader, sidebar, page router) so subsequent sub-tasks can slot render functions in.

**Expected Outcomes:**
- `.streamlit/config.toml` with dark green theme.
- `app.py` loads and caches the CSV, renders the sidebar, and routes to placeholder pages without errors.
- Running `streamlit run app.py` shows a dark-themed app with a working sidebar.

**Todo List:**
1. Create `.streamlit/config.toml` with the theme values above.
2. Create `app.py` with imports (`streamlit`, `pandas`, `numpy`, `plotly.express`, `plotly.graph_objects`).
3. Add `st.set_page_config` (title, icon, layout="wide").
4. Add CSS injection (`st.markdown`) for KPI cards and disclaimer banner.
5. Add `@st.cache_data` data loader that reads CSV, fills missing values, and returns the dataframe.
6. Build sidebar: season, team, position multiselects + player text search + download button.
7. Add page router using `st.sidebar.radio` with four page options.
8. Add stub `render_*` functions that just show `st.write("Coming soon")`.

**Relevant Context:** UI Theme, Module Layout, and Sidebar Filters sections above.

**Status:** [ ] pending

---

### Sub-Task 3 — Overview Page

**Intent:** Implement `render_overview(df)` with 5 KPI cards and two top-10 bar charts.

**Expected Outcomes:**
- Five metric cards display correct dynamic values from the filtered dataframe.
- Two horizontal bar charts (top-10 by goals, top-10 by rating) render with green accent and dark background.
- Synthetic data disclaimer banner visible at the top of this page.
- Empty-filter guard shows `st.warning` instead of crashing.

**Todo List:**
1. Implement disclaimer banner using `st.markdown` with amber-styled CSS.
2. Compute 5 KPIs from filtered `df`; display with `st.metric` inside `st.columns(5)`.
3. Build top-10 by goals horizontal bar chart with Plotly Express.
4. Build top-10 by rating horizontal bar chart with Plotly Express.
5. Apply `plotly_dark` template and `#00FF87` bar colour to both charts.
6. Wrap everything in `if df.empty: st.warning(...)` guard.

**Relevant Context:** KPI Calculations and Page 1 — Overview sections above.

**Status:** [ ] pending

---

### Sub-Task 4 — Player Analysis Page

**Intent:** Implement `render_player_analysis(df)` with a radar comparison chart and two scatter plots.

**Expected Outcomes:**
- Player multi-select (up to 5) renders a normalised radar chart.
- Goals vs Assists scatter shows position colouring and rating-sized markers with tooltips.
- Shots vs Goals scatter shows team colouring and a numpy trendline.
- Guard messages shown when < 2 players selected or no data.

**Todo List:**
1. Add player multi-select widget inside the render function.
2. Normalise the 6 stat columns (min-max) for radar chart parity.
3. Build radar chart with `plotly.graph_objects.Scatterpolar`; one trace per player.
4. Build Goals vs Assists scatter with `plotly.express.scatter`.
5. Build Shots vs Goals scatter; compute numpy polyfit trendline; overlay as a line trace.
6. Add input validation guards throughout.

**Relevant Context:** Page 2 — Player Analysis and Chart Choices sections above.

**Status:** [ ] pending

---

### Sub-Task 5 — Team Analysis Page

**Intent:** Implement `render_team_analysis(df)` with grouped/stacked bar charts and a summary table.

**Expected Outcomes:**
- Grouped bar chart showing goals and assists per team renders correctly.
- Stacked bar chart shows player count per team broken down by position.
- Sortable team summary table renders via `st.dataframe`.
- Empty-filter guard in place.

**Todo List:**
1. Aggregate `df` by team: sum goals, sum assists, mean rating, count unique players.
2. Build grouped bar chart with `plotly.express.bar(barmode='group')`.
3. Aggregate player counts by team and position.
4. Build stacked bar chart with `plotly.express.bar(barmode='stack')`.
5. Display team summary `st.dataframe` with formatted columns.

**Relevant Context:** Page 3 — Team Analysis section above.

**Status:** [ ] pending

---

### Sub-Task 6 — Position Analysis Page

**Intent:** Implement `render_position_analysis(df)` with position-level KPIs, a box plot, a bar chart, and position-specific sub-sections.

**Expected Outcomes:**
- Rating distribution box plot by position renders.
- Average goals by position bar chart renders.
- Each position group (GK, DEF, MID, FWD) has its own focused metric/chart.
- Goals-per-shot ratio correctly guards against division by zero.

**Todo List:**
1. Build rating box plot by position with `plotly.express.box`.
2. Build average goals by position bar chart.
3. Filter to Goalkeepers; display clean sheets leaderboard as `st.dataframe`.
4. Filter to Defenders; compute and display avg pass accuracy metric.
5. Filter to Midfielders; compute and display avg assists metric.
6. Filter to Forwards; compute goals-per-shot (where shots > 0); display top-10 as `st.dataframe`.

**Relevant Context:** Page 4 — Position Analysis section above.

**Status:** [ ] pending

---

### Sub-Task 7 — Player Statistics Table, Download Button & README

**Intent:** Ensure the searchable statistics table and CSV download work globally, and write the README.

**Expected Outcomes:**
- A full `st.dataframe` of the filtered dataset appears on every page below the charts.
- The sidebar CSV download button produces a correctly-encoded file.
- `README.md` contains: project description, setup steps, local run command, Streamlit Cloud deploy instructions, and a synthetic-data disclaimer.
- `requirements.txt` is present and correct.

**Todo List:**
1. Move the stats table render into a shared helper called from each render function.
2. Verify the `st.download_button` in the sidebar produces valid UTF-8 CSV.
3. Write `requirements.txt` with pinned minimum versions.
4. Write `README.md` with all required sections.

**Relevant Context:** Player Statistics Table, Sidebar Filters, and requirements.txt sections above.

**Status:** [ ] pending

---

## Implementation Order

```
Sub-Task 1 → Sub-Task 2 → Sub-Task 3 → Sub-Task 4 → Sub-Task 5 → Sub-Task 6 → Sub-Task 7
  Dataset      Scaffold     Overview    Player       Team          Position      Table +
  (CSV)        (app.py      Page        Analysis     Analysis      Analysis      README
               skeleton)               Page         Page          Page
```
