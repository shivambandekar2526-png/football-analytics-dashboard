"""
app.py — Football Player Performance Analytics & Tactical Intelligence Platform
Synthetic data only. Does not represent real-world football results.
Run: streamlit run app.py
"""

import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from modules.ui_theme import (
    inject_custom_css,
    style_chart,
    render_hero,
    render_kpi,
    render_section_header,
    ACCENT_GREEN,
    ACCENT_CYAN,
    ACCENT_PURPLE,
    ACCENT_GOLD,
    ACCENT_RED,
    ACCENT_BLUE,
    POSITION_COLORS,
    POSITION_ICONS,
    COUNTRY_FLAGS,
    TEAM_COLORS,
    TEAM_BADGES,
    CHART_PALETTE,
    DISCLAIMER_HTML,
    hex_to_rgba,
)
from modules.pitch_board import (
    FORMATIONS,
    select_best_xi,
    render_best_xi_pitch,
)
from modules.scouting import (
    render_scouting_dossier,
    render_head_to_head_duel,
)
from modules.analytics import (
    enrich_dataset,
    render_finishing_efficiency_matrix,
    render_creative_playmaker_matrix,
    render_team_power_rankings,
)

# ── Page Configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Football Analytics Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Global Ultra-Modern CSS
inject_custom_css()


# ── Data Loading & Caching ─────────────────────────────────────────────────────
@st.cache_data
def load_and_enrich_data() -> pd.DataFrame:
    try:
        raw_df = pd.read_csv("football_players.csv")
    except FileNotFoundError:
        st.error(
            "⚠️ **football_players.csv not found.** "
            "Please run `python generate_data.py` to create the dataset, then refresh."
        )
        st.stop()

    num_cols = raw_df.select_dtypes(include="number").columns
    str_cols = raw_df.select_dtypes(include="object").columns
    raw_df[num_cols] = raw_df[num_cols].fillna(0)
    raw_df[str_cols] = raw_df[str_cols].fillna("Unknown")

    return enrich_dataset(raw_df)


# ── Helper Components ──────────────────────────────────────────────────────────
def render_stats_table(df: pd.DataFrame, title: str = "Player Statistics Registry") -> None:
    render_section_header("📋", title, "Interactive database view with full column sorting and filtering.")
    display_cols = [
        "player_name", "team", "position", "season", "age", "nationality",
        "appearances", "goals", "assists", "goal_contributions", "goals_per_90",
        "assists_per_90", "shots", "shots_on_target", "shot_accuracy",
        "minutes_played", "pass_accuracy", "rating",
        "yellow_cards", "red_cards", "clean_sheets",
    ]
    available_cols = [c for c in display_cols if c in df.columns]
    renamed = df[available_cols].sort_values("rating", ascending=False).reset_index(drop=True)

    # Format column names for presentation
    renamed.columns = [
        c.replace("_", " ").title().replace("Per 90", "/90").replace("Accuracy", "Acc %")
        for c in renamed.columns
    ]
    st.dataframe(renamed, use_container_width=True, height=420)


def empty_guard(df: pd.DataFrame) -> bool:
    if df.empty:
        st.warning("⚠️ No players match the current filters. Try widening your filter selection in the sidebar.")
        return True
    return False


# ── Sidebar & Global Filtering ─────────────────────────────────────────────────
def build_sidebar(df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
    with st.sidebar:
        # Brand identity
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="brand-badge">⚡ PRO EDITION</div>
                <h2>FOOTBALL ANALYTICS</h2>
                <p>Tactical Intelligence Platform</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<p class="sidebar-nav-title">Navigation</p>', unsafe_allow_html=True)
        nav_options = [
            "🏠  Overview & Pulse",
            "⚽  Tactical Pitch & Best XI",
            "🌟  Scouting Dossier",
            "🔍  Player Comparison & Duel",
            "🏟️  Team Analytics & Standings",
            "📐  Positional Deep-Dive",
        ]
        page = st.radio("navigation_menu", nav_options, label_visibility="collapsed")

        st.markdown("---")
        st.markdown('<p class="sidebar-nav-title">Metric Mode</p>', unsafe_allow_html=True)
        metric_mode = st.radio(
            "metric_mode",
            ["📊 Raw Season Totals", "⚡ Normalized Per 90 Mins"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown('<p class="sidebar-nav-title">Quick Preset Filters</p>', unsafe_allow_html=True)
        preset = st.selectbox(
            "Filter Presets",
            [
                "🌐 All Players",
                "⚡ Wonderkids (Age ≤ 22)",
                "👑 Prime Stars (Age 23–29)",
                "🛡️ Veterans (Age ≥ 30)",
                "⭐ Elite Tier (Rating ≥ 8.0)",
                "🥅 Goal Machines (Goals ≥ 10)",
            ],
            label_visibility="collapsed",
        )

        st.markdown('<p class="sidebar-nav-title">Granular Filters</p>', unsafe_allow_html=True)

        seasons   = sorted(df["season"].unique())
        teams     = sorted(df["team"].unique())
        positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]

        sel_seasons   = st.multiselect("📅 Seasons", seasons, default=seasons)
        sel_teams     = st.multiselect("🏟️ Clubs", teams, default=teams)
        sel_positions = st.multiselect("🎽 Positions", positions, default=positions)

        min_age, max_age = int(df["age"].min()), int(df["age"].max())
        sel_age = st.slider("🎂 Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

        min_mins = st.slider("⏱️ Min Minutes Played", min_value=0, max_value=3200, value=0, step=100)
        player_search = st.text_input("🔍 Search Player Name", placeholder="e.g. Luca Rossi")

        # ── Filter Application ──
        filtered = df.copy()

        # Preset rules
        if preset == "⚡ Wonderkids (Age ≤ 22)":
            filtered = filtered[filtered["age"] <= 22]
        elif preset == "👑 Prime Stars (Age 23–29)":
            filtered = filtered[(filtered["age"] >= 23) & (filtered["age"] <= 29)]
        elif preset == "🛡️ Veterans (Age ≥ 30)":
            filtered = filtered[filtered["age"] >= 30]
        elif preset == "⭐ Elite Tier (Rating ≥ 8.0)":
            filtered = filtered[filtered["rating"] >= 8.0]
        elif preset == "🥅 Goal Machines (Goals ≥ 10)":
            filtered = filtered[filtered["goals"] >= 10]

        # Granular rules
        mask = (
            filtered["season"].isin(sel_seasons or seasons)
            & filtered["team"].isin(sel_teams or teams)
            & filtered["position"].isin(sel_positions or positions)
            & (filtered["age"] >= sel_age[0])
            & (filtered["age"] <= sel_age[1])
            & (filtered["minutes_played"] >= min_mins)
        )
        filtered = filtered[mask]

        if player_search.strip():
            filtered = filtered[
                filtered["player_name"].str.contains(player_search.strip(), case=False, na=False)
            ]

        st.markdown("---")
        # Export Hub
        st.markdown('<p class="sidebar-nav-title">Export Intelligence</p>', unsafe_allow_html=True)
        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Filtered CSV",
            data=csv_bytes,
            file_name="football_analytics_filtered.csv",
            mime="text/csv",
        )

        json_bytes = filtered.to_json(orient="records", indent=2).encode("utf-8")
        st.download_button(
            label="📦 Export Filtered JSON",
            data=json_bytes,
            file_name="football_analytics_filtered.json",
            mime="application/json",
        )

        st.markdown(
            f"""
            <div style="background:#111827; border:1px solid #1F293D; border-radius:8px; padding:10px; text-align:center; margin-top:12px;">
                <span style="color:#00FF87; font-weight:800; font-size:1.1rem;">{len(filtered):,}</span>
                <span style="color:#94A3B8; font-size:0.75rem; display:block;">Active Match Records</span>
                <span style="color:#64748B; font-size:0.7rem;">{filtered['player_name'].nunique()} unique players</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return filtered, page, metric_mode


# ── Page 1: Overview & Pulse ───────────────────────────────────────────────────
def render_overview(df: pd.DataFrame, metric_mode: str) -> None:
    render_hero(
        "⚽",
        "Overview & League Pulse",
        "High-altitude performance telemetry, league milestones, top scorers, and season momentum.",
        f"{df['player_name'].nunique()} Active Athletes",
    )
    st.markdown(DISCLAIMER_HTML, unsafe_allow_html=True)

    if empty_guard(df):
        return

    # ── KPI Cards Row (6 Cards) ──
    tot_players = df["player_name"].nunique()
    tot_goals   = int(df["goals"].sum())
    tot_assists = int(df["assists"].sum())
    tot_contrib = int(df["goal_contributions"].sum())
    tot_minutes = int(df["minutes_played"].sum())
    avg_rating  = round(float(df["rating"].mean()), 2)
    top_scorer  = df.groupby("player_name")["goals"].sum().idxmax()
    top_scorer_goals = int(df.groupby("player_name")["goals"].sum().max())

    c1, c2, c3, c4, c5, c6 = st.columns(6, gap="small")
    with c1:
        render_kpi("👤", "Unique Players", f"{tot_players:,}", f"across {df['team'].nunique()} clubs", ACCENT_GREEN)
    with c2:
        render_kpi("⚽", "Total Goals", f"{tot_goals:,}", f"Top: {top_scorer.split()[0]} ({top_scorer_goals})", ACCENT_GREEN)
    with c3:
        render_kpi("🅰️", "Total Assists", f"{tot_assists:,}", f"avg {(tot_assists/max(1, tot_players)):.1f}/player", ACCENT_CYAN)
    with c4:
        render_kpi("🔥", "Goal Contrib.", f"{tot_contrib:,}", "Goals + Assists combined", ACCENT_PURPLE)
    with c5:
        render_kpi("⏱️", "Minutes Played", f"{tot_minutes:,}", f"avg {(tot_minutes/max(1, len(df))):.0f} m/row", ACCENT_BLUE)
    with c6:
        render_kpi("⭐", "Average Rating", f"{avg_rating}", "scale 5.0 - 10.0", ACCENT_GOLD)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Top Performers Chart Grid ──
    col1, col2, col3 = st.columns(3, gap="medium")

    # Mapping of positions for bar coloring
    pos_map = df.drop_duplicates("player_name").set_index("player_name")["position"]

    with col1:
        render_section_header("🥅", "Top 10 Scorers", "Highest total goals in selection")
        top_goals = (
            df.groupby("player_name", as_index=False)["goals"]
            .sum()
            .nlargest(10, "goals")
            .sort_values("goals")
        )
        top_goals["position"] = top_goals["player_name"].map(pos_map)
        top_goals["color"] = top_goals["position"].map(POSITION_COLORS)

        fig_tg = go.Figure(go.Bar(
            x=top_goals["goals"],
            y=top_goals["player_name"],
            orientation="h",
            marker=dict(color=top_goals["color"], line=dict(width=0)),
            text=top_goals["goals"],
            textposition="outside",
            textfont=dict(color="#CBD5E1", size=11),
            hovertemplate="<b>%{y}</b><br>Goals: <b>%{x}</b><extra></extra>",
        ))
        fig_tg = style_chart(fig_tg, height=360, show_legend=False)
        fig_tg.update_layout(xaxis_title="Goals Scored", yaxis_title="")
        st.plotly_chart(fig_tg, use_container_width=True)

    with col2:
        render_section_header("⭐", "Top 10 by Rating", "Highest average match performance rating")
        top_rat = (
            df.groupby("player_name", as_index=False)["rating"]
            .mean()
            .round(2)
            .nlargest(10, "rating")
            .sort_values("rating")
        )
        top_rat["position"] = top_rat["player_name"].map(pos_map)
        top_rat["color"] = top_rat["position"].map(POSITION_COLORS)

        fig_tr = go.Figure(go.Bar(
            x=top_rat["rating"],
            y=top_rat["player_name"],
            orientation="h",
            marker=dict(color=top_rat["color"], line=dict(width=0)),
            text=top_rat["rating"],
            textposition="outside",
            textfont=dict(color="#CBD5E1", size=11),
            hovertemplate="<b>%{y}</b><br>Rating: <b>%{x:.2f} ⭐</b><extra></extra>",
        ))
        fig_tr = style_chart(fig_tr, height=360, show_legend=False)
        fig_tr.update_layout(xaxis_title="Avg Rating", yaxis_title="", xaxis=dict(range=[6, 9.8]))
        st.plotly_chart(fig_tr, use_container_width=True)

    with col3:
        render_section_header("🅰️", "Top 10 Playmakers", "Highest total assists provided")
        top_ast = (
            df.groupby("player_name", as_index=False)["assists"]
            .sum()
            .nlargest(10, "assists")
            .sort_values("assists")
        )
        top_ast["position"] = top_ast["player_name"].map(pos_map)
        top_ast["color"] = top_ast["position"].map(POSITION_COLORS)

        fig_ta = go.Figure(go.Bar(
            x=top_ast["assists"],
            y=top_ast["player_name"],
            orientation="h",
            marker=dict(color=ACCENT_CYAN, line=dict(width=0)),
            text=top_ast["assists"],
            textposition="outside",
            textfont=dict(color="#CBD5E1", size=11),
            hovertemplate="<b>%{y}</b><br>Assists: <b>%{x}</b><extra></extra>",
        ))
        fig_ta = style_chart(fig_ta, height=360, show_legend=False)
        fig_ta.update_layout(xaxis_title="Assists Provided", yaxis_title="")
        st.plotly_chart(fig_ta, use_container_width=True)

    # ── Season Trajectory ──
    render_section_header("📈", "Goals & Assists Season Trajectory", "Year-over-year aggregate production trend")
    season_agg = (
        df.groupby("season", as_index=False)
        .agg(Goals=("goals", "sum"), Assists=("assists", "sum"), AvgRating=("rating", "mean"))
        .sort_values("season")
    )
    fig_st = go.Figure()
    fig_st.add_trace(go.Scatter(
        x=season_agg["season"], y=season_agg["Goals"],
        mode="lines+markers+text", name="Total Goals",
        line=dict(color=ACCENT_GREEN, width=3.5),
        marker=dict(size=10, color=ACCENT_GREEN, line=dict(color="#0A0E17", width=2)),
        text=season_agg["Goals"], textposition="top center",
        textfont=dict(color=ACCENT_GREEN, size=12, family="Plus Jakarta Sans"),
    ))
    fig_st.add_trace(go.Scatter(
        x=season_agg["season"], y=season_agg["Assists"],
        mode="lines+markers+text", name="Total Assists",
        line=dict(color=ACCENT_CYAN, width=3.5),
        marker=dict(size=10, color=ACCENT_CYAN, line=dict(color="#0A0E17", width=2)),
        text=season_agg["Assists"], textposition="bottom center",
        textfont=dict(color=ACCENT_CYAN, size=12, family="Plus Jakarta Sans"),
    ))
    fig_st = style_chart(fig_st, height=320)
    fig_st.update_layout(xaxis_title="Season", yaxis_title="Total Output")
    st.plotly_chart(fig_st, use_container_width=True)

    render_stats_table(df)


# ── Page 2: Tactical Pitch & Best XI (NEW) ─────────────────────────────────────
def render_tactical_pitch_page(df: pd.DataFrame) -> None:
    render_hero(
        "⚽",
        "Tactical Pitch & Best XI",
        "Interactive virtual pitch board displaying the highest-rated Dream Team in your preferred tactical formation.",
        "Opta Tactical Engine",
    )
    st.markdown(DISCLAIMER_HTML, unsafe_allow_html=True)

    if empty_guard(df):
        return

    col_ctrl, col_info = st.columns([1, 2], gap="medium")
    with col_ctrl:
        formation_name = st.selectbox(
            "Select Tactical Formation",
            list(FORMATIONS.keys()),
            index=0,
        )

    slots_data, squad_df = select_best_xi(df, formation_name)

    # Best XI Squad KPIs
    if not squad_df.empty:
        sq_rating = round(float(squad_df["rating"].mean()), 2)
        sq_goals  = int(squad_df["goals"].sum())
        sq_assists= int(squad_df["assists"].sum())
        sq_age    = round(float(squad_df["age"].mean()), 1)

        with col_info:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Squad Avg Rating", f"★ {sq_rating}")
            c2.metric("Total Goals", f"{sq_goals} ⚽")
            c3.metric("Total Assists", f"{sq_assists} 🅰️")
            c4.metric("Average Squad Age", f"{sq_age} yrs")

    # Render pitch
    pitch_fig = render_best_xi_pitch(slots_data, formation_name)
    st.plotly_chart(pitch_fig, use_container_width=True)

    # Squad Roster Sheet
    render_section_header("📋", f"Best XI Starting Lineup ({formation_name})", "Selected purely on match rating merit from filtered data.")
    if not squad_df.empty:
        roster_disp = squad_df[[
            "tactical_role", "player_name", "position", "team", "nationality",
            "age", "rating", "goals", "assists", "clean_sheets", "pass_accuracy"
        ]].rename(columns={
            "tactical_role": "Role",
            "player_name": "Player Name",
            "position": "Position",
            "team": "Club",
            "nationality": "Nation",
            "age": "Age",
            "rating": "Rating",
            "goals": "Goals",
            "assists": "Assists",
            "clean_sheets": "Clean Sheets",
            "pass_accuracy": "Pass Acc %",
        })
        st.dataframe(roster_disp, use_container_width=True, hide_index=True)


# ── Page 3: Player Scouting Dossier (NEW) ──────────────────────────────────────
def render_scouting_page(df: pd.DataFrame) -> None:
    render_hero(
        "🌟",
        "Player Scouting Dossier",
        "EA FC style scouting dossier, comprehensive radar benchmarks against positional peers, and career form trajectory.",
        "Scout Pro 360",
    )
    st.markdown(DISCLAIMER_HTML, unsafe_allow_html=True)

    if empty_guard(df):
        return

    all_players = sorted(df["player_name"].unique())
    # Find highest rated player as default
    top_p = df.groupby("player_name")["rating"].mean().idxmax()
    def_idx = all_players.index(top_p) if top_p in all_players else 0

    selected_player = st.selectbox("Select Player to Inspect", all_players, index=def_idx)

    render_scouting_dossier(df, selected_player)


# ── Page 4: Player Comparison & Duel ───────────────────────────────────────────
def render_player_comparison_page(df: pd.DataFrame, metric_mode: str) -> None:
    render_hero(
        "🔍",
        "Player Comparison & Head-to-Head Duel",
        "Engage in 1-on-1 battle duels or multi-player radar comparisons with statistical scatter efficiency regressions.",
        "Combat Analytics",
    )
    st.markdown(DISCLAIMER_HTML, unsafe_allow_html=True)

    if empty_guard(df):
        return

    tab_duel, tab_multi = st.tabs(["⚔️ Head-to-Head Duel (1v1)", "🕸️ Multi-Player Radar & Scatter Intelligence"])

    all_players = sorted(df["player_name"].unique())

    # ── Tab 1: Head-to-Head Duel ──
    with tab_duel:
        render_section_header("⚔️", "Head-to-Head Player Duel Arena")
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            p1 = st.selectbox("Select Contender 1", all_players, index=0, key="duel_p1")
        with c2:
            p2 = st.selectbox("Select Contender 2", all_players, index=min(1, len(all_players)-1), key="duel_p2")

        if p1 == p2:
            st.info("ℹ️ Select two different players to see the head-to-head battle.")
        else:
            render_head_to_head_duel(df, p1, p2)

    # ── Tab 2: Multi-Player Radar & Scatter Intelligence ──
    with tab_multi:
        render_section_header("🕸️", "Multi-Player Normalized Radar Comparison")
        default_players = all_players[:3] if len(all_players) >= 3 else all_players
        comp_players = st.multiselect(
            "Select 2 to 5 players to compare on the radar:",
            options=all_players,
            default=default_players,
            max_selections=5,
        )

        RADAR_STATS  = ["goals", "assists", "pass_accuracy", "rating", "shots_on_target", "minutes_played"]
        RADAR_LABELS = ["Goals", "Assists", "Pass Acc %", "Match Rating", "Shots on Target", "Minutes"]

        if len(comp_players) < 2:
            st.info("ℹ️ Select at least 2 players to generate the comparative radar chart.")
        else:
            player_df = df[df["player_name"].isin(comp_players)].groupby("player_name")[RADAR_STATS].mean()
            norm_df   = player_df.copy()
            for col in RADAR_STATS:
                lo, hi = player_df[col].min(), player_df[col].max()
                norm_df[col] = (player_df[col] - lo) / (hi - lo) if hi > lo else 0.5

            fig_radar = go.Figure()
            for i, p in enumerate(comp_players):
                if p not in norm_df.index:
                    continue
                vals = norm_df.loc[p, RADAR_STATS].tolist() + norm_df.loc[p, RADAR_STATS].tolist()[:1]
                p_color = CHART_PALETTE[i % len(CHART_PALETTE)]
                fig_radar.add_trace(go.Scatterpolar(
                    r=vals,
                    theta=RADAR_LABELS + [RADAR_LABELS[0]],
                    fill="toself",
                    name=p,
                    line=dict(color=p_color, width=2.5),
                    fillcolor=hex_to_rgba(p_color, 0.14),
                ))

            fig_radar.update_layout(
                polar=dict(
                    bgcolor="#0D131F",
                    radialaxis=dict(visible=True, range=[0, 1], color="#475569", gridcolor="#1F293D"),
                    angularaxis=dict(color="#94A3B8", gridcolor="#1F293D"),
                ),
                showlegend=True,
            )
            fig_radar = style_chart(fig_radar, height=480, legend_inside=False)
            st.plotly_chart(fig_radar, use_container_width=True)

            # Comparative table
            comp_table = player_df.copy().round(2)
            comp_table.index.name = "Player"
            comp_table.columns = RADAR_LABELS
            st.dataframe(comp_table.reset_index(), use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Goals vs Assists Scatter ──
        render_section_header("🎯", "Goals vs Assists Correlation", "Sized by match rating and colored by position.")
        fig_ga = px.scatter(
            df,
            x="goals", y="assists",
            color="position",
            size="rating", size_max=22,
            hover_name="player_name",
            hover_data={"team": True, "season": True, "goals": True, "assists": True, "rating": ":.2f", "position": False},
            labels={"goals": "Goals Scored", "assists": "Assists Provided", "position": "Position"},
            color_discrete_map=POSITION_COLORS,
        )
        fig_ga.update_traces(marker=dict(line=dict(width=1.5, color="#0A0E17")))
        fig_ga = style_chart(fig_ga, height=440)
        st.plotly_chart(fig_ga, use_container_width=True)

        # ── Shots vs Goals with Trendline ──
        render_section_header("🔫", "Shots vs Goals (Finishing Efficiency Regression)")
        scatter_df = df[df["shots"] > 0].copy()
        fig_sg = px.scatter(
            scatter_df,
            x="shots", y="goals",
            color="position",
            hover_name="player_name",
            hover_data={"team": True, "season": True, "shots": True, "goals": True, "shot_conversion": ":.1f%"},
            labels={"shots": "Total Shots", "goals": "Goals Scored", "position": "Position"},
            color_discrete_map=POSITION_COLORS,
        )
        fig_sg.update_traces(marker=dict(size=9, line=dict(width=1, color="#0A0E17")))

        # Regression line
        if len(scatter_df) >= 2:
            z = np.polyfit(scatter_df["shots"], scatter_df["goals"], 1)
            p_line = np.poly1d(z)
            x_rng = np.linspace(scatter_df["shots"].min(), scatter_df["shots"].max(), 100)
            fig_sg.add_trace(go.Scatter(
                x=x_rng, y=p_line(x_rng),
                mode="lines", name="Efficiency Trend",
                line=dict(color=ACCENT_GREEN, width=2.5, dash="dot"),
                hoverinfo="skip",
            ))
        fig_sg = style_chart(fig_sg, height=440)
        st.plotly_chart(fig_sg, use_container_width=True)

        # ── Finishing Efficiency Quadrant Matrix (NEW) ──
        render_section_header("📊", "Finishing Efficiency Quadrants (Shots vs Conversion Rate)")
        fig_fin = render_finishing_efficiency_matrix(df)
        st.plotly_chart(fig_fin, use_container_width=True)

        # ── Pass Accuracy vs Rating Scatter ──
        render_section_header("📐", "Pass Accuracy vs Match Rating Distribution")
        fig_pr = px.scatter(
            df,
            x="pass_accuracy", y="rating",
            color="position",
            hover_name="player_name",
            hover_data={"team": True, "pass_accuracy": ":.1f%", "rating": ":.2f"},
            labels={"pass_accuracy": "Pass Accuracy (%)", "rating": "Rating", "position": "Position"},
            color_discrete_map=POSITION_COLORS,
        )
        fig_pr.update_traces(marker=dict(size=8, line=dict(width=1, color="#0A0E17")))
        fig_pr = style_chart(fig_pr, height=400)
        st.plotly_chart(fig_pr, use_container_width=True)

    render_stats_table(df)


# ── Page 5: Team Analytics & Standings ─────────────────────────────────────────
def render_team_analytics_page(df: pd.DataFrame, metric_mode: str) -> None:
    render_hero(
        "🏟️",
        "Team Analytics & Power Rankings",
        "Club attacking potency, squad composition, attacking vs defensive dominance matrix, and fair play leaderboard.",
        f"{df['team'].nunique()} Competing Clubs",
    )
    st.markdown(DISCLAIMER_HTML, unsafe_allow_html=True)

    if empty_guard(df):
        return

    team_agg = (
        df.groupby("team", as_index=False)
        .agg(
            total_goals=("goals", "sum"),
            total_assists=("assists", "sum"),
            avg_rating=("rating", "mean"),
            player_count=("player_name", "nunique"),
            total_minutes=("minutes_played", "sum"),
            clean_sheets=("clean_sheets", "sum"),
            yellow_cards=("yellow_cards", "sum"),
            red_cards=("red_cards", "sum"),
        )
        .round({"avg_rating": 2})
        .sort_values("total_goals", ascending=False)
    )

    # ── Team KPI Cards (4 Cards) ──
    best_scoring_club = team_agg.iloc[0]["team"]
    best_goals_count  = int(team_agg.iloc[0]["total_goals"])
    highest_rated_club= team_agg.loc[team_agg["avg_rating"].idxmax(), "team"]
    highest_rating_val= team_agg["avg_rating"].max()
    most_clean_sheets_club = team_agg.loc[team_agg["clean_sheets"].idxmax(), "team"]
    clean_sheets_val  = int(team_agg["clean_sheets"].max())

    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        render_kpi("🏆", "Top Scoring Club", best_scoring_club, f"{best_goals_count} total goals scored", ACCENT_GREEN)
    with c2:
        render_kpi("⭐", "Highest Rated Club", highest_rated_club, f"★ {highest_rating_val:.2f} avg rating", ACCENT_GOLD)
    with c3:
        render_kpi("🛡️", "Defensive Wall", most_clean_sheets_club, f"{clean_sheets_val} clean sheets registered", ACCENT_BLUE)
    with c4:
        render_kpi("🔢", "Total Active Clubs", str(team_agg["team"].nunique()), "in current filtered pool", ACCENT_PURPLE)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Goals & Assists per Team ──
    render_section_header("⚽", "Goals & Assists Production per Club")
    ga_melted = team_agg.melt(
        id_vars="team",
        value_vars=["total_goals", "total_assists"],
        var_name="metric", value_name="count",
    )
    ga_melted["metric"] = ga_melted["metric"].map({"total_goals": "Goals", "total_assists": "Assists"})
    fig_ga = px.bar(
        ga_melted, x="team", y="count", color="metric", barmode="group",
        labels={"team": "Club", "count": "Count", "metric": ""},
        color_discrete_map={"Goals": ACCENT_GREEN, "Assists": ACCENT_CYAN},
        text_auto=True,
    )
    fig_ga.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0)")
    fig_ga = style_chart(fig_ga, height=420)
    st.plotly_chart(fig_ga, use_container_width=True)

    # ── Squad Composition & Avg Rating ──
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        render_section_header("🎽", "Squad Composition by Position")
        pos_team = (
            df.groupby(["team", "position"], as_index=False)["player_name"]
            .nunique()
            .rename(columns={"player_name": "count"})
        )
        fig_pos = px.bar(
            pos_team, x="team", y="count", color="position", barmode="stack",
            labels={"team": "Club", "count": "Players", "position": "Position"},
            color_discrete_map=POSITION_COLORS,
        )
        fig_pos = style_chart(fig_pos, height=380)
        st.plotly_chart(fig_pos, use_container_width=True)

    with col2:
        render_section_header("⭐", "Average Match Rating by Club")
        rat_sorted = team_agg.sort_values("avg_rating", ascending=True)
        fig_rat = go.Figure(go.Bar(
            x=rat_sorted["avg_rating"],
            y=rat_sorted["team"],
            orientation="h",
            marker=dict(
                color=rat_sorted["avg_rating"],
                colorscale=[[0, "#162033"], [1, ACCENT_GREEN]],
                showscale=False,
            ),
            text=rat_sorted["avg_rating"],
            textposition="outside",
            textfont=dict(color="#CBD5E1", size=11),
            hovertemplate="<b>%{y}</b><br>Rating: <b>%{x:.2f} ⭐</b><extra></extra>",
        ))
        fig_rat = style_chart(fig_rat, height=380, show_legend=False)
        fig_rat.update_layout(xaxis=dict(range=[6.0, 9.2]))
        st.plotly_chart(fig_rat, use_container_width=True)

    # ── Team Power Rankings & Discipline Matrix (NEW) ──
    render_team_power_rankings(df)


# ── Page 6: Positional Deep-Dive ───────────────────────────────────────────────
def render_positional_deep_dive_page(df: pd.DataFrame) -> None:
    render_hero(
        "📐",
        "Positional Deep-Dive",
        "Granular positional role analysis, rating distributions, and specialized positional leaderboards.",
        "Role Specialization",
    )
    st.markdown(DISCLAIMER_HTML, unsafe_allow_html=True)

    if empty_guard(df):
        return

    pos_agg = (
        df.groupby("position")
        .agg(
            count=("player_name", "nunique"),
            goals=("goals", "sum"),
            assists=("assists", "sum"),
            avg_rating=("rating", "mean"),
        )
        .round({"avg_rating": 2})
    )
    pos_order = ["Goalkeeper", "Defender", "Midfielder", "Forward"]

    # ── 4 Position KPI Cards ──
    c1, c2, c3, c4 = st.columns(4, gap="small")
    cols = [c1, c2, c3, c4]
    for col, pos in zip(cols, pos_order):
        if pos in pos_agg.index:
            p_row = pos_agg.loc[pos]
            with col:
                render_kpi(
                    POSITION_ICONS.get(pos, "⚽"),
                    pos,
                    f"{int(p_row['count'])} Players",
                    f"{int(p_row['goals'])} G · {int(p_row['assists'])} A · ★ {p_row['avg_rating']}",
                    POSITION_COLORS[pos],
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Rating Distribution Box Plot ──
    render_section_header("⭐", "Performance Rating Distribution by Position")
    fig_box = px.box(
        df, x="position", y="rating", color="position",
        points="outliers",
        category_orders={"position": pos_order},
        labels={"position": "Position", "rating": "Match Rating"},
        color_discrete_map=POSITION_COLORS,
    )
    fig_box.update_traces(boxmean=True, marker=dict(size=5, opacity=0.7))
    fig_box = style_chart(fig_box, height=380, show_legend=False)
    st.plotly_chart(fig_box, use_container_width=True)

    # ── Avg Goals & Avg Assists by Position ──
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        render_section_header("⚽", "Average Goals by Position")
        avg_g = (
            df.groupby("position", as_index=False)["goals"].mean().round(2)
            .sort_values("goals", ascending=False)
        )
        fig_ag = px.bar(
            avg_g, x="position", y="goals", color="position",
            labels={"position": "Position", "goals": "Avg Goals"},
            color_discrete_map=POSITION_COLORS,
            text="goals",
            category_orders={"position": pos_order},
        )
        fig_ag.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0)")
        fig_ag = style_chart(fig_ag, height=340, show_legend=False)
        st.plotly_chart(fig_ag, use_container_width=True)

    with col2:
        render_section_header("🅰️", "Average Assists by Position")
        avg_a = (
            df.groupby("position", as_index=False)["assists"].mean().round(2)
            .sort_values("assists", ascending=False)
        )
        fig_aa = px.bar(
            avg_a, x="position", y="assists", color="position",
            labels={"position": "Position", "assists": "Avg Assists"},
            color_discrete_map=POSITION_COLORS,
            text="assists",
            category_orders={"position": pos_order},
        )
        fig_aa.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0)")
        fig_aa = style_chart(fig_aa, height=340, show_legend=False)
        st.plotly_chart(fig_aa, use_container_width=True)

    # ── Positional Benchmark Radar (NEW) ──
    render_section_header("🕸️", "Positional Benchmark Profile", "Comparative average attribute footprint for each pitch zone.")
    pos_metrics = (
        df.groupby("position")
        .agg(
            rating=("rating", "mean"),
            pass_acc=("pass_accuracy", "mean"),
            goals=("goals", "mean"),
            assists=("assists", "mean"),
            shots=("shots", "mean"),
        )
        .round(2)
    )

    # Normalize each column across positions
    norm_pos = pos_metrics.copy()
    for col in norm_pos.columns:
        mx = pos_metrics[col].max()
        norm_pos[col] = (pos_metrics[col] / mx) if mx > 0 else 0.5

    radar_cats = ["Rating", "Pass Acc", "Goals", "Assists", "Shots"]
    fig_pos_radar = go.Figure()
    for pos in pos_order:
        if pos in norm_pos.index:
            row_vals = norm_pos.loc[pos].tolist() + norm_pos.loc[pos].tolist()[:1]
            fig_pos_radar.add_trace(go.Scatterpolar(
                r=row_vals,
                theta=radar_cats + [radar_cats[0]],
                fill="toself",
                name=pos,
                line=dict(color=POSITION_COLORS[pos], width=2),
                fillcolor=hex_to_rgba(POSITION_COLORS[pos], 0.12),
            ))
    fig_pos_radar.update_layout(
        polar=dict(
            bgcolor="#0D131F",
            radialaxis=dict(visible=True, range=[0, 1.1], color="#475569", gridcolor="#1F293D"),
            angularaxis=dict(color="#94A3B8", gridcolor="#1F293D"),
        ),
        showlegend=True,
    )
    fig_pos_radar = style_chart(fig_pos_radar, height=420, legend_inside=False)
    st.plotly_chart(fig_pos_radar, use_container_width=True)

    # ── Specialized Position Spotlights ──
    render_section_header("🔦", "Position Spotlights & Specialists", "Role-specific performance masters")
    sp1, sp2, sp3, sp4 = st.columns(4, gap="small")

    with sp1:
        st.markdown(f'<p style="color:{POSITION_COLORS["Goalkeeper"]}; font-weight:800; font-size:14px;">🧤 Goalkeeper Fortress</p>', unsafe_allow_html=True)
        gk_df = df[df["position"] == "Goalkeeper"]
        if gk_df.empty:
            st.info("No Goalkeepers in current selection.")
        else:
            gk_top = gk_df.groupby("player_name", as_index=False)["clean_sheets"].sum().nlargest(8, "clean_sheets")
            gk_top.columns = ["Player", "Clean Sheets"]
            st.metric("Avg Clean Sheets", round(gk_df["clean_sheets"].mean(), 1))
            st.dataframe(gk_top, use_container_width=True, hide_index=True, height=260)

    with sp2:
        st.markdown(f'<p style="color:{POSITION_COLORS["Defender"]}; font-weight:800; font-size:14px;">🛡️ Defensive Architects</p>', unsafe_allow_html=True)
        def_df = df[df["position"] == "Defender"]
        if def_df.empty:
            st.info("No Defenders in current selection.")
        else:
            def_top = def_df.groupby("player_name", as_index=False)["pass_accuracy"].mean().round(1).nlargest(8, "pass_accuracy")
            def_top.columns = ["Player", "Pass Acc %"]
            st.metric("Avg Pass Accuracy", f"{round(def_df['pass_accuracy'].mean(), 1)}%")
            st.dataframe(def_top, use_container_width=True, hide_index=True, height=260)

    with sp3:
        st.markdown(f'<p style="color:{POSITION_COLORS["Midfielder"]}; font-weight:800; font-size:14px;">🎯 Midfield Virtuosos</p>', unsafe_allow_html=True)
        mid_df = df[df["position"] == "Midfielder"]
        if mid_df.empty:
            st.info("No Midfielders in current selection.")
        else:
            mid_top = mid_df.groupby("player_name", as_index=False)["assists"].sum().nlargest(8, "assists")
            mid_top.columns = ["Player", "Assists"]
            st.metric("Avg Assists", round(mid_df["assists"].mean(), 1))
            st.dataframe(mid_top, use_container_width=True, hide_index=True, height=260)

    with sp4:
        st.markdown(f'<p style="color:{POSITION_COLORS["Forward"]}; font-weight:800; font-size:14px;">🚀 Clinical Marksmen</p>', unsafe_allow_html=True)
        fwd_df = df[(df["position"] == "Forward") & (df["shots"] > 0)].copy()
        if fwd_df.empty:
            st.info("No Forwards with shots.")
        else:
            fwd_top = (
                fwd_df.groupby("player_name", as_index=False)
                .agg(goals=("goals", "sum"), shots=("shots", "sum"))
                .assign(conv=lambda x: (x["goals"] / x["shots"] * 100).round(1))
                .nlargest(8, "conv")
            )
            fwd_top.columns = ["Player", "Goals", "Shots", "Conv %"]
            st.metric("Avg Conversion Rate", f"{round((fwd_df['goals'].sum() / max(1, fwd_df['shots'].sum())) * 100, 1)}%")
            st.dataframe(fwd_top, use_container_width=True, hide_index=True, height=260)

    render_stats_table(df)


# ── Main Application Router ────────────────────────────────────────────────────
def main() -> None:
    raw_df = load_and_enrich_data()
    filtered_df, page, metric_mode = build_sidebar(raw_df)

    page_clean = page.split("  ", 1)[-1].strip()

    if "Overview" in page_clean:
        render_overview(filtered_df, metric_mode)
    elif "Tactical Pitch" in page_clean:
        render_tactical_pitch_page(filtered_df)
    elif "Scouting Dossier" in page_clean:
        render_scouting_page(filtered_df)
    elif "Player Comparison" in page_clean:
        render_player_comparison_page(filtered_df, metric_mode)
    elif "Team Analytics" in page_clean:
        render_team_analytics_page(filtered_df, metric_mode)
    elif "Positional" in page_clean:
        render_positional_deep_dive_page(filtered_df)


if __name__ == "__main__":
    main()
