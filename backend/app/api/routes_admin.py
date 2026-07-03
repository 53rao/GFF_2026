"""
routes_admin.py — Real Admin Operations Dashboard Endpoints
===========================================================
Serves real customer directory, signals, hypotheses, and joined case details
directly from data_store.py.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from app import data_store

router = APIRouter()


@router.get("/customers", summary="List all customers with pagination")
async def list_admin_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """Full customer list from JSON store with pagination."""
    customers = data_store.get_all_customers()
    total = len(customers)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": customers[start_idx:end_idx]
    }


@router.get("/signals", summary="List detected signals")
async def list_admin_signals(
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    date: Optional[str] = Query(None, description="Filter prefix date (YYYY-MM-DD)"),
):
    """All detected signals filterable by customer_id and detection date."""
    signals = data_store.get_signals(customer_id=customer_id)
    if date:
        signals = [s for s in signals if s.get("detected_at", "").startswith(date)]
    return signals


@router.get("/hypotheses", summary="List generated hypotheses")
async def list_admin_hypotheses(
    customer_id: Optional[str] = Query(None),
):
    """All hypotheses with confidence scores and product category."""
    return data_store.get_hypotheses(customer_id=customer_id)


@router.get("/cases", summary="List engagement cases")
async def list_admin_cases(
    status: Optional[str] = Query(None),
):
    """All engagement cases with current pipeline status."""
    return data_store.get_engagement_cases(status=status)


@router.get("/cases/{case_id}", summary="Get joined case detail")
async def get_admin_case_detail(case_id: str):
    """
    Full case detail joined from multiple JSON files:
    signal -> hypothesis -> engagement -> outcome chain.
    """
    cases = data_store.get_engagement_cases()
    case = None
    for c in cases:
        if c.get("id") == case_id or c.get("case_id") == case_id:
            case = c
            break

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    cid = case.get("customer_id")
    customer = data_store.get_customer(cid) if cid else None
    signals = data_store.get_signals(customer_id=cid) if cid else []
    hypotheses = data_store.get_hypotheses(customer_id=cid) if cid else []

    return {
        "case": case,
        "customer": customer,
        "signals": signals,
        "hypotheses": hypotheses,
        "chain_summary": {
            "signal_count": len(signals),
            "hypothesis_count": len(hypotheses),
            "status": case.get("status", "Open")
        }
    }
