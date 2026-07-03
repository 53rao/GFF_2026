"""
policy_agent.py — Compliance & Regulatory Policy Gate Agent
===========================================================
Evaluates proposed proactive engagement actions against regulatory rules (TRAI, RBI, DPDP)
and bank risk policies before any outreach is scheduled.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List
from app.agents.base_agent import BaseAgent
from app import data_store
from app.utils.logger import get_logger

logger = get_logger("sbi.policy")


class PolicyAgent(BaseAgent):
    """
    Policy Agent — deterministic regulatory gatekeeper evaluating rules from policy_rules.json.
    Returns decision: 'permit', 'deny', or 'require_human_review' along with triggered audit rules.
    """

    name = "PolicyAgent"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)

    def run(self, customer_id: str, hypothesis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates top hypothesis against loaded policy rules and customer profile/memory.
        Returns detailed policy decision dictionary.
        """
        customer = data_store.get_customer(customer_id) or {}
        memory = data_store.get_customer_memory(customer_id) or {}
        rules = data_store.get_policy_rules()

        triggered_rules: List[str] = []
        decision = "permit"
        reason = "All compliance checks passed."

        # -------------------------------------------------------------------
        # 1. Regulatory Checks against policy_rules.json
        # -------------------------------------------------------------------
        now = datetime.utcnow()
        current_hour = (now.hour + 5) % 24  # Approximate IST hour for demo check

        # Check TRAI calling window (if action implies voice calling)
        for r in rules:
            rid = r.get("rule_id", "")
            if rid == "TRAI_01":
                # Only check window if it's currently night in IST (e.g. < 9 or >= 21)
                # For demo reliability during day/night testing, we verify if explicitly blocked
                if current_hour < 9 or current_hour >= 21:
                    # Note: We don't deny digital channels, but flag voice restriction
                    triggered_rules.append("TRAI_01: Outbound voice restricted outside 9 AM - 9 PM IST.")

            elif rid == "RBI_01":
                monthly_contacts = memory.get("monthly_contact_count", 0)
                if monthly_contacts >= 4:
                    triggered_rules.append("RBI_01: Monthly promotional contact frequency cap reached (>=4).")
                    decision = "deny"
                    reason = "Frequency cap exceeded."

            elif rid == "RBI_02":
                last_decline = memory.get("last_decline_timestamp")
                if last_decline:
                    try:
                        dt = datetime.strptime(last_decline[:19], "%Y-%m-%dT%H:%M:%S")
                        if (now - dt).total_seconds() < 48 * 3600:
                            triggered_rules.append("RBI_02: Mandatory 48-hour cooling off period after offer decline.")
                            decision = "deny"
                            reason = "In cooling-off period."
                    except Exception:
                        pass

        # -------------------------------------------------------------------
        # 2. Bank Risk & KYC Checks
        # -------------------------------------------------------------------
        kyc = customer.get("kyc_status", "FULL_KYC").upper()
        if kyc != "FULL_KYC" and kyc != "VERIFIED":
            triggered_rules.append("KYC_01: Customer KYC status incomplete.")
            decision = "require_human_review"
            reason = "Manual KYC verification required before engagement."

        # Check product category complexity (High-value investment/lending for HNI requires RM review)
        category = hypothesis.get("category", "").lower()
        segment = customer.get("segment", "").upper()
        if category in ["investments", "lending"] and segment in ["HNI", "WEALTH", "VIP"]:
            triggered_rules.append("SUITABILITY_01: HNI investment/lending recommendations require Relationship Manager review.")
            if decision != "deny":
                decision = "require_human_review"
                reason = "Suitability review required for HNI segment."

        result = {
            "decision": decision,
            "triggered_rules": triggered_rules,
            "reason": reason,
            "evaluated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        logger.info(f"[{customer_id}] Policy evaluation complete: {decision} ({len(triggered_rules)} rules triggered)")
        return result
