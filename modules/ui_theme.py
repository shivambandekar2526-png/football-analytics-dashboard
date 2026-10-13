"""
modules/ui_theme.py
Design System, Theme Constants, CSS Injections, and Plotly Styling for Football Analytics.
"""

import plotly.graph_objects as go
import streamlit as st

# ── Color Palette ─────────────────────────────────────────────────────────────
ACCENT_GREEN   = "#00FF87"  # Pitch Neon Green
ACCENT_CYAN    = "#00D2FF"  # Electric Cyan
ACCENT_PURPLE  = "#8B5CF6"  # Royal Purple
ACCENT_GOLD    = "#F59E0B"  # Golden Trophy
ACCENT_RED     = "#EF4444"  # Aggressive Coral
ACCENT_BLUE    = "#3B82F6"  # Tactical Blue

BG_DARK        = "#0A0E17"  # Pitch Midnight
BG_CARD        = "#111827"  # Surface Deep Blue-Gray
BG_CARD_ALT    = "#162033"  # Slightly lighter card
BORDER_SUBTLE  = "#1F293D"  # Muted Border
BORDER_ACTIVE  = "#00FF87"  # Glow Border

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
    "Silver Wolves":      "#94A3B8",
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
    <div class="disc-icon">⚠️</div>
    <div>
        <strong>Synthetic Data Advisory:</strong>
        All player attributes, match statistics, and team totals are synthetically generated for demonstration.
    </div>
</div>
"""


def hex_to_rgba(hex_code: str, alpha: float = 0.2) -> str:
    """Converts a hex color code (e.g. #00FF87 or #FFF) to a valid Plotly rgba(r, g, b, a) string."""
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
    return f"rgba(0, 255, 135, {alpha})"


def inject_custom_css():
    """Injects high-end, responsive dark theme styling."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        /* ── Base Reset & Typography ── */
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: #0A0E17;
            color: #E2E8F0;
        }

        /* Hide unnecessary Streamlit default chrome */
        #MainMenu, footer, header { visibility: hidden; height: 0; }
        .stDeployButton { display: none; }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 7px; height: 7px; }
        ::-webkit-scrollbar-track { background: #0A0E17; }
        ::-webkit-scrollbar-thumb {
            background: #1F293D;
            border-radius: 999px;
            border: 2px solid #0A0E17;
        }
        ::-webkit-scrollbar-thumb:hover { background: #00FF87; }

        /* ── Modern Sidebar ── */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0D131F 0%, #090D15 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 4px 0 24px rgba(0,0,0,0.4);
        }
        section[data-testid="stSidebar"] .block-container {
            padding: 1.5rem 1rem 2rem 1rem !important;
        }

        .sidebar-brand {
            padding: 0.5rem 0.5rem 1rem 0.5rem;
            text-align: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.07);
            margin-bottom: 1.25rem;
        }
        .sidebar-brand .brand-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(0, 255, 135, 0.1);
            border: 1px solid rgba(0, 255, 135, 0.3);
            border-radius: 20px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 700;
            color: #00FF87 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        .sidebar-brand h2 {
            font-size: 1.25rem;
            font-weight: 800;
            margin: 0;
            background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        .sidebar-brand p {
            font-size: 0.72rem;
            color: #64748B !important;
            margin: 4px 0 0 0;
            font-weight: 500;
            letter-spacing: 0.5px;
        }

        .sidebar-nav-title {
            font-size: 0.68rem;
            font-weight: 700;
            color: #64748B !important;
            text-transform: uppercase;
            letter-spacing: 1.6px;
            margin: 1.2rem 0 0.5rem 0.4rem;
        }

        /* ── Hero Banners ── */
        .pro-hero {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(14, 22, 38, 0.95) 50%, rgba(6, 182, 212, 0.08) 100%);
            border: 1px solid rgba(0, 255, 135, 0.2);
            border-radius: 18px;
            padding: 1.8rem 2.2rem;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }
        .pro-hero::after {
            content: "";
            position: absolute;
            top: -50px;
            right: -50px;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(0, 255, 135, 0.12) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }
        .hero-title-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
        }
        .hero-left {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .hero-icon-box {
            width: 52px;
            height: 52px;
            border-radius: 14px;
            background: rgba(0, 255, 135, 0.1);
            border: 1px solid rgba(0, 255, 135, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
        }
        .hero-heading {
            font-size: 1.65rem;
            font-weight: 800;
            color: #FFFFFF !important;
            margin: 0;
            letter-spacing: -0.5px;
            line-height: 1.2;
        }
        .hero-desc {
            font-size: 0.88rem;
            color: #94A3B8 !important;
            margin: 4px 0 0 0;
            font-weight: 400;
        }
        .hero-pill {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            color: #00FF87 !important;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        /* ── Disclaimer Box ── */
        .pro-disclaimer {
            background: rgba(245, 158, 11, 0.08);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-left: 4px solid #F59E0B;
            border-radius: 10px;
            padding: 10px 16px;
            font-size: 0.8rem;
            color: #D97706 !important;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .disc-icon { font-size: 1.1rem; }
        .pro-disclaimer strong { color: #F59E0B !important; }

        /* ── Section Headers ── */
        .pro-section {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }
        .pro-section-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.1rem;
            font-weight: 700;
            color: #F8FAFC !important;
            margin: 0;
            letter-spacing: -0.2px;
        }
        .pro-section-subtitle {
            font-size: 0.78rem;
            color: #64748B !important;
            margin: 2px 0 0 0;
        }

        /* ── KPI Cards ── */
        .kpi-card {
            background: linear-gradient(145deg, #111827 0%, #162033 100%);
            border: 1px solid #1F293D;
            border-radius: 14px;
            padding: 1.1rem 1.1rem 0.95rem 1.1rem;
            position: relative;
            overflow: hidden;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            margin-bottom: 0.5rem;
        }
        .kpi-card:hover {
            transform: translateY(-3px);
            border-color: rgba(0, 255, 135, 0.5);
            box-shadow: 0 10px 24px -6px rgba(0, 255, 135, 0.15);
        }
        .kpi-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }
        .kpi-icon-wrap {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.05);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }
        .kpi-label {
            font-size: 0.72rem;
            font-weight: 700;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        .kpi-value {
            font-size: 1.75rem;
            font-weight: 800;
            color: #FFFFFF;
            line-height: 1.1;
            letter-spacing: -0.5px;
            font-feature-settings: "tnum";
            margin-bottom: 0.3rem;
        }
        .kpi-sub {
            font-size: 0.75rem;
            color: #64748B;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .kpi-sub-accent { color: #00FF87; font-weight: 600; }

        /* ── Chart Container ── */
        .chart-box {
            background: #111827;
            border: 1px solid #1F293D;
            border-radius: 14px;
            padding: 8px 8px 4px 8px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }

        /* ── Scouting Card (FIFA / FUT Style) ── */
        .fut-card {
            background: radial-gradient(circle at 50% 20%, #1A2740 0%, #0F172A 75%, #0A0F1D 100%);
            border: 2px solid #F59E0B;
            border-radius: 20px;
            padding: 1.6rem 1.4rem;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), 0 0 24px rgba(245, 158, 11, 0.2);
            position: relative;
            overflow: hidden;
            color: #FFFFFF;
        }
        .fut-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        .fut-rating-box {
            text-align: center;
        }
        .fut-rating {
            font-size: 2.8rem;
            font-weight: 800;
            color: #F59E0B;
            line-height: 1;
            letter-spacing: -1px;
        }
        .fut-position {
            font-size: 0.9rem;
            font-weight: 700;
            color: #E2E8F0;
            letter-spacing: 1px;
        }
        .fut-player-name {
            font-size: 1.4rem;
            font-weight: 800;
            color: #FFFFFF;
            text-align: center;
            margin: 0.5rem 0 0.2rem 0;
            letter-spacing: -0.3px;
        }
        .fut-meta {
            text-align: center;
            font-size: 0.8rem;
            color: #94A3B8;
            margin-bottom: 1.2rem;
        }
        .fut-attributes {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px 16px;
            background: rgba(0,0,0,0.35);
            border-radius: 12px;
            padding: 12px;
            border: 1px solid rgba(255,255,255,0.06);
        }
        .fut-attr-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.82rem;
        }
        .fut-attr-val {
            font-weight: 700;
            color: #00FF87;
        }
        .fut-attr-label {
            color: #94A3B8;
            font-weight: 600;
        }

        /* ── Head to Head Duel Cards ── */
        .duel-container {
            background: #111827;
            border: 1px solid #1F293D;
            border-radius: 16px;
            padding: 1.4rem;
            margin-bottom: 1.2rem;
        }
        .duel-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
        }
        .duel-player {
            flex: 1;
            text-align: center;
            padding: 12px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        .duel-vs {
            padding: 0 16px;
            font-weight: 800;
            font-size: 1.2rem;
            color: #64748B;
        }
        .duel-bar-row {
            margin-bottom: 12px;
        }
        .duel-label-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            font-weight: 600;
            color: #94A3B8;
            margin-bottom: 4px;
        }
        .duel-bar-track {
            height: 8px;
            background: #1F293D;
            border-radius: 4px;
            display: flex;
            overflow: hidden;
        }
        .duel-bar-left {
            background: #00FF87;
            height: 100%;
        }
        .duel-bar-right {
            background: #00D2FF;
            height: 100%;
        }

        /* ── Best XI Pitch Legend ── */
        .pitch-legend {
            display: flex;
            gap: 16px;
            justify-content: center;
            margin-top: 10px;
            font-size: 0.78rem;
            color: #94A3B8;
        }
        .pitch-legend-item {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .pitch-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
        }

        /* ── Streamlit Overrides ── */
        div[data-testid="stRadio"] > div {
            gap: 6px !important;
        }
        div[data-testid="stRadio"] label {
            background: #111827 !important;
            border: 1px solid #1F293D !important;
            border-radius: 10px !important;
            padding: 8px 14px !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            color: #94A3B8 !important;
            transition: all 0.15s ease !important;
        }
        div[data-testid="stRadio"] label:hover {
            border-color: rgba(0, 255, 135, 0.4) !important;
            color: #FFFFFF !important;
        }
        div[data-testid="stRadio"] label:has(input:checked) {
            background: rgba(0, 255, 135, 0.1) !important;
            border-color: #00FF87 !important;
            color: #00FF87 !important;
            box-shadow: 0 0 12px rgba(0, 255, 135, 0.15);
        }

        /* Streamlit Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px !important;
            background-color: transparent !important;
            border-bottom: 1px solid #1F293D !important;
            padding-bottom: 4px !important;
        }
        .stTabs [data-baseweb="tab"] {
            background: #111827 !important;
            border: 1px solid #1F293D !important;
            border-radius: 8px 8px 0 0 !important;
            color: #94A3B8 !important;
            font-weight: 600 !important;
            padding: 8px 16px !important;
        }
        .stTabs [aria-selected="true"] {
            background: #162033 !important;
            border-color: #00FF87 !important;
            border-bottom: 2px solid #00FF87 !important;
            color: #00FF87 !important;
        }

        /* Dataframe styling */
        div[data-testid="stDataFrame"] {
            border: 1px solid #1F293D !important;
            border-radius: 12px !important;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        }

        /* Multiselect Tags */
        span[data-baseweb="tag"] {
            background: rgba(0, 255, 135, 0.15) !important;
            border: 1px solid rgba(0, 255, 135, 0.4) !important;
            color: #00FF87 !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
        }

        /* Download Button */
        div[data-testid="stDownloadButton"] button {
            background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
            border: 1px solid #00FF87 !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            padding: 8px 16px !important;
            width: 100%;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stDownloadButton"] button:hover {
            background: #00FF87 !important;
            color: #0A0E17 !important;
            box-shadow: 0 0 16px rgba(0, 255, 135, 0.35);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_chart(
    fig: go.Figure,
    height: int = 420,
    legend_inside: bool = False,
    show_legend: bool = True,
    title: str = None,
) -> go.Figure:
    """Applies a bespoke dark football analytics styling to Plotly figures."""
    legend_cfg = dict(
        bgcolor="rgba(17, 24, 39, 0.85)",
        bordercolor=BORDER_SUBTLE,
        borderwidth=1,
        font=dict(size=11, color="#94A3B8"),
    )
    if legend_inside:
        legend_cfg.update(x=0.02, y=0.98, xanchor="left", yanchor="top")

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0D131F",
        height=height,
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#CBD5E1", size=12),
        margin=dict(l=20, r=20, t=44 if title else 24, b=24),
        legend=legend_cfg if show_legend else dict(visible=False),
        title=dict(
            text=f"<b>{title}</b>" if title else None,
            font=dict(size=14, color="#F8FAFC"),
            x=0.02,
            y=0.96,
        ) if title else None,
        hoverlabel=dict(
            bgcolor="#111827",
            bordercolor="#00FF87",
            font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#FFFFFF"),
        ),
        xaxis=dict(
            gridcolor="#1F293D",
            linecolor="#1F293D",
            zerolinecolor="#1F293D",
            tickfont=dict(color="#94A3B8", size=11),
        ),
        yaxis=dict(
            gridcolor="#1F293D",
            linecolor="#1F293D",
            zerolinecolor="#1F293D",
            tickfont=dict(color="#94A3B8", size=11),
        ),
    )
    return fig


def render_hero(icon: str, title: str, subtitle: str, pill_text: str = None):
    """Renders a sleek top-page hero banner."""
    pill_html = f'<div class="hero-pill">{pill_text}</div>' if pill_text else ""
    st.markdown(
        f"""
        <div class="pro-hero">
            <div class="hero-title-row">
                <div class="hero-left">
                    <div class="hero-icon-box">{icon}</div>
                    <div>
                        <h1 class="hero-heading">{title}</h1>
                        <p class="hero-desc">{subtitle}</p>
                    </div>
                </div>
                {pill_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi(icon: str, label: str, value: str, subtext: str, accent_color: str = "#00FF87"):
    """Renders an individual KPI card."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-label">{label}</span>
                <div class="kpi-icon-wrap">{icon}</div>
            </div>
            <div class="kpi-value" style="color: {accent_color};">{value}</div>
            <div class="kpi-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(icon: str, title: str, subtitle: str = None):
    """Renders a polished section divider."""
    sub_html = f'<div class="pro-section-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="pro-section">
            <div>
                <div class="pro-section-title"><span>{icon}</span> {title}</div>
                {sub_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
