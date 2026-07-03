"""
schemas.py — Pydantic Request / Response Models
================================================
Defines all Pydantic models used for API request validation and
response serialisation across all route modules.

Organised by domain:
    - Case schemas
    - Agent schemas
    - Admin / dashboard schemas
    - User-facing schemas
    - Webhook schemas
    - Shared/common schemas

NOTES:
    - All timestamps are ISO 8601 strings (UTC) for API layer
    - IDs are strings (UUIDs) throughout
    - Use Optional[X] for nullable fields
    - Response models use orm_mode = True (or model_config with from_attributes)
      to support direct SQLAlchemy model serialisation
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Common
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: str
    version: str


class PaginatedResponse(BaseModel):
    """Generic wrapper for paginated list responses."""
    total: int
    page: int
    page_size: int
    items: List[Any]


# ---------------------------------------------------------------------------
# Case Schemas
# ---------------------------------------------------------------------------

class CaseBase(BaseModel):
    customer_id: str
    case_type: str
    priority: str = "Medium"
    assigned_agent: Optional[str] = None


class CaseCreate(CaseBase):
    trigger_event: Optional[dict] = None


class CaseUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_agent: Optional[str] = None
    notes: Optional[str] = None


class CaseResponse(CaseBase):
    id: str
    status: str
    created_at: str
    updated_at: str
    sla_deadline: Optional[str] = None
    sla_breached: bool = False

    model_config = {"from_attributes": True}


class CaseDetailResponse(CaseResponse):
    """Extended case response including pipeline state and engagement history."""
    pipeline_id: Optional[str] = None
    hypotheses: List[dict] = []
    engagement_outcomes: List[dict] = []
    handoff_records: List[dict] = []


# ---------------------------------------------------------------------------
# Agent Schemas
# ---------------------------------------------------------------------------

class AgentRunRequest(BaseModel):
    """Request body to manually trigger an agent run."""
    customer_id: str
    trigger_event: dict
    agent_name: Optional[str] = None  # if None, runs full pipeline


class AgentRunResponse(BaseModel):
    run_id: str
    pipeline_id: str
    status: str
    started_at: str
    agent_name: Optional[str] = None


class AgentStatusResponse(BaseModel):
    agent_id: str
    name: str
    agent_type: str
    status: str                       # active | idle | offline
    cases_active: int
    cases_resolved: int
    success_rate: float
    avg_response_ms: int
    utilization: int                  # 0–100
    last_ping: str


# ---------------------------------------------------------------------------
# Admin Dashboard Schemas
# ---------------------------------------------------------------------------

class DashboardKPIResponse(BaseModel):
    open_cases: int
    cases_resolved_today: int
    agents_active: int
    sla_breach_rate: float
    pending_handoffs: int
    avg_resolution_hours: float


class HandoffResponse(BaseModel):
    id: str
    from_agent: str
    to_agent: str
    customer_id: str
    customer_name: str
    reason: str
    status: str
    created_at: str
    resolved_at: Optional[str] = None
    notes: Optional[str] = None
    priority: str = "Medium"

    model_config = {"from_attributes": True}


class HandoffUpdateRequest(BaseModel):
    status: str                       # Accepted | Rejected | Completed
    notes: Optional[str] = None


# ---------------------------------------------------------------------------
# User-Facing Schemas
# ---------------------------------------------------------------------------

class NotificationResponse(BaseModel):
    id: str
    title: str
    body: str
    notification_type: str
    priority: str
    read: bool
    created_at: str

    model_config = {"from_attributes": True}


class EngagementHistoryResponse(BaseModel):
    id: str
    engagement_type: str
    channel: str
    outcome_type: str
    summary: str
    created_at: str

    model_config = {"from_attributes": True}


class UserProfileResponse(BaseModel):
    customer_id: str
    name: str
    email: Optional[str] = None
    mobile: Optional[str] = None
    kyc_status: str
    relationship_type: str
    member_since: str


# ---------------------------------------------------------------------------
# Webhook Schemas (Twilio)
# ---------------------------------------------------------------------------

class TwilioCallStatusCallback(BaseModel):
    """Twilio's call status webhook payload (snake_case mapping of Twilio fields)."""
    CallSid: str
    CallStatus: str                   # initiated | ringing | in-progress | completed | failed
    CallDuration: Optional[str] = None
    To: Optional[str] = None
    From: Optional[str] = None
    AccountSid: Optional[str] = None


class TwilioTranscriptionCallback(BaseModel):
    """Twilio's transcription complete webhook payload."""
    TranscriptionSid: str
    TranscriptionText: Optional[str] = None
    TranscriptionStatus: str
    CallSid: Optional[str] = None
    RecordingSid: Optional[str] = None
