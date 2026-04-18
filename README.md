# RainLoom: Predictive Climate Intelligence for the Textile Supply Chain

[![Live App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rainloomtextiles.streamlit.app)
[![Institutional API](https://img.shields.io/badge/API-Gateway--v1.0-blue?logo=fastapi)](https://rainloom.vercel.app/)
![Causal Confidence](https://img.shields.io/badge/Confidence%20Metric-IV%20F--Stat%205.8-brightgreen)
![GIS Resolution](https://img.shields.io/badge/GIS%20Resolution-District--Level-orange)

### Quantifying Climate Risk. Protecting Textile Livelihoods.

RainLoom is a high-fidelity intelligence platform that bridges the gap between monsoon variability and textile equity risk. By integrating **Causal AI**, **Geospatial GIS Telemetry**, and **Institutional SaaS Gateways**, RainLoom transforms disparate climate data into actionable financial foresight for fund managers and supply-chain stakeholders.

---

## 🏛️ Project Architecture & Strategic Pillars

### 1. Robust Causal Inference Engine
Unlike traditional correlation models, RainLoom utilizes **Granger Causality** and **Instrumental Variable (IV) analysis** to isolate true risk propagation.
*   **Scientific Validation:** Uses ENSO (Oceanic Niño Index) as an exogenous instrument to prove the *Monsoon → Cotton Supply → Volatility* link.
*   **Predictive Modeling:** A multi-layered ensemble of **MS-GARCH** (regime detection), **XGBoost** (feature impact), and **Sequential NLP** (sentiment divergence).

### 2. High-Resolution GIS Telemetry
Real-time geospatial intelligence that monitors the physical health of the cotton belt.
*   **District-Level Choropleths:** True GIS polygon mapping through `streamlit-folium` for precise regional risk assessment.
*   **Raster Integration:** Live-sync with **NASA MODIS** and **NDVI Vegetation Indices** to track crop health ahead of market reporting.

### 3. Enterprise Infrastructure & B2B Integration
Built for seamless integration into the institutional finance and supply chain ecosystem.
*   **SaaS API Gateway:** Self-service portal for API key generation and developer documentation.
*   **Embedded Solutions:** Low-code iFrame widgets for embedding real-time risk gauges into external ERPs.
*   **Autonomous Alerting:** Background daemon-threads for multi-channel notification delivery (HTML Email & Telegram Telemetry).

### 4. ESG & Socio-Economic Intervention
Bridging the "last mile" between macro-analysis and community impact.
*   **Parametric Payout Gateway:** An automated "Oracle" for crop insurance, reducing payout latency from months to seconds via simulated UPI/AEPS triggers.
*   **Gender-Focused Risk Analysis:** Mapping economic vulnerability for the 27 million women employed in Indian textiles.

---

## 📊 Operational Framework

| Capability | Technical Implementation | Strategic Value |
|---|---|---|
| **Volatility Monitoring** | Causal Fan-Charts & Gauges | Real-time exposure assessment |
| **Propagation Analysis** | Sankey Flow & Knowledge Graphs | Mapping the value-chain domino effect |
| **Geospatial Nowcast** | Polygon GIS & Raster Overlays | Early-warning for supply chain epicenters |
| **Stress Testing** | Backtesting & Scenario Simulation | Evaluating resilience against historical droughts |
| **Livelihood Protection** | Multilingual Voice & Parametric Payouts | Closing the ESG and insurance gap |

---

## 🚀 Deployment Guide

### Installation
```bash
git clone https://github.com/Yasaswini-ch/Rain_Loom.git
cd Rain_Loom
pip install -r requirements.txt
```

### Configuration
Customize your system via the `.env` file for enterprise features:
```bash
# Core Intelligence
GROQ_API_KEY=your_key

# Notification Gateways
SMTP_USER=your_email
SMTP_PASS=app_password
TELEGRAM_BOT_TOKEN=your_token
```

### Execution
Run the primary dashboard or the institutional API separately:
```bash
# Analytics Dashboard
streamlit run monsoon_textile_app/app.py

# API Gateway
uvicorn monsoon_textile_app.api.app:app --host 0.0.0.0 --port 8000
```

---

## 🌍 Vision & Impact

**The Market Problem:** In the Indian textile sector, climate signals are often delayed or obfuscated by market sentiment. RainLoom solves this by providing "Information Symmetry"—allowing stakeholders to see physical risks (via NASA) and causal risks (via IV-models) weeks before they manifest in equity prices.

**The Resilience Goal:** Beyond finance, RainLoom serves as a policy tool. By automating parametric insurance and mapping gender-disaggregated labor risks, we provide the infrastructure necessary for a climate-resilient economy.

---

*RainLoom: Precision Agriculture meets Predictive Finance.*
