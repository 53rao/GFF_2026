"""
caller.py — Outbound Multi-Channel Execution Agent (Simulated Voice Dialogue)
==============================================================================
Simulates realistic engagement dialogues between the AI Voice Agent and customer
grounded in the hypothesis and strategy. Persists transcript to call_transcripts.json.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict
from pydantic import ValidationError

from app.agents.base_agent import BaseAgent
from app.agents.llm_client import call_structured_llm
from app.agents.prompts import CALLER_SYSTEM_PROMPT, CallerOutputSchema
from app import data_store
from app.utils.logger import get_logger

logger = get_logger("sbi.caller")


class CallerAgent(BaseAgent):
    """
    Caller Agent — executes outbound communication simulation producing speaker turns.
    Designed so a live Twilio voice stream can replace internals without altering interface.
    """

    name = "CallerAgent"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)

    def run(self, customer_id: str, hypothesis: Dict[str, Any], strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes simulated voice call dialogue and returns transcript dictionary.
        """
        customer = data_store.get_customer(customer_id) or {}
        name = customer.get("full_name", "Valued Customer")
        channel = strategy.get("channel", "call")
        action = hypothesis.get("recommended_action", "Personalized Review")

        user_prompt = (
            f"Customer Name: {name} (ID: {customer_id})\n"
            f"Channel: {channel}\n"
            f"Objective: {strategy.get('objective', 'educate')}\n"
            f"Recommended Product: {action}\n"
            f"Rationale: {hypothesis.get('rationale', '')}\n\n"
            "Generate a realistic 3-4 turn dialogue between Agent and Customer."
        )

        parsed_output = None
        for attempt in range(2):
            try:
                raw_dict = call_structured_llm(CALLER_SYSTEM_PROMPT, user_prompt)
                parsed_output = CallerOutputSchema.model_validate(raw_dict)
                break
            except (ValueError, ValidationError) as e:
                logger.warning(f"[{customer_id}] Caller attempt {attempt + 1} failed validation: {e}")
                if attempt == 1:
                    # Fallback structured simulation if schema parse fails twice
                    parsed_output = CallerOutputSchema(
                        call_sid=f"CA-SIM-{uuid.uuid4().hex[:8]}",
                        duration_seconds=95,
                        raw_outcome="COMPLETED",
                        transcript=f"Agent: Hello {name}, calling from State Bank of India regarding {action}.\nCustomer: Yes, please send me details over email and schedule a callback.\nAgent: Thank you, I have arranged that for you."
                    )

        transcript_record = {
            "call_sid": parsed_output.call_sid,
            "customer_id": customer_id,
            "channel": channel,
            "duration_seconds": parsed_output.duration_seconds,
            "status": parsed_output.raw_outcome,
            "transcript": parsed_output.transcript,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        data_store.save_call_transcript(transcript_record)
        logger.info(f"[{customer_id}] Simulated call completed: {parsed_output.call_sid}")
        return transcript_record
