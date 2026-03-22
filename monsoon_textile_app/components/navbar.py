"""
Reusable top navigation bar for the Monsoon-Textile Streamlit multipage app.

Usage:
    from monsoon_textile_app.components.navbar import render_navbar
    render_navbar(active_page="Overview")
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Page definitions: display name -> URL path
# ---------------------------------------------------------------------------
PAGES = {
    "Overview": "/",
    "Risk Monitor": "/Live_Risk_Monitor",
    "Causal Analysis": "/Causal_Analysis",
    "Model Performance": "/Model_Performance",
    "Simulator": "/Scenario_Simulator",
    "Hedging": "/Hedging_Backtest",
    "Impact": "/Societal_Impact",
    "Geospatial": "/Geospatial_Nowcast",
}


def render_navbar(active_page: str = "Overview") -> None:
    """Render a fixed top navbar and hide default Streamlit chrome.

    Parameters
    ----------
    active_page:
        Display name of the currently active page (must match a key in PAGES).
    """

    # -- Build navigation link HTML ----------------------------------------
    nav_links = ""
    for label, href in PAGES.items():
        is_active = label == active_page
        active_cls = "mt-nav-active" if is_active else ""
        nav_links += (
            f'<a class="mt-nav-link {active_cls}" href="{href}" target="_self">'
            f"<span>{label}</span>"
            f"</a>"
        )

    # -- Full HTML + CSS block ---------------------------------------------
    html = f"""
<!-- RainLoom Navbar -->
<style>
    /* ---- Import Inter font ---- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ---- Hide Streamlit default chrome ---- */
    #MainMenu {{visibility: hidden !important;}}
    header[data-testid="stHeader"] {{display: none !important;}}
    footer {{visibility: hidden !important;}}
    [data-testid="stToolbar"] {{display: none !important;}}
    [data-testid="stDecoration"] {{display: none !important;}}
    .stDeployButton {{display: none !important;}}

    /* ---- Hide sidebar completely ---- */
    [data-testid="stSidebar"] {{display: none !important;}}
    [data-testid="stSidebarNav"] {{display: none !important;}}
    section[data-testid="stSidebar"] {{display: none !important;}}
    button[kind="header"] {{display: none !important;}}
    [data-testid="collapsedControl"] {{display: none !important;}}

    /* ---- Push main content below the fixed navbar ---- */
    .main .block-container {{padding-top: 4rem !important;}}

    /* ---- Navbar container ---- */
    .mt-navbar {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(10, 15, 30, 0.92);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(99, 102, 241, 0.15);
        padding: 0 1.5rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
                     Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
        box-sizing: border-box;
    }}

    /* ---- Logo area (left) ---- */
    .mt-navbar-brand {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        text-decoration: none;
        flex-shrink: 0;
    }}

    .mt-navbar-monogram {{
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #ffffff;
        font-weight: 700;
        font-size: 0.97rem;
        width: 30px;
        height: 30px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        letter-spacing: 0.5px;
    }}

    .mt-navbar-title {{
        color: #e2e8f0;
        font-size: 1.06rem;
        font-weight: 600;
        letter-spacing: -0.01em;
        white-space: nowrap;
    }}

    /* ---- Navigation links (center / right) ---- */
    .mt-nav-links {{
        display: flex;
        align-items: center;
        gap: 0.25rem;
        height: 100%;
    }}

    .mt-nav-link {{
        color: #94a3b8;
        text-decoration: none;
        font-size: 0.95rem;
        font-weight: 500;
        padding: 0 0.75rem;
        height: 100%;
        display: flex;
        align-items: center;
        border-bottom: 2px solid transparent;
        transition: color 0.2s ease, border-color 0.2s ease;
        white-space: nowrap;
    }}

    .mt-nav-link:hover {{
        color: #e2e8f0;
        border-bottom-color: rgba(99, 102, 241, 0.4);
    }}

    .mt-nav-link.mt-nav-active {{
        color: #f1f5f9;
        border-bottom-color: #6366f1;
    }}
</style>

<div class="mt-navbar">
    <a class="mt-navbar-brand" href="/">
        <span class="mt-navbar-monogram">RL</span>
        <span class="mt-navbar-title">RainLoom</span>
    </a>
    <div class="mt-nav-links">
        {nav_links}
    </div>
</div>
"""

    st.markdown(html, unsafe_allow_html=True)
