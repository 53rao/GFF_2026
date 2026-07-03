"""
graph_builder.py — LangGraph Pipeline Graph Definition
=======================================================
Defines and compiles the 9-node LangGraph StateGraph connecting:
Memory Read -> Sentinel -> Analyst -> Policy -> Strategy -> Caller -> Transcript -> Router / Memory Write.
"""

from __future__ import annotations

from langgraph.graph import StateGraph, END

from app.graph.state import PipelineState
from app.graph import edges
from app.agents.memory_agent import MemoryAgent
from app.agents.sentinel import SentinelAgent
from app.agents.analyst import AnalystAgent
from app.agents.policy_agent import PolicyAgent
from app.agents.engagement_strategy_agent import EngagementStrategyAgent
from app.agents.caller import CallerAgent
from app.agents.transcript_analyzer import TranscriptAnalyzerAgent
from app.agents.router import RouterAgent
from app.utils.logger import get_logger

logger = get_logger("sbi.graph")

# Node name constants
NODE_MEMORY_READ    = "memory_read"
NODE_SENTINEL       = "sentinel"
NODE_ANALYST        = "analyst"
NODE_POLICY         = "policy"
NODE_STRATEGY       = "engagement_strategy"
NODE_CALLER         = "caller"
NODE_TRANSCRIPT     = "transcript_analyzer"
NODE_ROUTER         = "router"
NODE_MEMORY_WRITE   = "memory_write"

# Agent Singletons
memory_agent = MemoryAgent()
sentinel_agent = SentinelAgent()
analyst_agent = AnalystAgent()
policy_agent = PolicyAgent()
strategy_agent = EngagementStrategyAgent()
caller_agent = CallerAgent()
transcript_agent = TranscriptAnalyzerAgent()
router_agent = RouterAgent()


def memory_read_node(state: PipelineState) -> PipelineState:
    cid = state.get("customer_id", "")
    mem = memory_agent.read_memory(cid)
    state["customer_memory"] = mem
    return state


def sentinel_node(state: PipelineState) -> PipelineState:
    cid = state.get("customer_id", "")
    signals = sentinel_agent.run(cid)
    state["detected_signals"] = signals
    if not signals:
        state["pipeline_halted"] = True
        state["halt_reason"] = "No anomaly signals detected by Sentinel."
    return state


def analyst_node(state: PipelineState) -> PipelineState:
    cid = state.get("customer_id", "")
    signals = state.get("detected_signals", [])
    hyps = analyst_agent.run(cid, signals)
    state["hypotheses"] = hyps
    return state


def policy_node(state: PipelineState) -> PipelineState:
    cid = state.get("customer_id", "")
    hyps = state.get("hypotheses", [])
    if not hyps:
        state["pipeline_halted"] = True
        state["halt_reason"] = "No hypotheses formulated by Analyst."
        return state

    top_hyp = hyps[0]
    verdict = policy_agent.run(cid, top_hyp)
    state["policy_verdicts"] = [verdict]
    if verdict.get("decision") == "deny":
        state["pipeline_halted"] = True
        state["halt_reason"] = f"Policy Denied: {verdict.get('reason')}"
    return state


def strategy_node(state: PipelineState) -> PipelineState:
    cid = state.get("customer_id", "")
    hyps = state.get("hypotheses", [])
    verdicts = state.get("policy_verdicts", [])
    if not hyps or not verdicts:
        return state

    plan = strategy_agent.run(cid, hyps[0], verdicts[0])
    state["engagement_plans"] = [plan]
    return state


def caller_node(state: PipelineState) -> PipelineState:
    cid = state.get("customer_id", "")
    hyps = state.get("hypotheses", [])
    plans = state.get("engagement_plans", [])
    if not hyps or not plans:
        return state

    # If branch escalation was chosen due to policy, simulate branch scheduling instead of direct call
    if plans[0].get("channel") == "branch_escalation":
        transcript = {
            "call_sid": f"BRANCH-ESC-{cid}",
            "customer_id": cid,
            "channel": "branch_escalation",
            "duration_seconds": 0,
            "status": "SCHEDULED",
            "transcript": "Branch RM escalation scheduled per regulatory policy requirement."
        }
    else:
        transcript = caller_agent.run(cid, hyps[0], plans[0])

    state["call_logs"] = [transcript]
    return state


def transcript_node(state: PipelineState) -> PipelineState:
    cid = state.get("customer_id", "")
    logs = state.get("call_logs", [])
    if not logs:
        return state

    outcome = transcript_agent.run(cid, logs[0])
    state["engagement_outcomes"] = [outcome]
    if outcome.get("follow_up_required") or outcome.get("outcome_type") in ["hot_lead", "retention_risk"]:
        state["human_handoff_required"] = True
    return state


def router_node(state: PipelineState) -> PipelineState:
    cid = state.get("customer_id", "")
    hyps = state.get("hypotheses", [])
    outcomes = state.get("engagement_outcomes", [])
    verdicts = state.get("policy_verdicts", [])
    if not hyps:
        return state

    outcome = outcomes[0] if outcomes else {"outcome_type": "not_interested"}
    verdict = verdicts[0] if verdicts else {"decision": "permit"}

    case_record = router_agent.run(cid, hyps[0], outcome, verdict)
    state["handoff_records"] = [case_record]
    return state


def memory_write_node(state: PipelineState) -> PipelineState:
    cid = state.get("customer_id", "")
    outcomes = state.get("engagement_outcomes", [])
    if outcomes:
        updated_mem = memory_agent.write_memory(cid, outcomes[0])
        state["customer_memory"] = updated_mem
    return state


def build_graph():
    """Constructs and compiles the 9-node LangGraph StateGraph."""
    graph = StateGraph(PipelineState)

    # Register nodes
    graph.add_node(NODE_MEMORY_READ, memory_read_node)
    graph.add_node(NODE_SENTINEL, sentinel_node)
    graph.add_node(NODE_ANALYST, analyst_node)
    graph.add_node(NODE_POLICY, policy_node)
    graph.add_node(NODE_STRATEGY, strategy_node)
    graph.add_node(NODE_CALLER, caller_node)
    graph.add_node(NODE_TRANSCRIPT, transcript_node)
    graph.add_node(NODE_ROUTER, router_node)
    graph.add_node(NODE_MEMORY_WRITE, memory_write_node)

    # Set entrypoint
    graph.set_entry_point(NODE_MEMORY_READ)

    # Linear and conditional edges
    graph.add_edge(NODE_MEMORY_READ, NODE_SENTINEL)

    graph.add_conditional_edges(
        NODE_SENTINEL,
        edges.route_after_sentinel,
        {"continue": NODE_ANALYST, "end": END}
    )

    graph.add_edge(NODE_ANALYST, NODE_POLICY)

    graph.add_conditional_edges(
        NODE_POLICY,
        edges.route_after_policy,
        {"continue": NODE_STRATEGY, "end": END}
    )

    graph.add_edge(NODE_STRATEGY, NODE_CALLER)
    graph.add_edge(NODE_CALLER, NODE_TRANSCRIPT)

    graph.add_conditional_edges(
        NODE_TRANSCRIPT,
        edges.route_after_transcript,
        {"router": NODE_ROUTER, "memory_write": NODE_MEMORY_WRITE}
    )

    graph.add_edge(NODE_ROUTER, NODE_MEMORY_WRITE)
    graph.add_edge(NODE_MEMORY_WRITE, END)

    compiled = graph.compile()
    logger.info("LangGraph multi-agent pipeline compiled successfully.")
    return compiled
