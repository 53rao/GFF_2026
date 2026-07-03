"""
memory_agent.py — Persistent Longitudinal Customer Memory Agent
================================================================
Reads and writes per-customer engagement context and history via data_store.py.
Ensures the system "gets smarter over time" by recording engagement outcomes,
channel responses, and updating contact frequency counters across pipeline runs.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
from app.agents.base_agent import BaseAgent
from app import data_store
from app.utils.logger import get_logger

logger = get_logger("sbi.memory")


class MemoryAgent(BaseAgent):
    """
    Memory Agent — manages persistent longitudinal context per customer.
    Exposes read_memory(customer_id) and write_memory(customer_id, outcome).
    """

    name = "MemoryAgent"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)

    def run(self, customer_id: str) -> Dict[str, Any]:
        return self.read_memory(customer_id)

    def read_memory(self, customer_id: str) -> Dict[str, Any]:
        """
        Called at pipeline start. Returns existing customer memory or sensible defaults.
        """
        memory = data_store.get_customer_memory(customer_id)
        if not memory:
            memory = {
                "customer_id": customer_id,
                "preferred_channel": "call",
                "monthly_contact_count": 0,
                "interaction_history": [],
                "last_interaction_timestamp": None,
                "last_decline_timestamp": None,
                "customer_consents": ["investments", "lending", "insurance", "payments", "mobile_banking"]
            }
            logger.info(f"[{customer_id}] Initialized default memory for customer.")
        else:
            logger.info(f"[{customer_id}] Loaded persistent memory (contacts this month: {memory.get('monthly_contact_count', 0)})")
        return memory

    def write_memory(self, customer_id: str, outcome: Dict[str, Any]) -> Dict[str, Any]:
        """
        Called at pipeline end. Updates customer_memory.json with this engagement's outcome
        so future pipeline runs adapt dynamically.
        """
        memory = self.read_memory(customer_id)
        now_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Increment contact counter
        count = memory.get("monthly_contact_count", 0) + 1
        memory["monthly_contact_count"] = count
        memory["last_interaction_timestamp"] = now_str

        outcome_type = outcome.get("outcome_type", "").lower()
        if outcome_type in ["not_interested", "retention_risk"]:
            memory["last_decline_timestamp"] = now_str

        # Adapt preferred channel if customer responded positively
        channel_used = outcome.get("channel", "call")
        if outcome_type == "hot_lead":
            memory["preferred_channel"] = channel_used

        # Append summary to interaction history
        history = memory.get("interaction_history", [])
        history.append({
            "timestamp": now_str,
            "outcome_type": outcome_type,
            "confidence": outcome.get("confidence", 0.0),
            "reasoning": outcome.get("reasoning", "")
        })
        memory["interaction_history"] = history[-10:]  # Keep last 10 interactions

        updated = data_store.update_customer_memory(customer_id, memory)
        logger.info(f"[{customer_id}] Updated persistent memory with outcome '{outcome_type}'. Total contacts: {count}.")
        return updated
