"""
test_agents.py — Integration Tests for Pipeline Agents
=======================================================
Tests Sentinel, Analyst, and Policy agents against real seeded JSON data.
Uses the data_store module directly — no mocking required because
the JSON files are regenerated from generate_seed.py.

Run: cd backend && .venv/bin/python -m pytest tests/ -v
"""

import pytest
from app.agents.sentinel import SentinelAgent
from app.agents.analyst import AnalystAgent
from app.agents.policy_agent import PolicyAgent
from app.agents.memory_agent import MemoryAgent
from app import data_store


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def sentinel():
    return SentinelAgent()


@pytest.fixture(scope="module")
def analyst():
    return AnalystAgent()


@pytest.fixture(scope="module")
def policy():
    return PolicyAgent()


@pytest.fixture(scope="module")
def memory():
    return MemoryAgent()


# ──────────────────────────────────────────────────────────────────────────────
# Sentinel Agent Tests
# ──────────────────────────────────────────────────────────────────────────────

class TestSentinelAgent:
    """Validates rule-based detection heuristics against seeded customer data."""

    def test_detects_large_inflow_for_cust_1001(self, sentinel):
        """
        CUST-1001 (Rajesh Kumar) has an ₹8.5L bonus credit — LARGE_INFLOW.
        Sentinel should detect this against a ₹1.5L salary baseline.
        """
        signals = sentinel.run("CUST-1001")
        assert len(signals) >= 1
        signal_types = [s["signal_type"] for s in signals]
        assert "LARGE_INFLOW" in signal_types

        # Validate the large inflow signal structure
        large_inflow = next(s for s in signals if s["signal_type"] == "LARGE_INFLOW")
        assert large_inflow["customer_id"] == "CUST-1001"
        assert large_inflow["confidence"] >= 0.8
        assert large_inflow["urgency"] >= 3
        assert large_inflow["raw_evidence"]["amount"] == 850000.0

    def test_detects_spending_spike_for_cust_1002(self, sentinel):
        """
        CUST-1002 (Priya Sharma) has ₹2.4L in 3 days — SPENDING_SPIKE.
        """
        signals = sentinel.run("CUST-1002")
        signal_types = [s["signal_type"] for s in signals]
        assert "SPENDING_SPIKE" in signal_types

    def test_detects_dormancy_for_cust_1003(self, sentinel):
        """
        CUST-1003 (Amit Patel) has been inactive for 38+ days — DORMANCY_WARNING.
        """
        signals = sentinel.run("CUST-1003")
        signal_types = [s["signal_type"] for s in signals]
        assert "DORMANCY_WARNING" in signal_types

    def test_detects_investment_maturity_for_cust_1004(self, sentinel):
        """
        CUST-1004 (Sunita Verma) has FD maturing in 8 days — INVESTMENT_MATURITY.
        """
        signals = sentinel.run("CUST-1004")
        signal_types = [s["signal_type"] for s in signals]
        assert "INVESTMENT_MATURITY_APPROACHING" in signal_types

    def test_no_signals_for_boring_customer(self, sentinel):
        """
        CUST-1005+ are deliberately boring — steady salary, no anomalies.
        Sentinel should return empty for them.
        """
        signals = sentinel.run("CUST-1005")
        assert len(signals) == 0

    def test_returns_empty_for_nonexistent_customer(self, sentinel):
        """Sentinel should gracefully return empty for unknown customer IDs."""
        signals = sentinel.run("CUST-NONEXISTENT")
        assert signals == []

    def test_signal_has_required_fields(self, sentinel):
        """Every signal must have the full schema: signal_id, signal_type, customer_id, confidence, urgency, raw_evidence, detected_at."""
        signals = sentinel.run("CUST-1001")
        required_fields = {"signal_id", "signal_type", "customer_id", "confidence", "urgency", "raw_evidence", "detected_at"}
        for s in signals:
            assert required_fields.issubset(s.keys()), f"Signal missing fields: {required_fields - s.keys()}"


# ──────────────────────────────────────────────────────────────────────────────
# Analyst Agent Tests
# ──────────────────────────────────────────────────────────────────────────────

class TestAnalystAgent:
    """Validates LLM-driven hypothesis generation (uses local heuristic engine)."""

    def test_generates_hypothesis_for_large_inflow(self, analyst):
        """Analyst should produce at least one hypothesis for a LARGE_INFLOW signal."""
        mock_signal = {
            "signal_id": "SIG-TEST-INFLOW",
            "signal_type": "LARGE_INFLOW",
            "customer_id": "CUST-1001",
            "confidence": 0.95,
            "urgency": 4,
            "raw_evidence": {
                "transaction_id": "TX-1001-BONUS",
                "amount": 850000.0,
                "historical_avg_credit": 150000.0,
                "description": "ANNUAL PERFORMANCE BONUS FY25"
            },
            "detected_at": "2026-07-04T00:00:00Z"
        }
        hypotheses = analyst.run("CUST-1001", [mock_signal])
        assert len(hypotheses) >= 1

    def test_hypothesis_has_required_fields(self, analyst):
        """Each hypothesis must conform to the expected schema."""
        mock_signal = {
            "signal_id": "SIG-TEST-SCHEMA",
            "signal_type": "LARGE_INFLOW",
            "customer_id": "CUST-1001",
            "confidence": 0.9,
            "urgency": 4,
            "raw_evidence": {"amount": 850000.0},
            "detected_at": "2026-07-04T00:00:00Z"
        }
        hypotheses = analyst.run("CUST-1001", [mock_signal])
        required_fields = {"hypothesis_id", "customer_id", "signal_id", "category",
                          "recommended_action", "confidence", "rationale", "status"}
        for h in hypotheses:
            assert required_fields.issubset(h.keys()), f"Hypothesis missing fields: {required_fields - h.keys()}"

    def test_returns_empty_for_no_signals(self, analyst):
        """Analyst should return empty list when given no signals."""
        hypotheses = analyst.run("CUST-1001", [])
        assert hypotheses == []

    def test_hypothesis_confidence_is_valid(self, analyst):
        """Confidence must be between 0.0 and 1.0."""
        mock_signal = {
            "signal_id": "SIG-TEST-CONF",
            "signal_type": "LARGE_INFLOW",
            "customer_id": "CUST-1001",
            "confidence": 0.9,
            "urgency": 4,
            "raw_evidence": {"amount": 850000.0},
            "detected_at": "2026-07-04T00:00:00Z"
        }
        hypotheses = analyst.run("CUST-1001", [mock_signal])
        for h in hypotheses:
            assert 0.0 <= h["confidence"] <= 1.0


# ──────────────────────────────────────────────────────────────────────────────
# Policy Agent Tests
# ──────────────────────────────────────────────────────────────────────────────

class TestPolicyAgent:
    """Validates deterministic regulatory gate logic."""

    def test_hni_investment_requires_human_review(self, policy):
        """
        CUST-1001 is WEALTH segment. Investment hypothesis should
        trigger SUITABILITY_01 → require_human_review.
        """
        hypothesis = {
            "category": "investments",
            "recommended_action": "OFFER_TAX_FREE_BONDS_AND_FD",
            "confidence": 0.92
        }
        result = policy.run("CUST-1001", hypothesis)
        assert result["decision"] in ["require_human_review", "deny"]
        rule_ids = [r.split(":")[0] for r in result.get("triggered_rules", [])]
        assert "SUITABILITY_01" in rule_ids

    def test_permits_standard_mobile_banking_engagement(self, policy):
        """
        A non-HNI customer with a mobile_banking hypothesis should
        generally be permitted (no HNI suitability rule triggered).
        """
        hypothesis = {
            "category": "mobile_banking",
            "recommended_action": "YONO_ONBOARDING_ASSIST",
            "confidence": 0.8
        }
        # Use CUST-1005 (RETAIL segment, no special flags)
        result = policy.run("CUST-1005", hypothesis)
        # Should not deny unless frequency cap is hit
        assert result["decision"] in ["permit", "require_human_review"]

    def test_policy_returns_required_fields(self, policy):
        """Every policy verdict must include: decision, triggered_rules, reason, evaluated_at."""
        hypothesis = {"category": "insurance", "recommended_action": "OFFER_HEALTH_INSURANCE", "confidence": 0.7}
        result = policy.run("CUST-1001", hypothesis)
        required = {"decision", "triggered_rules", "reason", "evaluated_at"}
        assert required.issubset(result.keys())

    def test_policy_decision_values_are_valid(self, policy):
        """Decision must be one of: permit, deny, require_human_review."""
        hypothesis = {"category": "payments", "recommended_action": "OFFER_UPI_LITE", "confidence": 0.6}
        result = policy.run("CUST-1001", hypothesis)
        assert result["decision"] in ["permit", "deny", "require_human_review"]


# ──────────────────────────────────────────────────────────────────────────────
# Memory Agent Tests
# ──────────────────────────────────────────────────────────────────────────────

class TestMemoryAgent:
    """Validates longitudinal memory read/write."""

    def test_read_memory_returns_dict(self, memory):
        """read_memory should always return a dict (default or existing)."""
        mem = memory.read_memory("CUST-1001")
        assert isinstance(mem, dict)
        assert "customer_id" in mem or "preferred_channel" in mem

    def test_read_memory_for_new_customer_creates_default(self, memory):
        """New customer should get sensible defaults."""
        mem = memory.read_memory("CUST-NEW-TEST")
        assert mem.get("monthly_contact_count") == 0
        assert mem.get("preferred_channel") == "call"
        assert isinstance(mem.get("interaction_history"), list)
