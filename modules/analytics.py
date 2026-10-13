"""
modules/analytics.py
Advanced Football Metrics Calculations, Efficiency Matrices, and Team Power Rankings.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from modules.ui_theme import (
    POSITION_COLORS,
    TEAM_COLORS,
    TEAM_BADGES,
    ACCENT_GREEN,
    ACCENT_CYAN,
    ACCENT_PURPLE,
    ACCENT_GOLD,
    ACCENT_RED,
    BORDER_SUBTLE,
    style_chart,
)


def enrich_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Computes advanced soccer analytical metrics safely."""
    df = df.copy()

    # Per 90 metrics
    safe_mins = np.maximum(df["minutes_played"].values, 1)
    df["goals_per_90"] = np.where(
        df["minutes_played"] > 0,
        np.round((df["goals"] / safe_mins) * 90, 2),
        0.0,
    )
    df["assists_per_90"] = np.where(
        df["minutes_played"] > 0,
        np.round((df["assists"] / safe_mins) * 90, 2),
        0.0,
    )
    df["shots_per_90"] = np.where(
        df["minutes_played"] > 0,
        np.round((df["shots"] / safe_mins) * 90, 2),
        0.0,
    )

    # Goal Contributions
    df["goal_contributions"] = df["goals"] + df["assists"]
    df["mins_per_goal_contrib"] = np.where(
        df["goal_contributions"] > 0,
        np.round(df["minutes_played"] / np.maximum(df["goal_contributions"], 1), 1),
        999.0,
    )

    # Efficiency rates
    safe_shots = np.maximum(df["shots"].values, 1)
    df["shot_accuracy"] = np.where(
        df["shots"] > 0,
        np.round((df["shots_on_target"] / safe_shots) * 100, 1),
        0.0,
    )
    df["shot_conversion"] = np.where(
        df["shots"] > 0,
        np.round((df["goals"] / safe_shots) * 100, 1),
        0.0,
    )

    # Disciplinary Index
    df["discipline_index"] = (df["yellow_cards"] * 1) + (df["red_cards"] * 3)

    return df


def render_finishing_efficiency_matrix(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    """Renders the Clinical Finishing Efficiency Quadrant Matrix (Shots vs Conversion Rate)."""
    fwd_mid = df[(df["position"].isin(["Forward", "Midfielder"])) & (df["shots"] >= 10)].copy()

    if fwd_mid.empty:
        fwd_mid = df[df["shots"] > 0].copy()

    fig = px.scatter(
        fwd_mid,
        x="shots",
        y="shot_conversion",
        color="position",
        size="goals",
        size_max=22,
        hover_name="player_name",
        hover_data={
            "team": True,
            "goals": True,
            "shots": True,
            "shot_conversion": ":.1f%",
            "rating": ":.2f",
            "position": False,
        },
        labels={
            "shots": "Total Shots Attempted",
            "shot_conversion": "Shot Conversion Rate (%)",
            "position": "Position",
        },
        color_discrete_map=POSITION_COLORS,
    )

    # Add quadrant reference benchmark lines
    avg_shots = fwd_mid["shots"].median() if not fwd_mid.empty else 20
    avg_conv  = fwd_mid["shot_conversion"].median() if not fwd_mid.empty else 15

    fig.add_vline(x=avg_shots, line_dash="dash", line_color="rgba(255,255,255,0.25)", annotation_text="Median Shots", annotation_position="top left")
    fig.add_hline(y=avg_conv, line_dash="dash", line_color="rgba(255,255,255,0.25)", annotation_text="Median Conv %", annotation_position="bottom right")

    fig = style_chart(fig, theme=theme, height=440, title="Finishing Matrix: Volume vs Conversion Efficiency")
    return fig


def render_creative_playmaker_matrix(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    """Renders Playmaker Matrix (Pass Accuracy vs Total Assists)."""
    fig = px.scatter(
        df[df["appearances"] >= 5],
        x="pass_accuracy",
        y="assists",
        color="position",
        size="rating",
        size_max=18,
        hover_name="player_name",
        hover_data={
            "team": True,
            "assists": True,
            "pass_accuracy": ":.1f%",
            "rating": ":.2f",
        },
        labels={
            "pass_accuracy": "Pass Accuracy (%)",
            "assists": "Total Assists",
            "position": "Position",
        },
        color_discrete_map=POSITION_COLORS,
    )
    fig = style_chart(fig, theme=theme, height=420, title="Creative Matrix: Ball Distribution vs Key Assists")
    return fig


def render_team_power_rankings(df: pd.DataFrame, theme: str = "dark"):
    """Renders comprehensive club power rankings, attack vs defense index, and fair play table."""
    team_summary = (
        df.groupby("team", as_index=False)
        .agg(
            total_goals=("goals", "sum"),
            total_assists=("assists", "sum"),
            total_shots=("shots", "sum"),
            clean_sheets=("clean_sheets", "sum"),
            avg_rating=("rating", "mean"),
            avg_pass_acc=("pass_accuracy", "mean"),
            yellow_cards=("yellow_cards", "sum"),
            red_cards=("red_cards", "sum"),
            player_count=("player_name", "nunique"),
            total_minutes=("minutes_played", "sum"),
        )
        .round({"avg_rating": 2, "avg_pass_acc": 1})
    )

    # Attack Power Index (composite of goals, assists, shots)
    team_summary["attack_index"] = np.round(
        team_summary["total_goals"] * 1.5 + team_summary["total_assists"] * 1.0, 1
    )
    # Fair Play Score (lower penalty index = more disciplined)
    team_summary["fair_play_penalty"] = (
        team_summary["yellow_cards"] * 1 + team_summary["red_cards"] * 3
    )

    c1, c2 = st.columns(2, gap="medium")

    with c1:
        # Attack vs Defense Efficiency Scatter
        fig_matrix = px.scatter(
            team_summary,
            x="total_goals",
            y="clean_sheets",
            size="attack_index",
            size_max=24,
            color="team",
            color_discrete_map=TEAM_COLORS,
            hover_name="team",
            hover_data={
                "total_goals": True,
                "clean_sheets": True,
                "avg_rating": True,
                "team": False,
            },
            labels={
                "total_goals": "Total Goals Scored (Attack)",
                "clean_sheets": "Total Clean Sheets (Defense)",
            },
            text="team",
        )
        fig_matrix.update_traces(textposition="top center", textfont_size=10)
        fig_matrix = style_chart(fig_matrix, theme=theme, height=420, show_legend=False, title="Club Matrix: Attack vs Defense Dominance")
        st.plotly_chart(fig_matrix, use_container_width=True)

    with c2:
        # Fair Play Discipline Leaderboard
        fp_sorted = team_summary.sort_values("fair_play_penalty", ascending=True)
        fig_fp = go.Figure()
        fig_fp.add_trace(go.Bar(
            x=fp_sorted["yellow_cards"],
            y=fp_sorted["team"],
            orientation="h",
            name="Yellow Cards (1 pt)",
            marker=dict(color="#F59E0B"),
        ))
        fig_fp.add_trace(go.Bar(
            x=fp_sorted["red_cards"] * 3,
            y=fp_sorted["team"],
            orientation="h",
            name="Red Cards (3 pts penalty)",
            marker=dict(color="#EF4444"),
        ))
        fig_fp = style_chart(fig_fp, theme=theme, height=420, title="Fair Play & Disciplinary Leaderboard (Lower is Better)")
        fig_fp.update_layout(barmode="stack", xaxis_title="Penalty Points")
        st.plotly_chart(fig_fp, use_container_width=True)

    # Detailed Rankings Table
    st.markdown(
        """
        <div class="section-bar">
            <div>
                <h3 class="section-bar-title"><span>📋</span> Club Comprehensive Standings Matrix</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    display_team = team_summary.rename(columns={
        "team": "Club",
        "player_count": "Squad Size",
        "total_goals": "Goals",
        "total_assists": "Assists",
        "clean_sheets": "Clean Sheets",
        "avg_pass_acc": "Pass Acc %",
        "avg_rating": "Avg Rating",
        "attack_index": "Attack Index",
        "fair_play_penalty": "Discipline Pts",
    }).sort_values("Attack Index", ascending=False)

    st.dataframe(
        display_team[[
            "Club", "Squad Size", "Goals", "Assists", "Clean Sheets",
            "Pass Acc %", "Avg Rating", "Attack Index", "Discipline Pts"
        ]],
        use_container_width=True,
        hide_index=True,
        height=320,
    )
