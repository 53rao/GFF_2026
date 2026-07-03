"""
state.py — LangGraph Shared Pipeline State Schema
==================================================
Defines the TypedDict (and optional Pydantic model) that represents the
shared state flowing through the LangGraph pipeline graph.

Every agent node reads from and writes to this state object.
LangGraph merges state updates from each node automatically.

DESIGN NOTES:
    - All fields are optional (default None or []) to allow partial updates
    - Immutable fields (pipeline_id, customer_id, trigger_event) are set
      once at pipeline start by the Coordinator
    - Mutable list fields (detected_signals, hypotheses, etc.) are
      accumulated as the pipeline progresses
    - The state is serialisable to JSON for persistence and debugging
    - See each field's comment for which agent reads/writes it
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from typing_extensions import TypedDict


class Signal(TypedDict, total=False):
    """Represents a single detected signal from the Sentinel Agent."""
    signal_id: str
    signal_type: str              # e.g., "SPENDING_SPIKE", "LARGE_INFLOW"
    customer_id: str
    confidence: float             # 0.0 – 1.0
    urgency: int                  # 1–5 (5 = most urgent)
    raw_evidence: dict            # raw data that triggered the signal
    detected_at: str              # ISO 8601 timestamp


class Hypothesis(TypedDict, total=False):
    """Represents a single investigative hypothesis from the Analyst Agent."""
    hypothesis_id: str
    signal_id: str                # parent signal
    product_line: str             # PAYMENTS | INVESTMENTS | INSURANCE | LENDING | MOBILE_BANKING | FRAUD
    recommended_action: str       # e.g., "OFFER_FD_REINVESTMENT"
    confidence: float             # 0.0 – 1.0
    urgency: int                  # 1–5
    rationale: str                # LLM-generated explanation
    supporting_evidence: list     # list of evidence items


class PolicyVerdict(TypedDict, total=False):
    """Represents a policy ruling from the Policy Agent."""
    hypothesis_id: str
    approved: bool
    blocking_rules: list[str]     # list of rule IDs that blocked approval
    constraints: dict             # e.g., {"channel": "email_only", "time_window": "..."}
    audit_note: str


class EngagementPlan(TypedDict, total=False):
    """Represents the engagement plan from the Engagement Strategy Agent."""
    plan_id: str
    hypothesis_id: str
    channel: str                  # voice | sms | email | push | whatsapp
    scheduled_at: str             # ISO 8601 datetime
    objective: str
    engagement_brief: str
    script_template_key: str
    fallback_channel: str
    priority: int
    max_attempts: int


class CallLog(TypedDict, total=False):
    """Represents a call execution record from the Caller Agent."""
    call_sid: str
    plan_id: str
    customer_phone: str
    started_at: str
    ended_at: str
    duration_seconds: int
    transcript: str
    raw_outcome: str              # e.g., "ANSWERED", "NO_ANSWER", "VOICEMAIL"


class EngagementOutcome(TypedDict, total=False):
    """Represents the analyzed outcome from the Transcript Analyzer Agent."""
    call_sid: str
    outcome_type: str             # see OUTCOME_TYPES in transcript_analyzer.py
    customer_sentiment: str       # positive | neutral | negative
    intent_signals: list[str]
    commitments: list[str]
    follow_up_required: bool
    follow_up_type: Optional[str]
    human_handoff_required: bool
    handoff_team: Optional[str]
    summary: str


class HandoffRecord(TypedDict, total=False):
    """Represents a completed human handoff from the Router Agent."""
    handoff_id: str
    target_team: str
    priority: str
    created_at: str
    package: dict


class PipelineMetadata(TypedDict, total=False):
    """Pipeline-level metadata tracked by the Coordinator."""
    pipeline_id: str
    started_at: str
    completed_at: Optional[str]
    total_duration_ms: Optional[int]
    steps_completed: list[str]
    error: Optional[str]
    retry_count: int
    case_id: Optional[str]        # DB case record created at end


class PipelineState(TypedDict, total=False):
    """
    The complete shared state for the SBI multi-agent engagement pipeline.

    This is the single object passed between all LangGraph nodes.
    Each agent reads the fields it needs and writes to its output fields.

    Field ownership:
        pipeline_metadata   → Coordinator (init + update throughout)
        customer_id         → Coordinator (init)
        trigger_event       → Coordinator (init, from external event)
        customer_memory     → MemoryAgent (read phase)
        detected_signals    → SentinelAgent (write)
        hypotheses          → AnalystAgent (write)
        policy_verdicts     → PolicyAgent (write)
        engagement_plans    → EngagementStrategyAgent (write)
        call_logs           → CallerAgent (write)
        engagement_outcomes → TranscriptAnalyzerAgent (write)
        handoff_records     → RouterAgent (write)
    """

    # ── Immutable (set at pipeline start) ────────────────────────────────────
    pipeline_id: str
    customer_id: str
    trigger_event: dict           # raw event that started this pipeline run

    # ── Memory (populated by MemoryAgent read phase) ──────────────────────────
    customer_memory: dict         # customer profile + engagement history

    # ── Agent outputs (accumulated as pipeline progresses) ────────────────────
    detected_signals:    list[Signal]
    hypotheses:          list[Hypothesis]
    policy_verdicts:     list[PolicyVerdict]
    engagement_plans:    list[EngagementPlan]
    call_logs:           list[CallLog]
    engagement_outcomes: list[EngagementOutcome]
    handoff_records:     list[HandoffRecord]

    # ── Control flow flags (set by Coordinator / gate checks) ────────────────
    pipeline_halted:     bool     # True if PolicyAgent blocked all hypotheses
    halt_reason:         Optional[str] # Reason for early halt
    human_handoff_required: bool  # True if Router should be invoked

    # ── Pipeline data & metadata ─────────────────────────────────────────────
    status:              str
    customer_profile:    dict
    transaction_history: list
    app_clickstream:     list
    error_log:           list
    pipeline_metadata:   PipelineMetadata
