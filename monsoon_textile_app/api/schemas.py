"""
Pydantic schemas for the REST API request/response models.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Response Models ──────────────────────────────────────────────────────

class StockRisk(BaseModel):
    ticker: str
    name: str
    sector: str
    chain_position: str
    risk_score: float = Field(ge=0, le=1)
    risk_label: str
    volatility_20d: Optional[float] = None
    latest_price: Optional[float] = None


class RiskScoresResponse(BaseModel):
    timestamp: datetime
    n_stocks: int
    avg_risk: float
    scores: list[StockRisk]


class Alert(BaseModel):
    id: str
    severity: str  # "info", "warning", "critical"
    category: str  # "risk", "monsoon", "cotton", "model"
    title: str
    message: str
    timestamp: datetime


class AlertsResponse(BaseModel):
    timestamp: datetime
    n_alerts: int
    alerts: list[Alert]


class SubscribeRequest(BaseModel):
    email: str
    alert_types: list[str] = Field(
        default=["critical"],
        description="Alert severities to subscribe to",
    )


class SubscribeResponse(BaseModel):
    status: str
    email: str
    alert_types: list[str]
    message: str


class DispatchAlertsResponse(BaseModel):
    status: str
    timestamp: datetime
    total_subscribers: int
    recipients_targeted: int
    total_alerts: int
    emails_sent: int
    deliveries_skipped: int
    failures: list[str]
    dry_run: bool
    message: str


class HealthResponse(BaseModel):
    status: str  # "ok", "degraded", "error"
    version: str
    uptime_seconds: float
    data_loaded: bool
    n_stocks: int
    last_update: Optional[datetime] = None


class MonsoonStatus(BaseModel):
    avg_deficit_pct: float
    stressed_states: list[str]
    spatial_breadth_pct: float


class CottonStatus(BaseModel):
    price_change_30d_pct: float
    regime: str
    latest_price: Optional[float] = None


class DashboardSummaryResponse(BaseModel):
    timestamp: datetime
    risk: RiskScoresResponse
    monsoon: MonsoonStatus
    cotton: CottonStatus
    vix: Optional[float] = None
