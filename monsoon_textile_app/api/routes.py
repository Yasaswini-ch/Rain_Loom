"""
FastAPI route definitions for the Monsoon-Textile REST API.
"""

from __future__ import annotations

import time
from datetime import datetime

from fastapi import APIRouter, HTTPException

from monsoon_textile_app.api.schemas import (
    AlertsResponse,
    DispatchAlertsResponse,
    HealthResponse,
    RiskScoresResponse,
    StockRisk,
    Alert,
    SubscribeRequest,
    SubscribeResponse,
)

router = APIRouter(prefix="/api", tags=["Monsoon-Textile API"])

_START_TIME = time.time()


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    from monsoon_textile_app.api.data_bridge import get_dashboard_data

    data = get_dashboard_data()
    n_stocks = len(data.get("stock_data", {}))

    return HealthResponse(
        status="ok" if n_stocks > 0 else "degraded",
        version="4.0.0",
        uptime_seconds=round(time.time() - _START_TIME, 1),
        data_loaded=bool(data),
        n_stocks=n_stocks,
        last_update=datetime.utcnow(),
    )


@router.get("/risk-scores", response_model=RiskScoresResponse)
def get_risk_scores():
    """Get current ensemble risk scores for all tracked stocks."""
    from monsoon_textile_app.api.data_bridge import get_risk_scores as _get_scores

    scores = _get_scores()
    if not scores:
        raise HTTPException(status_code=503, detail="Risk data not yet loaded")

    avg_risk = sum(s["risk_score"] for s in scores) / len(scores)

    return RiskScoresResponse(
        timestamp=datetime.utcnow(),
        n_stocks=len(scores),
        avg_risk=round(avg_risk, 4),
        scores=[StockRisk(**s) for s in scores],
    )


@router.get("/alerts", response_model=AlertsResponse)
def get_alerts():
    """Get current active alerts based on risk scores and monsoon status."""
    from monsoon_textile_app.api.data_bridge import get_alerts as _get_alerts

    alerts = _get_alerts()

    return AlertsResponse(
        timestamp=datetime.utcnow(),
        n_alerts=len(alerts),
        alerts=[Alert(**a) for a in alerts],
    )


@router.post("/subscribe", response_model=SubscribeResponse)
def subscribe(req: SubscribeRequest):
    """Subscribe an email address to receive alerts."""
    from monsoon_textile_app.api.data_bridge import add_subscriber

    result = add_subscriber(req.email, req.alert_types)

    return SubscribeResponse(
        status=result["status"],
        email=result["email"],
        alert_types=result["alert_types"],
        message=f"Successfully {result['status']} {req.email} for {', '.join(req.alert_types)} alerts.",
    )


@router.post("/dispatch-alerts", response_model=DispatchAlertsResponse)
def dispatch_alerts(dry_run: bool = False):
    """Send current alerts to all subscribed email recipients."""
    from monsoon_textile_app.api.data_bridge import dispatch_alert_emails

    result = dispatch_alert_emails(dry_run=dry_run)
    if result["status"] == "error":
        raise HTTPException(status_code=503, detail=result["message"])
    return DispatchAlertsResponse(**result)
