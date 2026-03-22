"""
FastAPI Application -- Monsoon-Textile REST API Gateway
=======================================================

Run standalone:
    uvicorn monsoon_textile_app.api.app:app --host 0.0.0.0 --port 8000

Or enable alongside Streamlit by setting ENABLE_API=1 in environment.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from monsoon_textile_app.api.routes import router

app = FastAPI(
    title="RainLoom Volatility API",
    description=(
        "REST API for the RainLoom Risk System. "
        "Provides programmatic access to ensemble risk scores, "
        "alerts, and monsoon-cotton-textile transmission chain data."
    ),
    version="4.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS -- allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "name": "Monsoon-Textile Volatility API",
        "version": "4.0.0",
        "docs": "/api/docs",
        "endpoints": [
            "/api/health",
            "/api/risk-scores",
            "/api/alerts",
            "/api/subscribe",
        ],
    }


def start_api_background(host: str = "0.0.0.0", port: int = 8000):
    """Start the API server in a background thread (for Streamlit co-hosting)."""
    import threading
    import uvicorn

    def _run():
        uvicorn.run(app, host=host, port=port, log_level="warning")

    thread = threading.Thread(target=_run, daemon=True, name="fastapi-bg")
    thread.start()
    print(f"[API] FastAPI server started on http://{host}:{port}")
    return thread


# Auto-start when ENABLE_API=1
if os.environ.get("ENABLE_API", "").strip() in ("1", "true", "yes"):
    start_api_background()
