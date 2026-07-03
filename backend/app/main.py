"""
main.py — FastAPI Application Entrypoint
========================================
Configures FastAPI application lifecycle, CORS middleware for local frontend dev,
and registers functional API routers for user, admin, and pipeline automation.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import data_store
from app.api import (
    routes_user,
    routes_admin,
    routes_cases,
    routes_agents,
    routes_webhook,
    routes_pipeline,
)
from app.utils.logger import get_logger

logger = get_logger("sbi.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up SBI Multi-Agent Banking Engagement System backend...")
    customers = data_store.get_all_customers()
    logger.info(f"Loaded {len(customers)} customers from JSON data store.")
    yield
    logger.info("Shutting down SBI backend...")


app = FastAPI(
    title="SBI Proactive Banking Engagement API",
    version="0.2.0",
    description="Multi-agent banking engagement pipeline backed by JSON data store.",
    lifespan=lifespan,
)

# Enable CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow localhost:3000, 3001, etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes exactly matching requested paths
app.include_router(routes_user.router, prefix="/api/user", tags=["User API"])
app.include_router(routes_admin.router, prefix="/api/admin", tags=["Admin API"])
app.include_router(routes_pipeline.router, prefix="/api/pipeline", tags=["Pipeline Execution"])

# Also maintain /api/v1 aliases for backward compatibility with scaffolding routes
app.include_router(routes_user.router, prefix="/api/v1/user", tags=["User API v1"])
app.include_router(routes_admin.router, prefix="/api/v1/admin", tags=["Admin API v1"])
app.include_router(routes_cases.router, prefix="/api/v1/cases", tags=["Cases v1"])
app.include_router(routes_agents.router, prefix="/api/v1/agents", tags=["Agents v1"])
app.include_router(routes_webhook.router, prefix="/api/v1/webhook", tags=["Webhooks v1"])


@app.get("/health", tags=["System"])
async def health_check():
    """System health check returning version and customer store count."""
    customers = data_store.get_all_customers()
    return {
        "status": "healthy",
        "version": app.version,
        "customers_loaded": len(customers)
    }
