"""
Data Bridge -- connects FastAPI to the existing Streamlit data pipeline.
Caches data in memory with a configurable TTL to avoid reloading on every request.
"""

from __future__ import annotations

import os
import smtplib
import time
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from typing import Optional

_CACHE: dict = {}
_CACHE_TS: float = 0
_CACHE_TTL: float = 300  # 5 minutes
_ENV_LOADED: bool = False


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
                vals = [v for v in list(latest.values) if isinstance(v, (int, float))]
                avg_def = (sum(vals) / len(vals)) if vals else 0
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


def _get_smtp_config() -> dict:
    """Load SMTP configuration from environment variables."""
    global _ENV_LOADED

    # Load .env once for standalone API processes where env vars are not pre-exported.
    if not _ENV_LOADED:
        env_path = Path(__file__).resolve().parents[2] / ".env"
        if env_path.exists():
            try:
                for raw in env_path.read_text(encoding="utf-8").splitlines():
                    line = raw.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
            except Exception:
                # Keep fallback behavior: rely on pre-set environment if .env parsing fails.
                pass
        _ENV_LOADED = True

    host = os.environ.get("SMTP_HOST", "").strip()
    port_str = os.environ.get("SMTP_PORT", "587").strip()
    user = os.environ.get("SMTP_USER", "").strip()
    password = os.environ.get("SMTP_PASS", "").strip().replace(" ", "")
    sender = os.environ.get("SMTP_SENDER", user).strip()
    use_tls = os.environ.get("SMTP_USE_TLS", "1").strip().lower() in {"1", "true", "yes"}

    try:
        port = int(port_str)
    except ValueError:
        port = 587

    enabled = bool(host and port and user and password and sender)
    return {
        "enabled": enabled,
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "sender": sender,
        "use_tls": use_tls,
    }


def _filter_alerts_for_subscriber(alerts: list[dict], alert_types: list[str]) -> list[dict]:
    """Return only alerts matching subscriber severities."""
    requested = {str(a).strip().lower() for a in (alert_types or []) if str(a).strip()}
    if not requested or "all" in requested:
        return alerts
    return [a for a in alerts if str(a.get("severity", "")).lower() in requested]


def _format_alert_digest(alerts: list[dict]) -> str:
    """Build a plain-text digest for email delivery."""
    lines = [
        "RainLoom Alert Digest",
        f"Generated at (UTC): {datetime.utcnow().isoformat()}",
        "",
    ]
    for idx, alert in enumerate(alerts, start=1):
        ts = alert.get("timestamp")
        if hasattr(ts, "isoformat"):
            ts_text = ts.isoformat()
        else:
            ts_text = str(ts)
        lines.extend([
            f"{idx}. [{str(alert.get('severity', 'info')).upper()}] {alert.get('title', 'Alert')}",
            f"   Category: {alert.get('category', 'unknown')}",
            f"   Message : {alert.get('message', '')}",
            f"   Time    : {ts_text}",
            "",
        ])
    lines.append("You are receiving this because you subscribed to RainLoom alerts.")
    return "\n".join(lines)


def _send_email(recipient: str, alerts: list[dict], smtp_cfg: dict) -> None:
    """Send one alert email to one recipient."""
    highest = "critical" if any(a.get("severity") == "critical" for a in alerts) else "warning"
    subject = f"[RainLoom] {len(alerts)} alert(s) - {highest.upper()}"
    body = _format_alert_digest(alerts)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_cfg["sender"]
    msg["To"] = recipient
    msg.set_content(body)

    with smtplib.SMTP(smtp_cfg["host"], smtp_cfg["port"], timeout=20) as server:
        if smtp_cfg["use_tls"]:
            server.starttls()
        server.login(smtp_cfg["user"], smtp_cfg["password"])
        server.send_message(msg)


def dispatch_alert_emails(dry_run: bool = False) -> dict:
    """
    Send the current active alerts to all subscribers.

    Parameters
    ----------
    dry_run : bool
        If True, simulate delivery and return counts without sending emails.
    """
    subscribers = get_subscriber_list()
    alerts = get_alerts()
    smtp_cfg = _get_smtp_config()

    if not dry_run and not smtp_cfg["enabled"]:
        return {
            "status": "error",
            "timestamp": datetime.utcnow(),
            "total_subscribers": len(subscribers),
            "recipients_targeted": 0,
            "total_alerts": len(alerts),
            "emails_sent": 0,
            "deliveries_skipped": len(subscribers),
            "failures": ["SMTP is not configured. Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, and SMTP_SENDER."],
            "dry_run": dry_run,
            "message": "Email dispatch not attempted because SMTP is not configured.",
        }

    recipients_targeted = 0
    emails_sent = 0
    deliveries_skipped = 0
    failures: list[str] = []

    for sub in subscribers:
        recipient = str(sub.get("email", "")).strip()
        alert_types = sub.get("alert_types", ["critical"])

        if not recipient:
            deliveries_skipped += 1
            continue

        selected_alerts = _filter_alerts_for_subscriber(alerts, alert_types)
        if not selected_alerts:
            deliveries_skipped += 1
            continue

        recipients_targeted += 1
        if dry_run:
            emails_sent += 1
            continue

        try:
            _send_email(recipient=recipient, alerts=selected_alerts, smtp_cfg=smtp_cfg)
            emails_sent += 1
        except Exception as exc:
            failures.append(f"{recipient}: {exc}")

    status = "ok" if not failures else ("partial" if emails_sent > 0 else "error")
    msg = (
        f"Dispatched {emails_sent} email(s) to {recipients_targeted} targeted subscriber(s)."
        if not dry_run
        else f"Dry run complete: {emails_sent} email(s) would be sent to {recipients_targeted} subscriber(s)."
    )

    return {
        "status": status,
        "timestamp": datetime.utcnow(),
        "total_subscribers": len(subscribers),
        "recipients_targeted": recipients_targeted,
        "total_alerts": len(alerts),
        "emails_sent": emails_sent,
        "deliveries_skipped": deliveries_skipped,
        "failures": failures,
        "dry_run": dry_run,
        "message": msg,
    }
