"""
modules/pitch_board.py
Interactive Tactical Football Pitch and Best XI (Dream Team) Generator.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from modules.ui_theme import (
    POSITION_COLORS,
    COUNTRY_FLAGS,
    TEAM_BADGES,
    BORDER_SUBTLE,
)

# Formation definitions: (Position requirement, (x, y) coordinates, role label)
FORMATIONS = {
    "4-3-3 Attack": [
        ("Goalkeeper", 8,  34, "GK"),
        ("Defender",   28, 11, "LB"),
        ("Defender",   24, 25, "LCB"),
        ("Defender",   24, 43, "RCB"),
        ("Defender",   28, 57, "RB"),
        ("Midfielder", 52, 18, "LCM"),
        ("Midfielder", 48, 34, "CM"),
        ("Midfielder", 52, 50, "RCM"),
        ("Forward",    82, 13, "LW"),
        ("Forward",    86, 34, "ST"),
        ("Forward",    82, 55, "RW"),
    ],
    "4-4-2 Classic": [
        ("Goalkeeper", 8,  34, "GK"),
        ("Defender",   28, 11, "LB"),
        ("Defender",   24, 25, "LCB"),
        ("Defender",   24, 43, "RCB"),
        ("Defender",   28, 57, "RB"),
        ("Midfielder", 52, 12, "LM"),
        ("Midfielder", 50, 26, "LCM"),
        ("Midfielder", 50, 42, "RCM"),
        ("Midfielder", 52, 56, "RM"),
        ("Forward",    85, 26, "LS"),
        ("Forward",    85, 42, "RS"),
    ],
    "4-2-3-1 Modern": [
        ("Goalkeeper", 8,  34, "GK"),
        ("Defender",   28, 11, "LB"),
        ("Defender",   24, 25, "LCB"),
        ("Defender",   24, 43, "RCB"),
        ("Defender",   28, 57, "RB"),
        ("Midfielder", 46, 26, "LDM"),
        ("Midfielder", 46, 42, "RDM"),
        ("Midfielder", 68, 15, "LAM"),
        ("Midfielder", 70, 34, "CAM"),
        ("Midfielder", 68, 53, "RAM"),
        ("Forward",    88, 34, "ST"),
    ],
    "3-5-2 Fluid": [
        ("Goalkeeper", 8,  34, "GK"),
        ("Defender",   24, 18, "LCB"),
        ("Defender",   22, 34, "CB"),
        ("Defender",   24, 50, "RCB"),
        ("Midfielder", 48, 9,  "LWB"),
        ("Midfielder", 52, 23, "LCM"),
        ("Midfielder", 58, 34, "CAM"),
        ("Midfielder", 52, 45, "RCM"),
        ("Midfielder", 48, 59, "RWB"),
        ("Forward",    85, 26, "LS"),
        ("Forward",    85, 42, "RS"),
    ],
}


def draw_tactical_pitch(fig: go.Figure) -> go.Figure:
    """Adds pristine regulation-style football pitch markings to a Plotly figure."""
    # Alternating grass stripe bands for turf realism
    stripe_w = 10.5
    for i in range(10):
        x0 = i * stripe_w
        x1 = (i + 1) * stripe_w
        color = "rgba(16, 185, 129, 0.09)" if i % 2 == 0 else "rgba(16, 185, 129, 0.04)"
        fig.add_shape(
            type="rect",
            x0=x0, y0=0, x1=x1, y1=68,
            fillcolor=color, line=dict(width=0), layer="below"
        )

    pitch_line = dict(color="rgba(255, 255, 255, 0.75)", width=2)
    subtle_line = dict(color="rgba(255, 255, 255, 0.75)", width=1.5)

    # Outer boundary
    fig.add_shape(type="rect", x0=0, y0=0, x1=105, y1=68, line=pitch_line)
    # Halfway line
    fig.add_shape(type="line", x0=52.5, y0=0, x1=52.5, y1=68, line=pitch_line)
    # Center circle
    fig.add_shape(type="circle", x0=52.5 - 9.15, y0=34 - 9.15, x1=52.5 + 9.15, y1=34 + 9.15, line=pitch_line)
    # Center spot
    fig.add_shape(type="circle", x0=52.5 - 0.7, y0=34 - 0.7, x1=52.5 + 0.7, y1=34 + 0.7, fillcolor="white", line=dict(width=0))

    # 18-yard Penalty boxes
    fig.add_shape(type="rect", x0=0, y0=34 - 20.16, x1=16.5, y1=34 + 20.16, line=pitch_line)
    fig.add_shape(type="rect", x0=105 - 16.5, y0=34 - 20.16, x1=105, y1=34 + 20.16, line=pitch_line)

    # 6-yard Goal boxes
    fig.add_shape(type="rect", x0=0, y0=34 - 9.16, x1=5.5, y1=34 + 9.16, line=subtle_line)
    fig.add_shape(type="rect", x0=105 - 5.5, y0=34 - 9.16, x1=105, y1=34 + 9.16, line=subtle_line)

    # Penalty spots (11m)
    fig.add_shape(type="circle", x0=11 - 0.6, y0=34 - 0.6, x1=11 + 0.6, y1=34 + 0.6, fillcolor="white", line=dict(width=0))
    fig.add_shape(type="circle", x0=105 - 11 - 0.6, y0=34 - 0.6, x1=105 - 11 + 0.6, y1=34 + 0.6, fillcolor="white", line=dict(width=0))

    # Goal frames
    fig.add_shape(type="rect", x0=-2.2, y0=34 - 3.66, x1=0, y1=34 + 3.66, line=dict(color="#00FF87", width=2), fillcolor="rgba(0,255,135,0.1)")
    fig.add_shape(type="rect", x0=105, y0=34 - 3.66, x1=107.2, y1=34 + 3.66, line=dict(color="#00FF87", width=2), fillcolor="rgba(0,255,135,0.1)")

    return fig


def select_best_xi(df: pd.DataFrame, formation_name: str = "4-3-3 Attack") -> tuple[list[dict], pd.DataFrame]:
    """
    Selects the 11 highest-rated unique players according to the selected formation.
    Returns:
        slots_data: list of dicts with role, x, y, and player row
        squad_df: pd.DataFrame of the chosen squad
    """
    formation_slots = FORMATIONS.get(formation_name, FORMATIONS["4-3-3 Attack"])

    # Count requirements per position
    pos_counts = {}
    for pos, _, _, _ in formation_slots:
        pos_counts[pos] = pos_counts.get(pos, 0) + 1

    # Aggregate player performance across seasons if multiple exist
    player_summary = (
        df.groupby(["player_name", "position", "team", "nationality"], as_index=False)
        .agg(
            rating=("rating", "mean"),
            appearances=("appearances", "sum"),
            goals=("goals", "sum"),
            assists=("assists", "sum"),
            shots=("shots", "sum"),
            shots_on_target=("shots_on_target", "sum"),
            minutes_played=("minutes_played", "sum"),
            pass_accuracy=("pass_accuracy", "mean"),
            clean_sheets=("clean_sheets", "sum"),
            yellow_cards=("yellow_cards", "sum"),
            red_cards=("red_cards", "sum"),
            age=("age", "max"),
        )
        .round({"rating": 2, "pass_accuracy": 1})
        .sort_values("rating", ascending=False)
    )

    chosen_players = {}
    for pos, count in pos_counts.items():
        candidates = player_summary[player_summary["position"] == pos].nlargest(count, "rating")
        chosen_players[pos] = list(candidates.to_dict("records"))

    # Map selected players to formation coordinates
    slots_data = []
    used_players = set()
    squad_list = []

    pos_index = {pos: 0 for pos in pos_counts}

    for pos, x, y, role in formation_slots:
        p_list = chosen_players.get(pos, [])
        idx = pos_index[pos]
        if idx < len(p_list):
            p = p_list[idx]
            pos_index[pos] += 1
            slots_data.append({
                "role": role,
                "x": x,
                "y": y,
                "position": pos,
                "player": p,
            })
            if p["player_name"] not in used_players:
                used_players.add(p["player_name"])
                p_copy = dict(p)
                p_copy["tactical_role"] = role
                squad_list.append(p_copy)
        else:
            # Fallback placeholder if not enough players match filter
            slots_data.append({
                "role": role,
                "x": x,
                "y": y,
                "position": pos,
                "player": {
                    "player_name": f"Vacant {role}",
                    "team": "Unknown",
                    "nationality": "Unknown",
                    "rating": 6.0,
                    "goals": 0,
                    "assists": 0,
                    "appearances": 0,
                    "clean_sheets": 0,
                    "pass_accuracy": 0,
                    "age": 20,
                },
            })

    squad_df = pd.DataFrame(squad_list)
    return slots_data, squad_df


def render_best_xi_pitch(slots_data: list[dict], formation_name: str, theme: str = "dark") -> go.Figure:
    """Renders the Best XI interactive tactical pitch chart in Plotly."""
    is_dark = (theme == "dark")
    fig = go.Figure()
    fig = draw_tactical_pitch(fig)

    # Plot players grouped by position for clear styling
    for pos, color in POSITION_COLORS.items():
        pos_slots = [s for s in slots_data if s["position"] == pos]
        if not pos_slots:
            continue

        xs = [s["x"] for s in pos_slots]
        ys = [s["y"] for s in pos_slots]
        names = [s["player"]["player_name"] for s in pos_slots]
        roles = [s["role"] for s in pos_slots]
        ratings = [s["player"]["rating"] for s in pos_slots]
        teams = [s["player"]["team"] for s in pos_slots]
        nats = [s["player"]["nationality"] for s in pos_slots]
        goals = [s["player"].get("goals", 0) for s in pos_slots]
        assists = [s["player"].get("assists", 0) for s in pos_slots]
        cs = [s["player"].get("clean_sheets", 0) for s in pos_slots]

        # Hover cards
        hover_texts = []
        for name, role, rat, team, nat, g, a, c_sheet in zip(names, roles, ratings, teams, nats, goals, assists, cs):
            flag = COUNTRY_FLAGS.get(nat, "🌐")
            badge = TEAM_BADGES.get(team, "⚽")
            stat_str = f"🧤 Clean Sheets: <b>{c_sheet}</b>" if pos == "Goalkeeper" else f"⚽ Goals: <b>{g}</b> | 🅰️ Assists: <b>{a}</b>"
            hover_texts.append(
                f"<b>{name}</b> ({role})<br>"
                f"Rating: <b style='color:#10B981;'>{rat:.2f} ⭐</b><br>"
                f"Team: {badge} {team}<br>"
                f"Nation: {flag} {nat}<br>"
                f"{stat_str}"
            )

        # Player badge marker
        fig.add_trace(go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            name=pos,
            marker=dict(
                size=32,
                color=color,
                line=dict(color="#FFFFFF", width=2),
                symbol="circle",
                opacity=0.95,
            ),
            text=[f"<b>{r}</b>" for r in roles],
            textposition="middle center",
            textfont=dict(color="#0A0E17", size=10, family="Plus Jakarta Sans, sans-serif"),
            hoverinfo="text",
            hovertext=hover_texts,
        ))

        # Separate annotation below marker for player name and rating
        for s in pos_slots:
            p = s["player"]
            badge = TEAM_BADGES.get(p["team"], "")
            fig.add_annotation(
                x=s["x"],
                y=s["y"] - 4.2,
                text=f"<b>{p['player_name']}</b><br><span style='color:#10B981; font-size:10px;'>★ {p['rating']:.2f}</span>",
                showarrow=False,
                font=dict(size=10, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif"),
                bgcolor="rgba(15, 23, 42, 0.85)",
                bordercolor=BORDER_SUBTLE if is_dark else "#CBD5E1",
                borderwidth=1,
                borderpad=3,
            )

    fig.update_xaxes(range=[-3, 108], visible=False, fixedrange=True)
    fig.update_yaxes(range=[-3, 71], visible=False, scaleanchor="x", scaleratio=1, fixedrange=True)

    fig.update_layout(
        template="plotly_dark" if is_dark else "plotly_white",
        plot_bgcolor="#064E3B" if not is_dark else "#0A1512",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        height=520,
        showlegend=True,
        legend=dict(
            orientation="h",
            x=0.5,
            y=1.06,
            xanchor="center",
            yanchor="bottom",
            bgcolor="rgba(15, 23, 42, 0.8)" if is_dark else "rgba(255, 255, 255, 0.9)",
            bordercolor=BORDER_SUBTLE if is_dark else "#CBD5E1",
            borderwidth=1,
            font=dict(size=11, color="#CBD5E1" if is_dark else "#334155"),
        ),
    )
    return fig
