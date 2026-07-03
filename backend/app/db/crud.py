"""
crud.py — Basic CRUD Operations (Placeholder)
=============================================
Abstracts database read/write interactions for all domain entities.
Each function takes an async SQLAlchemy session and domain parameters.

FUTURE IMPLEMENTATION NOTES:
    - Implement async SELECT queries using `select(Model).where(...)`
    - Implement INSERT/UPDATE using standard SQLAlchemy session API
"""

from __future__ import annotations

from typing import Any, List, Optional
from app.api.schemas import CaseCreate, CaseUpdate, HandoffUpdateRequest


async def get_customer(session: Any, customer_id: str) -> Optional[Any]:
    """Retrieve customer by ID or CIF number."""
    raise NotImplementedError


async def create_case(session: Any, payload: CaseCreate) -> Any:
    """Create a new Case record and attach triggering signals."""
    raise NotImplementedError


async def get_case(session: Any, case_id: str) -> Optional[Any]:
    """Fetch Case along with relationships (signals, hypotheses)."""
    raise NotImplementedError


async def list_cases(session: Any, status: Optional[str] = None, limit: int = 20, offset: int = 0) -> List[Any]:
    """Retrieve paginated list of cases with optional status filtering."""
    raise NotImplementedError


async def update_case(session: Any, case_id: str, payload: CaseUpdate) -> Optional[Any]:
    """Update status, priority, or assignee on an existing Case."""
    raise NotImplementedError


async def create_handoff(session: Any, case_id: str, from_agent: str, target_team: str, reason: str) -> Any:
    """Create a Handoff record for human staff routing."""
    raise NotImplementedError


async def list_handoffs(session: Any, status: Optional[str] = None) -> List[Any]:
    """Retrieve pending or completed human handoffs."""
    raise NotImplementedError


async def update_handoff(session: Any, handoff_id: str, payload: HandoffUpdateRequest) -> Optional[Any]:
    """Update human handoff status (Accepted, Completed, Rejected)."""
    raise NotImplementedError


async def log_engagement(session: Any, customer_id: str, channel: str, outcome: str, summary: str) -> Any:
    """Persist an engagement interaction record to SQL audit log."""
    raise NotImplementedError
