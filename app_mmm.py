"""
K-MODA - Marketing Mix Modeling
Dashboard ejecutivo Streamlit.

Regla de interfaz:
- Cada st.markdown() con HTML es autocontenido.
- Los widgets Streamlit no se envuelven dentro de divs HTML.
- La lógica de negocio, datos y cálculos se mantiene sin cambios.
"""

import os
import re
from contextlib import contextmanager

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="K-Moda | Decisión de Inversión 2025",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Paleta editorial pastel
BG = "#F5F1EB"
CARD = "#FCFAF7"
CARD2 = "#F8F5F0"
BD = "#E8E2DA"
T = "#2B2B2B"
TS = "#8A817C"
TD = "#B7AFA9"
BLUE = "#C6A27E"       # sand
GREEN = "#A8B8A5"      # sage
INDIGO = "#9FB7C9"     # dusty blue
VIOLET = "#C7B8D6"     # soft lilac
AMBER = "#E6B8A2"      # peach
ROSE = "#A8B8A5"

CH_CLR = {
    "Digital Perf.": BLUE,
    "Digital Awareness": GREEN,
    "Offline": INDIGO,
    "CRM / Email": VIOLET,
}

IMG_DIRS = [
    "graficas_styled/graficas_base",
    "graficas_styled/graficas_decision",
    "graficas/graficas_base",
    "graficas/graficas_decision",
]


def img(name):
    for directory in IMG_DIRS:
        path = os.path.join(directory, name)
        if os.path.exists(path):
            return path
    return None


# Matplotlib
MPL_CARD = (0.988, 0.980, 0.969, 1.0)
MPL_SP = (0.910, 0.886, 0.855, 1.0)
MPL_GR = (0.910, 0.886, 0.855, 0.38)
MPL_T = (0.169, 0.169, 0.169, 1.0)
MPL_TS = (0.541, 0.506, 0.486, 1.0)
MPL_SAND = (0.776, 0.635, 0.494, 0.85)
MPL_SAGE = (0.659, 0.722, 0.647, 0.85)
MPL_DUSTY = (0.624, 0.718, 0.788, 0.85)
MPL_LILAC = (0.780, 0.722, 0.839, 0.85)
MPL_PEACH = (0.902, 0.722, 0.635, 0.85)
MPL_W20 = (0.776, 0.635, 0.494, 0.20)


def sfig(fs=(8, 4)):
    fig, ax = plt.subplots(figsize=fs)
    fig.patch.set_facecolor(MPL_CARD)
    ax.set_facecolor(MPL_CARD)
    ax.tick_params(colors=MPL_TS, labelsize=8.5, length=0, pad=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_edgecolor(MPL_SP)
    ax.spines["bottom"].set_edgecolor(MPL_SP)
    ax.spines["left"].set_linewidth(0.8)
    ax.spines["bottom"].set_linewidth(0.8)
    ax.grid(color=MPL_GR, linestyle="-", linewidth=0.8, axis="y")
    ax.set_axisbelow(True)
    return fig, ax


# CSS
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

*, *::before, *::after {{
    box-sizing: border-box;
}}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container {{
    background: linear-gradient(180deg, {BG} 0%, {CARD2} 100%) !important;
    color: {T} !important;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif !important;
}}

.block-container {{
    max-width: 1320px !important;
    padding: 1.6rem 3rem 6rem !important;
}}

#MainMenu, footer, [data-testid="stDecoration"] {{
    display: none !important;
}}

header {{
    background: transparent !important;
    height: 2.75rem !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    z-index: 999999 !important;
}}

[data-testid="stHeader"] {{
    background: transparent !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    z-index: 999999 !important;
}}

header [data-testid="stToolbar"],
header [data-testid="stHeaderActionElements"] {{
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
}}

header [data-testid="stStatusWidget"] {{
    display: none !important;
}}

[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] {{
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    color: {T} !important;
    z-index: 1000000 !important;
}}

[data-testid="collapsedControl"] button,
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stSidebarCollapseButton"] button {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    color: {T} !important;
    width: 2.25rem !important;
    height: 2.25rem !important;
    border-radius: 999px !important;
    background: {CARD} !important;
    border: 1px solid {BD} !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
}}

[data-testid="collapsedControl"] button *,
[data-testid="stSidebarCollapsedControl"] button *,
[data-testid="stSidebarCollapseButton"] button * {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}}

[data-testid="collapsedControl"] button::before,
[data-testid="stSidebarCollapsedControl"] button::before,
[data-testid="stSidebarCollapseButton"] button::before {{
    content: "☰" !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    color: {T} !important;
    font-family: Arial, sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 900 !important;
    line-height: 1 !important;
}}

[data-testid="stSidebar"] {{
    background: {CARD2} !important;
    border-right: 1px solid {BD} !important;
    box-shadow: none !important;
    z-index: 999998 !important;
}}

[data-testid="stSidebar"] > div:first-child {{
    padding: 2.25rem 1.2rem !important;
}}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {{
    font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif !important;
}}

[data-testid="stButton"] button {{
    width: 100%;
    min-height: 2.8rem;
    background: {CARD} !important;
    color: {T} !important;
    border: 1px solid {BD} !important;
    border-radius: 999px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}}

[data-testid="stButton"] button:hover {{
    border-color: {BLUE} !important;
    color: {T} !important;
    background: {CARD2} !important;
}}

[data-testid="stButton"] button:focus {{
    box-shadow: 0 0 0 2px rgba(198,162,126,0.18) !important;
    outline: none !important;
}}

img {{
    border-radius: 12px;
}}

hr {{
    border: none !important;
    border-top: 1px solid {BD} !important;
    margin: 2.6rem 0 !important;
}}

[data-testid="stSlider"] {{
    padding: 0.1rem 0 0.6rem !important;
}}

[data-testid="stSlider"] label {{
    color: {T} !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
}}

[data-testid="stSlider"] > div > div > div {{
    background: {BLUE} !important;
}}

[data-baseweb="slider"] > div {{
    background: rgba(198,162,126,0.18) !important;
}}

[data-testid="stSlider"] * {{
    text-decoration: none !important;
}}

[data-testid="stSlider"] *:hover {{
    text-decoration: none !important;
}}

[data-testid="stSlider"] [data-baseweb="slider"] {{
    padding-top: 0.35rem !important;
    text-decoration: none !important;
}}

[data-testid="stSlider"] [data-baseweb="slider"] * {{
    text-decoration: none !important;
}}

[data-testid="stSlider"] div[role="tooltip"],
[data-testid="stSlider"] [role="tooltip"],
[data-baseweb="slider"] div[role="tooltip"],
[data-baseweb="slider"] [role="tooltip"],
[data-testid="stSlider"] [data-baseweb="slider"] div[role="tooltip"],
[data-testid="stSlider"] [data-baseweb="slider"] [role="tooltip"] {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}}

[data-testid="stSlider"] [data-baseweb="slider"] div[aria-hidden="true"],
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] > div,
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] span,
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] p,
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"]::before,
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"]::after {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    content: none !important;
}}

[data-baseweb="slider"] div {{
    pointer-events: none;
}}

[data-baseweb="slider"] div[role="slider"] {{
    pointer-events: auto;
}}

[data-testid="stSlider"] [data-testid="stTickBar"],
[data-testid="stSlider"] [data-testid="stTickBar"] * {{
    color: {TS} !important;
    opacity: 1 !important;
    font-size: 0.9rem !important;
    font-weight: 650 !important;
}}

[data-testid="stSlider"] div[role="slider"] {{
    width: 18px !important;
    height: 18px !important;
    border: 2px solid {CARD} !important;
    background: {BLUE} !important;
    box-shadow: 0 0 0 5px rgba(198,162,126,0.12) !important;
}}

.section-card {{
    background: linear-gradient(180deg, {CARD} 0%, {CARD2} 100%);
    border: 1px solid {BD};
    border-radius: 16px;
    padding: 2.35rem;
    margin: 2.9rem 0 2rem;
    box-shadow: 0 6px 16px rgba(138,129,124,0.07);
}}

[data-testid="stVerticalBlockBorderWrapper"] {{
    background: linear-gradient(180deg, {CARD} 0%, {CARD2} 100%) !important;
    border: 1px solid {BD} !important;
    border-radius: 16px !important;
    padding: 2.35rem !important;
    margin: 2.9rem 0 2rem !important;
    box-shadow: 0 6px 16px rgba(138,129,124,0.07) !important;
    width: 100% !important;
    overflow: hidden !important;
}}

[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) {{
    background: linear-gradient(180deg, {CARD} 0%, {CARD2} 100%) !important;
    background-color: {CARD} !important;
    border: 1px solid {BD} !important;
    border-radius: 16px !important;
    padding: 2.35rem !important;
    margin: 2.9rem 0 2rem !important;
    box-shadow: 0 6px 16px rgba(138,129,124,0.07) !important;
}}

[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) > div,
[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) [data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) [data-testid="stVerticalBlock"] > div {{
    background: transparent !important;
    background-color: transparent !important;
}}

[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) [data-testid="stVerticalBlockBorderWrapper"] > div {{
    background: {CARD} !important;
    background-color: {CARD} !important;
}}

.section-card .ui-card,
[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) .ui-card {{
    background: {CARD} !important;
    background-color: {CARD} !important;
    border: 1px solid {BD} !important;
}}

[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) [data-testid="stRadio"] {{
    background: {CARD2} !important;
    background-color: {CARD2} !important;
    border: 1px solid {BD} !important;
}}

[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) [data-testid="stRadio"] label[data-baseweb="radio"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) div[style*="background:#111827"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) div[style*="background: #111827"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) div[style*="background:#162032"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.native-section-card) div[style*="background: #162032"] {{
    background: {CARD2} !important;
    background-color: {CARD2} !important;
}}

[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {{
    gap: 1rem !important;
}}

.element-container:has([data-testid="stVerticalBlockBorderWrapper"]) {{
    width: 100% !important;
    margin: 0 !important;
}}

[data-testid="stVerticalBlockBorderWrapper"] > div {{
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}}

[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stElementContainer"] {{
    width: 100% !important;
}}

[class*="st-key-section_card_"] {{
    background: linear-gradient(180deg, {CARD} 0%, {CARD2} 100%) !important;
    background-color: {CARD} !important;
    border: 1px solid {BD} !important;
    border-radius: 16px !important;
    padding: 2.35rem !important;
    margin: 2.9rem 0 2rem !important;
    box-shadow: 0 6px 16px rgba(138,129,124,0.07) !important;
}}

[class*="st-key-section_card_"] [data-testid="stVerticalBlock"],
[class*="st-key-section_card_"] [data-testid="stVerticalBlock"] > div,
[class*="st-key-section_card_"] [data-testid="stElementContainer"] {{
    background: transparent !important;
    background-color: transparent !important;
}}

[class*="st-key-section_card_"] .ui-card {{
    background: {CARD} !important;
    background-color: {CARD} !important;
    border: 1px solid {BD} !important;
}}

[class*="st-key-section_card_"] [data-testid="stRadio"] {{
    background: {CARD2} !important;
    background-color: {CARD2} !important;
    border: 1px solid {BD} !important;
}}

[class*="st-key-section_card_"] [data-testid="stRadio"] label[data-baseweb="radio"],
[class*="st-key-section_card_"] div[style*="background:#111827"],
[class*="st-key-section_card_"] div[style*="background: #111827"],
[class*="st-key-section_card_"] div[style*="background:#162032"],
[class*="st-key-section_card_"] div[style*="background: #162032"] {{
    background: {CARD2} !important;
    background-color: {CARD2} !important;
}}

.section-header {{
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.9rem;
}}

.section-number {{
    color: {BLUE};
    background: {CARD2};
    border: 1px solid {BD};
    border-radius: 999px;
    padding: 0.35rem 0.75rem;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    line-height: 1;
}}

h2.section-title,
.section-header h2.section-title,
.section-title {{
    margin: 0;
    color: {T} !important;
    font-family: "Playfair Display", serif !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    line-height: 1.2 !important;
    text-transform: none !important;
}}

.section-subtitle {{
    margin: 0;
    color: {TS};
    font-size: 0.96rem;
    line-height: 1.72;
    max-width: 820px;
}}

.section-content {{
    margin-top: 1.5rem;
}}

.section-grid {{
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
    align-items: stretch;
}}

.right-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.15rem;
    height: 100%;
}}

.insight-banner {{
    background: {CARD2};
    border: 1px solid {BD};
    border-left: 2px solid {BLUE};
    border-radius: 16px;
    padding: 1.2rem 1.25rem;
    min-height: 100%;
}}

.insight-banner-title {{
    color: {T};
    font-size: 0.78rem;
    font-weight: 850;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.45rem;
}}

.insight-banner-text {{
    color: {TS};
    font-size: 0.84rem;
    line-height: 1.58;
}}

.stColumn > div {{
    height: 100%;
}}

.element-container:has(.ui-card) {{
    height: 100%;
}}

.ui-card {{
    width: 100%;
    min-height: 100%;
    background: linear-gradient(180deg, {CARD} 0%, {CARD2} 100%);
    border: 1px solid {BD};
    border-radius: 16px;
    padding: 1.6rem;
    overflow-wrap: anywhere;
    word-break: normal;
    box-shadow: 0 6px 16px rgba(138,129,124,0.07);
}}

.metric-card {{
    height: 100%;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    border: 1px solid {BD};
}}

.metric-card:hover {{
    transform: none;
    box-shadow: 0 10px 22px rgba(138,129,124,0.09);
    border: 1px solid rgba(198,162,126,0.45) !important;
}}

.metric-card.no-hover:hover {{
    transform: none;
    box-shadow: none;
}}

.strategy-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.85rem;
}}

.strategy-card {{
    display: block;
    height: 100%;
    min-height: 104px;
    padding: 1rem 1.05rem;
    background: {CARD2};
    border: 1px solid {BD};
    border-radius: 16px;
    text-decoration: none !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}}

.strategy-card:hover {{
    box-shadow: 0 10px 22px rgba(138,129,124,0.09);
    border-color: rgba(198,162,126,0.45);
}}

[data-testid="stRadio"] > div {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.85rem;
}}

[data-testid="stRadio"] {{
    width: 100% !important;
    min-height: auto;
    margin-bottom: 1rem;
    padding: 1.55rem;
    background: {CARD2};
    border: 1px solid {BD};
    border-radius: 16px;
}}

.element-container:has([data-testid="stRadio"]) {{
    width: 100% !important;
}}

[data-testid="stRadio"] > label {{
    margin-bottom: 0.85rem !important;
}}

[data-testid="stRadio"] > label p {{
    color: {TS} !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}}

[data-testid="stRadio"] label[data-baseweb="radio"] {{
    width: 100%;
    min-height: 104px;
    margin: 0 !important;
    padding: 1rem 1.05rem !important;
    background: {CARD} !important;
    border: 1px solid {BD} !important;
    border-radius: 16px !important;
    align-items: flex-start !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
}}

[data-testid="stRadio"] label[data-baseweb="radio"]:hover {{
    border-color: rgba(198,162,126,0.45) !important;
    box-shadow: 0 10px 22px rgba(138,129,124,0.09) !important;
}}

[data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {{
    display: none !important;
}}

[data-testid="stRadio"] label[data-baseweb="radio"] p {{
    color: {T} !important;
    font-size: 0.76rem !important;
    font-weight: 650 !important;
    line-height: 1.4 !important;
    white-space: pre-line !important;
}}

[data-testid="stRadio"] label[data-baseweb="radio"] p::first-line {{
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    line-height: 1.35 !important;
}}

[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(1) p::first-line {{
    color: {GREEN} !important;
}}

[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(2) p::first-line {{
    color: {VIOLET} !important;
}}

[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(3) p::first-line {{
    color: {BLUE} !important;
}}

[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(1):has(input:checked),
[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(1):has([aria-checked="true"]),
[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(1)[aria-checked="true"] {{
    background: rgba(168,184,165,0.14) !important;
    border-color: rgba(168,184,165,0.58) !important;
    box-shadow: 0 10px 22px rgba(138,129,124,0.09) !important;
}}

[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(2):has(input:checked),
[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(2):has([aria-checked="true"]),
[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(2)[aria-checked="true"] {{
    background: rgba(199,184,214,0.16) !important;
    border-color: rgba(199,184,214,0.54) !important;
    box-shadow: 0 10px 22px rgba(138,129,124,0.09) !important;
}}

[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(3):has(input:checked),
[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(3):has([aria-checked="true"]),
[data-testid="stRadio"] label[data-baseweb="radio"]:nth-of-type(3)[aria-checked="true"] {{
    background: rgba(198,162,126,0.14) !important;
    border-color: rgba(198,162,126,0.55) !important;
    box-shadow: 0 10px 22px rgba(138,129,124,0.09) !important;
}}

.strategy-card-title {{
    color: {T};
    font-size: 0.92rem;
    font-weight: 850;
    line-height: 1.2;
}}

.strategy-card-copy {{
    color: {TS};
    font-size: 0.74rem;
    line-height: 1.45;
    margin-top: 0.35rem;
}}

.strategy-card-state {{
    display: inline-flex;
    align-items: center;
    margin-top: 0.75rem;
    padding: 0.16rem 0.5rem;
    border-radius: 6px;
    font-size: 0.66rem;
    font-weight: 850;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}}

.summary-grid {{
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
    align-items: stretch;
}}

.summary-kpi-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    height: 100%;
}}

.dashboard-hero {{
    position: relative;
    padding: 1.5rem 0 1.35rem 0;
    margin: 0 0 2.8rem;
    background: transparent;
    border-radius: 0;
}}

.dashboard-hero-inner {{
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    max-width: 1280px;
    margin-bottom: 0;
}}

.dashboard-hero-accent {{
    width: 44px;
    min-width: 44px;
    height: 1px;
    flex-shrink: 0;
    margin-top: 1.2rem;
    border-radius: 999px;
    background: {BLUE};
}}

.dashboard-hero-eyebrow {{
    margin: 0 0 0.2rem;
    color: {TS};
    font-family: "Inter", sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    line-height: 1.2;
    text-transform: uppercase;
}}

.dashboard-hero-title {{
    margin: 0;
    max-width: 1080px;
    font-family: "Playfair Display", serif !important;
    font-size: 2.5rem;
    font-weight: 600;
    line-height: 1.08;
    letter-spacing: -0.03em;
    color: {INDIGO};
}}

.dashboard-hero-subtitle {{
    margin: 1rem 0 0 0;
    max-width: 820px;
    color: {TS};
    font-family: "Inter", sans-serif;
    font-size: 0.98rem;
    font-weight: 400;
    line-height: 1.75;
}}

.dashboard-hero-pills {{
    display: flex;
    gap: 0.7rem;
    flex-wrap: wrap;
    margin-top: 1.6rem;
}}

.dashboard-hero-decision-grid {{
    display: grid;
    grid-template-columns: 1.35fr 1fr;
    gap: 1rem;
    margin-top: 1.35rem;
    align-items: stretch;
}}

.dashboard-hero-metric-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.75rem;
}}

.dashboard-hero-metric {{
    background: {CARD};
    border: 1px solid {BD};
    border-radius: 16px;
    padding: 1rem 1.05rem;
    min-width: 0;
    overflow-wrap: anywhere;
}}

.dashboard-hero-tradeoff {{
    background: {CARD2};
    border: 1px solid {BD};
    border-left: 2px solid {BLUE};
    border-radius: 16px;
    padding: 1.1rem 1.15rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.dashboard-hero-pill {{
    display: inline-flex;
    align-items: center;
    min-height: 2.25rem;
    padding: 0.45rem 0.9rem;
    border-radius: 999px;
    background: {CARD};
    border: 1px solid {BD};
    color: {TS};
    font-size: 0.78rem;
    font-weight: 500;
}}

.dashboard-hero-pill.is-active {{
    background: {CARD2};
    border-color: rgba(198,162,126,0.55);
    color: {T};
    box-shadow: none;
}}

@media (max-width: 980px) {{
    .dashboard-hero {{
        padding-top: 4.3rem;
    }}

    .dashboard-hero-title {{
        font-size: 2.15rem;
    }}

    .dashboard-hero-accent {{
        width: 28px;
        min-width: 28px;
    }}

    .dashboard-hero-decision-grid,
    .dashboard-hero-metric-grid {{
        grid-template-columns: 1fr !important;
    }}
}}

.glow-blue,
.glow-green,
.glow-violet {{
    text-shadow: none;
}}

@media (max-width: 980px) {{
    .section-grid,
    .summary-grid,
    .strategy-grid {{
        grid-template-columns: 1fr;
    }}

    .right-grid,
    .summary-kpi-grid {{
        grid-template-columns: 1fr;
    }}
}}

.ui-card-lg {{
    padding: 2rem;
}}

.ui-title {{
    margin: 0 0 0.35rem 0;
    color: {T};
    font-family: "Playfair Display", serif;
    font-weight: 600;
    font-size: 1.3rem;
    letter-spacing: -0.025em;
    line-height: 1.2;
}}

.ui-label {{
    margin: 0 0 0.8rem 0;
    color: {TS};
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}}

.ui-copy {{
    color: {TS};
    font-size: 0.94rem;
    line-height: 1.72;
}}

.ui-mono {{
    font-family: "Inter", sans-serif;
    font-variant-numeric: tabular-nums;
}}

h1, h2, h3 {{
    font-family: "Playfair Display", serif !important;
}}

[data-testid="stSubheader"] {{
    margin-top: 0.4rem;
}}

[data-testid="stSubheader"] h3 {{
    color: {T} !important;
    font-family: "Playfair Display", serif !important;
    font-weight: 600 !important;
}}

[data-testid="stAlert"] {{
    background: {CARD2} !important;
    border: 1px solid {BD} !important;
    color: {T} !important;
    border-radius: 16px !important;
}}

[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] p {{
    color: {TS} !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-size: 0.72rem !important;
}}

[data-testid="stSelectbox"] [data-baseweb="select"] > div {{
    background: {CARD} !important;
    border: 1px solid {BD} !important;
    border-radius: 999px !important;
    min-height: 3rem !important;
    box-shadow: none !important;
}}

[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] div {{
    color: {T} !important;
}}

[data-testid="stDataFrame"] {{
    background: {CARD} !important;
    border: 1px solid {BD} !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}}

[data-testid="stDataFrame"] [role="grid"] {{
    border: none !important;
}}

[data-testid="stDataFrame"] [role="columnheader"],
[data-testid="stDataFrame"] [role="gridcell"] {{
    border: none !important;
    background: {CARD} !important;
    color: {TS} !important;
}}

[data-testid="stDataFrame"] [role="columnheader"] {{
    color: {T} !important;
    font-weight: 600 !important;
    border-bottom: 1px solid {BD} !important;
}}

[data-testid="stDataFrame"] [role="row"] {{
    border-bottom: 1px solid rgba(232,226,218,0.55) !important;
}}

[data-testid="stDataFrame"] [role="row"]:last-child {{
    border-bottom: none !important;
}}

[data-testid="stImage"] {{
    background: {CARD} !important;
    border: 1px solid {BD} !important;
    border-radius: 18px !important;
    padding: 0.8rem !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
    overflow: hidden !important;
}}

[data-testid="stImage"] img {{
    border-radius: 12px !important;
}}

[data-testid="stCaptionContainer"] {{
    margin-top: 0.55rem !important;
}}

[data-testid="stCaptionContainer"] p {{
    color: {TS} !important;
    font-size: 0.82rem !important;
    line-height: 1.65 !important;
}}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<script>
function animateCountUps() {
  const nodes = document.querySelectorAll("[data-countup]:not([data-counted='true'])");
  nodes.forEach((node) => {
    node.dataset.counted = "true";
    const target = Number(node.dataset.target || "0");
    const decimals = Number(node.dataset.decimals || "0");
    const suffix = node.dataset.suffix || "";
    const prefix = node.dataset.prefix || "";
    const duration = Number(node.dataset.duration || "1000");
    const start = performance.now();
    const easeOut = (t) => 1 - Math.pow(1 - t, 3);
    function frame(now) {
      const progress = Math.min((now - start) / duration, 1);
      const value = target * easeOut(progress);
      node.textContent = prefix + value.toFixed(decimals).replace(".", ",") + suffix;
      if (progress < 1) requestAnimationFrame(frame);
    }
    node.textContent = prefix + (0).toFixed(decimals).replace(".", ",") + suffix;
    requestAnimationFrame(frame);
  });
}
document.addEventListener("DOMContentLoaded", animateCountUps);
setTimeout(animateCountUps, 250);
setTimeout(animateCountUps, 900);
</script>
""",
    unsafe_allow_html=True,
)


# Helpers visuales
def render_header_kmoda():
    st.markdown(
        f"""
<section class="dashboard-hero">
  <div class="dashboard-hero-inner">
    <div class="dashboard-hero-accent"></div>
    <div>
      <div class="dashboard-hero-eyebrow">K-MODA · MARKETING MIX MODELING · 2020-2024</div>
      <h1 class="dashboard-hero-title" style="color:{BLUE};">
        Asignación Óptima de Inversión en Marketing
      </h1>
      <p class="dashboard-hero-subtitle">
        Modelo econométrico para estimar qué parte de las ventas genera cada bloque de marketing,
        detectar saturación y redistribuir el presupuesto anual de
        <strong style="color:{T};font-weight:600;">12.000.000 €</strong> hacia el mix con mayor retorno esperado.
      </p>
      <div class="dashboard-hero-pills">
        <div class="dashboard-hero-pill is-active">BASE</div>
        <div class="dashboard-hero-pill">R² 0,885</div>
        <div class="dashboard-hero-pill">MAPE 7,53%</div>
        <div class="dashboard-hero-pill">ElasticNet</div>
        <div class="dashboard-hero-pill">260 semanas</div>
      </div>
    </div>
  </div>
</section>
""",
        unsafe_allow_html=True,
    )


def sec(number, title, subtitle, color=BLUE):
    st.markdown(
        f"""
<section class="section-card">
  <div class="section-header">
    <div class="section-number" style="color:{color};background:{color}14;border-color:{color}30;">{number:02d}</div>
    <h2 class="section-title" style="font-size:0.9rem !important;">{title}</h2>
  </div>
  <p class="section-subtitle">{subtitle}</p>
</section>
""",
        unsafe_allow_html=True,
    )


@contextmanager
def section_container(number, title, subtitle, color=BLUE):
    with st.container(border=False, key=f"section_card_{number}"):
        st.markdown(
            f"""
<div class="section-header native-section-card" style="margin-bottom:0.15rem;">
  <div class="section-number" style="color:{color};background:{color}14;border-color:{color}30;">{number:02d}</div>
  <div>
    <h2 class="section-title" style="font-size:0.9rem !important;">{title}</h2>
    <p class="section-subtitle">{subtitle}</p>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        yield


def card_html(title, body, label=None, accent=BLUE, extra_style=""):
    label_html = (
        f'<div class="ui-label" style="color:{accent};">{label}</div>'
        if label
        else ""
    )
    st.markdown(
        f"""
<div class="ui-card ui-card-lg" style="{extra_style}">
  {label_html}
  <h3 class="ui-title" style="font-size:1.08rem;">{title}</h3>
  {body}
</div>
""",
        unsafe_allow_html=True,
    )


def count_value(value, glow=""):
    raw = str(value)
    simple_number = re.match(r"^[+-]?\d+(?:[,.]\d+)?", raw.strip())
    if not simple_number:
        return f'<span class="{glow}">{raw}</span>'
    number = ""
    for char in raw:
        if char.isdigit() or char in ",.":
            number += char
        elif number:
            break
    if number.count(".") + number.count(",") > 1:
        return f'<span class="{glow}">{raw}</span>'
    suffix = raw.replace(number, "", 1)
    decimals = 0
    if "," in number:
        decimals = len(number.split(",", 1)[1])
    elif "." in number:
        decimals = len(number.split(".", 1)[1])
    target = number.replace(",", ".") if number else "0"
    return (
        f'<span class="count-up {glow}" data-countup data-target="{target}" '
        f'data-decimals="{decimals}" data-suffix="{suffix}" data-duration="1000">{raw}</span>'
    )


def kpi(label, value, delta=None, color=BLUE, value_font_size="2.2rem", value_white_space="nowrap"):
    delta_color = GREEN if delta and "+" in str(delta) else INDIGO
    glow = "glow-green" if color == GREEN else ("glow-violet" if color == VIOLET else ("glow-blue" if color == BLUE else ""))
    delta_html = (
        f'<div style="margin-top:0.45rem;color:{delta_color};font-size:0.76rem;'
        f'font-weight:500;line-height:1.45;">{delta}</div>'
        if delta
        else ""
    )
    st.markdown(
        f"""
<div class="ui-card metric-card" style="display:flex;flex-direction:column;justify-content:center;min-height:132px;">
  <div class="ui-label">{label}</div>
  <div class="ui-mono" style="color:{T};font-size:{value_font_size};font-weight:600;
       letter-spacing:-0.045em;line-height:1;white-space:{value_white_space};">{count_value(value, glow)}</div>
  {delta_html}
</div>
""",
        unsafe_allow_html=True,
    )


def insight(text, color=BLUE):
    st.markdown(
        f"""
<div style="border-left:2px solid {color};background:{CARD2};border:1px solid {BD};border-left:2px solid {color};border-radius:16px;
            padding:1.15rem 1.3rem;margin-top:1.5rem;color:{TS};font-size:0.9rem;line-height:1.72;">
  {text}
</div>
""",
        unsafe_allow_html=True,
    )


def image_card(title, subtitle, path):
    st.markdown(
        f"""
<div class="ui-card" style="padding:1rem 1rem 0.85rem;min-height:auto;">
  <div class="ui-label" style="margin-bottom:0.25rem;">{title}</div>
  <div style="color:{TS};font-size:0.78rem;line-height:1.45;margin-bottom:0.8rem;">{subtitle}</div>
</div>
""",
        unsafe_allow_html=True,
    )
    if path:
        st.markdown('<div style="margin-top:-0.2rem;"></div>', unsafe_allow_html=True)
        st.image(path, use_container_width=True)
    else:
        st.markdown(
            f"""
<div class="ui-card" style="display:flex;align-items:center;justify-content:center;
            min-height:320px;color:{TS};text-align:center;">
  Imagen no encontrada
</div>
""",
            unsafe_allow_html=True,
        )


def spacer(height="1rem"):
    st.markdown(f'<div style="height:{height};"></div>', unsafe_allow_html=True)


# Markdown como fuente de verdad
DOC_FILES = {
    "base": "BASE.md",
    "decisiones": "DECISIONES.md",
    "roi_vs_ventas": "ROI_VS_VENTAS.md",
}


@st.cache_data
def read_markdown(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def extract_section(text, heading):
    pattern = rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_subsection(text, heading):
    pattern = rf"^###\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^###\s+|^##\s+|\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def markdown_tables(section_text):
    tables = []
    lines = section_text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines) and "---" in lines[i + 1]:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            header = [c.strip() for c in table_lines[0].strip("|").split("|")]
            rows = []
            for row in table_lines[2:]:
                cells = [c.strip() for c in row.strip("|").split("|")]
                if len(cells) == len(header):
                    rows.append(cells)
            tables.append(pd.DataFrame(rows, columns=header))
        else:
            i += 1
    return tables


def first_table(section_text):
    tables = markdown_tables(section_text)
    return tables[0] if tables else pd.DataFrame()


@st.cache_data
def load_markdown_sources():
    base = read_markdown(DOC_FILES["base"])
    decisiones = read_markdown(DOC_FILES["decisiones"])
    roi_vs_ventas = read_markdown(DOC_FILES["roi_vs_ventas"])

    base_summary = extract_section(base, "Executive Summary")
    base_kpis = first_table(extract_section(base, "Model KPIs"))
    channel_roi = first_table(extract_section(base, "Channel Contribution & ROI"))
    budget_results = extract_section(base, "Budget Optimization Results")
    base_scenarios = first_table(extract_subsection(budget_results, "Scenario Comparison"))
    response_curves = first_table(extract_section(base, "Response Curves"))

    decision_scenarios = first_table(extract_subsection(decisiones, "Resultados centrales"))
    decision_budget = first_table(extract_subsection(decisiones, "Desglose de inversión por canal"))
    frontier = first_table(extract_subsection(decisiones, "Frontera de eficiencia"))
    roi_targets = first_table(extract_subsection(decisiones, "Presupuesto necesario por objetivo ROI"))
    frontier_zones = first_table(extract_subsection(decisiones, "Interpretación estratégica"))
    roi_strategy = first_table(extract_section(roi_vs_ventas, "Escenarios estratégicos"))

    return {
        "base_text": base,
        "decisiones_text": decisiones,
        "roi_text": roi_vs_ventas,
        "base_summary": base_summary,
        "base_kpis": base_kpis,
        "channel_roi": channel_roi,
        "base_scenarios": base_scenarios,
        "response_curves": response_curves,
        "decision_scenarios": decision_scenarios,
        "decision_budget": decision_budget,
        "frontier": frontier,
        "roi_targets": roi_targets,
        "frontier_zones": frontier_zones,
        "roi_strategy": roi_strategy,
    }


def table_value(df, key_col, key_value, value_col, fallback="Pendiente"):
    if df.empty or key_col not in df or value_col not in df:
        return fallback
    rows = df[df[key_col].astype(str).str.strip() == key_value]
    if rows.empty:
        return fallback
    return rows.iloc[0][value_col]


def parse_markdown_number(value):
    text = str(value)
    match = re.search(r"-?\d+(?:[.,]\d+)?", text)
    if not match:
        return np.nan
    return float(match.group(0).replace(",", "."))


def frontier_position(roi_value):
    if roi_value > 25:
        return "Máxima eficiencia", "Muy bajo", "Bajas", "Optimización extrema", GREEN
    if 17 <= roi_value <= 20:
        return "Eficiencia", "Bajo", "Medias", "Rentabilidad", GREEN
    if 12 <= roi_value <= 14:
        return "Equilibrio", "Medio", "Altas", "Sostenibilidad", BLUE
    if 8 <= roi_value <= 12:
        return "Crecimiento", "Alto", "Máximas", "Cuota de mercado", VIOLET
    return "Zona intermedia", "Ver frontera", "Ver frontera", "Trade-off", AMBER


def scenario_position(name):
    if "Agresivo" in name:
        return "Crecimiento"
    if "Eficiencia" in name or "Conservador" in name:
        return "Eficiencia"
    if "Marca" in name:
        return "Marca"
    return "Equilibrio"


def image_with_caption(path, caption):
    if path:
        st.image(path, use_container_width=True)
    else:
        st.markdown(
            f"""
<div class="ui-card" style="display:flex;align-items:center;justify-content:center;
            min-height:280px;color:{TS};text-align:center;">
  Imagen no encontrada
</div>
""",
            unsafe_allow_html=True,
        )
    st.caption(caption)


MD = load_markdown_sources()


# Datos
CHANNELS = {
    "Digital Perf.": {
        "inv": 23_820_560,
        "ventas": 102_881_773,
        "roi": 4.32,
        "inv_anual": 4_764_112,
        "inv_opt": 3_194_809,
        "k": 144_377,
    },
    "Digital Awareness": {
        "inv": 13_857_063,
        "ventas": 114_871_091,
        "roi": 8.29,
        "inv_anual": 2_771_413,
        "inv_opt": 3_770_113,
        "k": 214_460,
    },
    "Offline": {
        "inv": 19_230_564,
        "ventas": 85_659_456,
        "roi": 4.45,
        "inv_anual": 3_846_113,
        "inv_opt": 4_382_995,
        "k": 164_940,
    },
    "CRM / Email": {
        "inv": 2_933_929,
        "ventas": 71_211_477,
        "roi": 24.27,
        "inv_anual": 586_786,
        "inv_opt": 652_082,
        "k": 14_848,
    },
}


def rc(inv, k, beta):
    return beta * np.log1p(inv / k)


for ch, data in CHANNELS.items():
    ventas_anuales = data["ventas"] / 5
    data["beta"] = (
        ventas_anuales / np.log1p(data["inv_anual"] / data["k"])
        if data["inv_anual"] > 0
        else 1
    )

TOTAL = 12_000_000
BASE_Y = 391_393_401 / 5
BLINE = 156_207_159
ACTUAL_SALES = 153_203_439
current_marketing_sales = sum(data["ventas"] / 5 for data in CHANNELS.values())
current_roi = current_marketing_sales / TOTAL
optimal_marketing_sales = sum(
    rc(data["inv_opt"], data["k"], data["beta"]) for data in CHANNELS.values()
)
optimal_roi = optimal_marketing_sales / TOTAL

with st.sidebar:
    st.markdown(
        f"""
<div style="padding:0.25rem 0 0.9rem;">
  <div style="color:{TS};font-size:0.72rem;font-weight:600;letter-spacing:0.16em;text-transform:uppercase;margin-bottom:0.55rem;">
    K-MODA · DECISIÓN 2025
  </div>
  <h2 style="margin:0;color:{T};font-size:1.7rem;font-weight:600;letter-spacing:-0.03em;line-height:1.08;font-family:'Playfair Display',serif;">
    Crecimiento vs eficiencia
  </h2>
  <div style="margin-top:0.7rem;color:{TS};font-size:0.88rem;line-height:1.7;">
    El modelo no decide por la empresa: muestra el coste de elegir más ventas o más ROI.
  </div>
</div>

<div style="background:{CARD};border:1px solid {BD};border-left:2px solid {BLUE};
            border-radius:16px;padding:1.05rem 1.1rem;margin-top:0.9rem;box-shadow:0 4px 12px rgba(0,0,0,0.04);">
  <div style="color:{TS};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.45rem;">
    Pregunta central
  </div>
  <div style="color:#5F768A;font-size:1rem;font-weight:600;line-height:1.45;">
    ¿Priorizar volumen de ventas o eficiencia de inversión?
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.65rem;margin-top:0.8rem;">
  <div style="background:{CARD};border:1px solid {BD};border-radius:16px;padding:0.95rem 1rem;">
    <div style="color:{TS};font-size:0.66rem;font-weight:600;text-transform:uppercase;letter-spacing:0.12em;">Uplift validado</div>
    <div class="ui-mono" style="color:{T};font-size:1.35rem;font-weight:600;margin-top:0.3rem;">+3,0M€</div>
  </div>
  <div style="background:{CARD};border:1px solid {BD};border-radius:16px;padding:0.95rem 1rem;">
    <div style="color:{TS};font-size:0.66rem;font-weight:600;text-transform:uppercase;letter-spacing:0.12em;">Presupuesto base</div>
    <div class="ui-mono" style="color:{T};font-size:1.35rem;font-weight:600;margin-top:0.3rem;">12M€</div>
  </div>
</div>

<div style="margin-top:0.95rem;background:{CARD};border:1px solid {BD};border-radius:16px;
            padding:1rem;color:{TS};font-size:0.82rem;line-height:1.65;">
  <strong style="color:{T};">Frontera:</strong> higher ROI → lower budget → lower sales.
</div>
""",
        unsafe_allow_html=True,
    )


# Hero
render_header_kmoda()


# 01 Resumen ejecutivo
st.markdown(
    f"""
<section class="section-card">
  <div class="section-header">
    <span class="section-number" style="color:{BLUE};background:{BLUE}14;border-color:{BLUE}30;">01</span>
    <div>
      <h2 class="section-title" style="font-size:0.9rem !important;">Resumen ejecutivo</h2>
      <p class="section-subtitle">El marketing genera 374,6M€ en ventas incrementales, casi la mitad del total modelado.</p>
    </div>
  </div>
  <div class="section-content">
    <div class="section-grid">
      <div class="ui-card metric-card" style="min-height:100%;padding:1.65rem 1.75rem;background:{CARD};display:flex;flex-direction:column;justify-content:center;">
        <div class="ui-label" style="color:{BLUE};margin-bottom:0.45rem;">Ventas totales modeladas · 2020-2024</div>
        <div class="ui-mono glow-blue" style="font-size:4rem;font-weight:600;color:{T};
             letter-spacing:-0.055em;line-height:0.98;margin:0 0 0.35rem;">
          <span data-countup data-target="766" data-decimals="0" data-suffix="" data-duration="1000">766</span>
          <span style="display:inline-block;margin-left:0.28rem;font-size:1.82rem;color:{TS};font-weight:650;letter-spacing:-0.02em;">M€</span>
        </div>
        <div class="ui-copy" style="font-size:0.86rem;margin-bottom:0.85rem;">Ventas totales generadas en el periodo analizado.</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.65rem;margin-bottom:1rem;">
          <div style="background:{CARD2};border:1px solid {BD};border-radius:14px;padding:0.85rem 0.9rem;">
            <div class="ui-label" style="margin-bottom:0.25rem;">Periodo</div>
            <div class="ui-mono" style="color:{T};font-size:0.98rem;font-weight:600;">2020-2024</div>
          </div>
          <div style="background:{CARD2};border:1px solid {BD};border-radius:14px;padding:0.85rem 0.9rem;">
            <div class="ui-label" style="margin-bottom:0.25rem;">Semanas</div>
            <div class="ui-mono" style="color:{T};font-size:0.98rem;font-weight:600;">260</div>
          </div>
          <div style="background:{CARD2};border:1px solid {BD};border-radius:14px;padding:0.85rem 0.9rem;">
            <div class="ui-label" style="margin-bottom:0.25rem;">Bloques</div>
            <div class="ui-mono" style="color:{T};font-size:0.98rem;font-weight:600;">4</div>
          </div>
        </div>
        <div style="display:flex;gap:1rem;align-items:stretch;">
          <div style="flex:1;">
            <div class="ui-label" style="margin-bottom:0.18rem;">Marketing</div>
            <div class="ui-mono glow-violet" style="color:{T};font-size:1.5rem;font-weight:600;line-height:1;">48,9%</div>
          </div>
          <div style="width:1px;background:{BD};"></div>
          <div style="flex:1;">
            <div class="ui-label" style="margin-bottom:0.18rem;">Base</div>
            <div class="ui-mono" style="color:{TS};font-size:1.5rem;font-weight:600;line-height:1;">51,1%</div>
          </div>
        </div>
      </div>
      <div class="right-grid">
        <div class="ui-card metric-card" style="display:flex;flex-direction:column;justify-content:center;min-height:132px;">
          <div class="ui-label">Contribución marketing</div>
          <div class="ui-mono glow-violet" style="color:{T};font-size:1.55rem;font-weight:600;letter-spacing:-0.03em;line-height:1;white-space:nowrap;">
            <span data-countup data-target="374.6" data-decimals="1" data-suffix="M€" data-duration="1000">374,6M€</span>
          </div>
          <div style="margin-top:0.45rem;color:{TS};font-size:0.76rem;font-weight:500;line-height:1.45;">+ ventas incrementales</div>
        </div>
        <div class="ui-card metric-card" style="display:flex;flex-direction:column;justify-content:center;min-height:132px;">
          <div class="ui-label">ROI canal top</div>
          <div class="ui-mono glow-green" style="color:{T};font-size:2.2rem;font-weight:600;letter-spacing:-0.045em;line-height:1;">
            <span data-countup data-target="24.3" data-decimals="1" data-suffix="x" data-duration="1000">24,3x</span>
          </div>
          <div style="margin-top:0.45rem;color:{TS};font-size:0.76rem;font-weight:500;line-height:1.45;">CRM / Email</div>
        </div>
        <div class="ui-card metric-card" style="display:flex;flex-direction:column;justify-content:center;min-height:132px;">
          <div class="ui-label">Impacto potencial</div>
          <div class="ui-mono glow-green" style="color:{GREEN};font-size:1.7rem;font-weight:600;letter-spacing:-0.03em;line-height:1;white-space:nowrap;">
            +<span data-countup data-target="3.0" data-decimals="1" data-suffix="M€" data-duration="1000">3,0M€</span>
          </div>
          <div style="margin-top:0.45rem;color:{TS};font-size:0.76rem;font-weight:500;line-height:1.45;">mix óptimo · predict directo</div>
        </div>
        <div class="ui-card metric-card" style="display:flex;flex-direction:column;justify-content:center;min-height:132px;">
          <div class="ui-label">Error modelo</div>
          <div class="ui-mono" style="color:{T};font-size:2.2rem;font-weight:600;letter-spacing:-0.045em;line-height:1;">
            <span data-countup data-target="7.53" data-decimals="2" data-suffix="%" data-duration="1000">7,53%</span>
          </div>
          <div style="margin-top:0.45rem;color:{TS};font-size:0.76rem;font-weight:500;line-height:1.45;">R² = 0,885</div>
        </div>
      </div>
    </div>
    <div style="margin-top:1.2rem;background:{CARD2};border:1px solid {BD};border-left:2px solid {BLUE};
                border-radius:16px;padding:1.15rem 1.2rem;color:{TS};font-size:0.92rem;line-height:1.72;">
      <strong style="color:{T};">Lectura ejecutiva:</strong> K-Moda mantiene el 51,1% de sus ventas por
      base estructural. El 48,9% restante, <strong style="color:{T};">374,6M€</strong>,
      se atribuye al efecto incremental del marketing. La lectura prioritaria es proteger la base de negocio
      y reasignar la inversión hacia los canales con mayor retorno marginal esperado.
      <strong style="color:{T};">El modelo identifica una oportunidad clara, pero no define la estrategia:
      crecer implica sacrificar eficiencia.</strong>
    </div>
  </div>
</section>
""",
    unsafe_allow_html=True,
)


# 02 Problema de negocio
with section_container(
    2,
    "Problema de atribución",
    "Los canales se activan de forma sincronizada; por eso el último clic no separa correctamente el impacto real.",
    ROSE,
):
    col_p1, col_p2 = st.columns([3, 2], gap="large")
    with col_p1:
        image_card(
            "Ventas vs inversión total",
            "La inversión se activa en momentos comerciales concretos; por eso hace falta separar base, calendario y marketing.",
            img("03_yt_vs_inversion_total.png"),
        )
        card_html(
            "Lectura de negocio",
            f"""
<div class="ui-copy">
  Las ventas no se explican solo por presión publicitaria. La inversión acompaña campañas,
  calendario comercial, promociones y momentos de demanda inducida. El MMM separa esas señales
  para no confundir correlación temporal con contribución incremental.
</div>
""",
            label="Por qué importa",
            accent=ROSE,
            extra_style="margin-top:0.85rem;min-height:auto;",
        )

    with col_p2:
        problem_rows = [
            ("Sobre-atribución al último clic", "Search y Social capturan crédito de compras ya influenciadas por otros medios.", ROSE),
            ("Canales offline menos visibles", "Radio, prensa y exterior construyen demanda sin dejar trazas digitales directas.", AMBER),
            ("Efecto temporal acumulado", "El impacto publicitario puede aparecer con retraso y persistir varias semanas.", INDIGO),
        ]
        rows_html = ""
        for title, desc, color in problem_rows:
            rows_html += f"""
  <div style="display:flex;gap:0.85rem;padding:1rem 0;border-bottom:1px solid {BD};">
    <div style="width:4px;min-height:46px;background:{color};border-radius:4px;flex:0 0 auto;"></div>
    <div>
      <div style="color:{T};font-size:0.9rem;font-weight:750;margin-bottom:0.25rem;">{title}</div>
      <div class="ui-copy" style="font-size:0.84rem;">{desc}</div>
    </div>
  </div>
"""
        card_html(
            "Por qué el MMM es necesario",
            rows_html
            + f"""
<div style="margin-top:1rem;background:{CARD2};border:1px solid {BD};border-radius:16px;
            padding:1rem;color:{TS};font-size:0.88rem;line-height:1.7;">
  <strong style="color:{T};">Enfoque aplicado:</strong> datos agregados semanales, adstock,
  saturación y regularización para estimar impacto incremental sin depender de cookies.
</div>
""",
            label="Diagnóstico metodológico",
            accent=ROSE,
        )

# 03 Diagnóstico del mix
with section_container(
    3,
    "Diagnóstico del mix actual",
    "Digital Performance concentra el mayor presupuesto anual, pero muestra el ROI histórico más bajo del portfolio.",
    AMBER,
):
    col_d1, col_d2 = st.columns([3, 2], gap="large")
    with col_d1:
        p = img("economic_current_vs_optimal_investment.png")
        if p:
            image_card(
                "Inversión actual vs óptima",
                "Comparativa por bloque de inversión, expresada en millones de euros al año.",
                p,
            )
        else:
            fig, ax = sfig((7.4, 4.4))
            chs = list(CHANNELS.keys())
            x = np.arange(len(chs))
            actual = [CHANNELS[c]["inv_anual"] / 1e6 for c in chs]
            optimal = [CHANNELS[c]["inv_opt"] / 1e6 for c in chs]
            ax.bar(x - 0.2, actual, 0.35, color=MPL_DUSTY, alpha=0.85, label="Actual")
            ax.bar(x + 0.2, optimal, 0.35, color=MPL_SAND, alpha=0.9, label="Óptimo")
            for i, (a, o) in enumerate(zip(actual, optimal)):
                ax.text(i - 0.2, a + 0.05, f"{a:.1f}", ha="center", fontsize=7.5, color=MPL_TS)
                ax.text(i + 0.2, o + 0.05, f"{o:.1f}", ha="center", fontsize=7.5, color=MPL_T)
            ax.set_xticks(x)
            ax.set_xticklabels(chs, fontsize=7.5, color=MPL_TS)
            ax.set_ylabel("M€/año", color=MPL_TS, fontsize=8)
            legend = ax.legend(fontsize=7.5, frameon=True, borderpad=0.6, labelcolor=MPL_TS, loc="upper right")
            legend.get_frame().set_facecolor((0.973, 0.961, 0.941, 1.0))
            legend.get_frame().set_edgecolor(MPL_SP)
            legend.get_frame().set_linewidth(0.8)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    with col_d2:
        roi_rows = ""
        for name, roi, color, width, note in [
            ("CRM / Email", 24.27, GREEN, 99, "Alta eficiencia histórica"),
            ("Digital Awareness", 8.29, VIOLET, 34, "Potencial de crecimiento"),
            ("Offline", 4.45, INDIGO, 18, "Rol complementario"),
            ("Digital Perf.", 4.32, ROSE, 18, "Saturación relativa"),
        ]:
            roi_rows += f"""
  <div style="padding:0.95rem 0;border-bottom:1px solid {BD};">
    <div style="display:flex;justify-content:space-between;gap:1rem;align-items:center;margin-bottom:0.45rem;">
      <div style="min-width:0;">
        <div style="color:{T};font-size:0.9rem;font-weight:750;">{name}</div>
        <div style="color:{TS};font-size:0.74rem;line-height:1.4;">{note}</div>
      </div>
      <div class="ui-mono" style="color:{T};font-size:1.18rem;font-weight:600;white-space:nowrap;">{roi:.1f}x</div>
    </div>
    <div style="height:7px;background:{BD};border-radius:999px;overflow:hidden;">
      <div style="height:100%;width:{width}%;background:{color};border-radius:999px;"></div>
    </div>
  </div>
"""
        card_html("Eficiencia por canal", roi_rows, label="ROI histórico", accent=AMBER)

    insight(
        f"""
<strong style="color:{T};">Diagnóstico:</strong> el 40% del presupuesto se concentra en Digital Performance,
el canal menos eficiente del mix. La optimización propone liberar inversión de este bloque y reforzar
Awareness, Offline y CRM sin elevar el presupuesto total.
""",
        AMBER,
    )

# 04 Saturación
with section_container(
    4,
    "Saturación de canales",
    "La relación inversión-ventas no es lineal; cada bloque tiene rendimientos marginales decrecientes.",
    INDIGO,
):
    col_s1, col_s2 = st.columns([3, 2], gap="large")
    with col_s1:
        p = img("fase6_curvas_respuesta.png")
        if p:
            image_card(
                "Curvas de respuesta",
                "Delta de ventas estimado frente al mix actual y niveles de inversión alternativos.",
                p,
            )
        else:
            fig, ax = sfig((7.4, 4.4))
            inv_range = np.linspace(0.1e6, 8e6, 300)
            for ch, data in CHANNELS.items():
                ventas = [rc(x, data["k"], data["beta"]) for x in inv_range]
                ax.plot(inv_range / 1e6, [v / 1e6 for v in ventas], color=CH_CLR[ch], linewidth=2.0, label=ch)
                ax.axvline(data["inv_anual"] / 1e6, color=CH_CLR[ch], linestyle=(0, (2, 3)), linewidth=0.9, alpha=0.5)
            ax.set_xlabel("Inversión (M€/año)", color=MPL_TS, fontsize=8)
            ax.set_ylabel("Ventas atribuidas (M€)", color=MPL_TS, fontsize=8)
            legend = ax.legend(fontsize=7.2, frameon=True, borderpad=0.6, labelcolor=MPL_TS, loc="upper left")
            legend.get_frame().set_facecolor((0.973, 0.961, 0.941, 1.0))
            legend.get_frame().set_edgecolor(MPL_SP)
            legend.get_frame().set_linewidth(0.8)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    with col_s2:
        sat_rows = ""
        for name, level, color, width, desc in [
            ("Digital Perf.", "Alta", ROSE, 92, "Cerca del techo; ROI marginal bajo."),
            ("Offline", "Media", AMBER, 65, "Margen de crecimiento moderado."),
            ("Digital Awareness", "Baja", GREEN, 40, "Recorrido significativo disponible."),
            ("CRM / Email", "Muy baja", GREEN, 18, "Potencial adicional con inversión contenida."),
        ]:
            sat_rows += f"""
  <div style="padding:0.95rem 0;border-bottom:1px solid {BD};">
    <div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;margin-bottom:0.5rem;">
      <span style="color:{T};font-size:0.9rem;font-weight:750;">{name}</span>
      <span style="color:{T};background:{CARD2};border:1px solid {BD};border-radius:999px;
                   padding:0.22rem 0.65rem;font-size:0.72rem;font-weight:600;white-space:nowrap;">Sat. {level}</span>
    </div>
    <div style="height:7px;background:{BD};border-radius:999px;overflow:hidden;margin-bottom:0.45rem;">
      <div style="height:100%;width:{width}%;background:{color};
                  border-radius:999px;"></div>
    </div>
    <div style="color:{TS};font-size:0.76rem;line-height:1.45;">{desc}</div>
  </div>
"""
        card_html("Estado de saturación", sat_rows, label="Rendimiento marginal", accent=INDIGO)
    insight(
        f"""
<strong style="color:{T};">Lectura ejecutiva:</strong> más inversión en Performance ya no genera
crecimiento proporcional. La siguiente mejora viene de reasignar presupuesto hacia canales con más recorrido marginal.
""",
        INDIGO,
    )

# 05 Frontera ROI vs Ventas
with section_container(
    5,
    "Frontera ROI vs ventas",
    "El punto estratégico no es solo el mix: es el nivel de presupuesto que dirección está dispuesta a sostener.",
    ROSE,
):
    insight(
        f"""
<strong style="color:{T};">Decisión central:</strong> este gráfico define la única decisión estratégica relevante del modelo:
elegir entre más ventas con menor ROI o más eficiencia con menor volumen.
""",
        ROSE,
    )
    st.subheader("Frontera estratégica")
    f1, f2 = st.columns(2, gap="large")
    with f1:
        image_with_caption(
            img("decision_05_efficiency_frontier.png"),
            "Un ROI más alto exige menor presupuesto; crecimiento y eficiencia avanzan en direcciones opuestas.",
        )
    with f2:
        image_with_caption(
            img("decision_06_frontier_alloc.png"),
            "La asignación presupuestaria evoluciona a lo largo de la frontera: el posicionamiento estratégico cambia con el nivel de inversión.",
        )

    frontier_targets = MD["roi_targets"]
    if not frontier_targets.empty:
        st.dataframe(frontier_targets, use_container_width=True, hide_index=True)
    else:
        st.info("Objetivos ROI pendientes en DECISIONES.md.")

    c13, c17, c20 = st.columns(3, gap="large")
    with c13:
        card_html(
            "ROI ≈ 13",
            f'<div class="ui-mono" style="color:{T};font-size:1.45rem;font-weight:600;">12,1 M€ · 161,0 M€ ventas</div>',
            label="Presupuesto equivalente",
            accent=BLUE,
        )
    with c17:
        card_html(
            "ROI ≈ 17",
            f'<div class="ui-mono" style="color:{T};font-size:1.45rem;font-weight:600;">8,5 M€ · 147,2 M€ ventas</div>',
            label="Alta eficiencia",
            accent=VIOLET,
        )
    with c20:
        card_html(
            "ROI ≈ 20",
            f'<div class="ui-mono" style="color:{T};font-size:1.45rem;font-weight:600;">7,3 M€ · 141,4 M€ ventas</div>',
            label="Eficiencia extrema",
            accent=GREEN,
        )

    insight(
        """
<strong style="color:{T};">Interpretación estratégica:</strong>
No existe un ROI óptimo único; cada nivel de eficiencia implica un nivel distinto de ventas y un posicionamiento estratégico diferente.
Un ROI más alto exige menor presupuesto. Crecimiento y eficiencia son objetivos en tensión.
<strong style="color:{T};">No existe un punto óptimo universal: depende del objetivo de negocio.</strong>
""",
        ROSE,
    )

# 06 Recomendación de mix óptimo
with section_container(
    6,
    "Recomendación de inversión 2025",
    "Con el mismo presupuesto total, el mix óptimo estima 3,0M€ adicionales en ventas.",
    GREEN,
):
    st.markdown(
        f"""
<div class="ui-card ui-card-lg metric-card" style="border-color:{BD};margin-bottom:1rem;padding:2.2rem 2.35rem;">
  <h3 style="margin:0 0 1rem;color:{T};font-size:1.15rem;font-weight:800;letter-spacing:-0.02em;">
    La redistribución del mix permite capturar +3,0M€ sin aumentar inversión
  </h3>
  <div class="ui-mono glow-green" style="color:{GREEN};font-size:4.15rem;font-weight:600;letter-spacing:-0.065em;line-height:0.95;">
    +<span data-countup data-target="3.0" data-decimals="1" data-suffix="M€" data-duration="1000">3,0M€</span>
  </div>
  <div style="margin-top:0.55rem;color:{TS};font-size:1rem;font-weight:650;line-height:1.45;">
    El crecimiento no viene de invertir más, sino de invertir mejor.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0.75rem;margin-bottom:0.25rem;">
  <div style="background:{CARD};border:1px solid {BD};border-radius:10px;padding:0.8rem 0.95rem;">
    <div style="color:{TS};font-size:0.76rem;font-weight:750;margin-bottom:0.25rem;">Digital Perf.</div>
    <div class="ui-mono" style="color:{T};font-size:1rem;font-weight:600;">↓ 1.6M</div>
  </div>
  <div style="background:{CARD};border:1px solid {BD};border-radius:10px;padding:0.8rem 0.95rem;">
    <div style="color:{TS};font-size:0.76rem;font-weight:750;margin-bottom:0.25rem;">Awareness</div>
    <div class="ui-mono" style="color:{T};font-size:1rem;font-weight:600;">↑ 1.0M</div>
  </div>
  <div style="background:{CARD};border:1px solid {BD};border-radius:10px;padding:0.8rem 0.95rem;">
    <div style="color:{TS};font-size:0.76rem;font-weight:750;margin-bottom:0.25rem;">Offline</div>
    <div class="ui-mono" style="color:{T};font-size:1rem;font-weight:600;">↑ 0.5M</div>
  </div>
  <div style="background:{CARD};border:1px solid {BD};border-radius:10px;padding:0.8rem 0.95rem;">
    <div style="color:{TS};font-size:0.76rem;font-weight:750;margin-bottom:0.25rem;">CRM</div>
    <div class="ui-mono" style="color:{T};font-size:1rem;font-weight:600;">↑ 0.1M</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

# 07 Decisión estratégica
with section_container(
    7,
    "Decisión estratégica: crecimiento o eficiencia",
    "El modelo cuantifica la oportunidad, pero la decisión depende del equilibrio entre volumen, ROI y presupuesto.",
    BLUE,
):
    model_name = table_value(MD["base_kpis"], "KPI", "R² in-sample", "Valor")
    total_sales = table_value(MD["base_kpis"], "KPI", "Ventas reales", "Valor")
    predicted_sales = table_value(MD["base_kpis"], "KPI", "Ventas predichas", "Valor")
    mape = table_value(MD["base_kpis"], "KPI", "MAPE in-sample", "Valor")
    top_roi = table_value(MD["channel_roi"], "Canal / grupo", "CRM / Email", "ROI")

    decision_kpi_size = "1.45rem"
    k1, k2, k3, k4 = st.columns(4, gap="large")
    with k1:
        kpi("Ventas totales", "766,0M€", total_sales, BLUE, value_font_size=decision_kpi_size)
    with k2:
        kpi("ROI canal top", f"{top_roi}x", "CRM / Email", GREEN, value_font_size=decision_kpi_size)
    with k3:
        kpi("Uplift mix óptimo", "+3,00 M€/año", "predict directo ElasticNet", VIOLET, value_font_size=decision_kpi_size)
    with k4:
        kpi("Precisión modelo", mape, f"R² {model_name}", AMBER, value_font_size=decision_kpi_size)

    card_html(
        "Modelo de decisión",
        f"""
<div class="ui-copy">
  ElasticNetCV con coeficientes positivos, canales agrupados para reducir multicolinealidad,
  controles de demanda base y curvas de respuesta para interpretar saturación.
</div>
<div style="margin-top:1rem;color:{TS};font-size:0.9rem;line-height:1.65;">
  El modelo identifica una oportunidad cuantificada, pero la decisión depende de los equilibrios estratégicos.
</div>
""",
        label="Resumen ejecutivo",
        accent=BLUE,
        extra_style=f"margin-top:1rem;border-left:3px solid {BLUE};",
    )

    spacer("0.35rem")

    objective = st.selectbox(
        "Objetivo estratégico",
        ["Crecimiento", "Equilibrio", "Eficiencia"],
        index=1,
    )

    strategy_lookup = {
        "Crecimiento": ("Crecimiento", "presupuesto alto, ROI menor"),
        "Equilibrio": ("Equilibrio", "punto medio"),
        "Eficiencia": ("Eficiencia", "presupuesto bajo, ROI alto"),
    }
    needle, logic = strategy_lookup[objective]
    strategic_df = MD["roi_strategy"]
    row = pd.DataFrame()
    if not strategic_df.empty:
        row = strategic_df[
            strategic_df["Estrategia"].astype(str).str.contains(needle, case=False, regex=False)
        ]

    if not row.empty:
        selected_row = row.iloc[0]
        strategic_kpi_size = "1.5rem"
        p1, p2, p3, p4 = st.columns(4, gap="large")
        with p1:
            kpi("ROI esperado", selected_row["ROI"], logic, GREEN if objective == "Eficiencia" else BLUE, value_font_size=strategic_kpi_size)
        with p2:
            kpi("Ventas esperadas", selected_row["Ventas"], selected_row["Enfoque"], VIOLET, value_font_size=strategic_kpi_size)
        with p3:
            budget_value = str(selected_row["Presupuesto"]).replace(" (", "<br>(")
            kpi("Nivel de presupuesto", budget_value, objective, AMBER, value_font_size="1.3rem", value_white_space="normal")
        with p4:
            kpi("Objetivo estratégico", objective, "Elección estratégica", BLUE, value_font_size=strategic_kpi_size)
    else:
        st.info("Placeholder: falta la tabla de estrategias en ROI_VS_VENTAS.md.")

    card_html(
        "La pregunta central",
        f"""
<div class="ui-copy" style="font-size:1rem;">
  ¿Debe K-Moda priorizar crecimiento o eficiencia?
</div>
<div style="margin-top:0.9rem;color:{TS};font-size:0.9rem;line-height:1.65;">
  <strong style="color:{T};">La decisión no es técnica, es estratégica.</strong>
  Maximizar ventas exige más inversión y menor ROI;
  maximizar eficiencia exige reducir inversión y aceptar menos volumen.
</div>
""",
        label="Decisión estratégica",
        accent=GREEN,
        extra_style=f"margin-top:1rem;border-left:3px solid {GREEN};",
    )

# 08 Simulador
with section_container(
    8,
    "Simulador de frontera estratégica",
    "Selecciona un ROI objetivo y observa sus implicaciones reales en presupuesto, ventas y posicionamiento.",
    BLUE,
):
    frontier_df = MD["frontier"].copy()
    if frontier_df.empty:
        st.info("Placeholder: falta la tabla de frontera en DECISIONES.md.")
    else:
        frontier_df["_roi"] = frontier_df["ROI"].apply(parse_markdown_number)
        frontier_df["_sales"] = frontier_df["Ventas (M€)"].apply(parse_markdown_number)
        frontier_df = frontier_df.dropna(subset=["_roi", "_sales"]).sort_values("_roi")

        default_roi = 13.3
        if not frontier_df[frontier_df["Fracción actual"].astype(str).str.strip() == "100%"].empty:
            default_roi = frontier_df[frontier_df["Fracción actual"].astype(str).str.strip() == "100%"].iloc[0]["_roi"]

        target_roi = st.slider(
            "ROI objetivo",
            float(frontier_df["_roi"].min()),
            25.0,
            float(min(default_roi, 25.0)),
            0.1,
            format="%.1fx",
        )

        selected_idx = (frontier_df["_roi"] - target_roi).abs().idxmin()
        selected_row = frontier_df.loc[selected_idx]
        selected_roi = selected_row["_roi"]
        position, budget_level, sales_level, focus, position_color = frontier_position(selected_roi)
        delta_value = str(selected_row["Δ vs actual"]).strip()
        delta_color = GREEN if delta_value.startswith("+") else AMBER

        st.markdown(
            f"""
<div class="ui-card ui-card-lg metric-card" style="min-height:auto;margin:1rem 0;background:{CARD} !important;border-color:{BD} !important;box-shadow:0 4px 12px rgba(0,0,0,0.04);">
  <div style="display:flex;justify-content:space-between;gap:1.5rem;align-items:flex-start;">
    <div>
      <div class="ui-label" style="color:{position_color};margin-bottom:0.35rem;">Punto más cercano en la frontera documentada</div>
      <div style="color:{T};font-size:1.1rem;font-weight:600;letter-spacing:-0.025em;margin-bottom:0.75rem;">{position}</div>
      <div class="ui-mono" style="color:{T};font-size:3.25rem;font-weight:600;letter-spacing:-0.06em;line-height:0.95;">{selected_row['ROI']} ROI</div>
      <div style="color:{delta_color};font-size:0.9rem;font-weight:600;margin-top:0.55rem;">{delta_value} vs actual</div>
    </div>
    <div style="max-width:430px;color:{TS};font-size:0.9rem;line-height:1.65;text-align:right;">
      Subir el ROI no es optimizar mejor el mix: es elegir un nivel de inversión más bajo en la frontera.
      Este simulador no interpola datos; selecciona el punto real más cercano del README.
    </div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0.75rem;margin-top:1.35rem;padding-top:1rem;border-top:1px solid {BD};">
    <div>
      <div class="ui-label" style="margin-bottom:0.25rem;">Presupuesto</div>
      <div class="ui-mono" style="color:{T};font-size:1rem;font-weight:600;">{selected_row['Presupuesto']}</div>
    </div>
    <div>
      <div class="ui-label" style="margin-bottom:0.25rem;">Ventas</div>
      <div class="ui-mono" style="color:{T};font-size:1rem;font-weight:600;">{selected_row['Ventas (M€)']} M€</div>
    </div>
    <div>
      <div class="ui-label" style="margin-bottom:0.25rem;">Nivel de presupuesto</div>
      <div class="ui-mono" style="color:{T};font-size:1rem;font-weight:600;">{budget_level}</div>
    </div>
    <div>
      <div class="ui-label" style="margin-bottom:0.25rem;">Enfoque</div>
      <div class="ui-mono" style="color:{T};font-size:1rem;font-weight:600;">{focus}</div>
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        col_left, col_right = st.columns([3, 2], gap="large")
        with col_left:
            fig, ax = sfig((7.4, 4.4))
            ax.plot(frontier_df["_roi"], frontier_df["_sales"], color=MPL_LILAC, linewidth=1.8, alpha=0.95)
            ax.scatter(frontier_df["_roi"], frontier_df["_sales"], color=MPL_SAND, s=34, edgecolors="none")
            ax.scatter([selected_roi], [selected_row["_sales"]], color=MPL_SAGE, s=120, zorder=4, edgecolors=(1, 1, 1, 0.95), linewidths=1.4)
            ax.annotate(
                "Punto seleccionado",
                (selected_roi, selected_row["_sales"]),
                xytext=(10, 12),
                textcoords="offset points",
                color=MPL_T,
                fontsize=8,
                fontweight="bold",
            )
            ax.set_xlabel("ROI", color=MPL_TS, fontsize=8)
            ax.set_ylabel("Ventas (M€)", color=MPL_TS, fontsize=8)
            ax.set_title("Frontera documentada ROI vs ventas", color=MPL_T, fontsize=10, fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with col_right:
            frontier_note = f"""
<div style="display:grid;gap:0.75rem;">
  <div class="ui-card" style="min-height:auto;padding:1rem;">
    <div class="ui-label" style="color:{position_color};margin-bottom:0.35rem;">Posicionamiento</div>
      <div style="color:{T};font-size:1rem;font-weight:600;">{position}</div>
    <div style="color:{TS};font-size:0.82rem;line-height:1.55;margin-top:0.45rem;">
      Ventas {sales_level}; presupuesto {budget_level}; foco en {focus.lower()}.
    </div>
  </div>
  <div class="ui-card" style="min-height:auto;padding:1rem;border-left:2px solid {BLUE};">
    <div class="ui-label" style="color:{ROSE};margin-bottom:0.35rem;">Lectura estratégica</div>
    <div style="color:{TS};font-size:0.84rem;line-height:1.6;">
      Mayor ROI = menor presupuesto = menores ventas. La pregunta no es qué canal tocar, sino dónde quiere situarse K-Moda en la curva.
    </div>
  </div>
</div>
"""
            st.markdown(frontier_note, unsafe_allow_html=True)

        st.dataframe(
            frontier_df[["Fracción actual", "Presupuesto", "ROI", "Ventas (M€)", "Δ vs actual"]],
            use_container_width=True,
            hide_index=True,
        )

# 09 Escenarios desde DECISIONES.md
with section_container(
    9,
    "Escenarios estratégicos",
    "Comparativa de ventas, ROI, delta y riesgo extraída del cuaderno de decisión.",
    VIOLET,
):
    insight(
        f"""
<strong style="color:{T};">Validación:</strong> los escenarios confirman la frontera:
mayor inversión aumenta ventas, pero reduce eficiencia.
""",
        VIOLET,
    )
    scenario_df = MD["decision_scenarios"].copy()
    if not scenario_df.empty:
        scenario_df["Posicionamiento estratégico"] = scenario_df["Escenario"].apply(scenario_position)
        st.dataframe(
            scenario_df[
                [
                    "Escenario",
                    "Ventas (M€)",
                    "ROI",
                    "Δ vs actual",
                    "Riesgo",
                    "Posicionamiento estratégico",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Tabla de escenarios pendiente en DECISIONES.md.")

    st.subheader("Análisis de escenarios")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        image_with_caption(
            img("decision_02_scenario_comparison.png"),
            "Investment scenarios comparison: ventas, ROI, delta y mix por escenario.",
        )
    with c2:
        image_with_caption(
            img("economic_scenario_comparison_sales_roi.png"),
            "Sales vs ROI by scenario: más ventas suele exigir aceptar menor eficiencia marginal.",
        )

# 10 Descomposición
with section_container(
    10,
    "Descomposición de ventas",
    "El modelo separa la base estructural de las ventas atribuibles a cada bloque de marketing.",
    VIOLET,
):
    col_w, col_dc = st.columns([4, 2], gap="large")
    with col_w:
        p = img("economic_waterfall_sales_decomposition.png")
        if p:
            image_card(
                "Descomposición de ventas",
                "Base vs contribución incremental por bloque de marketing, periodo 2020-2024.",
                p,
            )
        else:
            fig, ax = sfig((8.2, 4.9))
            cats = ["Base", "Dig. Perf.", "Dig. Aware.", "Offline", "CRM", "Total"]
            vals = [391.4, 102.9, 114.9, 85.7, 71.2, 766.0]
            bots = [0, 391.4, 494.3, 609.2, 694.9, 0]
            clrs_w = [MPL_TS, MPL_SAND, MPL_SAGE, MPL_DUSTY, MPL_LILAC, MPL_TS]
            for i, (cat, val, bottom, color) in enumerate(zip(cats, vals, bots, clrs_w)):
                ax.bar(i, val, bottom=bottom, color=color, width=0.54)
                ax.text(i, bottom + val / 2, f"{val:.0f}M", ha="center", va="center", fontsize=8, color=MPL_T, fontweight="bold")
            ax.set_xticks(range(len(cats)))
            ax.set_xticklabels(cats, color=MPL_TS, fontsize=8)
            ax.set_title("Descomposición ventas (M€)", color=MPL_T, fontsize=10, fontweight="bold")
            ax.grid(False)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    with col_dc:
        bars_html = ""
        for name, val, pct, color, width in [
            ("Base estructural", 391.4, 51.1, TS, 100),
            ("Digital Awareness", 114.9, 15.0, VIOLET, 29),
            ("Digital Perf.", 102.9, 13.4, BLUE, 26),
            ("Offline", 85.7, 11.2, INDIGO, 22),
            ("CRM / Email", 71.2, 9.3, GREEN, 18),
        ]:
            bars_html += f"""
  <div style="margin-bottom:1.05rem;">
    <div style="display:flex;justify-content:space-between;gap:1rem;align-items:baseline;margin-bottom:0.35rem;">
      <span style="color:{T};font-size:0.86rem;font-weight:650;">{name}</span>
      <span class="ui-mono" style="color:{color};font-size:0.8rem;font-weight:750;white-space:nowrap;">{val:.0f}M · {pct}%</span>
    </div>
    <div style="height:6px;background:{BD};border-radius:999px;overflow:hidden;">
      <div style="height:100%;width:{width}%;background:{color};border-radius:999px;"></div>
    </div>
  </div>
"""
        card_html(
            "La base explica algo más de la mitad",
            bars_html
            + f"""
<div style="margin-top:1.1rem;padding:1rem;background:{CARD2};border:1px solid {BD};
            border-radius:16px;color:{TS};font-size:0.86rem;line-height:1.7;">
  <strong style="color:{T};">Implicación:</strong> la inversión no debe evaluarse solo por volumen.
  La clave está en redistribuir hacia los bloques con mejor retorno marginal.
</div>
""",
            label="Mix de contribución",
            accent=VIOLET,
        )

# 11 Biblioteca visual del modelo
with section_container(
    11,
    "Biblioteca visual del modelo",
    "Gráficas generadas por el proyecto, organizadas para lectura ejecutiva.",
    INDIGO,
):
    st.subheader("Visión general del modelo")
    image_with_caption(
        img("economic_marketing_vs_base_share_over_time.png"),
        "Base vs marketing a lo largo del tiempo. La contribución de marketing varía por periodo y debe leerse junto a la demanda estructural.",
    )

    st.subheader("Confianza del modelo")
    image_with_caption(
        img("decision_03_mape.png"),
        "MAPE por escenario. Las desviaciones grandes del mix histórico elevan la incertidumbre esperada.",
    )

    st.subheader("Análisis por canal")
    ca1, ca2 = st.columns(2, gap="large")
    with ca1:
        image_with_caption(
            img("decision_01_roi_curves.png"),
            "Curvas de ROI por canal. Un ROI histórico alto no siempre implica mayor retorno marginal escalable.",
        )
    with ca2:
        image_with_caption(
            img("fase6_curvas_respuesta.png"),
            "Curvas de respuesta. La inversión adicional genera rendimientos decrecientes.",
        )
    ca3, ca4 = st.columns(2, gap="large")
    with ca3:
        image_with_caption(
            img("economic_roi_vs_investment_scatter.png"),
            "ROI vs inversión por canal. La eficiencia debe leerse junto al tamaño de inversión.",
        )
    with ca4:
        image_with_caption(
            img("economic_marginal_roi_curves.png"),
            "Curvas de ROI marginal. La decisión óptima depende del siguiente euro invertido.",
        )

    st.subheader("Análisis riesgo-retorno")
    risk_col, risk_note = st.columns([2, 1], gap="large")
    with risk_col:
        image_with_caption(
            img("decision_04_risk_return.png"),
            "Mapa riesgo-retorno. Cada estrategia combina ventas, ROI e incertidumbre de forma distinta.",
        )
    with risk_note:
        card_html(
            "Lectura riesgo-retorno",
            f"""
<div class="ui-copy">
  El mapa funciona como control ejecutivo: no basta con mirar ventas o ROI.
  Cada escenario debe evaluarse junto a su incertidumbre y distancia al mix histórico.
</div>
""",
            label="Riesgo-retorno",
            accent=ROSE,
        )

    st.subheader("Diagnóstico del modelo")
    md1, md2 = st.columns([2, 1], gap="large")
    with md1:
        image_with_caption(
            img("05_heatmap_correlaciones.png"),
            "Matriz de correlaciones. La multicolinealidad justifica agrupar canales y evitar lecturas causales canal a canal demasiado finas.",
        )
    with md2:
        card_html(
            "Diagnóstico de multicolinealidad",
            f"""
<div class="ui-copy">
  La matriz se mantiene como evidencia metodológica, no como pieza central de decisión.
  Su lectura principal es que los canales se activan de forma sincronizada y por eso el modelo agrupa inversión.
</div>
""",
            label="Diagnóstico del modelo",
            accent=INDIGO,
        )

st.markdown(
    f"""
<section class="section-card" style="border-left:3px solid {GREEN};">
  <div class="section-header">
    <span class="section-number" style="color:{GREEN};background:{GREEN}14;border-color:{GREEN}30;">12</span>
    <div>
      <h2 class="section-title" style="font-size:0.9rem !important;">Veredicto final</h2>
      <p class="section-subtitle">El modelo no sustituye la decisión: la estructura y cuantifica.</p>
    </div>
  </div>
  <div class="section-content">
    <div style="display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:0.85rem;align-items:stretch;">
      <div class="ui-card ui-card-lg" style="background:{CARD};">
        <div class="ui-label" style="color:{GREEN};">Recomendación ejecutiva</div>
        <h3 class="ui-title" style="font-size:1.18rem;">La mejor decisión base es equilibrio con redistribución del mix</h3>
        <div class="ui-copy">
          Con la evidencia actual, K-Moda no necesita invertir más para crecer. La recomendación es mantener una posición de equilibrio
          y capturar <strong style="color:{T};">+3,0M€</strong> moviendo inversión desde Digital Performance hacia Awareness, Offline y CRM.
        </div>
      </div>
      <div class="ui-card">
        <div class="ui-label" style="color:{BLUE};">Si prioriza crecimiento</div>
        <div style="color:{T};font-size:0.94rem;font-weight:600;line-height:1.45;">Acepta menor ROI para ganar ventas y cuota.</div>
        <div style="color:{TS};font-size:0.8rem;line-height:1.55;margin-top:0.5rem;">Más presupuesto, más volumen, menor eficiencia.</div>
      </div>
      <div class="ui-card">
        <div class="ui-label" style="color:{VIOLET};">Si prioriza eficiencia</div>
        <div style="color:{T};font-size:0.94rem;font-weight:600;line-height:1.45;">Acepta menor volumen para elevar el retorno.</div>
        <div style="color:{TS};font-size:0.8rem;line-height:1.55;margin-top:0.5rem;">Menor presupuesto, mayor ROI, menos ventas.</div>
      </div>
    </div>
  </div>
</section>
""",
    unsafe_allow_html=True,
)

# Footer
st.markdown(
    f"""
<footer style="margin-top:5rem;padding:1.4rem 0;border-top:1px solid {BD};
               display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;">
  <div style="color:{TS};font-size:0.78rem;line-height:1.45;">
    <strong style="color:{T};">K-Moda · Marketing Mix Modeling</strong>
    · ElasticNetCV · R² 0,885 · MAPE 7,53% · Periodo 2020-2024
  </div>
  <div style="color:{TD};font-size:0.72rem;line-height:1.45;">
    Las métricas son del ajuste histórico y no constituyen garantía de rendimiento futuro.
  </div>
</footer>
""",
    unsafe_allow_html=True,
)
