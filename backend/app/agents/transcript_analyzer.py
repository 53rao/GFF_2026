"""
transcript_analyzer.py — Post-Call Conversation Outcome Classification Agent
=============================================================================
Analyzes dialogue transcripts using structured LLM inference to categorize
customer sentiment, commitments, and exact follow-up classification.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict
from pydantic import ValidationError

from app.agents.base_agent import BaseAgent
from app.agents.llm_client import call_structured_llm
from app.agents.prompts import TRANSCRIPT_ANALYZER_SYSTEM_PROMPT, TranscriptAnalyzerOutputSchema
from app import data_store
from app.utils.logger import get_logger

logger = get_logger("sbi.analyzer")


class TranscriptAnalyzerAgent(BaseAgent):
    """
    Transcript Analyzer Agent — classifies transcript into actionable outcome category.
    Enforces structured JSON output and persists result to engagement_outcomes.json.
    """

    name = "TranscriptAnalyzerAgent"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)

    def run(self, customer_id: str, transcript_obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes conversation transcript and returns structured classification.
        """
        transcript_text = transcript_obj.get("transcript", "")
        if not transcript_text:
            logger.warning(f"[{customer_id}] No transcript text provided for analysis.")
            return {}

        user_prompt = f"Analyze the following SBI customer conversation:\n\n{transcript_text}"

        parsed_output = None
        for attempt in range(2):
            try:
                raw_dict = call_structured_llm(TRANSCRIPT_ANALYZER_SYSTEM_PROMPT, user_prompt)
                parsed_output = TranscriptAnalyzerOutputSchema.model_validate(raw_dict)
                break
            except (ValueError, ValidationError) as e:
                logger.warning(f"[{customer_id}] Analyzer attempt {attempt + 1} failed validation: {e}")
                if attempt == 1:
                    raise RuntimeError(f"TranscriptAnalyzerAgent failed validation after 2 attempts: {e}") from e

        outcome_record = {
            "outcome_id": f"OUT-{customer_id}-{uuid.uuid4().hex[:6]}",
            "customer_id": customer_id,
            "call_sid": transcript_obj.get("call_sid", ""),
            "outcome_type": parsed_output.outcome_type,
            "confidence": parsed_output.confidence,
            "sentiment": parsed_output.customer_sentiment,
            "reasoning": parsed_output.reasoning,
            "commitments": parsed_output.commitments,
            "follow_up_required": parsed_output.follow_up_required,
            "handoff_team": parsed_output.handoff_team,
            "analyzed_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        data_store.save_engagement_outcome(outcome_record)
        logger.info(f"[{customer_id}] Transcript analyzed: {parsed_output.outcome_type} ({parsed_output.confidence:.2f})")
        return outcome_record
