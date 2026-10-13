"""
app.py — Football Player Performance Analytics Dashboard
Synthetic data only. Does not represent real-world football results.
Run: streamlit run app.py
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* KPI card tile */
    .kpi-card {
        background: #1a1f2e;
        border: 1px solid #00FF87;
        border-radius: 10px;
        padding: 18px 14px;
        text-align: center;
    }
    .kpi-label { font-size: 13px; color: #adb5bd; margin-bottom: 4px; }
    .kpi-value { font-size: 28px; font-weight: 700; color: #00FF87; }

    /* Disclaimer banner */
    .disclaimer {
        background: #2d2006;
        border-left: 4px solid #f0ad00;
        padding: 10px 16px;
        border-radius: 4px;
        font-size: 13px;
        color: #f0ad00;
        margin-bottom: 18px;
    }

    /* Section header */
    .section-header {
        font-size: 20px;
        font-weight: 600;
        color: #00FF87;
        border-bottom: 1px solid #2a3040;
        padding-bottom: 6px;
        margin: 22px 0 12px 0;
    }

    /* Scrollable dataframe container */
    div[data-testid="stDataFrame"] { border: 1px solid #2a3040; border-radius: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Constants ──────────────────────────────────────────────────────────────────
PLOTLY_TEMPLATE = "plotly_dark"
ACCENT = "#00FF87"
POSITION_COLORS = {
    "Goalkeeper": "#F59E0B",
    "Defender":   "#3B82F6",
    "Midfielder": "#8B5CF6",
    "Forward":    "#EF4444",
}

DISCLAIMER = (
    '<div class="disclaimer">⚠️ <strong>Synthetic Data Notice:</strong> '
    "All player statistics shown in this dashboard are entirely synthetic and generated "
    "for demonstration purposes only. They do not represent real-world football results, "
    "clubs, or players.</div>"
)


# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    try:
        df = pd.read_csv("football_players.csv")
    except FileNotFoundError:
        st.error(
            "**football_players.csv not found.** "
            "Run `python generate_data.py` to create the dataset, then refresh this page."
        )
        st.stop()

    # Fill any missing values defensively
    num_cols = df.select_dtypes(include="number").columns
    str_cols = df.select_dtypes(include="object").columns
    df[num_cols] = df[num_cols].fillna(0)
    df[str_cols] = df[str_cols].fillna("Unknown")
    return df


# ── Shared helpers ─────────────────────────────────────────────────────────────
def apply_chart_style(fig: go.Figure, height: int = 420) -> go.Figure:
    """Apply consistent dark theme and sizing to every Plotly figure."""
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font_color="#ffffff",
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def render_stats_table(df: pd.DataFrame) -> None:
    """Render the searchable / sortable player statistics table."""
    st.markdown('<p class="section-header">📋 Player Statistics Table</p>', unsafe_allow_html=True)
    display_cols = [
        "player_name", "team", "position", "season", "age",
        "appearances", "goals", "assists", "shots", "shots_on_target",
        "minutes_played", "pass_accuracy", "rating",
        "yellow_cards", "red_cards", "clean_sheets",
    ]
    st.dataframe(
        df[display_cols].sort_values("rating", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=380,
    )


def empty_guard(df: pd.DataFrame) -> bool:
    """Return True (and show warning) when the filtered dataframe is empty."""
    if df.empty:
        st.warning("⚠️ No players match the current filters. Try widening your selection.")
        return True
    return False


# ── Sidebar ────────────────────────────────────────────────────────────────────
def build_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Soccerball.svg/240px-Soccerball.svg.png",
        width=60,
    )
    st.sidebar.title("⚽ Football Analytics")
    st.sidebar.markdown("---")

    # Season filter
    seasons = sorted(df["season"].unique())
    sel_seasons = st.sidebar.multiselect("📅 Season", seasons, default=seasons)

    # Team filter
    teams = sorted(df["team"].unique())
    sel_teams = st.sidebar.multiselect("🏟️ Team", teams, default=teams)

    # Position filter
    positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
    sel_positions = st.sidebar.multiselect("🎽 Position", positions, default=positions)

    # Player name search
    player_search = st.sidebar.text_input("🔍 Search player name", value="")

    st.sidebar.markdown("---")

    # Apply filters
    mask = (
        df["season"].isin(sel_seasons if sel_seasons else seasons)
        & df["team"].isin(sel_teams if sel_teams else teams)
        & df["position"].isin(sel_positions if sel_positions else positions)
    )
    filtered = df[mask].copy()
    if player_search.strip():
        filtered = filtered[
            filtered["player_name"].str.contains(player_search.strip(), case=False, na=False)
        ]

    # Download button
    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        label="⬇️ Download filtered data (CSV)",
        data=csv_bytes,
        file_name="filtered_football_data.csv",
        mime="text/csv",
    )

    st.sidebar.markdown(f"**{len(filtered):,}** rows after filtering")
    return filtered


# ── Page 1: Overview ───────────────────────────────────────────────────────────
def render_overview(df: pd.DataFrame) -> None:
    st.markdown(DISCLAIMER, unsafe_allow_html=True)
    st.title("⚽ Football Analytics Dashboard — Overview")

    if empty_guard(df):
        return

    # ── KPI Cards ──────────────────────────────────────────────────────────────
    total_players  = df["player_name"].nunique()
    total_goals    = int(df["goals"].sum())
    total_assists  = int(df["assists"].sum())
    total_minutes  = int(df["minutes_played"].sum())
    avg_rating     = round(float(df["rating"].mean()), 2)

    kpi_data = [
        ("👤 Total Players",       f"{total_players:,}"),
        ("⚽ Total Goals",          f"{total_goals:,}"),
        ("🅰️ Total Assists",        f"{total_assists:,}"),
        ("⏱️ Total Minutes Played", f"{total_minutes:,}"),
        ("⭐ Avg Player Rating",    f"{avg_rating}"),
    ]

    cols = st.columns(5)
    for col, (label, value) in zip(cols, kpi_data):
        col.markdown(
            f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Top-10 charts ──────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-header">🥅 Top 10 Players by Goals</p>', unsafe_allow_html=True)
        top_goals = (
            df.groupby("player_name", as_index=False)["goals"]
            .sum()
            .nlargest(10, "goals")
            .sort_values("goals")
        )
        fig = px.bar(
            top_goals,
            x="goals",
            y="player_name",
            orientation="h",
            labels={"goals": "Goals", "player_name": "Player"},
            color_discrete_sequence=[ACCENT],
        )
        fig = apply_chart_style(fig)
        fig.update_traces(marker_color=ACCENT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-header">⭐ Top 10 Players by Rating</p>', unsafe_allow_html=True)
        top_rating = (
            df.groupby("player_name", as_index=False)["rating"]
            .mean()
            .round(2)
            .nlargest(10, "rating")
            .sort_values("rating")
        )
        fig2 = px.bar(
            top_rating,
            x="rating",
            y="player_name",
            orientation="h",
            labels={"rating": "Avg Rating", "player_name": "Player"},
            color_discrete_sequence=["#7C5CD8"],
        )
        fig2 = apply_chart_style(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    render_stats_table(df)


# ── Page 2: Player Analysis ────────────────────────────────────────────────────
def render_player_analysis(df: pd.DataFrame) -> None:
    st.title("🔍 Player Analysis")
    st.markdown(DISCLAIMER, unsafe_allow_html=True)

    if empty_guard(df):
        return

    # ── Radar comparison ───────────────────────────────────────────────────────
    st.markdown('<p class="section-header">🕸️ Player Comparison Radar</p>', unsafe_allow_html=True)

    all_players = sorted(df["player_name"].unique())
    default_players = all_players[:2] if len(all_players) >= 2 else all_players
    selected_players = st.multiselect(
        "Select players to compare (2–5):",
        options=all_players,
        default=default_players,
        max_selections=5,
    )

    RADAR_STATS = ["goals", "assists", "pass_accuracy", "rating", "shots_on_target", "minutes_played"]
    RADAR_LABELS = ["Goals", "Assists", "Pass Acc.", "Rating", "Shots on Target", "Minutes"]

    if len(selected_players) < 2:
        st.info("ℹ️ Select at least 2 players to display the radar chart.")
    else:
        player_df = df[df["player_name"].isin(selected_players)].groupby("player_name")[RADAR_STATS].mean()

        # Min-max normalise per stat column
        norm_df = player_df.copy()
        for col in RADAR_STATS:
            col_min, col_max = player_df[col].min(), player_df[col].max()
            if col_max > col_min:
                norm_df[col] = (player_df[col] - col_min) / (col_max - col_min)
            else:
                norm_df[col] = 0.5

        radar_colors = [ACCENT, "#7C5CD8", "#F59E0B", "#EF4444", "#3B82F6"]
        fig_radar = go.Figure()
        for i, player in enumerate(selected_players):
            if player not in norm_df.index:
                continue
            vals = norm_df.loc[player, RADAR_STATS].tolist()
            vals += vals[:1]  # close the polygon
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=vals,
                    theta=RADAR_LABELS + [RADAR_LABELS[0]],
                    fill="toself",
                    name=player,
                    line_color=radar_colors[i % len(radar_colors)],
                    opacity=0.75,
                )
            )
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#1a1f2e",
                radialaxis=dict(visible=True, range=[0, 1], color="#adb5bd"),
                angularaxis=dict(color="#adb5bd"),
            ),
            showlegend=True,
        )
        fig_radar = apply_chart_style(fig_radar, height=480)
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── Goals vs Assists scatter ───────────────────────────────────────────────
    st.markdown('<p class="section-header">🎯 Goals vs Assists</p>', unsafe_allow_html=True)
    fig_ga = px.scatter(
        df,
        x="goals",
        y="assists",
        color="position",
        size="rating",
        size_max=18,
        hover_data=["player_name", "team", "season"],
        labels={"goals": "Goals", "assists": "Assists", "position": "Position"},
        color_discrete_map=POSITION_COLORS,
    )
    fig_ga = apply_chart_style(fig_ga)
    st.plotly_chart(fig_ga, use_container_width=True)

    # ── Shots vs Goals scatter with trendline ─────────────────────────────────
    st.markdown('<p class="section-header">🔫 Shots vs Goals (with Trend)</p>', unsafe_allow_html=True)
    scatter_df = df[df["shots"] > 0].copy()
    fig_sg = px.scatter(
        scatter_df,
        x="shots",
        y="goals",
        color="team",
        hover_data=["player_name", "position", "season"],
        labels={"shots": "Shots", "goals": "Goals", "team": "Team"},
    )

    # Numpy polyfit trendline overlay
    z = np.polyfit(scatter_df["shots"], scatter_df["goals"], 1)
    p = np.poly1d(z)
    x_range = np.linspace(scatter_df["shots"].min(), scatter_df["shots"].max(), 100)
    fig_sg.add_trace(
        go.Scatter(
            x=x_range,
            y=p(x_range),
            mode="lines",
            name="Trend",
            line=dict(color=ACCENT, width=2, dash="dash"),
        )
    )
    fig_sg = apply_chart_style(fig_sg)
    st.plotly_chart(fig_sg, use_container_width=True)

    render_stats_table(df)


# ── Page 3: Team Analysis ──────────────────────────────────────────────────────
def render_team_analysis(df: pd.DataFrame) -> None:
    st.title("🏟️ Team Analysis")
    st.markdown(DISCLAIMER, unsafe_allow_html=True)

    if empty_guard(df):
        return

    # Aggregate by team
    team_agg = (
        df.groupby("team", as_index=False)
        .agg(
            total_goals=("goals", "sum"),
            total_assists=("assists", "sum"),
            avg_rating=("rating", "mean"),
            player_count=("player_name", "nunique"),
        )
        .round({"avg_rating": 2})
        .sort_values("total_goals", ascending=False)
    )

    # ── Grouped bar: goals & assists per team ──────────────────────────────────
    st.markdown('<p class="section-header">⚽ Goals & Assists per Team</p>', unsafe_allow_html=True)
    goals_assists_long = team_agg.melt(
        id_vars="team",
        value_vars=["total_goals", "total_assists"],
        var_name="metric",
        value_name="count",
    )
    goals_assists_long["metric"] = goals_assists_long["metric"].map(
        {"total_goals": "Goals", "total_assists": "Assists"}
    )
    fig_ga_team = px.bar(
        goals_assists_long,
        x="team",
        y="count",
        color="metric",
        barmode="group",
        labels={"team": "Team", "count": "Count", "metric": "Metric"},
        color_discrete_map={"Goals": ACCENT, "Assists": "#7C5CD8"},
    )
    fig_ga_team = apply_chart_style(fig_ga_team)
    st.plotly_chart(fig_ga_team, use_container_width=True)

    col1, col2 = st.columns(2)

    # ── Stacked bar: player count by position per team ─────────────────────────
    with col1:
        st.markdown('<p class="section-header">🎽 Squad Composition by Position</p>', unsafe_allow_html=True)
        pos_team = (
            df.groupby(["team", "position"], as_index=False)["player_name"]
            .nunique()
            .rename(columns={"player_name": "count"})
        )
        fig_pos = px.bar(
            pos_team,
            x="team",
            y="count",
            color="position",
            barmode="stack",
            labels={"team": "Team", "count": "Players", "position": "Position"},
            color_discrete_map=POSITION_COLORS,
        )
        fig_pos = apply_chart_style(fig_pos)
        st.plotly_chart(fig_pos, use_container_width=True)

    # ── Team summary table ────────────────────────────────────────────────────
    with col2:
        st.markdown('<p class="section-header">📊 Team Summary</p>', unsafe_allow_html=True)
        st.dataframe(
            team_agg.rename(columns={
                "team": "Team",
                "total_goals": "Goals",
                "total_assists": "Assists",
                "avg_rating": "Avg Rating",
                "player_count": "Players",
            }),
            use_container_width=True,
            height=380,
        )

    render_stats_table(df)


# ── Page 4: Position Analysis ──────────────────────────────────────────────────
def render_position_analysis(df: pd.DataFrame) -> None:
    st.title("📐 Position Analysis")
    st.markdown(DISCLAIMER, unsafe_allow_html=True)

    if empty_guard(df):
        return

    # ── Rating distribution box plot ──────────────────────────────────────────
    st.markdown('<p class="section-header">⭐ Rating Distribution by Position</p>', unsafe_allow_html=True)
    fig_box = px.box(
        df,
        x="position",
        y="rating",
        color="position",
        points="outliers",
        labels={"position": "Position", "rating": "Rating"},
        color_discrete_map=POSITION_COLORS,
    )
    fig_box = apply_chart_style(fig_box)
    st.plotly_chart(fig_box, use_container_width=True)

    # ── Avg goals by position bar ──────────────────────────────────────────────
    st.markdown('<p class="section-header">⚽ Average Goals by Position</p>', unsafe_allow_html=True)
    avg_goals = (
        df.groupby("position", as_index=False)["goals"]
        .mean()
        .round(2)
        .sort_values("goals", ascending=False)
    )
    fig_avg = px.bar(
        avg_goals,
        x="position",
        y="goals",
        color="position",
        labels={"position": "Position", "goals": "Avg Goals"},
        color_discrete_map=POSITION_COLORS,
    )
    fig_avg.update_layout(showlegend=False)
    fig_avg = apply_chart_style(fig_avg, height=320)
    st.plotly_chart(fig_avg, use_container_width=True)

    # ── Position-specific sub-sections ────────────────────────────────────────
    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<p class="section-header">🧤 Goalkeepers — Clean Sheets Leaderboard</p>', unsafe_allow_html=True)
        gk_df = df[df["position"] == "Goalkeeper"]
        if gk_df.empty:
            st.info("No Goalkeepers in current filter.")
        else:
            gk_table = (
                gk_df.groupby("player_name", as_index=False)["clean_sheets"]
                .sum()
                .nlargest(10, "clean_sheets")
                .rename(columns={"player_name": "Player", "clean_sheets": "Clean Sheets"})
            )
            st.dataframe(gk_table, use_container_width=True, hide_index=True)
            st.metric("Avg Clean Sheets (GK)", round(gk_df["clean_sheets"].mean(), 1))

    with c2:
        st.markdown('<p class="section-header">🛡️ Defenders — Pass Accuracy</p>', unsafe_allow_html=True)
        def_df = df[df["position"] == "Defender"]
        if def_df.empty:
            st.info("No Defenders in current filter.")
        else:
            st.metric("Avg Pass Accuracy (DEF)", f"{round(def_df['pass_accuracy'].mean(), 1)}%")
            def_table = (
                def_df.groupby("player_name", as_index=False)["pass_accuracy"]
                .mean()
                .round(1)
                .nlargest(10, "pass_accuracy")
                .rename(columns={"player_name": "Player", "pass_accuracy": "Pass Acc. %"})
            )
            st.dataframe(def_table, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<p class="section-header">🎯 Midfielders — Assists</p>', unsafe_allow_html=True)
        mid_df = df[df["position"] == "Midfielder"]
        if mid_df.empty:
            st.info("No Midfielders in current filter.")
        else:
            st.metric("Avg Assists (MID)", round(mid_df["assists"].mean(), 1))
            mid_table = (
                mid_df.groupby("player_name", as_index=False)["assists"]
                .sum()
                .nlargest(10, "assists")
                .rename(columns={"player_name": "Player", "assists": "Assists"})
            )
            st.dataframe(mid_table, use_container_width=True, hide_index=True)

    with c4:
        st.markdown('<p class="section-header">🚀 Forwards — Goals per Shot</p>', unsafe_allow_html=True)
        fwd_df = df[(df["position"] == "Forward") & (df["shots"] > 0)].copy()
        if fwd_df.empty:
            st.info("No Forwards with shots in current filter.")
        else:
            fwd_df["goals_per_shot"] = (fwd_df["goals"] / fwd_df["shots"]).round(3)
            st.metric("Avg Goals per Shot (FWD)", round(fwd_df["goals_per_shot"].mean(), 3))
            fwd_table = (
                fwd_df.groupby("player_name", as_index=False)
                .agg(goals=("goals", "sum"), shots=("shots", "sum"))
                .assign(goals_per_shot=lambda x: (x["goals"] / x["shots"]).round(3))
                .nlargest(10, "goals_per_shot")
                .rename(columns={
                    "player_name": "Player",
                    "goals": "Goals",
                    "shots": "Shots",
                    "goals_per_shot": "Goals/Shot",
                })
            )
            st.dataframe(fwd_table, use_container_width=True, hide_index=True)

    render_stats_table(df)


# ── Main ───────────────────────────────────────────────────────────────────────
def main() -> None:
    raw_df = load_data()
    filtered_df = build_sidebar(raw_df)

    page = st.sidebar.radio(
        "📂 Navigate",
        ["Overview", "Player Analysis", "Team Analysis", "Position Analysis"],
        index=0,
    )

    if page == "Overview":
        render_overview(filtered_df)
    elif page == "Player Analysis":
        render_player_analysis(filtered_df)
    elif page == "Team Analysis":
        render_team_analysis(filtered_df)
    elif page == "Position Analysis":
        render_position_analysis(filtered_df)


if __name__ == "__main__":
    main()
