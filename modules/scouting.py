"""
modules/scouting.py
Player Scouting Dossier, EA FC Style Attributes Card, and Head-to-Head Duel Engine.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from modules.ui_theme import (
    POSITION_COLORS,
    COUNTRY_FLAGS,
    TEAM_BADGES,
    ACCENT_GREEN,
    ACCENT_CYAN,
    ACCENT_PURPLE,
    ACCENT_GOLD,
    ACCENT_RED,
    BORDER_SUBTLE,
    style_chart,
    hex_to_rgba,
)


def compute_player_attributes(player_df: pd.DataFrame, position_df: pd.DataFrame) -> dict:
    """Computes FIFA-style 0-99 scaled attributes for a player relative to positional peers."""
    # Summary of target player
    tot_goals   = player_df["goals"].sum()
    tot_assists = player_df["assists"].sum()
    tot_shots   = player_df["shots"].sum()
    tot_sot     = player_df["shots_on_target"].sum()
    tot_mins    = player_df["minutes_played"].sum()
    avg_pass    = player_df["pass_accuracy"].mean()
    avg_rating  = player_df["rating"].mean()
    tot_cards   = player_df["yellow_cards"].sum() + (player_df["red_cards"].sum() * 2)
    tot_cs      = player_df["clean_sheets"].sum()

    # Calculate 0-99 scaled metrics
    rating_score = int(np.clip((avg_rating - 5.0) / 4.5 * 100, 50, 99))
    pass_score   = int(np.clip(avg_pass, 50, 98))

    shot_acc = (tot_sot / tot_shots * 100) if tot_shots > 0 else 40
    goals_factor = np.clip(tot_goals * 4, 10, 50)
    shoot_score  = int(np.clip(shot_acc * 0.5 + goals_factor, 45, 99))

    playmaker_score = int(np.clip(avg_pass * 0.6 + (tot_assists * 3), 40, 98))
    stamina_score   = int(np.clip((tot_mins / max(1, player_df["appearances"].sum() * 90)) * 95, 50, 96))
    defense_score   = int(np.clip(tot_cs * 5 + 40, 40, 95))

    return {
        "overall": rating_score,
        "shooting": shoot_score,
        "passing": pass_score,
        "playmaking": playmaker_score,
        "stamina": stamina_score,
        "defending": defense_score,
        "discipline_penalty": tot_cards,
    }


def render_scouting_dossier(df: pd.DataFrame, player_name: str, theme: str = "dark"):
    """Renders the comprehensive player scouting dossier."""
    is_dark = (theme == "dark")
    p_df = df[df["player_name"] == player_name].sort_values("season")
    if p_df.empty:
        st.warning("Player not found in current dataset selection.")
        return

    # Basic Info
    latest_row = p_df.iloc[-1]
    position = latest_row["position"]
    nationality = latest_row["nationality"]
    team = latest_row["team"]
    flag = COUNTRY_FLAGS.get(nationality, "🌐")
    badge = TEAM_BADGES.get(team, "⚽")

    # Positional cohort for benchmark
    pos_cohort = df[df["position"] == position]

    attrs = compute_player_attributes(p_df, pos_cohort)
    pos_color = POSITION_COLORS.get(position, ACCENT_GREEN)

    # ── Top Overview: Card & Core Stats ──
    col_card, col_details = st.columns([1, 2], gap="medium")

    with col_card:
        st.markdown(
            f"""
            <div class="fut-card" style="border-color: {pos_color};">
                <div class="fut-card-header">
                    <div class="fut-rating-box">
                        <div class="fut-rating" style="color: {pos_color};">{attrs['overall']}</div>
                        <div class="fut-position">{position.upper()[:3]}</div>
                    </div>
                    <div style="font-size: 2.2rem;">{flag}</div>
                </div>
                <div class="fut-player-name">{player_name}</div>
                <div class="fut-meta">{badge} {team} · Age {latest_row['age']}</div>
                <div class="fut-attributes">
                    <div class="fut-attr-row">
                        <span class="fut-attr-label">SHOOT</span>
                        <span class="fut-attr-val">{attrs['shooting']}</span>
                    </div>
                    <div class="fut-attr-row">
                        <span class="fut-attr-label">PASS</span>
                        <span class="fut-attr-val">{attrs['passing']}</span>
                    </div>
                    <div class="fut-attr-row">
                        <span class="fut-attr-label">CREATIVE</span>
                        <span class="fut-attr-val">{attrs['playmaking']}</span>
                    </div>
                    <div class="fut-attr-row">
                        <span class="fut-attr-label">STAMINA</span>
                        <span class="fut-attr-val">{attrs['stamina']}</span>
                    </div>
                    <div class="fut-attr-row">
                        <span class="fut-attr-label">DEF/CS</span>
                        <span class="fut-attr-val">{attrs['defending']}</span>
                    </div>
                    <div class="fut-attr-row">
                        <span class="fut-attr-label">RATING</span>
                        <span class="fut-attr-val" style="color:#F59E0B;">★ {p_df['rating'].mean():.2f}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_details:
        # Per 90 Performance Metrics
        tot_mins = p_df["minutes_played"].sum()
        tot_goals = p_df["goals"].sum()
        tot_assists = p_df["assists"].sum()
        tot_shots = p_df["shots"].sum()
        tot_sot = p_df["shots_on_target"].sum()
        tot_apps = p_df["appearances"].sum()
        g_per_90 = round((tot_goals / tot_mins) * 90, 2) if tot_mins > 0 else 0
        a_per_90 = round((tot_assists / tot_mins) * 90, 2) if tot_mins > 0 else 0
        shot_acc = round((tot_sot / tot_shots) * 100, 1) if tot_shots > 0 else 0

        st.markdown(
            f"""
            <div style="background:#111827; border:1px solid #1F293D; border-radius:14px; padding:1.2rem; margin-bottom:1rem;">
                <h4 style="margin:0 0 10px 0; color:#FFFFFF; font-size:1.05rem;">⚡ Career Performance Snapshot</h4>
                <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; text-align:center;">
                    <div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:10px; border:1px solid rgba(255,255,255,0.05);">
                        <div style="color:#94A3B8; font-size:0.75rem; font-weight:700;">MATCHES</div>
                        <div style="color:#FFFFFF; font-size:1.4rem; font-weight:800;">{tot_apps}</div>
                        <div style="color:#64748B; font-size:0.7rem;">{tot_mins:,} mins</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:10px; border:1px solid rgba(255,255,255,0.05);">
                        <div style="color:#94A3B8; font-size:0.75rem; font-weight:700;">GOALS</div>
                        <div style="color:#00FF87; font-size:1.4rem; font-weight:800;">{tot_goals}</div>
                        <div style="color:#64748B; font-size:0.7rem;">{g_per_90} / 90 min</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:10px; border:1px solid rgba(255,255,255,0.05);">
                        <div style="color:#94A3B8; font-size:0.75rem; font-weight:700;">ASSISTS</div>
                        <div style="color:#00D2FF; font-size:1.4rem; font-weight:800;">{tot_assists}</div>
                        <div style="color:#64748B; font-size:0.7rem;">{a_per_90} / 90 min</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:10px; border:1px solid rgba(255,255,255,0.05);">
                        <div style="color:#94A3B8; font-size:0.75rem; font-weight:700;">SHOT ACCURACY</div>
                        <div style="color:#F59E0B; font-size:1.4rem; font-weight:800;">{shot_acc}%</div>
                        <div style="color:#64748B; font-size:0.7rem;">{tot_sot}/{tot_shots} on target</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Radar: Player vs Position Cohort Benchmark
        categories = ["Match Rating", "Pass Accuracy", "Goals/90", "Assists/90", "Shot Accuracy", "Minutes"]
        # Normalization scale
        p_vals = [
            p_df["rating"].mean() / 10.0,
            p_df["pass_accuracy"].mean() / 100.0,
            min(1.0, g_per_90 / 0.8),
            min(1.0, a_per_90 / 0.6),
            shot_acc / 100.0,
            min(1.0, tot_mins / 3000),
        ]
        cohort_g_per_90 = ((pos_cohort["goals"].sum() / max(1, pos_cohort["minutes_played"].sum())) * 90)
        cohort_a_per_90 = ((pos_cohort["assists"].sum() / max(1, pos_cohort["minutes_played"].sum())) * 90)
        cohort_shot_acc = (pos_cohort["shots_on_target"].sum() / max(1, pos_cohort["shots"].sum())) * 100
        bench_vals = [
            pos_cohort["rating"].mean() / 10.0,
            pos_cohort["pass_accuracy"].mean() / 100.0,
            min(1.0, cohort_g_per_90 / 0.8),
            min(1.0, cohort_a_per_90 / 0.6),
            cohort_shot_acc / 100.0,
            min(1.0, pos_cohort["minutes_played"].mean() / 3000),
        ]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=p_vals + [p_vals[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name=player_name,
            line=dict(color=pos_color, width=2.5),
            fillcolor=hex_to_rgba(pos_color, 0.18),
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=bench_vals + [bench_vals[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name=f"Avg {position}",
            line=dict(color="#64748B", width=1.5, dash="dot"),
            fillcolor="rgba(100, 116, 139, 0.1)",
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#0D131F" if is_dark else "#FFFFFF",
                radialaxis=dict(visible=True, range=[0, 1], color="#475569" if is_dark else "#94A3B8", gridcolor="#1F293D" if is_dark else "#F1F5F9"),
                angularaxis=dict(color="#94A3B8" if is_dark else "#334155", gridcolor="#1F293D" if is_dark else "#F1F5F9"),
            ),
            height=320,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            legend=dict(x=0.01, y=0.99, bgcolor="rgba(17,24,39,0.8)" if is_dark else "rgba(255,255,255,0.9)", bordercolor=BORDER_SUBTLE if is_dark else "#E2E8F0"),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── Career Season Progression ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-bar">
            <div>
                <h3 class="section-bar-title"><span>📈</span> Season Progression & Form History</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        # Rating trend over seasons
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(
            x=p_df["season"],
            y=p_df["rating"],
            mode="lines+markers+text",
            line=dict(color="#F59E0B", width=3),
            marker=dict(size=10, color="#F59E0B", line=dict(color="#FFFFFF", width=2)),
            text=[f"★ {r:.2f}" for r in p_df["rating"]],
            textposition="top center",
            name="Rating",
        ))
        fig_r = style_chart(fig_r, theme=theme, height=260, title="Match Rating Trend")
        fig_r.update_layout(yaxis=dict(range=[5.5, 10]))
        st.plotly_chart(fig_r, use_container_width=True)

    with c2:
        # Goals and assists over seasons
        fig_ga = go.Figure()
        fig_ga.add_trace(go.Bar(
            x=p_df["season"], y=p_df["goals"],
            name="Goals", marker=dict(color=ACCENT_GREEN),
            text=p_df["goals"], textposition="outside",
        ))
        fig_ga.add_trace(go.Bar(
            x=p_df["season"], y=p_df["assists"],
            name="Assists", marker=dict(color=ACCENT_CYAN),
            text=p_df["assists"], textposition="outside",
        ))
        fig_ga = style_chart(fig_ga, theme=theme, height=260, title="Goals & Assists by Season")
        fig_ga.update_layout(barmode="group")
        st.plotly_chart(fig_ga, use_container_width=True)


def render_head_to_head_duel(df: pd.DataFrame, player1: str, player2: str):
    """Renders an exciting head-to-head comparison battle between two players."""
    p1_df = df[df["player_name"] == player1]
    p2_df = df[df["player_name"] == player2]

    if p1_df.empty or p2_df.empty:
        st.warning("Please ensure both players exist in current dataset.")
        return

    # Aggregates
    p1_pos = p1_df.iloc[-1]["position"]
    p2_pos = p2_df.iloc[-1]["position"]
    p1_nat = p1_df.iloc[-1]["nationality"]
    p2_nat = p2_df.iloc[-1]["nationality"]
    p1_team = p1_df.iloc[-1]["team"]
    p2_team = p2_df.iloc[-1]["team"]

    # Metrics
    metrics = [
        ("Average Rating", round(float(p1_df["rating"].mean()), 2), round(float(p2_df["rating"].mean()), 2), "higher"),
        ("Total Goals", int(p1_df["goals"].sum()), int(p2_df["goals"].sum()), "higher"),
        ("Total Assists", int(p1_df["assists"].sum()), int(p2_df["assists"].sum()), "higher"),
        ("Pass Accuracy (%)", round(float(p1_df["pass_accuracy"].mean()), 1), round(float(p2_df["pass_accuracy"].mean()), 1), "higher"),
        ("Shots on Target (%)",
         round((p1_df["shots_on_target"].sum() / max(1, p1_df["shots"].sum())) * 100, 1),
         round((p2_df["shots_on_target"].sum() / max(1, p2_df["shots"].sum())) * 100, 1), "higher"),
        ("Goals per 90",
         round((p1_df["goals"].sum() / max(1, p1_df["minutes_played"].sum())) * 90, 2),
         round((p2_df["goals"].sum() / max(1, p2_df["minutes_played"].sum())) * 90, 2), "higher"),
        ("Total Minutes Played", int(p1_df["minutes_played"].sum()), int(p2_df["minutes_played"].sum()), "higher"),
        ("Cards / Discipline Index",
         int(p1_df["yellow_cards"].sum() + p1_df["red_cards"].sum() * 3),
         int(p2_df["yellow_cards"].sum() + p2_df["red_cards"].sum() * 3), "lower"),
    ]

    p1_wins = 0
    p2_wins = 0
    for _, v1, v2, criteria in metrics:
        if criteria == "higher":
            if v1 > v2:
                p1_wins += 1
            elif v2 > v1:
                p2_wins += 1
        else:
            if v1 < v2:
                p1_wins += 1
            elif v2 < v1:
                p2_wins += 1

    # Banner with scores
    if p1_wins > p2_wins:
        winner_text = f"👑 <b>{player1}</b> leads the duel with <b>{p1_wins}</b> wins vs <b>{p2_wins}</b>"
    elif p2_wins > p1_wins:
        winner_text = f"👑 <b>{player2}</b> leads the duel with <b>{p2_wins}</b> wins vs <b>{p1_wins}</b>"
    else:
        winner_text = f"⚖️ It's a dead heat! Tied at <b>{p1_wins} - {p2_wins}</b>"

    st.markdown(
        f"""
        <div class="duel-container">
            <div class="duel-header">
                <div class="duel-player" style="border-left: 4px solid {ACCENT_GREEN};">
                    <div style="font-size: 1.5rem;">{COUNTRY_FLAGS.get(p1_nat, '🌐')}</div>
                    <div style="font-size: 1.15rem; font-weight:800; color:#FFFFFF;">{player1}</div>
                    <div style="font-size: 0.78rem; color:#94A3B8;">{TEAM_BADGES.get(p1_team, '⚽')} {p1_team} · {p1_pos}</div>
                    <div style="font-size: 1.6rem; font-weight:800; color:{ACCENT_GREEN}; margin-top:6px;">{p1_wins} Wins</div>
                </div>
                <div class="duel-vs">⚔️ VS</div>
                <div class="duel-player" style="border-right: 4px solid {ACCENT_CYAN};">
                    <div style="font-size: 1.5rem;">{COUNTRY_FLAGS.get(p2_nat, '🌐')}</div>
                    <div style="font-size: 1.15rem; font-weight:800; color:#FFFFFF;">{player2}</div>
                    <div style="font-size: 0.78rem; color:#94A3B8;">{TEAM_BADGES.get(p2_team, '⚽')} {p2_team} · {p2_pos}</div>
                    <div style="font-size: 1.6rem; font-weight:800; color:{ACCENT_CYAN}; margin-top:6px;">{p2_wins} Wins</div>
                </div>
            </div>
            <div style="text-align:center; padding:10px; background:rgba(255,255,255,0.03); border-radius:10px; margin-bottom:1.5rem; color:#00FF87;">
                {winner_text}
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Duel Bars for each metric
    for label, v1, v2, criteria in metrics:
        tot = max(1e-5, (v1 + v2))
        pct1 = int((v1 / tot) * 100) if criteria == "higher" else int(((tot - v1) / tot) * 100)
        pct2 = 100 - pct1

        v1_color = ACCENT_GREEN if ((v1 > v2 and criteria == "higher") or (v1 < v2 and criteria == "lower")) else "#94A3B8"
        v2_color = ACCENT_CYAN if ((v2 > v1 and criteria == "higher") or (v2 < v1 and criteria == "lower")) else "#94A3B8"

        st.markdown(
            f"""
            <div class="duel-bar-row">
                <div class="duel-label-row">
                    <span style="color:{v1_color}; font-weight:700;">{v1}</span>
                    <span style="color:#CBD5E1;">{label}</span>
                    <span style="color:{v2_color}; font-weight:700;">{v2}</span>
                </div>
                <div class="duel-bar-track">
                    <div class="duel-bar-left" style="width: {pct1}%;"></div>
                    <div class="duel-bar-right" style="width: {pct2}%;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
