"""
engagement_strategy_agent.py — Channel, Timing & Objective Strategy Agent
==========================================================================
Determines the optimal outreach channel, timing, and communication objective
based on hypothesis confidence, policy constraints, and customer memory.
"""

from __future__ import annotations

from typing import Any, Dict
from app.agents.base_agent import BaseAgent
from app import data_store
from app.utils.logger import get_logger

logger = get_logger("sbi.strategy")


class EngagementStrategyAgent(BaseAgent):
    """
    Engagement Strategy Agent — selects optimal communication channel, timing, and objective.
    Forces branch_escalation if policy requires human review. Uses customer memory preferences.
    """

    name = "EngagementStrategyAgent"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)

    def run(self, customer_id: str, hypothesis: Dict[str, Any], policy_decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines channel, timing, and objective for the outreach campaign.
        """
        memory = data_store.get_customer_memory(customer_id) or {}
        p_decision = policy_decision.get("decision", "permit")

        # 1. Check Policy Override
        if p_decision == "require_human_review":
            strategy = {
                "channel": "branch_escalation",
                "timing": "Immediate during business hours",
                "objective": "retain" if hypothesis.get("category") == "retention_risk" else "educate",
                "reasoning": "Policy required human/RM review before direct outreach.",
                "script_guidelines": f"RM to review {hypothesis.get('recommended_action')} with customer in person or over personal call."
            }
            logger.info(f"[{customer_id}] Strategy set to branch_escalation due to policy review requirement.")
            return strategy

        # 2. Score and select channel based on memory & category
        preferred_channel = memory.get("preferred_channel", "call")
        category = hypothesis.get("category", "").lower()
        confidence = float(hypothesis.get("confidence", 0.7))

        if category == "retention_risk":
            channel = "call"
            objective = "retain"
            timing = "Within 2 hours"
        elif confidence >= 0.88 and preferred_channel in ["call", "whatsapp"]:
            channel = preferred_channel
            objective = "convert"
            timing = "Next business morning at 11:00 AM IST"
        else:
            channel = "whatsapp" if preferred_channel == "whatsapp" else "email"
            objective = "educate"
            timing = "Afternoon 3:00 PM IST"

        strategy = {
            "channel": channel,
            "timing": timing,
            "objective": objective,
            "reasoning": f"Selected {channel} based on customer memory preference ({preferred_channel}) and hypothesis confidence ({int(confidence*100)}%).",
            "script_guidelines": f"Emphasize value proposition of {hypothesis.get('recommended_action')} with non-pushy, consultative tone."
        }

        logger.info(f"[{customer_id}] Strategy formulated: {channel} ({objective}) at {timing}.")
        return strategy
