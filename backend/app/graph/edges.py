"""
edges.py — LangGraph Conditional Edge Logic
============================================
Defines routing functions used as conditional edges in LangGraph StateGraph.
Evaluates current pipeline state and directs flow to appropriate node or END.
"""

from __future__ import annotations

from langgraph.graph import END
from app.graph.state import PipelineState


def route_after_sentinel(state: PipelineState) -> str:
    """
    After Sentinel:
    - If signals found -> route to analyst
    - If no signals -> route to END
    """
    signals = state.get("detected_signals", [])
    if signals:
        return "continue"
    return "end"


def route_after_policy(state: PipelineState) -> str:
    """
    After Policy:
    - If decision is 'permit' -> route to strategy
    - If decision is 'require_human_review' or 'deny' -> route to strategy (if review required, Strategy creates branch escalation; if deny, router/end)
    Let's check: if decision == 'deny', route to router or end.
    """
    verdicts = state.get("policy_verdicts", [])
    if not verdicts:
        return "end"

    top_verdict = verdicts[0]
    decision = top_verdict.get("decision", "permit")

    if decision == "permit" or decision == "require_human_review":
        return "continue"
    elif decision == "deny":
        return "end"
    return "end"


def route_after_transcript(state: PipelineState) -> str:
    """
    After Transcript Analyzer:
    - Always route to router first to create/update engagement case, or check human_handoff_required.
    Let's check graph topology: Caller -> Transcript -> Router / Memory Write.
    If human_handoff_required or any outcome -> route to router, then memory write.
    """
    outcomes = state.get("engagement_outcomes", [])
    if not outcomes:
        return "memory_write"

    outcome = outcomes[0]
    if outcome.get("follow_up_required") or outcome.get("outcome_type") in ["hot_lead", "retention_risk"]:
        return "router"
    return "memory_write"


def route_after_router(state: PipelineState) -> str:
    """Always routes to memory_write to persist outcome after routing."""
    return "memory_write"
