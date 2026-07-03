"""
llm_client.py — Centralized LLM Initialization & Structured Output Service
==========================================================================
All agents (Analyst, Caller, TranscriptAnalyzer) import their LLM capabilities
from this single location. 

Configure your preferred model, provider, and API credentials here or via .env.
"""

import os
import json
from typing import Any, Dict, Optional
from app.config import settings


class LLMConfigurationError(Exception):
    """Raised when LLM API credentials or initialization fail."""
    pass


def get_llm_client():
    """
    Returns an initialized LLM client (OpenAI or Anthropic).
    Modify this single function to configure your specific model or provider.
    """
    provider = os.getenv("LLM_PROVIDER", settings.LLM_PROVIDER).lower()
    openai_key = os.getenv("OPENAI_API_KEY", settings.OPENAI_API_KEY)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", settings.ANTHROPIC_API_KEY)

    if provider == "local":
        return "local_engine"

    if provider == "openai":
        if not openai_key or openai_key == "your_openai_api_key_here":
            raise LLMConfigurationError(
                "OPENAI_API_KEY is not configured. Please declare your key in .env or app/agents/llm_client.py."
            )
        try:
            from openai import OpenAI
            return OpenAI(api_key=openai_key)
        except ImportError:
            raise LLMConfigurationError("The 'openai' Python package is required for OpenAI provider.")

    elif provider == "anthropic":
        if not anthropic_key or anthropic_key == "your_anthropic_api_key_here":
            raise LLMConfigurationError(
                "ANTHROPIC_API_KEY is not configured. Please declare your key in .env or app/agents/llm_client.py."
            )
        try:
            import anthropic
            return anthropic.Anthropic(api_key=anthropic_key)
        except ImportError:
            raise LLMConfigurationError("The 'anthropic' Python package is required for Anthropic provider.")

    else:
        raise LLMConfigurationError(f"Unsupported LLM provider: {provider}")


def call_structured_llm(
    system_prompt: str,
    user_prompt: str,
    response_model: Optional[Any] = None,
    model_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes a prompt against the configured LLM and enforces JSON output.
    If LLM_PROVIDER="local" is set, performs grounded local heuristic parsing.
    """
    provider = os.getenv("LLM_PROVIDER", settings.LLM_PROVIDER).lower()
    client = get_llm_client()

    if provider == "local":
        # Grounded local heuristic engine when LLM_PROVIDER="local"
        return _simulate_local_llm(system_prompt, user_prompt)

    if provider == "openai":
        model = model_name or os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        kwargs: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "response_format": {"type": "json_object"}
        }
        response = client.chat.completions.create(**kwargs)
        raw_content = response.choices[0].message.content or "{}"
        try:
            return json.loads(raw_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned malformed JSON: {raw_content}") from e

    elif provider == "anthropic":
        model = model_name or os.getenv("LLM_MODEL_NAME", "claude-3-5-sonnet-20241022")
        full_system = f"{system_prompt}\n\nYou MUST respond ONLY with a valid JSON object. Do not include markdown code fences or conversational text."
        response = client.messages.create(
            model=model,
            max_tokens=1500,
            system=full_system,
            messages=[{"role": "user", "content": user_prompt}]
        )
        raw_content = response.content[0].text if response.content else "{}"
        if "```json" in raw_content:
            raw_content = raw_content.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_content:
            raw_content = raw_content.split("```")[1].split("```")[0].strip()
        try:
            return json.loads(raw_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned malformed JSON: {raw_content}") from e

    raise LLMConfigurationError(f"Provider {provider} not supported.")


def _simulate_local_llm(system_prompt: str, user_prompt: str) -> Dict[str, Any]:
    """Local deterministic reasoning engine for offline/demo testing."""
    up = user_prompt.lower()
    if "analyst" in system_prompt.lower() or "hypothes" in system_prompt.lower():
        if "large_inflow" in up or "850000" in up:
            return {
                "hypotheses": [
                    {
                        "category": "investments",
                        "recommended_action": "OFFER_TAX_FREE_BONDS_AND_FD",
                        "confidence": 0.92,
                        "rationale": "Customer received ₹8,50,000 performance bonus sitting idle in savings account.",
                        "supporting_evidence": ["Single credit of ₹8.5L exceeds 3x historical salary baseline."],
                        "disconfirming_evidence": ["Customer may have pending property purchase or short-term liquidity need."]
                    }
                ]
            }
        elif "spending_spike" in up or "240000" in up:
            return {
                "hypotheses": [
                    {
                        "category": "lending",
                        "recommended_action": "OFFER_EMERGENCY_CREDIT_LINE_OR_EMI_CONVERSION",
                        "confidence": 0.89,
                        "rationale": "High velocity luxury spending (₹2.4L in 3 days) may require cash flow smoothing.",
                        "supporting_evidence": ["Spend velocity is 83x higher than normal weekly average."],
                        "disconfirming_evidence": ["Customer may have planned luxury purchases with existing savings buffer."]
                    }
                ]
            }
        elif "dormancy_warning" in up or "inactive" in up:
            return {
                "hypotheses": [
                    {
                        "category": "retention_risk",
                        "recommended_action": "PROACTIVE_CHECK_IN_AND_YONO_ASSISTANCE",
                        "confidence": 0.85,
                        "rationale": "Customer hasn't logged into app for 38 days after previously regular usage.",
                        "supporting_evidence": ["Zero logins over 38 days."],
                        "disconfirming_evidence": ["Customer may be traveling internationally or switched device."]
                    }
                ]
            }
        else:
            return {
                "hypotheses": [
                    {
                        "category": "payments",
                        "recommended_action": "STANDARD_SAVINGS_REVIEW",
                        "confidence": 0.60,
                        "rationale": "General routine banking activity.",
                        "supporting_evidence": ["Regular account activity."],
                        "disconfirming_evidence": ["None observed."]
                    }
                ]
            }
    elif "caller" in system_prompt.lower() or "transcript" in system_prompt.lower():
        if "outcome" in system_prompt.lower() or "classify" in system_prompt.lower():
            if "not interested" in up or "busy" in up or "decline" in up:
                return {
                    "outcome_type": "not_interested",
                    "confidence": 0.90,
                    "customer_sentiment": "negative",
                    "reasoning": "Customer explicitly stated they are busy or declined the offer.",
                    "commitments": [],
                    "follow_up_required": False
                }
            elif "retention" in up or "unhappy" in up or "close account" in up:
                return {
                    "outcome_type": "retention_risk",
                    "confidence": 0.95,
                    "customer_sentiment": "negative",
                    "reasoning": "Customer expressed dissatisfaction or mentioned closing account.",
                    "commitments": [],
                    "follow_up_required": True,
                    "handoff_team": "Retention Team Queue"
                }
            else:
                return {
                    "outcome_type": "hot_lead",
                    "confidence": 0.92,
                    "customer_sentiment": "positive",
                    "reasoning": "Customer showed active interest in the recommended banking product.",
                    "commitments": ["Send product brochure and schedule RM call."],
                    "follow_up_required": True,
                    "handoff_team": "Investment RM Queue"
                }
        else:
            # Simulated Caller conversation generation
            return {
                "call_sid": "CA-SIMULATED-8890",
                "duration_seconds": 120,
                "raw_outcome": "ANSWERED",
                "transcript": "Agent: Good afternoon, calling from State Bank of India regarding your recent account activity.\nCustomer: Yes, tell me.\nAgent: We noticed a significant inflow in your account and wanted to suggest our premium Tax-Free Bonds and Fixed Deposit schemes offering 7.1% interest.\nCustomer: That sounds interesting, could you send me more details or have an RM contact me tomorrow?\nAgent: Certainly! I will schedule our relationship manager to contact you with the complete details."
            }

    return {}
