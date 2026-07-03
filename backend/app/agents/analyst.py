"""
analyst.py — Investigative Hypothesis Formulation Agent
=======================================================
Analyzes detected Sentinel anomaly signals using structured LLM inference
to formulate ranked, evidence-grounded proactive banking hypotheses.
"""

from __future__ import annotations

import json
import uuid
from typing import Any, List, Dict
from pydantic import ValidationError

from app.agents.base_agent import BaseAgent
from app.agents.llm_client import call_structured_llm
from app.agents.prompts import ANALYST_SYSTEM_PROMPT, AnalystOutputSchema
from app import data_store
from app.utils.logger import get_logger

logger = get_logger("sbi.analyst")


class AnalystAgent(BaseAgent):
    """
    Analyst Agent — formulates ranked engagement hypotheses from detected signals.
    Forces structured JSON output and validates via Pydantic schema before persistence.
    """

    name = "AnalystAgent"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)

    def run(self, customer_id: str, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generates 1-3 ranked hypotheses for a customer based on input signals.
        Persists validated hypotheses to hypotheses.json via data_store and returns them.
        """
        if not signals:
            logger.info(f"[{customer_id}] No signals provided to Analyst. Skipping hypothesis generation.")
            return []

        user_prompt = (
            f"Customer ID: {customer_id}\n"
            f"Detected Signals:\n{json.dumps(signals, indent=2)}\n\n"
            "Formulate 1 to 3 ranked hypotheses explaining these signals and recommending proactive SBI outreach."
        )

        # Attempt structured LLM call with 1 retry on malformed JSON or schema failure
        parsed_output = None
        for attempt in range(2):
            try:
                raw_dict = call_structured_llm(ANALYST_SYSTEM_PROMPT, user_prompt)
                parsed_output = AnalystOutputSchema.model_validate(raw_dict)
                break
            except (ValueError, ValidationError) as e:
                logger.warning(f"[{customer_id}] Analyst attempt {attempt + 1} failed validation: {e}")
                if attempt == 1:
                    raise RuntimeError(f"AnalystAgent failed after 2 attempts to produce valid schema: {e}") from e

        if not parsed_output:
            return []

        formatted_hypotheses = []
        for h in parsed_output.hypotheses:
            hyp_record = {
                "hypothesis_id": f"HYP-{customer_id}-{uuid.uuid4().hex[:6]}",
                "customer_id": customer_id,
                "signal_id": signals[0].get("signal_id", "UNKNOWN"),
                "category": h.category,
                "product_line": h.category.upper(),
                "recommended_action": h.recommended_action,
                "confidence": h.confidence,
                "rationale": h.rationale,
                "supporting_evidence": h.supporting_evidence,
                "disconfirming_evidence": h.disconfirming_evidence,
                "status": "Formulated"
            }
            data_store.save_hypothesis(hyp_record)
            formatted_hypotheses.append(hyp_record)

        logger.info(f"[{customer_id}] Analyst generated {len(formatted_hypotheses)} verified hypotheses.")
        return formatted_hypotheses
