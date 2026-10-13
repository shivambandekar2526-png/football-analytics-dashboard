"""
modules/ui_theme.py
Design System, Dual-Theme (Day & Night Mode), CSS Injections, and Plotly Styling for Football Analytics.
"""

import plotly.graph_objects as go
import streamlit as st

# ── Color Palette ─────────────────────────────────────────────────────────────
ACCENT_GREEN   = "#10B981"  # Vibrant Pitch Emerald
ACCENT_CYAN    = "#06B6D4"  # Electric Cyan
ACCENT_PURPLE  = "#8B5CF6"  # Royal Purple
ACCENT_GOLD    = "#F59E0B"  # Golden Trophy
ACCENT_RED     = "#EF4444"  # Coral / Red
ACCENT_BLUE    = "#3B82F6"  # Tactical Blue
BORDER_SUBTLE  = "#1F293D"  # Subtle Border

POSITION_COLORS = {
    "Goalkeeper": "#F59E0B",
    "Defender":   "#3B82F6",
    "Midfielder": "#10B981",
    "Forward":    "#EF4444",
}

POSITION_ICONS = {
    "Goalkeeper": "🧤",
    "Defender":   "🛡️",
    "Midfielder": "🎯",
    "Forward":    "🚀",
}

COUNTRY_FLAGS = {
    "Brazil":      "🇧🇷",
    "France":      "🇫🇷",
    "Germany":     "🇩🇪",
    "Spain":       "🇪🇸",
    "England":     "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Argentina":   "🇦🇷",
    "Portugal":    "🇵🇹",
    "Italy":       "🇮🇹",
    "Netherlands": "🇳🇱",
    "Belgium":     "🇧🇪",
}

TEAM_COLORS = {
    "Atletico United":   "#EF4444",
    "City Blues":         "#0EA5E9",
    "Riverside FC":       "#10B981",
    "Northern Star":      "#F59E0B",
    "Capital Rovers":     "#8B5CF6",
    "Eastside FC":        "#F97316",
    "Golden Eagles":      "#EAB308",
    "Silver Wolves":      "#64748B",
    "Harbor City":        "#06B6D4",
    "Redstone Athletic":  "#DC2626",
}

TEAM_BADGES = {
    "Atletico United":   "🔴",
    "City Blues":         "🔵",
    "Riverside FC":       "🟢",
    "Northern Star":      "⭐",
    "Capital Rovers":     "🟣",
    "Eastside FC":        "🟠",
    "Golden Eagles":      "🦅",
    "Silver Wolves":      "🐺",
    "Harbor City":        "⚓",
    "Redstone Athletic":  "🧱",
}

CHART_PALETTE = [ACCENT_GREEN, ACCENT_CYAN, ACCENT_PURPLE, ACCENT_GOLD, ACCENT_RED, ACCENT_BLUE]

DISCLAIMER_HTML = """
<div class="pro-disclaimer">
    <span>⚠️</span>
    <span><strong>Synthetic Data Notice:</strong> All metrics, attributes, and match records are synthetically modeled for demonstration.</span>
</div>
"""


def hex_to_rgba(hex_code: str, alpha: float = 0.2) -> str:
    """Converts a hex color code (e.g. #00FF87) to a valid Plotly rgba(r, g, b, a) string."""
    clean = str(hex_code).lstrip("#")
    if len(clean) == 3:
        clean = "".join([c * 2 for c in clean])
    if len(clean) == 6:
        try:
            r = int(clean[0:2], 16)
            g = int(clean[2:4], 16)
            b = int(clean[4:6], 16)
            return f"rgba({r}, {g}, {b}, {alpha})"
        except ValueError:
            pass
    return f"rgba(16, 185, 129, {alpha})"


def inject_custom_css(theme: str = "dark"):
    """Injects high-end, responsive styling tailored to either Day (Light) or Night (Dark) mode."""
    is_dark = (theme == "dark")

    # Dynamic Theme Variables
    bg_app       = "#0A0E17" if is_dark else "#F8FAFC"
    text_main    = "#F8FAFC" if is_dark else "#0F172A"
    text_muted   = "#94A3B8" if is_dark else "#64748B"
    bg_card      = "#111827" if is_dark else "#FFFFFF"
    border_card  = "#1F293D" if is_dark else "#E2E8F0"
    bg_sidebar   = "linear-gradient(180deg, #0D131F 0%, #090D15 100%)" if is_dark else "linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%)"
    border_side  = "rgba(255, 255, 255, 0.08)" if is_dark else "#E2E8F0"
    card_shadow  = "0 4px 20px rgba(0, 0, 0, 0.3)" if is_dark else "0 2px 12px rgba(0, 0, 0, 0.04)"
    input_bg     = "#111827" if is_dark else "#FFFFFF"
    accent_glow  = "rgba(16, 185, 129, 0.15)" if is_dark else "rgba(16, 185, 129, 0.1)"

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        /* ── Base Reset & Typography ── */
        html, body, [class*="css"], .stApp {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: {bg_app} !important;
            color: {text_main} !important;
        }}

        /* Clean scrollbar */
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: {bg_app}; }}
        ::-webkit-scrollbar-thumb {{
            background: {border_card};
            border-radius: 999px;
        }}
        ::-webkit-scrollbar-thumb:hover {{ background: #10B981; }}

        /* ── Header & Drawer Toggle Controls ── */
        header[data-testid="stHeader"] {{
            background: transparent !important;
            color: {text_main} !important;
            z-index: 999990 !important;
            pointer-events: none !important;
        }}

        /* Hide Deploy button and Main Menu ONLY - NEVER hide stToolbar which houses the drawer expand button! */
        #MainMenu, footer, .stDeployButton, [data-testid="stDeployButton"], [data-testid="stMainMenu"] {{
            visibility: hidden !important;
            display: none !important;
        }}

        [data-testid="stToolbar"] {{
            background: transparent !important;
            pointer-events: none !important;
        }}

        /* Styled Drawer Collapse & Expand Buttons (Modern Streamlit 1.35+ & legacy compatibility) */
        button[data-testid="stExpandSidebarButton"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stSidebarHeader"] button,
        [data-testid="stSidebarCollapsedControl"],
        button[data-testid="stBaseButton-header"] {{
            pointer-events: auto !important;
            display: inline-flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            background: {bg_card} !important;
            border: 1.5px solid #10B981 !important;
            border-radius: 8px !important;
            color: #10B981 !important;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25) !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            z-index: 999999 !important;
        }}

        button[data-testid="stExpandSidebarButton"]:hover,
        [data-testid="stSidebarCollapseButton"]:hover,
        [data-testid="stSidebarCollapseButton"] button:hover,
        [data-testid="stSidebarHeader"] button:hover {{
            background: {"#162033" if is_dark else "#F1F5F9"} !important;
            border-color: #10B981 !important;
            box-shadow: 0 0 16px {accent_glow} !important;
            transform: scale(1.08) !important;
        }}

        button[data-testid="stExpandSidebarButton"] svg,
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="stSidebarHeader"] button svg {{
            fill: #10B981 !important;
            stroke: #10B981 !important;
        }}

        /* ── Sidebar Layout ── */
        section[data-testid="stSidebar"] {{
            background: {bg_sidebar} !important;
            border-right: 1px solid {border_side} !important;
            box-shadow: 4px 0 20px rgba(0,0,0,0.15) !important;
        }}
        section[data-testid="stSidebar"] .block-container {{
            padding: 1.2rem 0.9rem 1.8rem 0.9rem !important;
        }}

        .brand-container {{
            text-align: center;
            padding: 0.4rem 0.2rem 0.8rem 0.2rem;
            border-bottom: 1px solid {border_card};
            margin-bottom: 0.8rem;
        }}
        .brand-tag {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: {accent_glow};
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px;
            padding: 2px 8px;
            font-size: 10px;
            font-weight: 700;
            color: #10B981 !important;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            margin-bottom: 4px;
        }}
        .brand-title {{
            font-size: 1.15rem;
            font-weight: 800;
            margin: 0;
            color: {text_main} !important;
            letter-spacing: -0.3px;
        }}
        .brand-sub {{
            font-size: 0.72rem;
            color: {text_muted} !important;
            margin: 2px 0 0 0;
        }}

        /* ── Clean Header Banner ── */
        .clean-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.8rem 0 1.2rem 0;
            border-bottom: 1px solid {border_card};
            margin-bottom: 1.2rem;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .clean-header-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .clean-header-icon {{
            font-size: 1.6rem;
            width: 44px;
            height: 44px;
            border-radius: 10px;
            background: {accent_glow};
            border: 1px solid rgba(16, 185, 129, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .clean-header-title {{
            font-size: 1.45rem;
            font-weight: 800;
            color: {text_main} !important;
            margin: 0;
            line-height: 1.2;
            letter-spacing: -0.4px;
        }}
        .clean-header-desc {{
            font-size: 0.84rem;
            color: {text_muted} !important;
            margin: 2px 0 0 0;
        }}
        .clean-header-pill {{
            background: {bg_card};
            border: 1px solid {border_card};
            border-radius: 20px;
            padding: 4px 12px;
            font-size: 0.75rem;
            font-weight: 600;
            color: #10B981 !important;
            box-shadow: {card_shadow};
        }}

        /* ── Compact Disclaimer ── */
        .pro-disclaimer {{
            background: {"rgba(245, 158, 11, 0.08)" if is_dark else "rgba(245, 158, 11, 0.12)"};
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-left: 3px solid #F59E0B;
            border-radius: 8px;
            padding: 7px 12px;
            font-size: 0.76rem;
            color: {"#F59E0B" if is_dark else "#B45309"} !important;
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        /* ── Structured Section Divider ── */
        .section-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 1.6rem 0 0.8rem 0;
            padding-bottom: 0.4rem;
            border-bottom: 1px solid {border_card};
        }}
        .section-bar-title {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 1.05rem;
            font-weight: 700;
            color: {text_main} !important;
            margin: 0;
        }}
        .section-bar-sub {{
            font-size: 0.76rem;
            color: {text_muted} !important;
            margin: 2px 0 0 0;
        }}

        /* ── High-Contrast Clean KPI Cards ── */
        .kpi-box {{
            background: {bg_card};
            border: 1px solid {border_card};
            border-radius: 12px;
            padding: 1rem 1.1rem;
            box-shadow: {card_shadow};
            transition: transform 0.15s ease, border-color 0.15s ease;
            position: relative;
            overflow: hidden;
            margin-bottom: 0.4rem;
        }}
        .kpi-box:hover {{
            transform: translateY(-2px);
            border-color: #10B981;
        }}
        .kpi-box-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.4rem;
        }}
        .kpi-box-label {{
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: {text_muted};
        }}
        .kpi-box-icon {{
            font-size: 1.1rem;
        }}
        .kpi-box-value {{
            font-size: 1.7rem;
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -0.5px;
            margin-bottom: 0.25rem;
            color: {text_main};
        }}
        .kpi-box-sub {{
            font-size: 0.74rem;
            color: {text_muted};
        }}

        /* ── Scouting FIFA Card ── */
        .fut-card {{
            background: {"radial-gradient(circle at 50% 20%, #1A2740 0%, #0F172A 75%, #0A0F1D 100%)" if is_dark else "linear-gradient(145deg, #FFFFFF 0%, #F1F5F9 100%)"};
            border: 2px solid #F59E0B;
            border-radius: 16px;
            padding: 1.4rem 1.2rem;
            box-shadow: {"0 14px 36px rgba(0, 0, 0, 0.5), 0 0 20px rgba(245, 158, 11, 0.15)" if is_dark else "0 8px 24px rgba(0, 0, 0, 0.08)"};
            color: {text_main};
            position: relative;
        }}
        .fut-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.8rem;
        }}
        .fut-rating {{
            font-size: 2.6rem;
            font-weight: 800;
            color: #F59E0B;
            line-height: 1;
            letter-spacing: -1px;
        }}
        .fut-position {{
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 1px;
            color: {text_muted};
        }}
        .fut-player-name {{
            font-size: 1.3rem;
            font-weight: 800;
            color: {text_main};
            text-align: center;
            margin: 0.3rem 0;
            letter-spacing: -0.3px;
        }}
        .fut-meta {{
            text-align: center;
            font-size: 0.78rem;
            color: {text_muted};
            margin-bottom: 1rem;
        }}
        .fut-attributes {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px 14px;
            background: {"rgba(0,0,0,0.3)" if is_dark else "rgba(241, 245, 249, 0.8)"};
            border-radius: 10px;
            padding: 10px;
            border: 1px solid {border_card};
        }}
        .fut-attr-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
        }}
        .fut-attr-val {{
            font-weight: 700;
            color: #10B981;
        }}
        .fut-attr-label {{
            color: {text_muted};
            font-weight: 600;
        }}

        /* ── Duel Arena ── */
        .duel-container {{
            background: {bg_card};
            border: 1px solid {border_card};
            border-radius: 14px;
            padding: 1.2rem;
            box-shadow: {card_shadow};
            margin-bottom: 1rem;
        }}
        .duel-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.2rem;
        }}
        .duel-player {{
            flex: 1;
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            background: {"rgba(255,255,255,0.02)" if is_dark else "#F8FAFC"};
            border: 1px solid {border_card};
        }}
        .duel-vs {{
            padding: 0 14px;
            font-weight: 800;
            font-size: 1.1rem;
            color: {text_muted};
        }}
        .duel-bar-row {{
            margin-bottom: 10px;
        }}
        .duel-label-row {{
            display: flex;
            justify-content: space-between;
            font-size: 0.78rem;
            font-weight: 600;
            color: {text_muted};
            margin-bottom: 3px;
        }}
        .duel-bar-track {{
            height: 7px;
            background: {border_card};
            border-radius: 4px;
            display: flex;
            overflow: hidden;
        }}
        .duel-bar-left {{ background: #10B981; height: 100%; }}
        .duel-bar-right {{ background: #06B6D4; height: 100%; }}

        /* ── Streamlit UI Elements Polish ── */
        div[data-testid="stRadio"] > div {{
            gap: 4px !important;
        }}
        div[data-testid="stRadio"] label {{
            background: {input_bg} !important;
            border: 1px solid {border_card} !important;
            border-radius: 8px !important;
            padding: 7px 12px !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            color: {text_muted} !important;
            transition: all 0.15s ease !important;
        }}
        div[data-testid="stRadio"] label:hover {{
            border-color: #10B981 !important;
            color: {text_main} !important;
        }}
        div[data-testid="stRadio"] label:has(input:checked) {{
            background: {accent_glow} !important;
            border-color: #10B981 !important;
            color: #10B981 !important;
        }}

        /* Clean Streamlit Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 6px !important;
            background-color: transparent !important;
            border-bottom: 1px solid {border_card} !important;
            padding-bottom: 2px !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            background: {bg_card} !important;
            border: 1px solid {border_card} !important;
            border-radius: 6px 6px 0 0 !important;
            color: {text_muted} !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            padding: 6px 14px !important;
        }}
        .stTabs [aria-selected="true"] {{
            border-color: #10B981 !important;
            border-bottom: 2px solid #10B981 !important;
            color: #10B981 !important;
        }}

        /* Clean Dataframe */
        div[data-testid="stDataFrame"] {{
            border: 1px solid {border_card} !important;
            border-radius: 10px !important;
            box-shadow: {card_shadow} !important;
            background: {bg_card} !important;
        }}

        /* Clean Inputs */
        div[data-baseweb="select"], div[data-baseweb="input"] {{
            border-radius: 8px !important;
        }}

        /* Download Buttons */
        div[data-testid="stDownloadButton"] button {{
            background: {"linear-gradient(135deg, #059669 0%, #047857 100%)" if is_dark else "#10B981"} !important;
            border: 1px solid #10B981 !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            padding: 7px 14px !important;
            width: 100%;
            transition: all 0.2s ease !important;
        }}
        div[data-testid="stDownloadButton"] button:hover {{
            background: #059669 !important;
            box-shadow: 0 0 12px {accent_glow} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_chart(
    fig: go.Figure,
    theme: str = "dark",
    height: int = 400,
    legend_inside: bool = False,
    show_legend: bool = True,
    title: str = None,
) -> go.Figure:
    """Applies a clean, uncluttered Plotly layout matching Day or Night mode."""
    is_dark = (theme == "dark")
    text_color  = "#CBD5E1" if is_dark else "#334155"
    grid_color  = "#1F293D" if is_dark else "#F1F5F9"
    plot_bg     = "#0D131F" if is_dark else "#FFFFFF"
    hover_bg    = "#111827" if is_dark else "#FFFFFF"
    hover_border= "#10B981" if is_dark else "#059669"
    hover_text  = "#FFFFFF" if is_dark else "#0F172A"

    legend_cfg = dict(
        bgcolor="rgba(17, 24, 39, 0.8)" if is_dark else "rgba(255, 255, 255, 0.9)",
        bordercolor="#1F293D" if is_dark else "#E2E8F0",
        borderwidth=1,
        font=dict(size=11, color=text_color),
    )
    if legend_inside:
        legend_cfg.update(x=0.02, y=0.98, xanchor="left", yanchor="top")

    fig.update_layout(
        template="plotly_dark" if is_dark else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=plot_bg,
        height=height,
        font=dict(family="Plus Jakarta Sans, sans-serif", color=text_color, size=12),
        margin=dict(l=16, r=16, t=38 if title else 20, b=20),
        legend=legend_cfg if show_legend else dict(visible=False),
        title=dict(
            text=f"<b>{title}</b>" if title else None,
            font=dict(size=13, color=text_color),
            x=0.01,
            y=0.97,
        ) if title else None,
        hoverlabel=dict(
            bgcolor=hover_bg,
            bordercolor=hover_border,
            font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color=hover_text),
        ),
        xaxis=dict(
            gridcolor=grid_color,
            linecolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(color=text_color, size=11),
        ),
        yaxis=dict(
            gridcolor=grid_color,
            linecolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(color=text_color, size=11),
        ),
    )
    return fig


def render_header(icon: str, title: str, subtitle: str, pill: str = None):
    """Renders a clean, uncluttered page header."""
    pill_html = f'<div class="clean-header-pill">{pill}</div>' if pill else ""
    st.markdown(
        f"""
        <div class="clean-header">
            <div class="clean-header-left">
                <div class="clean-header-icon">{icon}</div>
                <div>
                    <h1 class="clean-header-title">{title}</h1>
                    <p class="clean-header-desc">{subtitle}</p>
                </div>
            </div>
            {pill_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi(icon: str, label: str, value: str, subtext: str, accent_color: str = "#10B981"):
    """Renders a clean, high-contrast KPI card."""
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-box-top">
                <span class="kpi-box-label">{label}</span>
                <span class="kpi-box-icon">{icon}</span>
            </div>
            <div class="kpi-box-value" style="color: {accent_color};">{value}</div>
            <div class="kpi-box-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(icon: str, title: str, subtitle: str = None):
    """Renders a crisp section separator with clear hierarchy."""
    sub_html = f'<p class="section-bar-sub">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f"""
        <div class="section-bar">
            <div>
                <h3 class="section-bar-title"><span>{icon}</span> {title}</h3>
                {sub_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
