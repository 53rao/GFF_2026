"""
models.py — SQLAlchemy ORM Models
===================================
Defines database tables representing entities across the SBI banking pipeline:
customers, cases, detected signals, generated hypotheses, policy audit logs,
engagement records, and human handoffs.

FUTURE IMPLEMENTATION NOTES:
    - Use async SQLAlchemy (`Mapped`, `mapped_column`, `DeclarativeBase`)
    - All primary keys use UUID strings or UUID native database types
    - Implement proper foreign key constraints and relationships
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass


class Customer(Base):
    """Stores customer 360 profile summary and banking segment data."""
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    cif_number: Mapped[str] = mapped_column(String, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    mobile: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    segment: Mapped[str] = mapped_column(String, default="RETAIL")
    kyc_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cases: Mapped[List["Case"]] = relationship(back_populates="customer")


class Case(Base):
    """Represents a proactive pipeline workflow execution for a specific customer."""
    __tablename__ = "cases"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), index=True)
    status: Mapped[str] = mapped_column(String, default="Open", index=True)
    priority: Mapped[str] = mapped_column(String, default="Medium")
    assigned_agent: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer: Mapped["Customer"] = relationship(back_populates="cases")
    signals: Mapped[List["SignalRecord"]] = relationship(back_populates="case")
    hypotheses: Mapped[List["HypothesisRecord"]] = relationship(back_populates="case")


class SignalRecord(Base):
    """Stores Sentinel detection events that initiated or influenced a Case."""
    __tablename__ = "signals"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"), index=True)
    signal_type: Mapped[str] = mapped_column(String, index=True)
    confidence: Mapped[float] = mapped_column(Float)
    raw_evidence: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    case: Mapped["Case"] = relationship(back_populates="signals")


class HypothesisRecord(Base):
    """Stores Analyst agent recommendations and product line mappings."""
    __tablename__ = "hypotheses"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"), index=True)
    product_line: Mapped[str] = mapped_column(String, index=True)
    recommended_action: Mapped[str] = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float)
    rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    case: Mapped["Case"] = relationship(back_populates="hypotheses")


class EngagementLog(Base):
    """Logs all outbound communications (calls, SMS, emails) and their outcomes."""
    __tablename__ = "engagement_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), index=True)
    case_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    channel: Mapped[str] = mapped_column(String)
    outcome_type: Mapped[str] = mapped_column(String, index=True)
    transcript: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PolicyAuditLog(Base):
    """Audit trail of regulatory and internal compliance checks performed by PolicyAgent."""
    __tablename__ = "policy_audit_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    case_id: Mapped[str] = mapped_column(String, index=True)
    hypothesis_id: Mapped[str] = mapped_column(String)
    approved: Mapped[bool] = mapped_column(Boolean)
    blocking_rules: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    audit_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Handoff(Base):
    """Tracks cases handed off to human branch staff or specialized banking teams."""
    __tablename__ = "handoffs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    case_id: Mapped[str] = mapped_column(String, index=True)
    from_agent: Mapped[str] = mapped_column(String)
    to_team: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[str] = mapped_column(String, default="Pending", index=True)
    reason: Mapped[str] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
