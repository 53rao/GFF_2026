"""
routes_cases.py — Case Management API Endpoints
================================================
Provides REST endpoints for creating, listing, viewing, and updating
Cases in the SBI Multi-Agent Banking Engagement System.

Cases represent a single pipeline run for a customer: from signal
detection through to engagement outcome and optional human handoff.

Endpoints:
    GET  /api/v1/cases/                         List cases (paginated, filterable)
    POST /api/v1/cases/                         Create a new case manually
    GET  /api/v1/cases/{case_id}                Get case detail (full pipeline state)
    PATCH /api/v1/cases/{case_id}               Update case status / priority
    GET  /api/v1/cases/{case_id}/timeline       Case event timeline

TODO: Implement DB queries via app.db.crud and response serialisation via schemas.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from app.api.schemas import CaseCreate, CaseResponse, CaseDetailResponse, CaseUpdate, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse, summary="List all cases")
async def list_cases(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    assigned_agent: Optional[str] = Query(None, description="Filter by assigned agent"),
):
    """
    Returns a paginated list of cases, optionally filtered by status,
    priority, or assigned agent.

    TODO: Implement DB query via crud.list_cases() with filters.
    """
    raise NotImplementedError


@router.post("/", response_model=CaseResponse, status_code=201, summary="Create a case")
async def create_case(payload: CaseCreate):
    """
    Manually creates a new case and optionally triggers the pipeline
    via the CoordinatorAgent.

    TODO: Implement crud.create_case() + coordinator.trigger_pipeline().
    """
    raise NotImplementedError


@router.get("/{case_id}", response_model=CaseDetailResponse, summary="Get case detail")
async def get_case(case_id: str):
    """
    Returns the full detail for a single case, including pipeline state
    summary, hypotheses, engagement outcomes, and handoff records.

    TODO: Implement crud.get_case(case_id) with 404 handling.
    """
    raise NotImplementedError


@router.patch("/{case_id}", response_model=CaseResponse, summary="Update a case")
async def update_case(case_id: str, payload: CaseUpdate):
    """
    Updates mutable fields on a case (status, priority, notes, assignee).

    TODO: Implement crud.update_case(case_id, payload) with 404 handling.
    """
    raise NotImplementedError


@router.get("/{case_id}/timeline", summary="Get case event timeline")
async def get_case_timeline(case_id: str):
    """
    Returns an ordered list of pipeline events for a case:
    signal detected → hypothesis formed → policy verdict → engagement planned
    → call executed → outcome classified → [handoff created].

    TODO: Implement from pipeline_metadata + EngagementLog query.
    """
    raise NotImplementedError
