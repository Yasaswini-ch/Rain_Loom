"""
Monsoon-Textile Volatility Risk Monitor -- Overview / About Page
================================================================

Comprehensive landing page explaining the project, methodology,
dashboard pages, data sources, and technical architecture.

Launch:
    streamlit run monsoon_textile_app/app.py --server.port 8501
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
from monsoon_textile_app.components.navbar import render_navbar
from monsoon_textile_app.components.chat_bubble import render_chat_bubble

# -- Page Configuration --------------------------------------------------------
st.set_page_config(
    page_title="RainLoom -- Monsoon & Textile Volatility",
    page_icon="\u26a1",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -- Navbar (MUST come before any other content) --------------------------------
render_navbar(active_page="Overview")
render_chat_bubble()

# -- Master CSS ----------------------------------------------------------------
st.markdown("""
<style>
    /* ---- Import font ---- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ---- Root variables ---- */
    :root {
        --bg-primary: #0a0f1e;
        --bg-card: rgba(15, 23, 42, 0.60);
        --bg-card-hover: rgba(20, 30, 55, 0.75);
        --border-subtle: rgba(255, 255, 255, 0.06);
        --border-accent: rgba(59, 130, 246, 0.25);
        --text-primary: #e2e8f0;
        --text-secondary: #8892b0;
        --text-muted: #64748b;
        --accent-blue: #3b82f6;
        --accent-red: #ef4444;
        --accent-green: #10b981;
        --accent-gold: #f59e0b;
        --accent-cyan: #06b6d4;
        --accent-purple: #8b5cf6;
        --radius-lg: 16px;
        --radius-md: 12px;
        --radius-sm: 8px;
    }

    /* ---- Hide all Streamlit chrome ---- */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    [data-testid="stDeployButton"] { display: none; }
    [data-testid="stToolbar"] { display: none; }
    .stDeployButton { display: none !important; }

    /* ---- Global resets ---- */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: var(--text-primary);
    }

    [data-testid="stAppViewContainer"] {
        background: var(--bg-primary);
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(59,130,246,0.08) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(16,185,129,0.04) 0%, transparent 50%);
    }

    .main .block-container {
        padding-bottom: 2rem;
        max-width: 1440px;
    }

    /* ---- Glass card base ---- */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 1.4rem 1.5rem;
        margin-bottom: 0.75rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        border-color: var(--border-accent);
        box-shadow: 0 4px 30px rgba(59, 130, 246, 0.06);
    }

    /* ---- Hero header ---- */
    .hero-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .hero-title {
        font-size: 2.46rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.15;
        background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 40%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .hero-tagline {
        font-size: 1.03rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin-top: 0.6rem;
        letter-spacing: 0.01em;
    }

    /* ---- Section headers ---- */
    .section-header {
        font-size: 1.11rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-top: 1.8rem;
        margin-bottom: 1rem;
        position: relative;
        display: inline-block;
    }
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-blue) 0%, transparent 100%);
        border-radius: 1px;
    }

    /* ---- Gradient divider ---- */
    .gradient-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(59,130,246,0.3) 30%, rgba(59,130,246,0.3) 70%, transparent 100%);
        border: none;
        margin: 1.5rem 0;
    }

    /* ---- Content labels & text ---- */
    .content-label {
        font-size: 0.80rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.5rem;
    }
    .content-text {
        font-size: 0.94rem;
        color: var(--text-secondary);
        line-height: 1.65;
        margin: 0 0 0.2rem 0;
    }

    /* ---- Solution steps ---- */
    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.4rem 0;
    }
    .step-num {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.82rem;
        font-weight: 700;
        flex-shrink: 0;
        margin-top: 1px;
    }
    .step-text {
        font-size: 0.94rem;
        color: var(--text-secondary);
        line-height: 1.55;
    }

    /* ---- Causal chain stepper ---- */
    .chain-container {
        display: flex;
        align-items: flex-start;
        gap: 0;
        margin: 0.5rem 0;
        position: relative;
    }
    .chain-step {
        flex: 1;
        text-align: center;
        position: relative;
        padding: 0 0.4rem;
    }
    .chain-node {
        background: var(--bg-card);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 1.1rem 0.8rem;
        position: relative;
        z-index: 2;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .chain-node:hover {
        border-color: var(--border-accent);
        box-shadow: 0 4px 24px rgba(0,0,0,0.25);
    }
    .chain-number {
        font-size: 0.77rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    .chain-title {
        font-size: 0.92rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.4rem;
    }
    .chain-desc {
        font-size: 0.84rem;
        color: var(--text-secondary);
        line-height: 1.45;
        margin-bottom: 0.4rem;
    }
    .chain-lag {
        font-size: 0.80rem;
        color: var(--text-muted);
        font-weight: 500;
    }
    .chain-connector {
        position: absolute;
        top: 50%;
        right: -0.5rem;
        transform: translateY(-50%);
        z-index: 3;
        color: var(--text-muted);
        font-size: 1rem;
        font-weight: 300;
    }

    /* ---- Dashboard guide cards ---- */
    .guide-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 0.85rem;
    }
    .guide-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 1.3rem 1.4rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .guide-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
    }
    .guide-card:hover {
        border-color: var(--border-accent);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .guide-card-icon {
        width: 36px;
        height: 36px;
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.03rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }
    .guide-card-page {
        font-size: 0.77rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.3rem;
    }
    .guide-card-title {
        font-size: 1.02rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 0.55rem 0;
    }
    .guide-card-desc {
        font-size: 0.88rem;
        color: var(--text-secondary);
        line-height: 1.55;
        margin: 0 0 0.65rem 0;
    }
    .guide-card-usage {
        font-size: 0.86rem;
        color: var(--accent-cyan);
        font-weight: 500;
        font-style: italic;
    }

    /* ---- Data table ---- */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.90rem;
    }
    .data-table-header {
        display: grid;
        grid-template-columns: 1.2fr 1fr 1.5fr 1fr;
        gap: 0.5rem;
        padding: 0.65rem 1rem;
        background: rgba(59, 130, 246, 0.08);
        border-radius: var(--radius-sm);
        margin-bottom: 0.3rem;
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .data-table-row {
        display: grid;
        grid-template-columns: 1.2fr 1fr 1.5fr 1fr;
        gap: 0.5rem;
        padding: 0.6rem 1rem;
        border-bottom: 1px solid var(--border-subtle);
        font-size: 0.90rem;
        color: var(--text-secondary);
        transition: background 0.2s ease;
    }
    .data-table-row:hover {
        background: rgba(59, 130, 246, 0.04);
    }
    .data-table-row:last-child {
        border-bottom: none;
    }
    .dt-source {
        color: var(--text-primary);
        font-weight: 600;
    }
    .dt-api {
        font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
        font-size: 0.87rem;
        color: var(--accent-cyan);
    }

    /* ---- Securities grid ---- */
    .sec-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.6rem;
    }
    .sec-card {
        background: rgba(15, 23, 42, 0.45);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .sec-card:hover {
        border-color: var(--border-accent);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .sec-ticker {
        font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
        font-size: 0.88rem;
        color: var(--accent-blue);
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .sec-name {
        font-size: 0.92rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.3rem;
    }
    .sec-role {
        font-size: 0.84rem;
        color: var(--text-secondary);
        line-height: 1.45;
    }

    /* ---- Tech stack pills ---- */
    .tech-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.6rem;
    }
    .tech-pill {
        display: inline-block;
        background: rgba(59, 130, 246, 0.1);
        color: var(--accent-blue);
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: 20px;
        padding: 0.3rem 0.75rem;
        font-size: 0.86rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .tech-pill:hover {
        background: rgba(59, 130, 246, 0.18);
        border-color: rgba(59, 130, 246, 0.3);
    }
    .tech-pill-green {
        background: rgba(16, 185, 129, 0.1);
        color: var(--accent-green);
        border-color: rgba(16, 185, 129, 0.15);
    }
    .tech-pill-green:hover {
        background: rgba(16, 185, 129, 0.18);
        border-color: rgba(16, 185, 129, 0.3);
    }
    .tech-pill-gold {
        background: rgba(245, 158, 11, 0.1);
        color: var(--accent-gold);
        border-color: rgba(245, 158, 11, 0.15);
    }
    .tech-pill-gold:hover {
        background: rgba(245, 158, 11, 0.18);
        border-color: rgba(245, 158, 11, 0.3);
    }
    .tech-pill-purple {
        background: rgba(139, 92, 246, 0.1);
        color: var(--accent-purple);
        border-color: rgba(139, 92, 246, 0.15);
    }
    .tech-pill-purple:hover {
        background: rgba(139, 92, 246, 0.18);
        border-color: rgba(139, 92, 246, 0.3);
    }

    /* ---- Footer ---- */
    .app-footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        color: var(--text-muted);
        font-size: 0.84rem;
    }
    .footer-version {
        display: inline-block;
        background: rgba(59, 130, 246, 0.12);
        color: var(--accent-blue);
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.80rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        margin-bottom: 0.4rem;
    }
    .footer-tagline {
        color: var(--text-muted);
        font-size: 0.86rem;
        margin-top: 0.3rem;
        letter-spacing: 0.02em;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 1. Hero Header
# ==============================================================================
st.markdown("""
<div class="hero-header">
    <div class="hero-title">RainLoom &mdash; Monsoon Failures &amp; Textile Stock Volatility</div>
    <div class="hero-tagline">
        Predicting NSE textile-sector volatility regimes from IMD rainfall deficits,
        satellite NDVI, and cotton futures using causal machine learning
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ==============================================================================
# 2. The Problem
# ==============================================================================
st.markdown('<div class="section-header">The Problem</div>', unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <div class="content-text">
        India's &#8377;12 lakh crore textile industry is structurally exposed to monsoon
        failures. When June&#8211;September (JJAS) rainfall falls 20% or more below the
        Long Period Average, cotton yields drop 15&#8211;25%, triggering a predictable
        cascade: cotton prices spike, manufacturer margins compress, and stock volatility
        surges. Despite this well-documented chain, no existing system provides early
        warning of the full transmission from rainfall deficit to equity risk. This
        dashboard fills that gap.
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. Our Solution
# ==============================================================================
st.markdown('<div class="section-header">Our Solution</div>', unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <div class="content-text" style="margin-bottom: 0.8rem;">
        A 4-layer causal ML pipeline that transforms raw climate data into actionable
        risk scores with 8+ weeks of lead time:
    </div>
</div>
""", unsafe_allow_html=True)

_steps = [
    ("#60a5fa", "1", "Proves causation",
     "(not just correlation) using stationarity-corrected Granger causality tests on cotton log-returns and rainfall deficit, with Vector Autoregression (VAR) models validating each link in the chain."),
    ("#34d399", "2", "Detects regime shifts",
     "using GJR-GARCH(1,1) with AIC-based model selection to identify when markets transition between calm and turbulent volatility states."),
    ("#fbbf24", "3", "Classifies risk states",
     "using XGBoost with 24 climate-informed features including spatial rainfall deficit breadth, lag-transformed cotton returns, NDVI satellite anomalies, and seasonal indicators."),
    ("#f97316", "4", "Captures temporal sequences",
     "using MLP neural network with temporal cross-validation to model the multi-week propagation dynamics from rainfall shock to market response."),
    ("#a78bfa", "5", "Combines into ensemble",
     "risk score (XGBoost 40% + GARCH 30% + MLP 30%) that fuses all layer outputs with calibrated weights, delivering actionable alerts with 8+ weeks of lead time."),
]
for color, num, title, desc in _steps:
    st.markdown(
        f'<div class="step-item">'
        f'<div class="step-num" style="background: {color}22; color: {color};">{num}</div>'
        f'<div class="step-text"><span style="color:{color}; font-weight:600;">{title}</span> {desc}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ==============================================================================
# 4. Causal Transmission Mechanism
# ==============================================================================
st.markdown('<div class="section-header">Causal Transmission Mechanism</div>', unsafe_allow_html=True)

_stages = [
    ("Stage 01", "Climate Signal",   "IMD rainfall anomaly &lt; &#8211;20% LPA", "T + 0 weeks",  "#60a5fa"),
    ("Stage 02", "Crop Stress",      "NDVI drops below threshold",               "T + 2&#8211;4 wks", "#34d399"),
    ("Stage 03", "Price Spike",      "MCX cotton futures surge",                 "T + 4&#8211;6 wks", "#fbbf24"),
    ("Stage 04", "Margin Squeeze",   "EBITDA margin compression",                "T + 6&#8211;10 wks", "#f97316"),
    ("Stage 05", "Volatility Shift", "Stock realized vol &gt; 2&#963;",          "T + 4&#8211;8 wks", "#ef4444"),
]

_chain_cols = st.columns(len(_stages))
for i, (num, title, desc, lag, color) in enumerate(_stages):
    with _chain_cols[i]:
        connector = '&rsaquo;' if i < len(_stages) - 1 else ''
        st.markdown(
            f'<div class="chain-node" style="border-top: 2px solid {color};">'
            f'<div class="chain-number" style="color: {color};">{num}</div>'
            f'<div class="chain-title">{title}</div>'
            f'<div class="chain-desc">{desc}</div>'
            f'<div class="chain-lag">{lag}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ==============================================================================
# 5. Dashboard Guide
# ==============================================================================
st.markdown('<div class="section-header">How to Use This System</div>', unsafe_allow_html=True)

_guide_pages = [
    {
        "num": "01",
        "icon": "\u26a0",
        "icon_bg": "linear-gradient(135deg, #1e3a5f 0%, #0f2440 100%)",
        "accent": "#3b82f6",
        "title": "Risk Monitor",
        "desc": (
            "Real-time risk scores for 5 NSE textile stocks. Gauge indicators display "
            "the ensemble risk level for each security. A rainfall deficit map highlights "
            "stressed cotton-belt states across India. Position alerts flag when risk "
            "crosses actionable thresholds."
        ),
        "usage": "Use this to monitor current conditions and identify emerging risk.",
    },
    {
        "num": "02",
        "icon": "\u21c4",
        "icon_bg": "linear-gradient(135deg, #1a3a2a 0%, #0f2a1a 100%)",
        "accent": "#10b981",
        "title": "Causal Analysis",
        "desc": (
            "Statistical proof that monsoon rainfall causes textile stock volatility. "
            "Stationarity-corrected Granger causality tests on cotton log-returns and "
            "rainfall deficit validate each link at p &lt; 0.05. Lag heatmaps show "
            "optimal transmission delays across 4 causal pathways."
        ),
        "usage": "Use this to understand WHY the model works and validate causal claims.",
    },
    {
        "num": "03",
        "icon": "\u2713",
        "icon_bg": "linear-gradient(135deg, #3a2a10 0%, #2a1f08 100%)",
        "accent": "#f59e0b",
        "title": "Model Performance",
        "desc": (
            "ROC curves (AUC 0.84&#8211;0.98), SHAP feature importance across 24 features "
            "including NDVI satellite data, and 5-fold temporal cross-validation results. "
            "Per-stock model cards show XGBoost, GARCH, and MLP performance with "
            "ensemble risk scoring."
        ),
        "usage": "Use this to evaluate model reliability and compare against benchmarks.",
    },
    {
        "num": "04",
        "icon": "\u2699",
        "icon_bg": "linear-gradient(135deg, #2a1a3a 0%, #1a0f2a 100%)",
        "accent": "#8b5cf6",
        "title": "Scenario Simulator",
        "desc": (
            "Interactive what-if tool powered by trained XGBoost models. Adjust monsoon "
            "deficit percentage, cotton spot prices, India VIX level, and spatial deficit "
            "breadth using sliders to see ML-predicted risk scores update in real time. "
            "Historical presets recreate conditions from past drought years."
        ),
        "usage": "Use this to stress-test portfolios under hypothetical climate scenarios.",
    },
    {
        "num": "05",
        "icon": "\u2764",
        "icon_bg": "linear-gradient(135deg, #2a1525 0%, #1f0f1a 100%)",
        "accent": "#ef4444",
        "title": "Societal Impact",
        "desc": (
            "Translates model predictions into actionable advisories for three stakeholder "
            "groups: cotton farmers receive crop insurance enrollment alerts, textile MSMEs "
            "get forward-contract hedging recommendations, and state agriculture departments "
            "access weekly risk dashboards for pre-positioned relief planning."
        ),
        "usage": "Use this to see real-world impact beyond financial markets.",
    },
    {
        "num": "06",
        "icon": "\u2696",
        "icon_bg": "linear-gradient(135deg, #1a1a3a 0%, #0f0f2a 100%)",
        "accent": "#8b5cf6",
        "title": "Hedging Backtest",
        "desc": (
            "Simulates risk-signal-driven hedging strategies across historical drought "
            "events (2009, 2014, 2015, 2023). Compares hedged vs unhedged portfolio P&amp;L, "
            "Sharpe ratios, and maximum drawdowns to quantify the economic value of the "
            "ensemble risk forecast."
        ),
        "usage": "Use this to measure if the risk signal has real economic value.",
    },
]

# Render guide cards using st.columns to avoid deep nesting
_row1_pages = _guide_pages[:3]
_row2_pages = _guide_pages[3:]

_g_cols1 = st.columns(len(_row1_pages))
for col, p in zip(_g_cols1, _row1_pages):
    with col:
        st.markdown(
            f'<div class="guide-card" style="border-top: 2px solid {p["accent"]};">'
            f'<div class="guide-card-icon" style="background: {p["icon_bg"]}; color: {p["accent"]};">{p["icon"]}</div>'
            f'<div class="guide-card-page" style="color: {p["accent"]};">Page {p["num"]}</div>'
            f'<div class="guide-card-title">{p["title"]}</div>'
            f'<div class="guide-card-desc">{p["desc"]}</div>'
            f'<div class="guide-card-usage">{p["usage"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

_g_cols2 = st.columns(len(_row2_pages))
for col, p in zip(_g_cols2, _row2_pages):
    with col:
        st.markdown(
            f'<div class="guide-card" style="border-top: 2px solid {p["accent"]};">'
            f'<div class="guide-card-icon" style="background: {p["icon_bg"]}; color: {p["accent"]};">{p["icon"]}</div>'
            f'<div class="guide-card-page" style="color: {p["accent"]};">Page {p["num"]}</div>'
            f'<div class="guide-card-title">{p["title"]}</div>'
            f'<div class="guide-card-desc">{p["desc"]}</div>'
            f'<div class="guide-card-usage">{p["usage"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ==============================================================================
# 6. Data Sources & APIs
# ==============================================================================
st.markdown('<div class="section-header">Data Sources &amp; APIs</div>', unsafe_allow_html=True)

import pandas as pd
_data_sources = pd.DataFrame({
    "Source": [
        "IMD Gridded Rainfall",
        "Live Rainfall (Open-Meteo)",
        "NSE Equity OHLCV",
        "Cotton Futures (MCX / ICE proxy)",
        "NDVI Satellite (NASA MODIS)",
        "Macro Controls",
    ],
    "API": [
        "imdlib",
        "Open-Meteo Archive API",
        "yfinance",
        "yfinance + USD/INR forex",
        "ORNL DAAC REST API",
        "yfinance",
    ],
    "Data": [
        "0.25 deg daily rainfall grid, 2000-2025",
        "900+ daily observations across 10 cotton-belt states",
        "5 textile stocks + Nifty50 + India VIX",
        "MCX Cotton (primary) or ICE CT=F with real forex conversion",
        "MOD13Q1 250m vegetation index for 10 states",
        "USD/INR exchange rate, Brent Crude",
    ],
    "Update Frequency": [
        "Daily during JJAS",
        "Daily (real-time)",
        "Daily",
        "Daily",
        "16-day composites",
        "Daily",
    ],
})
st.dataframe(_data_sources, use_container_width=True, hide_index=True)


# ==============================================================================
# 7. Target Securities
# ==============================================================================
st.markdown('<div class="section-header">Target Securities</div>', unsafe_allow_html=True)

_securities = [
    ("ARVIND.NS", "Arvind Ltd", "Vertically integrated textile manufacturer. Cotton is primary raw material input (~40% of COGS).", "#3b82f6"),
    ("TRIDENT.NS", "Trident Ltd", "Home textiles and yarn producer. High cotton dependency with significant export exposure.", "#3b82f6"),
    ("KPRMILL.NS", "KPR Mill", "Integrated spinning and garment manufacturer. Cotton yarn is core intermediate product.", "#3b82f6"),
    ("WELSPUNLIV.NS", "Welspun Living", "Home textiles (towels, bed linen). Premium cotton dependency with global supply chain.", "#3b82f6"),
    ("RSWM.NS", "RSWM Ltd", "Spinning and weaving division under LNJ Bhilwara Group. Cotton and synthetic yarn producer.", "#3b82f6"),
    ("VTL.NS", "Vardhman Textiles", "Largest yarn manufacturer in India. Direct upstream cotton exposure (82% dependency).", "#10b981"),
    ("PAGEIND.NS", "Page Industries", "Innerwear and athleisure (Jockey licensee). Downstream apparel with moderate cotton input.", "#f59e0b"),
    ("RAYMOND.NS", "Raymond Ltd", "Fabric and apparel conglomerate. Integrated value chain with diversified fibre mix.", "#f59e0b"),
]

# Row 1: Original textile stocks
_sec_cols1 = st.columns(5)
for col, (ticker, name, role, accent) in zip(_sec_cols1, _securities[:5]):
    with col:
        st.markdown(
            f'<div class="sec-card" style="border-top: 2px solid {accent};">'
            f'<div class="sec-ticker">{ticker}</div>'
            f'<div class="sec-name">{name}</div>'
            f'<div class="sec-role">{role}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# Row 2: Adjacent sectors
st.markdown('<div class="content-label" style="margin-top: 0.8rem; color: #10b981;">TEXTILE-ADJACENT SECTORS</div>',
            unsafe_allow_html=True)
_sec_cols2 = st.columns(3)
for col, (ticker, name, role, accent) in zip(_sec_cols2, _securities[5:]):
    with col:
        st.markdown(
            f'<div class="sec-card" style="border-top: 2px solid {accent};">'
            f'<div class="sec-ticker">{ticker}</div>'
            f'<div class="sec-name">{name}</div>'
            f'<div class="sec-role">{role}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ==============================================================================
# 8. Technical Architecture
# ==============================================================================
st.markdown('<div class="section-header">Technical Architecture</div>', unsafe_allow_html=True)

st.markdown("""
<div class="content-text" style="margin-bottom: 0.6rem;">
    Built as a modular Python application with a Streamlit frontend. Each analytical
    layer runs independently and feeds into the ensemble scoring engine. The pipeline
    supports both batch processing of historical data and near-real-time ingestion
    during monsoon season.
</div>
""", unsafe_allow_html=True)

_tech_stacks = [
    ("Core Framework", "",
     ["Python 3.10+", "Streamlit", "Plotly", "pandas", "NumPy"]),
    ("Machine Learning", "tech-pill-green",
     ["XGBoost", "scikit-learn", "SHAP", "MLP Neural Network", "Quantile Regression"]),
    ("Econometrics & Time Series", "tech-pill-gold",
     ["statsmodels", "arch (GJR-GARCH)", "scipy", "Granger Causality"]),
    ("Data Sources & APIs", "tech-pill-purple",
     ["imdlib", "yfinance", "Open-Meteo API", "NASA MODIS ORNL DAAC"]),
    ("Infrastructure", "tech-pill-purple",
     ["loguru", "pickle (model caching)", "TimeSeriesSplit CV"]),
]
for label, pill_cls, pills in _tech_stacks:
    pills_html = " ".join(f'<span class="{pill_cls} tech-pill">{p}</span>' for p in pills)
    st.markdown(
        f'<div class="content-label" style="margin-top: 0.8rem;">{label}</div>'
        f'<div class="tech-pills">{pills_html}</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ==============================================================================
# 9. Footer
# ==============================================================================
st.markdown("""
<div class="app-footer">
    <div class="footer-version">v3.0.0</div>
    <div class="footer-tagline">
        RainLoom &mdash; Monsoon &rarr; Cotton &rarr; Margin &rarr; Volatility
    </div>
</div>
""", unsafe_allow_html=True)
