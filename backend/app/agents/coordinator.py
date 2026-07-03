"""
coordinator.py — Pipeline Orchestrator & LangGraph Execution Engine
=====================================================================
Orchestrates the multi-agent banking pipeline using the compiled LangGraph StateGraph.
Handles initialization, execution tracing, and error recovery to manual_review state.
"""

from __future__ import annotations

import traceback
from datetime import datetime
from typing import Any, Dict
from app.agents.base_agent import BaseAgent
from app.graph.state import PipelineState
from app.graph.graph_builder import build_graph
from app import data_store
from app.utils.logger import get_logger

logger = get_logger("sbi.coordinator")


class CoordinatorAgent(BaseAgent):
    """
    Coordinator Agent — drives full pipeline execution via LangGraph.
    Catches node exceptions and routes failed runs to 'manual_review' terminal state.
    """

    name = "CoordinatorAgent"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)
        self.graph = build_graph()

    def run(self, customer_id: str) -> Dict[str, Any]:
        return self.run_pipeline(customer_id)

    def run_pipeline(self, customer_id: str) -> Dict[str, Any]:
        """
        Initializes state and runs the full compiled LangGraph pipeline for customer_id.
        Returns the complete trace showing every node's output.
        """
        logger.info(f"[{customer_id}] Initiating full LangGraph pipeline run...")

        # Build initial state
        initial_state: PipelineState = {
            "customer_id": customer_id,
            "pipeline_run_id": f"RUN-{customer_id}-{int(datetime.utcnow().timestamp())}",
            "start_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "RUNNING",
            "customer_profile": data_store.get_customer(customer_id) or {},
            "customer_memory": {},
            "transaction_history": data_store.get_transactions(customer_id),
            "app_clickstream": data_store.get_behavior_events(customer_id),
            "detected_signals": [],
            "hypotheses": [],
            "policy_verdicts": [],
            "engagement_plans": [],
            "call_logs": [],
            "engagement_outcomes": [],
            "handoff_records": [],
            "pipeline_halted": False,
            "halt_reason": None,
            "human_handoff_required": False,
            "error_log": []
        }

        try:
            final_state = self.graph.invoke(initial_state)
            
            if final_state.get("pipeline_halted"):
                final_state["status"] = f"HALTED: {final_state.get('halt_reason')}"
            elif final_state.get("human_handoff_required"):
                final_state["status"] = "COMPLETED_WITH_HANDOFF"
            else:
                final_state["status"] = "COMPLETED"

            logger.info(f"[{customer_id}] Pipeline execution finished with status: {final_state['status']}")
            return dict(final_state)

        except Exception as e:
            logger.error(f"[{customer_id}] Pipeline exception encountered: {e}\n{traceback.format_exc()}")
            # Route to manual_review terminal state
            initial_state["status"] = "ERROR_MANUAL_REVIEW"
            initial_state["pipeline_halted"] = True
            initial_state["halt_reason"] = f"Runtime exception in graph node: {str(e)}"
            initial_state["error_log"] = [str(e), traceback.format_exc()]

            # Save emergency case for human review
            emergency_case = {
                "id": f"CASE-{customer_id}-ERR",
                "case_id": f"CASE-{customer_id}-ERR",
                "customer_id": customer_id,
                "customerName": initial_state["customer_profile"].get("full_name", customer_id),
                "type": "System Execution Exception",
                "priority": "Critical",
                "status": "Escalated",
                "assigned_queue": "Manual IT & Operations Review Queue",
                "sla": "1h",
                "slaBreached": False,
                "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            data_store.save_engagement_case(emergency_case)
            return dict(initial_state)
