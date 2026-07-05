"""
routes_cases.py — Case Management API Endpoints
================================================
Provides REST endpoints for creating, listing, viewing, and updating
Cases in the SBI Multi-Agent Banking Engagement System.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.database import get_db
from app.db import crud
from app.api.schemas import CaseCreate, CaseResponse, CaseDetailResponse, CaseUpdate, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse, summary="List all cases")
async def list_cases(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns a paginated list of cases, optionally filtered by status.
    """
    offset = (page - 1) * page_size
    # List filtered cases
    cases = await crud.list_cases(db, status=status, limit=page_size, offset=offset)
    # Total count for pagination
    all_cases = await crud.list_cases(db, status=status, limit=9999, offset=0)
    total = len(all_cases)

    # Convert database cases to response format
    items = []
    for c in cases:
        items.append({
            "customer_id": c.customer_id,
            "case_type": c.type or "Opportunity",
            "priority": c.priority,
            "assigned_agent": c.assigned_agent,
            "id": c.id,
            "status": c.status,
            "created_at": c.created_at.strftime("%Y-%m-%dT%H:%M:%SZ") if c.created_at else "",
            "updated_at": c.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ") if c.updated_at else "",
            "sla_deadline": "",
            "sla_breached": c.slaBreached or False
        })

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }


@router.post("/", response_model=CaseResponse, status_code=status.HTTP_201_CREATED, summary="Create a case")
async def create_case(payload: CaseCreate, db: AsyncSession = Depends(get_db)):
    """
    Manually creates a new case.
    """
    c = await crud.create_case(db, payload)
    return {
        "customer_id": c.customer_id,
        "case_type": c.type or payload.case_type,
        "priority": c.priority,
        "assigned_agent": c.assigned_agent,
        "id": c.id,
        "status": c.status,
        "created_at": c.created_at.strftime("%Y-%m-%dT%H:%M:%SZ") if c.created_at else "",
        "updated_at": c.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ") if c.updated_at else "",
        "sla_deadline": "",
        "sla_breached": False
    }


@router.get("/{case_id}", response_model=CaseDetailResponse, summary="Get case detail")
async def get_case(case_id: str, db: AsyncSession = Depends(get_db)):
    """
    Returns the full detail for a single case.
    """
    c = await crud.get_case(db, case_id)
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
        
    return {
        "customer_id": c.customer_id,
        "case_type": c.type or "Opportunity",
        "priority": c.priority,
        "assigned_agent": c.assigned_agent,
        "id": c.id,
        "status": c.status,
        "created_at": c.created_at.strftime("%Y-%m-%dT%H:%M:%SZ") if c.created_at else "",
        "updated_at": c.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ") if c.updated_at else "",
        "sla_deadline": "",
        "sla_breached": c.slaBreached or False,
        "pipeline_id": "",
        "hypotheses": [{"recommended_action": h.recommended_action, "confidence": h.confidence, "rationale": h.rationale} for h in c.hypotheses],
        "engagement_outcomes": [],
        "handoff_records": []
    }


@router.patch("/{case_id}", response_model=CaseResponse, summary="Update a case")
async def update_case(case_id: str, payload: CaseUpdate, db: AsyncSession = Depends(get_db)):
    """
    Updates mutable fields on a case (status, priority, assignee).
    """
    c = await crud.update_case(db, case_id, payload)
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
        
    return {
        "customer_id": c.customer_id,
        "case_type": c.type or "Opportunity",
        "priority": c.priority,
        "assigned_agent": c.assigned_agent,
        "id": c.id,
        "status": c.status,
        "created_at": c.created_at.strftime("%Y-%m-%dT%H:%M:%SZ") if c.created_at else "",
        "updated_at": c.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ") if c.updated_at else "",
        "sla_deadline": "",
        "sla_breached": c.slaBreached or False
    }


@router.get("/{case_id}/timeline", summary="Get case event timeline")
async def get_case_timeline(case_id: str, db: AsyncSession = Depends(get_db)):
    """
    Returns an ordered list of pipeline events for a case.
    """
    c = await crud.get_case(db, case_id)
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
        
    timeline = [
        {"event": "Case Created", "timestamp": c.created_at.strftime("%Y-%m-%dT%H:%M:%SZ") if c.created_at else ""}
    ]
    for s in c.signals:
        timeline.append({"event": f"Signal Detected: {s.signal_type}", "timestamp": s.detected_at.strftime("%Y-%m-%dT%H:%M:%SZ") if s.detected_at else ""})
    for h in c.hypotheses:
        timeline.append({"event": f"Hypothesis Formed: {h.recommended_action}", "timestamp": h.created_at.strftime("%Y-%m-%dT%H:%M:%SZ") if h.created_at else ""})
        
    return timeline
