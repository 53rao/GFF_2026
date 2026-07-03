"""
routes_user.py — Real User-Facing API Endpoints
===============================================
Serves real customer profile, transaction histories, and engagement records
directly from data_store.py.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from app import data_store

router = APIRouter()


@router.get("/{customer_id}/profile", summary="Get customer profile")
async def get_user_profile(customer_id: str):
    """Returns actual customer 360 profile data from JSON store."""
    customer = data_store.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/{customer_id}/transactions", summary="Get customer transactions")
async def get_user_transactions(
    customer_id: str,
    limit: int = Query(50, ge=1, le=500),
    start_date: Optional[str] = Query(None, description="Filter transactions after this ISO date"),
    end_date: Optional[str] = Query(None, description="Filter transactions before this ISO date"),
):
    """Returns actual transaction list for the customer with optional date range and limit."""
    customer = data_store.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    txs = data_store.get_transactions(customer_id)

    if start_date:
        txs = [t for t in txs if t.get("timestamp", "") >= start_date]
    if end_date:
        txs = [t for t in txs if t.get("timestamp", "") <= end_date]

    # Sort descending by timestamp
    txs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return txs[:limit]


@router.get("/{customer_id}/engagements", summary="Get customer engagement history")
async def get_user_engagements(customer_id: str):
    """Returns actual engagement cases / notifications for this customer."""
    customer = data_store.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    cases = data_store.get_engagement_cases()
    customer_cases = [c for c in cases if c.get("customer_id") == customer_id]
    return customer_cases
