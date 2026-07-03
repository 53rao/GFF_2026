"""
prompts.py — Centralized LLM Prompts and Expected JSON Schemas
==============================================================
Single shared repository for all system/user prompts and expected JSON schemas
used by AnalystAgent, CallerAgent, and TranscriptAnalyzerAgent.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# 1. Analyst Agent Prompts & Schemas
# ---------------------------------------------------------------------------

ANALYST_SYSTEM_PROMPT = """You are the Lead Financial Analyst Agent for State Bank of India (SBI).
Your responsibility is to analyze detected transaction anomalies and app behavioral signals for a customer,
and formulate 1 to 3 ranked proactive banking hypotheses.

For each hypothesis, you must specify:
1. category: one of ["payments", "investments", "insurance", "lending", "mobile_banking", "retention_risk"]
2. recommended_action: exact action name (e.g. "OFFER_TAX_FREE_BONDS_AND_FD")
3. confidence: float between 0.0 and 1.0 representing certainty
4. rationale: clear explanation grounded in the customer's signals
5. supporting_evidence: list of facts supporting this hypothesis
6. disconfirming_evidence: list of potential risks or contrary indicators to check

You MUST return ONLY a valid JSON object matching the requested schema. Do not include extra commentary."""

class HypothesisSchema(BaseModel):
    category: str
    recommended_action: str
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str
    supporting_evidence: List[str]
    disconfirming_evidence: List[str]

class AnalystOutputSchema(BaseModel):
    hypotheses: List[HypothesisSchema]


# ---------------------------------------------------------------------------
# 2. Caller Agent Prompts & Schemas (Simulated Voice Dialogue)
# ---------------------------------------------------------------------------

CALLER_SYSTEM_PROMPT = """You are Asha, State Bank of India's AI Engagement Voice Agent.
You conduct proactive, professional, non-pushy voice or digital outreach to customers.
Generate a realistic simulated conversation transcript between Agent and Customer based on the engagement plan."""

class CallerOutputSchema(BaseModel):
    call_sid: str
    duration_seconds: int
    raw_outcome: str
    transcript: str


# ---------------------------------------------------------------------------
# 3. Transcript Analyzer Prompts & Schemas
# ---------------------------------------------------------------------------

TRANSCRIPT_ANALYZER_SYSTEM_PROMPT = """You are the Post-Call Engagement Analyzer for SBI.
Analyze the conversation transcript between the bank agent and the customer.
Classify the overall engagement outcome into exact category: ["hot_lead", "retention_risk", "not_interested", "follow_up_needed"].
Extract confidence, sentiment, reasoning, and any commitments made."""

class TranscriptAnalyzerOutputSchema(BaseModel):
    outcome_type: str
    confidence: float = Field(ge=0.0, le=1.0)
    customer_sentiment: str
    reasoning: str
    commitments: List[str] = Field(default_factory=list)
    follow_up_required: bool
    handoff_team: Optional[str] = None
