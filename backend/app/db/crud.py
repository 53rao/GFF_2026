"""
crud.py — Basic CRUD Operations using SQLAlchemy Async API
==========================================================
Abstracts database read/write interactions for all domain entities.
Each function takes an async SQLAlchemy session and returns ORM model instances.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, List, Optional
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.api.schemas import CaseCreate, CaseUpdate, HandoffUpdateRequest
from app.db.models import Customer, Case, SignalRecord, Handoff, EngagementLog


async def get_customer(session: Any, customer_id: str) -> Optional[Customer]:
    """Retrieve customer by ID or CIF number."""
    stmt = select(Customer).where(
        (Customer.id == customer_id) | (Customer.cif_number == customer_id)
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_case(session: Any, payload: CaseCreate) -> Case:
    """Create a new Case record and attach triggering signals if trigger_event is provided."""
    case_id = f"CASE-MAN-{uuid.uuid4().hex[:6].upper()}"
    new_case = Case(
        id=case_id,
        customer_id=payload.customer_id,
        status="Open",
        priority=payload.priority,
        type=payload.case_type,
        assigned_agent=payload.assigned_agent or "Manual Agent",
        sla="2h" if payload.priority in ["Critical", "High"] else "24h",
        slaBreached=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(new_case)
    
    if payload.trigger_event:
        signal_id = f"SIG-{uuid.uuid4().hex[:6].upper()}"
        new_signal = SignalRecord(
            id=signal_id,
            case_id=case_id,
            signal_type=payload.trigger_event.get("signal_type", payload.case_type),
            confidence=payload.trigger_event.get("confidence", 1.0),
            raw_evidence=payload.trigger_event.get("raw_evidence", {}),
            detected_at=datetime.utcnow()
        )
        session.add(new_signal)
        
    await session.flush()
    return new_case


async def get_case(session: Any, case_id: str) -> Optional[Case]:
    """Fetch Case along with relationships (signals, hypotheses)."""
    stmt = (
        select(Case)
        .where(Case.id == case_id)
        .options(selectinload(Case.signals), selectinload(Case.hypotheses), selectinload(Case.customer))
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def list_cases(
    session: Any, 
    status: Optional[str] = None, 
    limit: int = 20, 
    offset: int = 0
) -> List[Case]:
    """Retrieve paginated list of cases with optional status filtering."""
    stmt = select(Case).options(selectinload(Case.customer))
    if status:
        stmt = stmt.where(Case.status == status)
    stmt = stmt.order_by(Case.created_at.desc()).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def update_case(session: Any, case_id: str, payload: CaseUpdate) -> Optional[Case]:
    """Update status, priority, or assignee on an existing Case."""
    case = await get_case(session, case_id)
    if not case:
        return None
        
    if payload.status is not None:
        case.status = payload.status
    if payload.priority is not None:
        case.priority = payload.priority
    if payload.assigned_agent is not None:
        case.assigned_agent = payload.assigned_agent
    
    case.updated_at = datetime.utcnow()
    await session.flush()
    return case


async def create_handoff(
    session: Any, 
    case_id: str, 
    from_agent: str, 
    target_team: str, 
    reason: str
) -> Handoff:
    """Create a Handoff record for human staff routing."""
    handoff_id = f"HO-{uuid.uuid4().hex[:6].upper()}"
    new_handoff = Handoff(
        id=handoff_id,
        case_id=case_id,
        from_agent=from_agent,
        to_team=target_team,
        status="Pending",
        reason=reason,
        created_at=datetime.utcnow()
    )
    session.add(new_handoff)
    await session.flush()
    return new_handoff


async def list_handoffs(session: Any, status: Optional[str] = None) -> List[Handoff]:
    """Retrieve pending or completed human handoffs."""
    stmt = select(Handoff)
    if status:
        stmt = stmt.where(Handoff.status == status)
    stmt = stmt.order_by(Handoff.created_at.desc())
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def update_handoff(
    session: Any, 
    handoff_id: str, 
    payload: HandoffUpdateRequest
) -> Optional[Handoff]:
    """Update human handoff status (Accepted, Completed, Rejected)."""
    stmt = select(Handoff).where(Handoff.id == handoff_id)
    result = await session.execute(stmt)
    handoff = result.scalars().first()
    if not handoff:
        return None
        
    handoff.status = payload.status
    if payload.notes is not None:
        handoff.notes = payload.notes
        
    await session.flush()
    return handoff


async def log_engagement(
    session: Any, 
    customer_id: str, 
    channel: str, 
    outcome: str, 
    summary: str
) -> EngagementLog:
    """Persist an engagement interaction record to SQL audit log."""
    log_id = f"EL-{uuid.uuid4().hex[:6].upper()}"
    new_log = EngagementLog(
        id=log_id,
        customer_id=customer_id,
        channel=channel,
        outcome_type=outcome,
        summary=summary,
        created_at=datetime.utcnow()
    )
    session.add(new_log)
    await session.flush()
    return new_log
