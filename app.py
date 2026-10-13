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
    page_title="Football Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Base ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Hide default Streamlit header/footer */
    #MainMenu, footer, header { visibility: hidden; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0e1117; }
    ::-webkit-scrollbar-thumb { background: #2a3040; border-radius: 4px; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1520 0%, #0e1117 100%);
        border-right: 1px solid #1e2a3a;
    }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    .sidebar-logo {
        text-align: center;
        padding: 8px 0 4px 0;
    }
    .sidebar-logo .ball { font-size: 48px; line-height: 1; }
    .sidebar-logo h1 {
        font-size: 18px;
        font-weight: 800;
        color: #00FF87 !important;
        margin: 4px 0 0 0;
        letter-spacing: 0.5px;
    }
    .sidebar-logo p {
        font-size: 11px;
        color: #64748b !important;
        margin: 2px 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .nav-label {
        font-size: 10px;
        font-weight: 700;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 16px 0 4px 4px;
    }
    .filter-label {
        font-size: 10px;
        font-weight: 700;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 12px 0 4px 4px;
    }
    .row-count {
        background: #1a2332;
        border: 1px solid #1e2a3a;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 12px;
        color: #94a3b8 !important;
        text-align: center;
        margin-top: 8px;
    }
    .row-count span { color: #00FF87 !important; font-weight: 700; font-size: 15px; }

    /* ── Page hero ── */
    .page-hero {
        background: linear-gradient(135deg, #0d2818 0%, #0e1117 60%, #0d1a2e 100%);
        border: 1px solid #1e3a2a;
        border-radius: 16px;
        padding: 28px 32px 24px 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .page-hero::before {
        content: "";
        position: absolute;
        top: -40px; right: -40px;
        width: 160px; height: 160px;
        background: radial-gradient(circle, rgba(0,255,135,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .page-hero h1 {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff !important;
        margin: 0 0 6px 0;
        letter-spacing: -0.3px;
    }
    .page-hero p {
        font-size: 14px;
        color: #64748b !important;
        margin: 0;
    }
    .page-hero .accent { color: #00FF87 !important; }

    /* ── Disclaimer ── */
    .disclaimer {
        background: linear-gradient(90deg, #1c1400 0%, #0e1117 100%);
        border-left: 3px solid #f59e0b;
        border-radius: 0 8px 8px 0;
        padding: 10px 16px;
        font-size: 12px;
        color: #a16207 !important;
        margin-bottom: 20px;
    }
    .disclaimer strong { color: #f59e0b !important; }

    /* ── KPI cards ── */
    .kpi-grid { display: flex; gap: 14px; margin-bottom: 8px; flex-wrap: wrap; }
    .kpi-card {
        flex: 1; min-width: 140px;
        background: linear-gradient(135deg, #111827 0%, #1a2332 100%);
        border: 1px solid #1e2a3a;
        border-radius: 14px;
        padding: 20px 16px 16px 16px;
        position: relative;
        overflow: hidden;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .kpi-card:hover { transform: translateY(-2px); border-color: #00FF87; }
    .kpi-card::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #00FF87, transparent);
        border-radius: 0 0 14px 14px;
    }
    .kpi-icon { font-size: 22px; margin-bottom: 8px; display: block; }
    .kpi-label { font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
    .kpi-value { font-size: 30px; font-weight: 800; color: #00FF87; line-height: 1; }
    .kpi-sub { font-size: 11px; color: #475569; margin-top: 4px; }

    /* ── Section headers ── */
    .section-header {
        font-size: 15px;
        font-weight: 700;
        color: #e2e8f0;
        border-left: 3px solid #00FF87;
        padding-left: 10px;
        margin: 28px 0 14px 0;
        letter-spacing: 0.2px;
    }

    /* ── Chart card wrapper ── */
    .chart-card {
        background: #111827;
        border: 1px solid #1e2a3a;
        border-radius: 12px;
        padding: 4px 4px 0 4px;
        margin-bottom: 8px;
    }

    /* ── Dataframe ── */
    div[data-testid="stDataFrame"] {
        border: 1px solid #1e2a3a !important;
        border-radius: 10px !important;
        overflow: hidden;
    }

    /* ── Divider ── */
    hr { border-color: #1e2a3a !important; }

    /* ── Metric widget override ── */
    div[data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #1e2a3a;
        border-radius: 10px;
        padding: 14px 16px;
    }
    div[data-testid="stMetric"] label { color: #64748b !important; font-size: 12px !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #00FF87 !important; font-size: 22px !important; font-weight: 700 !important; }

    /* ── Radio nav pills ── */
    div[data-testid="stRadio"] > div { gap: 4px !important; }
    div[data-testid="stRadio"] label {
        background: #111827 !important;
        border: 1px solid #1e2a3a !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        transition: all 0.15s !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: #0d2818 !important;
        border-color: #00FF87 !important;
        color: #00FF87 !important;
    }

    /* ── Download button ── */
    div[data-testid="stDownloadButton"] button {
        width: 100%;
        background: linear-gradient(135deg, #065f46, #0d2818) !important;
        border: 1px solid #00FF87 !important;
        color: #00FF87 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        font-size: 13px !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: #00FF87 !important;
        color: #0e1117 !important;
    }

    /* ── Info / warning boxes ── */
    div[data-testid="stInfo"] { border-radius: 8px; font-size: 13px; }
    div[data-testid="stWarning"] { border-radius: 8px; font-size: 13px; }

    /* ── Multiselect tags ── */
    span[data-baseweb="tag"] { background: #0d2818 !important; border-color: #00FF87 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Constants ──────────────────────────────────────────────────────────────────
PLOTLY_TEMPLATE = "plotly_dark"
ACCENT        = "#00FF87"
ACCENT2       = "#7C5CD8"
BG_CARD       = "#111827"
BG_PLOT       = "#0d1117"
BORDER        = "#1e2a3a"

POSITION_COLORS = {
    "Goalkeeper": "#F59E0B",
    "Defender":   "#3B82F6",
    "Midfielder": "#8B5CF6",
    "Forward":    "#EF4444",
}

CHART_COLORS = [ACCENT, ACCENT2, "#F59E0B", "#EF4444", "#3B82F6", "#EC4899"]

DISCLAIMER = (
    '<div class="disclaimer">⚠️ <strong>Synthetic Data Notice:</strong> '
    "All statistics are entirely synthetic and generated for demonstration purposes only. "
    "They do not represent real-world football results, clubs, or players.</div>"
)

# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    try:
        df = pd.read_csv("football_players.csv")
    except FileNotFoundError:
        st.error(
            "**football_players.csv not found.** "
            "Run `python generate_data.py` to create the dataset, then refresh."
        )
        st.stop()
    num_cols = df.select_dtypes(include="number").columns
    str_cols = df.select_dtypes(include="object").columns
    df[num_cols] = df[num_cols].fillna(0)
    df[str_cols] = df[str_cols].fillna("Unknown")
    return df


# ── Chart helpers ──────────────────────────────────────────────────────────────
def style(fig: go.Figure, height: int = 420, legend_inside: bool = False) -> go.Figure:
    """Apply a consistent dark polish to every Plotly figure."""
    legend_cfg = dict(
        bgcolor="rgba(13,17,23,0.8)",
        bordercolor=BORDER,
        borderwidth=1,
        font=dict(size=11, color="#94a3b8"),
    )
    if legend_inside:
        legend_cfg.update(x=0.01, y=0.99, xanchor="left", yanchor="top")

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=BG_PLOT,
        plot_bgcolor=BG_CARD,
        font=dict(family="Inter, sans-serif", color="#cbd5e1", size=12),
        height=height,
        margin=dict(l=16, r=16, t=36, b=16),
        legend=legend_cfg,
        xaxis=dict(gridcolor="#1e2a3a", linecolor="#1e2a3a", zerolinecolor="#1e2a3a"),
        yaxis=dict(gridcolor="#1e2a3a", linecolor="#1e2a3a", zerolinecolor="#1e2a3a"),
    )
    return fig


def chart_wrap(fig: go.Figure) -> None:
    """Render a chart inside a subtle card wrapper."""
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


def section(icon: str, title: str) -> None:
    st.markdown(
        f'<p class="section-header">{icon}&nbsp; {title}</p>',
        unsafe_allow_html=True,
    )


# ── Shared helpers ─────────────────────────────────────────────────────────────
def render_stats_table(df: pd.DataFrame) -> None:
    section("📋", "Player Statistics Table")
    display_cols = [
        "player_name", "team", "position", "season", "age",
        "appearances", "goals", "assists", "shots", "shots_on_target",
        "minutes_played", "pass_accuracy", "rating",
        "yellow_cards", "red_cards", "clean_sheets",
    ]
    renamed = df[display_cols].sort_values("rating", ascending=False).reset_index(drop=True)
    renamed.columns = [c.replace("_", " ").title() for c in renamed.columns]
    st.dataframe(renamed, use_container_width=True, height=380)


def empty_guard(df: pd.DataFrame) -> bool:
    if df.empty:
        st.warning("⚠️ No players match the current filters. Try widening your selection.")
        return True
    return False


def hero(icon: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="page-hero">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Sidebar ────────────────────────────────────────────────────────────────────
def build_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-logo">'
            '<div class="ball">⚽</div>'
            '<h1>Football Analytics</h1>'
            '<p>Performance Dashboard</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        st.markdown('<p class="nav-label">Navigate</p>', unsafe_allow_html=True)
        page = st.radio(
            "page",
            ["🏠  Overview", "🔍  Player Analysis", "🏟️  Team Analysis", "📐  Position Analysis"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown('<p class="filter-label">Filters</p>', unsafe_allow_html=True)

        seasons   = sorted(df["season"].unique())
        teams     = sorted(df["team"].unique())
        positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]

        sel_seasons   = st.multiselect("📅 Season",   seasons,   default=seasons)
        sel_teams     = st.multiselect("🏟️ Team",     teams,     default=teams)
        sel_positions = st.multiselect("🎽 Position", positions, default=positions)
        player_search = st.text_input("🔍 Search player", placeholder="e.g. Luca Rossi")

        # Apply filters
        mask = (
            df["season"].isin(sel_seasons   or seasons)
            & df["team"].isin(sel_teams     or teams)
            & df["position"].isin(sel_positions or positions)
        )
        filtered = df[mask].copy()
        if player_search.strip():
            filtered = filtered[
                filtered["player_name"].str.contains(
                    player_search.strip(), case=False, na=False
                )
            ]

        st.markdown("---")
        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️  Download filtered CSV",
            data=csv_bytes,
            file_name="filtered_football_data.csv",
            mime="text/csv",
        )
        st.markdown(
            f'<div class="row-count"><span>{len(filtered):,}</span><br>rows after filtering</div>',
            unsafe_allow_html=True,
        )

    return filtered, page


# ── Page 1: Overview ───────────────────────────────────────────────────────────
def render_overview(df: pd.DataFrame) -> None:
    hero("⚽", "Overview", "Season-level snapshot — KPIs, top scorers and highest-rated players.")
    st.markdown(DISCLAIMER, unsafe_allow_html=True)

    if empty_guard(df):
        return

    # ── KPI row ────────────────────────────────────────────────────────────────
    total_players = df["player_name"].nunique()
    total_goals   = int(df["goals"].sum())
    total_assists = int(df["assists"].sum())
    total_minutes = int(df["minutes_played"].sum())
    avg_rating    = round(float(df["rating"].mean()), 2)
    top_scorer    = df.groupby("player_name")["goals"].sum().idxmax()

    kpis = [
        ("👤", "Players",          f"{total_players:,}",    "unique in selection"),
        ("⚽", "Goals",             f"{total_goals:,}",       "combined total"),
        ("🅰️", "Assists",           f"{total_assists:,}",     "combined total"),
        ("⏱️", "Minutes Played",    f"{total_minutes:,}",     "across all matches"),
        ("⭐", "Avg Rating",        f"{avg_rating}",          f"top: {top_scorer.split()[0]}"),
    ]

    cols = st.columns(5, gap="small")
    for col, (icon, label, value, sub) in zip(cols, kpis):
        col.markdown(
            f'<div class="kpi-card">'
            f'<span class="kpi-icon">{icon}</span>'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-sub">{sub}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Top-10 charts ──────────────────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        section("🥅", "Top 10 Scorers")
        top_goals = (
            df.groupby("player_name", as_index=False)["goals"]
            .sum()
            .nlargest(10, "goals")
            .sort_values("goals")
        )
        # Add position colour per player
        pos_map = df.drop_duplicates("player_name").set_index("player_name")["position"]
        top_goals["position"] = top_goals["player_name"].map(pos_map)
        top_goals["color"] = top_goals["position"].map(POSITION_COLORS)

        fig = go.Figure(go.Bar(
            x=top_goals["goals"],
            y=top_goals["player_name"],
            orientation="h",
            marker=dict(
                color=top_goals["color"],
                line=dict(color="rgba(0,0,0,0)", width=0),
            ),
            text=top_goals["goals"],
            textposition="outside",
            textfont=dict(color="#94a3b8", size=11),
            hovertemplate="<b>%{y}</b><br>Goals: %{x}<extra></extra>",
        ))
        fig = style(fig, height=380)
        fig.update_layout(xaxis_title="Goals", yaxis_title="", showlegend=False)
        chart_wrap(fig)

    with col2:
        section("⭐", "Top 10 by Rating")
        top_rating = (
            df.groupby("player_name", as_index=False)["rating"]
            .mean()
            .round(2)
            .nlargest(10, "rating")
            .sort_values("rating")
        )
        top_rating["position"] = top_rating["player_name"].map(pos_map)
        top_rating["color"] = top_rating["position"].map(POSITION_COLORS)

        fig2 = go.Figure(go.Bar(
            x=top_rating["rating"],
            y=top_rating["player_name"],
            orientation="h",
            marker=dict(color=top_rating["color"]),
            text=top_rating["rating"],
            textposition="outside",
            textfont=dict(color="#94a3b8", size=11),
            hovertemplate="<b>%{y}</b><br>Rating: %{x:.2f}<extra></extra>",
        ))
        fig2 = style(fig2, height=380)
        fig2.update_layout(xaxis_title="Avg Rating", yaxis_title="", showlegend=False,
                           xaxis=dict(range=[6, top_rating["rating"].max() + 0.3]))
        chart_wrap(fig2)

    # ── Goals trend by season ──────────────────────────────────────────────────
    section("📈", "Goals & Assists Trend by Season")
    season_agg = (
        df.groupby("season", as_index=False)
        .agg(Goals=("goals", "sum"), Assists=("assists", "sum"))
        .sort_values("season")
    )
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=season_agg["season"], y=season_agg["Goals"],
        mode="lines+markers+text", name="Goals",
        line=dict(color=ACCENT, width=3),
        marker=dict(size=10, color=ACCENT, line=dict(color="#0e1117", width=2)),
        text=season_agg["Goals"], textposition="top center",
        textfont=dict(color=ACCENT, size=12),
    ))
    fig_trend.add_trace(go.Scatter(
        x=season_agg["season"], y=season_agg["Assists"],
        mode="lines+markers+text", name="Assists",
        line=dict(color=ACCENT2, width=3),
        marker=dict(size=10, color=ACCENT2, line=dict(color="#0e1117", width=2)),
        text=season_agg["Assists"], textposition="bottom center",
        textfont=dict(color=ACCENT2, size=12),
    ))
    fig_trend = style(fig_trend, height=320)
    fig_trend.update_layout(xaxis_title="Season", yaxis_title="Total")
    chart_wrap(fig_trend)

    render_stats_table(df)


# ── Page 2: Player Analysis ────────────────────────────────────────────────────
def render_player_analysis(df: pd.DataFrame) -> None:
    hero("🔍", "Player Analysis", "Compare players head-to-head with radar charts and scatter insights.")
    st.markdown(DISCLAIMER, unsafe_allow_html=True)

    if empty_guard(df):
        return

    # ── Radar comparison ───────────────────────────────────────────────────────
    section("🕸️", "Player Comparison Radar")

    all_players     = sorted(df["player_name"].unique())
    default_players = all_players[:2] if len(all_players) >= 2 else all_players
    selected_players = st.multiselect(
        "Select 2–5 players to compare:",
        options=all_players,
        default=default_players,
        max_selections=5,
    )

    RADAR_STATS  = ["goals", "assists", "pass_accuracy", "rating", "shots_on_target", "minutes_played"]
    RADAR_LABELS = ["Goals", "Assists", "Pass Acc.", "Rating", "Shots on Target", "Minutes"]

    if len(selected_players) < 2:
        st.info("ℹ️ Select at least 2 players to display the radar chart.")
    else:
        player_df = df[df["player_name"].isin(selected_players)].groupby("player_name")[RADAR_STATS].mean()
        norm_df   = player_df.copy()
        for col in RADAR_STATS:
            lo, hi = player_df[col].min(), player_df[col].max()
            norm_df[col] = (player_df[col] - lo) / (hi - lo) if hi > lo else 0.5

        fig_radar = go.Figure()
        for i, player in enumerate(selected_players):
            if player not in norm_df.index:
                continue
            vals = norm_df.loc[player, RADAR_STATS].tolist() + norm_df.loc[player, RADAR_STATS].tolist()[:1]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals,
                theta=RADAR_LABELS + [RADAR_LABELS[0]],
                fill="toself",
                name=player,
                line=dict(color=CHART_COLORS[i % len(CHART_COLORS)], width=2),
                fillcolor=CHART_COLORS[i % len(CHART_COLORS)].replace("#", "rgba(") + ",0.12)",
                opacity=0.9,
            ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#0d1117",
                radialaxis=dict(visible=True, range=[0, 1], color="#475569",
                                gridcolor="#1e2a3a", linecolor="#1e2a3a"),
                angularaxis=dict(color="#94a3b8", gridcolor="#1e2a3a", linecolor="#1e2a3a"),
            ),
            showlegend=True,
        )
        fig_radar = style(fig_radar, height=500, legend_inside=False)
        chart_wrap(fig_radar)

        # Stats comparison table below radar
        st.markdown("<br>", unsafe_allow_html=True)
        comp_df = player_df.copy().round(2)
        comp_df.index.name = "Player"
        comp_df.columns = RADAR_LABELS
        st.dataframe(comp_df.reset_index(), use_container_width=True, hide_index=True)

    # ── Goals vs Assists scatter ───────────────────────────────────────────────
    section("🎯", "Goals vs Assists")
    fig_ga = px.scatter(
        df,
        x="goals", y="assists",
        color="position",
        size="rating", size_max=20,
        hover_data={"player_name": True, "team": True, "season": True,
                    "goals": True, "assists": True, "rating": True},
        labels={"goals": "Goals", "assists": "Assists", "position": "Position"},
        color_discrete_map=POSITION_COLORS,
    )
    fig_ga.update_traces(marker=dict(line=dict(width=1, color="#0e1117")))
    fig_ga = style(fig_ga, height=440)
    chart_wrap(fig_ga)

    # ── Shots vs Goals with trendline ─────────────────────────────────────────
    section("🔫", "Shots vs Goals (with Efficiency Trendline)")
    scatter_df = df[df["shots"] > 0].copy()
    fig_sg = px.scatter(
        scatter_df,
        x="shots", y="goals",
        color="position",
        hover_data={"player_name": True, "team": True, "season": True},
        labels={"shots": "Shots", "goals": "Goals", "position": "Position"},
        color_discrete_map=POSITION_COLORS,
    )
    fig_sg.update_traces(marker=dict(size=9, line=dict(width=1, color="#0e1117")))

    z      = np.polyfit(scatter_df["shots"], scatter_df["goals"], 1)
    p_line = np.poly1d(z)
    x_rng  = np.linspace(scatter_df["shots"].min(), scatter_df["shots"].max(), 120)
    fig_sg.add_trace(go.Scatter(
        x=x_rng, y=p_line(x_rng),
        mode="lines", name="Trend",
        line=dict(color=ACCENT, width=2.5, dash="dot"),
        hoverinfo="skip",
    ))
    fig_sg = style(fig_sg, height=440)
    chart_wrap(fig_sg)

    # ── Pass accuracy vs rating ───────────────────────────────────────────────
    section("📊", "Pass Accuracy vs Rating")
    fig_pr = px.scatter(
        df,
        x="pass_accuracy", y="rating",
        color="position",
        hover_data={"player_name": True, "team": True},
        labels={"pass_accuracy": "Pass Accuracy (%)", "rating": "Rating", "position": "Position"},
        color_discrete_map=POSITION_COLORS,
    )
    fig_pr.update_traces(marker=dict(size=8, line=dict(width=1, color="#0e1117")))
    fig_pr = style(fig_pr, height=400)
    chart_wrap(fig_pr)

    render_stats_table(df)


# ── Page 3: Team Analysis ──────────────────────────────────────────────────────
def render_team_analysis(df: pd.DataFrame) -> None:
    hero("🏟️", "Team Analysis", "Aggregate goals, assists and squad composition broken down by club.")
    st.markdown(DISCLAIMER, unsafe_allow_html=True)

    if empty_guard(df):
        return

    team_agg = (
        df.groupby("team", as_index=False)
        .agg(
            total_goals   =("goals",       "sum"),
            total_assists =("assists",      "sum"),
            avg_rating    =("rating",       "mean"),
            player_count  =("player_name",  "nunique"),
            total_minutes =("minutes_played","sum"),
        )
        .round({"avg_rating": 2})
        .sort_values("total_goals", ascending=False)
    )

    # ── KPI row for teams ──────────────────────────────────────────────────────
    best_team   = team_agg.iloc[0]["team"]
    most_goals  = int(team_agg.iloc[0]["total_goals"])
    best_rating = team_agg.loc[team_agg["avg_rating"].idxmax(), "team"]
    biggest_sq  = team_agg.loc[team_agg["player_count"].idxmax(), "team"]

    kpis = [
        ("🏆", "Top Scoring Club",    best_team,   f"{most_goals} goals"),
        ("⭐", "Highest Rated Club",  best_rating,  "by avg rating"),
        ("👥", "Largest Squad",       biggest_sq,   "by player count"),
        ("🔢", "Total Clubs",         str(team_agg["team"].nunique()), "in selection"),
    ]
    cols = st.columns(4, gap="small")
    for col, (icon, label, value, sub) in zip(cols, kpis):
        col.markdown(
            f'<div class="kpi-card">'
            f'<span class="kpi-icon">{icon}</span>'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value" style="font-size:18px;line-height:1.3">{value}</div>'
            f'<div class="kpi-sub">{sub}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Grouped bar ───────────────────────────────────────────────────────────
    section("⚽", "Goals & Assists per Team")
    ga_long = team_agg.melt(
        id_vars="team",
        value_vars=["total_goals", "total_assists"],
        var_name="metric", value_name="count",
    )
    ga_long["metric"] = ga_long["metric"].map({"total_goals": "Goals", "total_assists": "Assists"})
    fig_ga = px.bar(
        ga_long, x="team", y="count", color="metric", barmode="group",
        labels={"team": "Team", "count": "Count", "metric": ""},
        color_discrete_map={"Goals": ACCENT, "Assists": ACCENT2},
        text_auto=True,
    )
    fig_ga.update_traces(textfont_size=10, textangle=0,
                         marker_line_color="rgba(0,0,0,0)", textposition="outside")
    fig_ga.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    fig_ga = style(fig_ga, height=420)
    chart_wrap(fig_ga)

    col1, col2 = st.columns(2, gap="medium")

    # ── Stacked bar ───────────────────────────────────────────────────────────
    with col1:
        section("🎽", "Squad Composition")
        pos_team = (
            df.groupby(["team", "position"], as_index=False)["player_name"]
            .nunique()
            .rename(columns={"player_name": "count"})
        )
        fig_pos = px.bar(
            pos_team, x="team", y="count", color="position", barmode="stack",
            labels={"team": "Team", "count": "Players", "position": "Position"},
            color_discrete_map=POSITION_COLORS,
        )
        fig_pos.update_traces(marker_line_color="rgba(0,0,0,0)")
        fig_pos = style(fig_pos, height=380)
        chart_wrap(fig_pos)

    # ── Summary table ─────────────────────────────────────────────────────────
    with col2:
        section("📊", "Team Summary")
        st.dataframe(
            team_agg.rename(columns={
                "team":           "Team",
                "total_goals":    "Goals",
                "total_assists":  "Assists",
                "avg_rating":     "Avg Rating",
                "player_count":   "Players",
                "total_minutes":  "Minutes",
            }),
            use_container_width=True,
            height=380,
            hide_index=True,
        )

    # ── Avg rating per team ───────────────────────────────────────────────────
    section("⭐", "Average Rating by Team")
    rating_sorted = team_agg.sort_values("avg_rating", ascending=True)
    fig_rat = go.Figure(go.Bar(
        x=rating_sorted["avg_rating"],
        y=rating_sorted["team"],
        orientation="h",
        marker=dict(
            color=rating_sorted["avg_rating"],
            colorscale=[[0, "#1a3a2a"], [1, ACCENT]],
            showscale=False,
        ),
        text=rating_sorted["avg_rating"],
        textposition="outside",
        textfont=dict(size=11, color="#94a3b8"),
        hovertemplate="<b>%{y}</b><br>Avg Rating: %{x:.2f}<extra></extra>",
    ))
    fig_rat = style(fig_rat, height=360)
    fig_rat.update_layout(xaxis_title="Avg Rating", xaxis=dict(range=[6, 9.5]))
    chart_wrap(fig_rat)

    render_stats_table(df)


# ── Page 4: Position Analysis ──────────────────────────────────────────────────
def render_position_analysis(df: pd.DataFrame) -> None:
    hero("📐", "Position Analysis", "Drill into Goalkeepers, Defenders, Midfielders and Forwards.")
    st.markdown(DISCLAIMER, unsafe_allow_html=True)

    if empty_guard(df):
        return

    # ── Position KPI row ──────────────────────────────────────────────────────
    pos_agg = (
        df.groupby("position")
        .agg(count=("player_name","nunique"), goals=("goals","sum"), avg_rating=("rating","mean"))
        .round({"avg_rating": 2})
    )
    pos_order = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
    pos_icons = {"Goalkeeper": "🧤", "Defender": "🛡️", "Midfielder": "🎯", "Forward": "🚀"}

    cols = st.columns(4, gap="small")
    for col, pos in zip(cols, pos_order):
        if pos in pos_agg.index:
            row = pos_agg.loc[pos]
            col.markdown(
                f'<div class="kpi-card" style="border-color:{POSITION_COLORS[pos]}">'
                f'<span class="kpi-icon">{pos_icons[pos]}</span>'
                f'<div class="kpi-label" style="color:{POSITION_COLORS[pos]}">{pos}</div>'
                f'<div class="kpi-value" style="color:{POSITION_COLORS[pos]}">{int(row["count"])}</div>'
                f'<div class="kpi-sub">{int(row["goals"])} goals · {row["avg_rating"]} avg rating</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Box plot ──────────────────────────────────────────────────────────────
    section("⭐", "Rating Distribution by Position")
    fig_box = px.box(
        df, x="position", y="rating", color="position",
        points="outliers",
        category_orders={"position": pos_order},
        labels={"position": "Position", "rating": "Rating"},
        color_discrete_map=POSITION_COLORS,
    )
    fig_box.update_traces(
        marker=dict(size=5, opacity=0.6),
        line=dict(width=2),
        boxmean=True,
    )
    fig_box.update_layout(showlegend=False)
    fig_box = style(fig_box, height=380)
    chart_wrap(fig_box)

    # ── Side-by-side avg goals & avg assists ──────────────────────────────────
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        section("⚽", "Avg Goals by Position")
        avg_goals = (
            df.groupby("position", as_index=False)["goals"].mean().round(2)
            .sort_values("goals", ascending=False)
        )
        fig_ag = px.bar(
            avg_goals, x="position", y="goals", color="position",
            labels={"position": "Position", "goals": "Avg Goals"},
            color_discrete_map=POSITION_COLORS,
            text="goals",
            category_orders={"position": pos_order},
        )
        fig_ag.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0)")
        fig_ag.update_layout(showlegend=False)
        fig_ag = style(fig_ag, height=340)
        chart_wrap(fig_ag)

    with col2:
        section("🅰️", "Avg Assists by Position")
        avg_ast = (
            df.groupby("position", as_index=False)["assists"].mean().round(2)
            .sort_values("assists", ascending=False)
        )
        fig_aa = px.bar(
            avg_ast, x="position", y="assists", color="position",
            labels={"position": "Position", "assists": "Avg Assists"},
            color_discrete_map=POSITION_COLORS,
            text="assists",
            category_orders={"position": pos_order},
        )
        fig_aa.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0)")
        fig_aa.update_layout(showlegend=False)
        fig_aa = style(fig_aa, height=340)
        chart_wrap(fig_aa)

    # ── Position-specific spotlight cards ─────────────────────────────────────
    st.markdown("---")
    section("🔦", "Position Spotlight")

    c1, c2, c3, c4 = st.columns(4, gap="small")

    with c1:
        st.markdown(f'<p style="color:{POSITION_COLORS["Goalkeeper"]};font-weight:700;font-size:14px">🧤 Goalkeepers</p>', unsafe_allow_html=True)
        gk_df = df[df["position"] == "Goalkeeper"]
        if gk_df.empty:
            st.info("No Goalkeepers in filter.")
        else:
            gk_cs = gk_df.groupby("player_name", as_index=False)["clean_sheets"].sum().nlargest(8, "clean_sheets")
            gk_cs.columns = ["Player", "Clean Sheets"]
            st.metric("Avg Clean Sheets", round(gk_df["clean_sheets"].mean(), 1))
            st.dataframe(gk_cs, use_container_width=True, hide_index=True, height=260)

    with c2:
        st.markdown(f'<p style="color:{POSITION_COLORS["Defender"]};font-weight:700;font-size:14px">🛡️ Defenders</p>', unsafe_allow_html=True)
        def_df = df[df["position"] == "Defender"]
        if def_df.empty:
            st.info("No Defenders in filter.")
        else:
            def_pa = def_df.groupby("player_name", as_index=False)["pass_accuracy"].mean().round(1).nlargest(8, "pass_accuracy")
            def_pa.columns = ["Player", "Pass Acc. %"]
            st.metric("Avg Pass Acc.", f"{round(def_df['pass_accuracy'].mean(), 1)}%")
            st.dataframe(def_pa, use_container_width=True, hide_index=True, height=260)

    with c3:
        st.markdown(f'<p style="color:{POSITION_COLORS["Midfielder"]};font-weight:700;font-size:14px">🎯 Midfielders</p>', unsafe_allow_html=True)
        mid_df = df[df["position"] == "Midfielder"]
        if mid_df.empty:
            st.info("No Midfielders in filter.")
        else:
            mid_ast = mid_df.groupby("player_name", as_index=False)["assists"].sum().nlargest(8, "assists")
            mid_ast.columns = ["Player", "Assists"]
            st.metric("Avg Assists", round(mid_df["assists"].mean(), 1))
            st.dataframe(mid_ast, use_container_width=True, hide_index=True, height=260)

    with c4:
        st.markdown(f'<p style="color:{POSITION_COLORS["Forward"]};font-weight:700;font-size:14px">🚀 Forwards</p>', unsafe_allow_html=True)
        fwd_df = df[(df["position"] == "Forward") & (df["shots"] > 0)].copy()
        if fwd_df.empty:
            st.info("No Forwards with shots.")
        else:
            fwd_gps = (
                fwd_df.groupby("player_name", as_index=False)
                .agg(goals=("goals","sum"), shots=("shots","sum"))
                .assign(gps=lambda x: (x["goals"]/x["shots"]).round(3))
                .nlargest(8, "gps")
            )
            fwd_gps.columns = ["Player", "Goals", "Shots", "G/Shot"]
            st.metric("Avg Goals/Shot", round((fwd_df["goals"]/fwd_df["shots"]).mean(), 3))
            st.dataframe(fwd_gps, use_container_width=True, hide_index=True, height=260)

    render_stats_table(df)


# ── Main ───────────────────────────────────────────────────────────────────────
def main() -> None:
    raw_df = load_data()
    filtered_df, page = build_sidebar(raw_df)

    page_key = page.split("  ", 1)[-1].strip()   # strip icon prefix

    if page_key == "Overview":
        render_overview(filtered_df)
    elif page_key == "Player Analysis":
        render_player_analysis(filtered_df)
    elif page_key == "Team Analysis":
        render_team_analysis(filtered_df)
    elif page_key == "Position Analysis":
        render_position_analysis(filtered_df)


if __name__ == "__main__":
    main()
