"""
routes_pipeline.py — Pipeline Execution Endpoints
=================================================
Endpoints to execute individual multi-agent steps or full LangGraph pipeline runs.
Runs real LangGraph detection, analysis, policy, strategy, voice simulation, and routing.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app import data_store
from app.agents.sentinel import SentinelAgent
from app.agents.analyst import AnalystAgent
from app.agents.policy_agent import PolicyAgent
from app.agents.engagement_strategy_agent import EngagementStrategyAgent
from app.agents.caller import CallerAgent
from app.agents.transcript_analyzer import TranscriptAnalyzerAgent
from app.agents.router import RouterAgent
from app.agents.coordinator import CoordinatorAgent

router = APIRouter()
sentinel_agent = SentinelAgent()
analyst_agent = AnalystAgent()
policy_agent = PolicyAgent()
strategy_agent = EngagementStrategyAgent()
caller_agent = CallerAgent()
transcript_agent = TranscriptAnalyzerAgent()
router_agent = RouterAgent()
coordinator_agent = CoordinatorAgent()


@router.post("/run-full/{customer_id}", summary="Run full compiled LangGraph pipeline")
async def run_full_pipeline_endpoint(customer_id: str) -> Dict[str, Any]:
    """
    Executes the complete 9-node LangGraph pipeline for a customer:
    Memory Read -> Sentinel -> Analyst -> Policy Gate -> Strategy -> Caller -> Transcript -> Router -> Memory Write.
    Returns full trace showing every node's output.
    """
    customer = data_store.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found in data store")

    trace = coordinator_agent.run_pipeline(customer_id)
    return trace


@router.post("/run-sentinel/{customer_id}", summary="Run Sentinel detection on customer")
async def run_sentinel_endpoint(customer_id: str) -> List[Dict[str, Any]]:
    customer = data_store.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found in data store")
    return sentinel_agent.run(customer_id)


@router.post("/run-analyst/{customer_id}", summary="Run Analyst hypothesis formulation")
async def run_analyst_endpoint(customer_id: str) -> List[Dict[str, Any]]:
    customer = data_store.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    signals = data_store.get_signals(customer_id)
    if not signals:
        signals = sentinel_agent.run(customer_id)
    return analyst_agent.run(customer_id, signals)


@router.post("/run-policy/{customer_id}", summary="Run Policy evaluation")
async def run_policy_endpoint(customer_id: str) -> Dict[str, Any]:
    hyps = data_store.get_hypotheses(customer_id)
    if not hyps:
        raise HTTPException(status_code=400, detail="No hypotheses found. Run analyst first.")
    return policy_agent.run(customer_id, hyps[0])


@router.post("/run-strategy/{customer_id}", summary="Run Engagement Strategy scheduling")
async def run_strategy_endpoint(customer_id: str) -> Dict[str, Any]:
    hyps = data_store.get_hypotheses(customer_id)
    if not hyps:
        raise HTTPException(status_code=400, detail="No hypotheses found.")
    verdict = policy_agent.run(customer_id, hyps[0])
    return strategy_agent.run(customer_id, hyps[0], verdict)


@router.post("/run-caller/{customer_id}", summary="Run Caller outbound voice execution")
async def run_caller_endpoint(customer_id: str) -> Dict[str, Any]:
    hyps = data_store.get_hypotheses(customer_id)
    if not hyps:
        raise HTTPException(status_code=400, detail="No hypotheses found.")
    verdict = policy_agent.run(customer_id, hyps[0])
    plan = strategy_agent.run(customer_id, hyps[0], verdict)
    return caller_agent.run(customer_id, hyps[0], plan)
