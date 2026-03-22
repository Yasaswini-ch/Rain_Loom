# RainLoom

### When the monsoon falters, the market unravels.

> A causal machine learning system that predicts Indian NSE textile stock volatility from monsoon rainfall deficits — bridging climate science, cotton markets, and equity risk management with live data, AI advisories, and geospatial nowcasting.

---

## What This Project Does

When the Indian monsoon underperforms, cotton supply can tighten and input costs can rise across the textile value chain.

RainLoom turns that signal into a practical early-warning system: it estimates 4-week volatility risk for key NSE textile stocks and translates those signals into actionable guidance for farmers, MSMEs, investors, and policy teams through an 8-page dashboard and AI assistant.

---

## Dashboard Pages

### Page 1: Live Risk Monitor
Real-time risk scores for 8 NSE textile stocks with per-stock glass cards showing risk level, cotton dependency, 20-day volatility, and last price. Includes rainfall deficit charts across 8 cotton states, cotton futures with regime zones, and 120-week risk evolution timelines. Live NSE market status indicator with smart next-open messaging.

### Page 2: Causal Analysis
Granger causality heatmaps, impulse response functions, lag correlation analysis, and **Instrumental Variable (IV/2SLS) analysis** using ENSO ONI as an instrument — proving monsoon→volatility causation beyond correlation. Includes first-stage F-statistics, Hausman test diagnostics, and ONI scatter plots.

### Page 3: Model Performance
ROC/AUC curves, SHAP feature importance, confusion matrices, walk-forward backtesting results, and **Adaptive Online Learning** with drift detection (Page-Hinkley, ADWIN, KS test). Model Health Monitor shows rolling performance metrics with traffic-light drift indicators.

### Page 4: Scenario Simulator
4 historical presets (Normal, 2009 Drought, 2015 Drought, El Niño) plus interactive sliders for rainfall deficit, cotton price change, VIX level, and drought spatial breadth. Shows per-stock risk predictions with confidence intervals and sensitivity sweep charts.

### Page 5: Societal Impact
Farmer advisories with district-level risk tables, crop insurance recommendations, and yield-drop estimates. MSME hedging guidance with hedge ratios and instrument suggestions. Policy recommendations with employment impact estimates and intervention triggers.

### Page 6: Hedging Backtest
Historical backtesting of hedging strategies against cotton price volatility. Evaluates hedge effectiveness using signal-triggered vs buy-and-hold approaches with quantile regression bands.

### Page 7: Geospatial Nowcast
**Live district-level rainfall map** for 83 cotton-belt districts across 10 states. Uses Open-Meteo API for real 30-day rainfall data, compared against monthly climatological normals. Plotly choropleth with diverging RdYlGn colorscale, state filters, and stressed-district summary tables. Data refreshes every 10 minutes.

### RainLoom AI Assistant
Built-in AI chat panel accessible from every page. Powered by **Groq Llama 3.1** (SLM) when API key is available, with template engine fallback. Contextual answers grounded in live dashboard data — ask about risk, monsoon status, cotton prices, or get stakeholder-specific advice.

---

## Tech Stack

| Category | Libraries |
|---|---|
| Language | Python 3.10+ |
| Data | pandas, numpy, pyarrow, yfinance, requests |
| Econometrics | statsmodels, scipy, arch |
| Machine Learning | XGBoost, scikit-learn, SHAP, Optuna |
| Deep Learning | TensorFlow / Keras |
| Visualization | Plotly, matplotlib, seaborn |
| Dashboard | Streamlit |
| AI Chat | Groq API (Llama 3.1 8B) |
| REST API | FastAPI, uvicorn |
| Infra | Docker, loguru, pyyaml, python-dotenv |

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/Yasaswini-ch/Rain_Loom.git
cd Rain_Loom

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
# Groq API key for AI chat (free at console.groq.com)
GROQ_API_KEY=your_groq_api_key_here

# Enable REST API alongside Streamlit
ENABLE_API=1

# Email alerts (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

### Run the Dashboard

```bash
streamlit run monsoon_textile_app/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Run the REST API (Standalone)

```bash
uvicorn monsoon_textile_app.api.app:app --host 0.0.0.0 --port 8000
```

API docs at [http://localhost:8000/api/docs](http://localhost:8000/api/docs).

### Docker

```bash
docker build -t rainloom .
docker run -p 8501:8501 rainloom
```

---

## How to Use

### For Investors
1. Open **Page 1 (Live Risk Monitor)** to see current risk levels for all 8 textile stocks
2. Check **Page 4 (Scenario Simulator)** to stress-test your portfolio against drought scenarios
3. Use **Page 6 (Hedging Backtest)** to evaluate hedging strategies
4. Ask **RainLoom AI**: *"How should I position my textile portfolio?"*

### For Farmers
1. Check **Page 7 (Geospatial Nowcast)** for district-level rainfall status
2. See **Page 5 (Societal Impact)** → Farmer Advisory tab for insurance recommendations
3. Ask **RainLoom AI**: *"What should farmers do right now?"*

### For MSMEs / Textile Manufacturers
1. Monitor **Page 1** for cotton price trends and volatility regime
2. Check **Page 5** → MSME Hedging tab for procurement advice and hedge ratios
3. Ask **RainLoom AI**: *"What should MSMEs do about cotton procurement?"*

### For Researchers / Policy-Makers
1. **Page 2 (Causal Analysis)** shows the statistical proof of monsoon→market transmission
2. **Page 3 (Model Performance)** shows model accuracy, drift monitoring, and validation
3. **Page 5** → Policy tab for intervention thresholds and employment impact estimates

---

## Architecture

### Data Pipeline
```
IMD Rainfall + NSE Stocks + Cotton Futures + Macro Indicators + ENSO ONI
        │
        ▼
  Feature Engineering
  (climate deficits, lagged returns, volatility estimators)
        │
        ▼
  Causal Analysis
  (Granger → VAR → IRF → IV/2SLS → prove the chain)
        │
        ▼
  ┌──────────┬──────────┬──────────┐
  │ MS-GARCH │ XGBoost  │   LSTM   │
  │  (30%)   │  (40%)   │  (30%)   │
  └──────────┴──────────┴──────────┘
        │
        ▼
  Stacked Ensemble → Platt Calibration → Risk Score [0, 1]
        │
        ▼
  Dashboard · Geospatial Map · AI Advisor · REST API · Email Alerts
```

### Three-Layer Ensemble

| Layer | Model | Weight | Strengths |
|---|---|---|---|
| 1 | MS-GARCH (Markov-Switching) | 30% | Regime detection, fat-tail volatility |
| 2 | XGBoost Classifier | 40% | Tabular feature power, SHAP explainability |
| 3 | Stacked LSTM | 30% | Sequential memory, attention mechanism |

Risk scores map to four regimes: **LOW** (0–30%), **MODERATE** (30–60%), **HIGH** (60–80%), **EXTREME** (80–100%).

### REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/risk-scores` | Current ensemble risk scores for all stocks |
| GET | `/api/alerts` | Active alerts and advisories |
| POST | `/api/subscribe` | Subscribe to email alerts |
| GET | `/api/docs` | Interactive Swagger documentation |

---

## Project Structure

```
Rain_Loom/
├── configs/
│   └── settings.yaml              # Model hyperparams, thresholds, data sources
├── monsoon_textile_app/
│   ├── app.py                     # Streamlit entry point + dark theme
│   ├── api/                       # FastAPI REST gateway
│   │   ├── app.py                 # FastAPI app + CORS + background server
│   │   ├── routes.py              # API endpoint handlers
│   │   ├── schemas.py             # Pydantic response models
│   │   └── data_bridge.py         # Bridges API to data pipeline
│   ├── components/
│   │   ├── navbar.py              # Navigation bar with active-page highlighting
│   │   ├── chat_bubble.py         # RainLoom AI chat panel
│   │   ├── advisory_engine.py     # Template-based advisory generation
│   │   └── slm_engine.py          # Groq LLM integration
│   ├── data/
│   │   ├── fetch_real_data.py     # Yahoo Finance / IMD / MCX / ENSO data
│   │   ├── ml_models.py           # Feature matrix + model training + online learning
│   │   └── pipeline.py            # Data orchestration with retry logic
│   ├── models/
│   │   ├── causal.py              # Granger, VAR, IRF, IV/2SLS
│   │   ├── regime.py              # GARCH, MS-GARCH, regime detection
│   │   ├── xgb_classifier.py      # XGBoost + SHAP + Optuna
│   │   ├── lstm_model.py          # Stacked LSTM + attention
│   │   ├── backtester.py          # Walk-forward validation
│   │   └── drift_detector.py      # Page-Hinkley, ADWIN drift detection
│   ├── pages/
│   │   ├── 1_Live_Risk_Monitor.py
│   │   ├── 2_Causal_Analysis.py
│   │   ├── 3_Model_Performance.py
│   │   ├── 4_Scenario_Simulator.py
│   │   ├── 5_Societal_Impact.py
│   │   ├── 6_Hedging_Backtest.py
│   │   └── 7_Geospatial_Nowcast.py
│   └── utils/
│       ├── risk_score.py          # Ensemble scoring + calibration
│       ├── features.py            # Feature engineering
│       └── alerts.py              # Alert generation
├── .streamlit/
│   └── config.toml                # Streamlit theme config
├── requirements.txt
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Monitored Stocks

| Ticker | Company | Supply Chain | Cotton Dependency |
|---|---|---|---|
| ARVIND.NS | Arvind Ltd | Integrated | 72% |
| TRIDENT.NS | Trident Ltd | Upstream | 78% |
| KPRMILL.NS | KPR Mill | Upstream | 80% |
| WELSPUNLIV.NS | Welspun Living | Downstream | 65% |
| RSWM.NS | RSWM Ltd | Upstream | 75% |
| PAGEIND.NS | Page Industries | Downstream | 55% |
| RAYMOND.NS | Raymond Ltd | Integrated | 68% |
| KITEX.NS | Kitex Garments | Downstream | 60% |

---

## Design

- **Dark glass-morphism theme** — navy base (`#0f172a`), frosted card backgrounds, gradient accents
- **Inter typography** (300–800 weight) via Google Fonts
- **Plotly dark template** — transparent backgrounds, unified hover, no grid clutter
- **Responsive layout** — `max-width: 1480px` containers with CSS Grid

---

## Key Design Decisions

- **No data leakage:** `TimeSeriesSplit` everywhere — no random shuffling of time-series data
- **Causal-first:** Granger tests + IV/2SLS justify predictions before stakeholders act
- **Calibrated outputs:** Platt scaling ensures risk scores are meaningful probabilities
- **Live data:** Yahoo Finance, Open-Meteo, NOAA ENSO — no synthetic training data
- **Stakeholder-centric:** Risk scores translated to ₹/acre premiums, hedge ratios, worker counts
- **10-minute caching:** Geospatial API calls cached with TTL to avoid excessive requests

---

## Core Features (Live + Real-Time)

- **Live market monitoring:** Continuously tracks NSE textile stocks, cotton futures, and volatility with dashboard-level risk updates.
- **Real-time rainfall intelligence:** District-level rainfall nowcasting with frequent refreshes to detect emerging stress zones early.
- **Live risk scoring engine:** Ensemble model inference updates risk regimes (LOW/MODERATE/HIGH/EXTREME) from streaming inputs.
- **Real-time alerting surface:** API + dashboard + advisory panels expose current risk state for fast operational decisions.
- **Live AI assistant context:** Chat responses are grounded in the latest dashboard state, not static offline snapshots.
- **Near real-time geospatial refresh:** Open-Meteo rainfall ingestion refreshes every 10 minutes for the nowcast map.

---

## How To Further Scale RainLoom

- **Decouple ingestion from UI:** Move data collection to scheduled/background workers and let Streamlit/FastAPI read from a shared data store.
- **Add a streaming layer:** Introduce Kafka/Redpanda/PubSub for event-driven, real-time pipelines (rainfall, prices, alerts, model outputs).
- **Serve models separately:** Deploy inference as an independent microservice with autoscaling and versioned model endpoints.
- **Use online feature store patterns:** Persist low-latency, reusable features for both dashboard serving and training consistency.
- **Scale storage by workload:** Use time-series storage for tick/climate feeds and object storage for model artifacts/backtests.
- **Harden caching strategy:** Multi-tier caching (in-memory + Redis) for high-frequency reads and lower API pressure.
- **Improve reliability:** Add retries, circuit breakers, dead-letter queues, and replayable jobs for upstream API failures.
- **Expand observability:** Track latency, drift, prediction quality, and data freshness with Prometheus/Grafana + structured logs.
- **Operationalize retraining:** Automated retrain/evaluate/deploy pipelines with shadow testing and rollback-safe model releases.
- **Deploy for horizontal scale:** Container orchestration (Kubernetes/ECS) with HPA, regional failover, and blue-green deployments.
- **Secure production traffic:** API gateway, auth/rate limits, secrets management, and audit logs for enterprise-grade usage.
- **Globalize stakeholder delivery:** Webhooks, email/SMS channels, and tenant-aware alert routing for multi-organization adoption.

---
## Why This Matters In Practice

- **Causal, not just correlational:** Decisions are backed by Granger + IV/2SLS evidence, reducing false confidence from spurious market links.
- **Operationally live:** Risk, rainfall, and advisory surfaces refresh continuously, so users act on current conditions rather than stale reports.
- **Actionable for multiple stakeholders:** The same intelligence is translated into investor positioning, MSME hedging signals, farmer advisories, and policy triggers.
- **Built for reliability:** Caching, retries, and API fallbacks keep the system useful even when upstream data quality fluctuates.
- **Transparent model behavior:** SHAP, drift monitors, and calibration make model outputs explainable and auditable for high-stakes use.
- **Ready to expand:** The architecture supports stepwise growth into streaming pipelines, autoscaled inference, and enterprise integrations.

---
## Societal Value: Claim -> Evidence -> Outcome

| Claim | Evidence In Codebase | Practical Outcome |
|---|---|---|
| Farmers get earlier risk signals before severe monsoon stress. | [5_Societal_Impact.py](./monsoon_textile_app/pages/5_Societal_Impact.py), [alerts.py](./monsoon_textile_app/utils/alerts.py) implement farmer advisory flows and district-level risk handling. | Earlier insurance and cropping decisions can reduce avoidable loss during deficit periods. |
| MSME textile operators receive procurement and hedging guidance. | [5_Societal_Impact.py](./monsoon_textile_app/pages/5_Societal_Impact.py), [advisory_engine.py](./monsoon_textile_app/components/advisory_engine.py), [alerts.py](./monsoon_textile_app/utils/alerts.py) generate MSME-specific advisory signals. | Better timing on cotton buying/hedging can reduce input-cost shocks. |
| Policy teams can monitor risk concentration and respond faster. | [5_Societal_Impact.py](./monsoon_textile_app/pages/5_Societal_Impact.py), [7_Geospatial_Nowcast.py](./monsoon_textile_app/pages/7_Geospatial_Nowcast.py) provide district/state risk visibility and policy-facing summaries. | More targeted interventions and communication during high-risk windows. |
| Decisions are grounded in causal analysis, not only correlation. | [2_Causal_Analysis.py](./monsoon_textile_app/pages/2_Causal_Analysis.py), [causal.py](./monsoon_textile_app/models/causal.py) implement Granger and IV/2SLS workflows. | Higher confidence that alerts track meaningful transmission effects. |
| The system is usable in live operations through API and alerts. | [routes.py](./monsoon_textile_app/api/routes.py), [data_bridge.py](./monsoon_textile_app/api/data_bridge.py) expose risk, alerts, and subscription endpoints. | Institutions can integrate outputs into existing monitoring and notification workflows. |

### Current Limits (Transparent)

- Estimates are decision-support signals, not guaranteed outcomes.
- Live quality depends on upstream market/weather data availability.
- Some policy and economic impact numbers are scenario-based and should be validated with field data.

---
## Version

**v4.0.0** — 8 pages, REST API, AI chat, geospatial nowcasting, IV/2SLS, drift detection, online learning

---

## License

This project is for educational and research purposes.




