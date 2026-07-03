"""
router.py — Case Disposition & Queue Routing Agent
==================================================
Maps classified engagement outcomes and product lines to specific bank operational queues.
Persists final case status into engagement_cases in data_store.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict
from app.agents.base_agent import BaseAgent
from app import data_store
from app.utils.logger import get_logger

logger = get_logger("sbi.router")


class RouterAgent(BaseAgent):
    """
    Router Agent — routes cases to human relationship managers or automated nurture loops.
    Updates or creates case record in cases.json.
    """

    name = "RouterAgent"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)

    def run(
        self,
        customer_id: str,
        hypothesis: Dict[str, Any],
        outcome: Dict[str, Any],
        policy_decision: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Determines target operational queue and creates/updates final engagement case.
        """
        outcome_type = outcome.get("outcome_type", "").lower()
        category = hypothesis.get("category", "").lower()
        p_decision = policy_decision.get("decision", "permit")

        customer = data_store.get_customer(customer_id) or {}
        cname = customer.get("full_name", customer_id)

        # Map to specific bank queues
        if p_decision == "require_human_review":
            target_queue = "Compliance & Suitability Review Queue"
            status = "Escalated"
            priority = "High"
        elif outcome_type == "retention_risk":
            target_queue = "Retention Team Queue"
            status = "Escalated"
            priority = "Critical"
        elif outcome_type == "hot_lead":
            if category == "investments":
                target_queue = "Investment RM Queue"
            elif category == "lending":
                target_queue = "Retail Asset Specialist Queue"
            elif category == "insurance":
                target_queue = "Bancassurance RM Queue"
            else:
                target_queue = "General Sales RM Queue"
            status = "Assigned"
            priority = "High"
        elif outcome_type == "follow_up_needed":
            target_queue = "Customer Care Callback Queue"
            status = "In Progress"
            priority = "Medium"
        else:  # not_interested or default
            target_queue = "Automated Nurture Loop"
            status = "Resolved"
            priority = "Low"

        case_id = f"CASE-{customer_id}-{uuid.uuid4().hex[:6].upper()}"

        case_record = {
            "id": case_id,
            "case_id": case_id,
            "customer_id": customer_id,
            "customerName": cname,
            "type": hypothesis.get("recommended_action", category.title()),
            "priority": priority,
            "status": status,
            "assigned_queue": target_queue,
            "sla": "2h" if priority in ["Critical", "High"] else "24h",
            "slaBreached": False,
            "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        data_store.save_engagement_case(case_record)
        logger.info(f"[{customer_id}] Routed to {target_queue} (Case: {case_id}, Status: {status})")
        return case_record
