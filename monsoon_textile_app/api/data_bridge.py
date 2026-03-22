"""
Data Bridge -- connects FastAPI to the existing Streamlit data pipeline.
Caches data in memory with a configurable TTL to avoid reloading on every request.
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Optional

_CACHE: dict = {}
_CACHE_TS: float = 0
_CACHE_TTL: float = 300  # 5 minutes


def get_dashboard_data(force_refresh: bool = False) -> dict:
    """
    Get dashboard data, using an in-memory cache with TTL.

    Parameters
    ----------
    force_refresh : bool
        Force a fresh data load, bypassing the cache.

    Returns
    -------
    dict
        Same structure as load_all_data().
    """
    global _CACHE, _CACHE_TS

    now = time.time()
    if not force_refresh and _CACHE and (now - _CACHE_TS) < _CACHE_TTL:
        return _CACHE

    try:
        from monsoon_textile_app.data.fetch_real_data import load_all_data
        data = load_all_data(use_cache=True)
        _CACHE = data
        _CACHE_TS = now
        return data
    except Exception as e:
        print(f"[API Bridge] Data load failed: {e}")
        return _CACHE or {}


def get_risk_scores() -> list[dict]:
    """Extract current risk scores for all stocks."""
    from monsoon_textile_app.data.fetch_real_data import STOCKS

    data = get_dashboard_data()
    stock_data = data.get("stock_data", {})
    scores = []

    for ticker, info in STOCKS.items():
        sdf = stock_data.get(ticker)
        if sdf is None or sdf.empty:
            continue

        risk = float(sdf["risk_score"].iloc[-1]) if "risk_score" in sdf.columns else 0.5
        vol = float(sdf["vol_20d"].iloc[-1]) if "vol_20d" in sdf.columns else None
        price = float(sdf["price"].iloc[-1]) if "price" in sdf.columns else None

        label = "LOW" if risk < 0.3 else "MODERATE" if risk < 0.6 else "HIGH" if risk < 0.8 else "EXTREME"

        scores.append({
            "ticker": ticker,
            "name": info["name"],
            "sector": info.get("sector", "Textile"),
            "chain_position": info.get("chain", "Unknown"),
            "risk_score": round(risk, 4),
            "risk_label": label,
            "volatility_20d": round(vol, 4) if vol is not None else None,
            "latest_price": round(price, 2) if price is not None else None,
        })

    return scores


def get_alerts() -> list[dict]:
    """Generate current alerts based on dashboard data."""
    data = get_dashboard_data()
    alerts = []
    now = datetime.utcnow()

    # Risk-based alerts
    stock_data = data.get("stock_data", {})
    from monsoon_textile_app.data.fetch_real_data import STOCKS

    for ticker, sdf in stock_data.items():
        if sdf.empty or "risk_score" not in sdf.columns:
            continue
        risk = float(sdf["risk_score"].iloc[-1])
        name = STOCKS.get(ticker, {}).get("name", ticker)

        if risk >= 0.8:
            alerts.append({
                "id": f"risk-extreme-{ticker}",
                "severity": "critical",
                "category": "risk",
                "title": f"EXTREME risk: {name}",
                "message": f"{name} ({ticker}) risk score at {risk:.1%}. Consider hedging or reducing exposure.",
                "timestamp": now,
            })
        elif risk >= 0.6:
            alerts.append({
                "id": f"risk-high-{ticker}",
                "severity": "warning",
                "category": "risk",
                "title": f"HIGH risk: {name}",
                "message": f"{name} ({ticker}) risk score at {risk:.1%}. Monitor closely.",
                "timestamp": now,
            })

    # Monsoon alerts
    rainfall = data.get("rainfall", {})
    if isinstance(rainfall, dict):
        annual = rainfall.get("annual_deficit")
        if hasattr(annual, "iloc") and len(annual) > 0:
            latest = annual.iloc[-1]
            if hasattr(latest, "values"):
                avg_def = float(latest.mean()) if hasattr(latest, "mean") else 0
            elif isinstance(latest, dict):
                vals = [v for v in latest.values() if isinstance(v, (int, float))]
                avg_def = sum(vals) / max(len(vals), 1) if vals else 0
            else:
                avg_def = 0

            if avg_def < -20:
                alerts.append({
                    "id": "monsoon-severe-deficit",
                    "severity": "critical",
                    "category": "monsoon",
                    "title": "Severe monsoon deficit",
                    "message": f"Average cotton-belt rainfall deficit at {avg_def:+.1f}% from LPA.",
                    "timestamp": now,
                })

    return alerts


def get_subscriber_list() -> list[dict]:
    """Load email subscriber list from JSON file."""
    import json
    from pathlib import Path

    sub_file = Path(__file__).parent / "subscribers.json"
    if sub_file.exists():
        try:
            with open(sub_file) as f:
                return json.load(f)
        except Exception:
            return []
    return []


def add_subscriber(email: str, alert_types: list[str]) -> dict:
    """Add an email subscriber."""
    import json
    from pathlib import Path

    sub_file = Path(__file__).parent / "subscribers.json"
    subs = get_subscriber_list()

    # Check if already subscribed
    for sub in subs:
        if sub["email"] == email:
            sub["alert_types"] = alert_types
            with open(sub_file, "w") as f:
                json.dump(subs, f, indent=2)
            return {"status": "updated", "email": email, "alert_types": alert_types}

    subs.append({"email": email, "alert_types": alert_types})
    with open(sub_file, "w") as f:
        json.dump(subs, f, indent=2)

    return {"status": "subscribed", "email": email, "alert_types": alert_types}
