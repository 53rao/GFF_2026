"""
test_api.py — Integration Tests for FastAPI REST Endpoints
===========================================================
Tests the FastAPI endpoints using httpx AsyncClient (FastAPI's recommended
test approach). Validates status codes, response schemas, and data integrity.

NOTE: Pipeline tests mutate JSON state via data_store. Some tests regenerate
seed data to ensure clean state.

Run: cd backend && .venv/bin/python -m pytest tests/test_api/ -v
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import data_store


# ──────────────────────────────────────────────────────────────────────────────
# Fixture
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def client():
    """Creates a synchronous test client for FastAPI."""
    with TestClient(app) as c:
        yield c


# ──────────────────────────────────────────────────────────────────────────────
# Health Endpoint
# ──────────────────────────────────────────────────────────────────────────────

class TestHealthEndpoint:

    def test_health_returns_200(self, client):
        res = client.get("/health")
        assert res.status_code == 200

    def test_health_response_schema(self, client):
        data = client.get("/health").json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert data["customers_loaded"] == 30


# ──────────────────────────────────────────────────────────────────────────────
# User API Endpoints
# ──────────────────────────────────────────────────────────────────────────────

class TestUserAPI:

    def test_get_profile_returns_customer(self, client):
        res = client.get("/api/user/CUST-1001/profile")
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == "CUST-1001"
        assert data["full_name"] == "Rajesh Kumar"
        assert data["segment"] == "WEALTH"

    def test_get_profile_not_found(self, client):
        res = client.get("/api/user/CUST-NONEXISTENT/profile")
        assert res.status_code == 404

    def test_get_transactions_returns_list(self, client):
        res = client.get("/api/user/CUST-1001/transactions?limit=5")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert len(data) <= 5

    def test_get_transactions_sorted_by_date(self, client):
        """Transactions should be sorted newest-first."""
        res = client.get("/api/user/CUST-1001/transactions?limit=10")
        data = res.json()
        if len(data) >= 2:
            dates = [t["timestamp"] for t in data]
            assert dates == sorted(dates, reverse=True)

    def test_get_engagements_returns_list(self, client):
        res = client.get("/api/user/CUST-1001/engagements")
        assert res.status_code == 200
        assert isinstance(res.json(), list)


# ──────────────────────────────────────────────────────────────────────────────
# Admin API Endpoints
# ──────────────────────────────────────────────────────────────────────────────

class TestAdminAPI:

    def test_get_customers_paginated(self, client):
        res = client.get("/api/admin/customers?page=1&page_size=5")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] == 30
        assert data["page"] == 1
        assert data["page_size"] == 5
        assert len(data["items"]) == 5

    def test_get_customers_page_2(self, client):
        res = client.get("/api/admin/customers?page=2&page_size=10")
        data = res.json()
        assert data["page"] == 2
        assert len(data["items"]) == 10

    def test_get_signals_returns_list(self, client):
        res = client.get("/api/admin/signals")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_get_hypotheses_returns_list(self, client):
        res = client.get("/api/admin/hypotheses")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_get_cases_returns_list(self, client):
        res = client.get("/api/admin/cases")
        assert res.status_code == 200
        assert isinstance(res.json(), list)


# ──────────────────────────────────────────────────────────────────────────────
# Pipeline API Endpoints
# ──────────────────────────────────────────────────────────────────────────────

class TestPipelineAPI:

    def test_run_sentinel_returns_signals(self, client):
        res = client.post("/api/pipeline/run-sentinel/CUST-1002")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_run_sentinel_not_found(self, client):
        res = client.post("/api/pipeline/run-sentinel/CUST-NONEXISTENT")
        assert res.status_code == 404

    def test_run_full_pipeline(self, client):
        """Full pipeline should return complete execution trace."""
        # Use CUST-1002 to avoid state pollution from earlier CUST-1001 runs
        res = client.post("/api/pipeline/run-full/CUST-1002")
        assert res.status_code == 200
        data = res.json()
        assert "detected_signals" in data
        assert "hypotheses" in data
        assert "status" in data
        # Status may include a reason suffix like 'HALTED: ...'
        assert any(data["status"].startswith(s) for s in ["COMPLETED", "HALTED"])

    def test_run_full_pipeline_not_found(self, client):
        res = client.post("/api/pipeline/run-full/CUST-NONEXISTENT")
        assert res.status_code == 404


# ──────────────────────────────────────────────────────────────────────────────
# Agent Status Endpoints
# ──────────────────────────────────────────────────────────────────────────────

class TestAgentStatusAPI:

    def test_list_agents_returns_list(self, client):
        # The agent status endpoint is mounted with trailing slash
        res = client.get("/api/v1/agents/")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        # The hardcoded list has 8 agents
        assert len(data) >= 7

    def test_agent_entry_has_required_fields(self, client):
        res = client.get("/api/v1/agents/")
        assert res.status_code == 200
        data = res.json()
        for agent in data:
            assert "id" in agent
            assert "name" in agent
            assert "status" in agent


# ──────────────────────────────────────────────────────────────────────────────
# Case Queue API Endpoints (v1 DB routes)
# ──────────────────────────────────────────────────────────────────────────────

class TestCasesAPI:

    def test_create_case_endpoint(self, client):
        payload = {
            "customer_id": "CUST-1001",
            "case_type": "Lending — Spending Spike",
            "priority": "High",
            "assigned_agent": "Analyst Agent",
            "trigger_event": {
                "signal_type": "SPENDING_SPIKE",
                "confidence": 0.85,
                "raw_evidence": {"amount": 250000}
            }
        }
        res = client.post("/api/v1/cases/", json=payload)
        assert res.status_code == 201
        data = res.json()
        assert data["customer_id"] == "CUST-1001"
        assert data["priority"] == "High"
        assert "id" in data
        assert data["status"] == "Open"

    def test_list_cases_endpoint(self, client):
        res = client.get("/api/v1/cases/?page=1&page_size=10")
        assert res.status_code == 200
        data = res.json()
        assert "total" in data
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_get_case_detail_endpoint(self, client):
        # First create a case
        payload = {
            "customer_id": "CUST-1002",
            "case_type": "Insurance Opportunity",
            "priority": "Medium",
            "assigned_agent": "Sentinel Agent"
        }
        create_res = client.post("/api/v1/cases/", json=payload)
        case_id = create_res.json()["id"]

        # Get details
        res = client.get(f"/api/v1/cases/{case_id}")
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == case_id
        assert data["customer_id"] == "CUST-1002"

    def test_get_case_not_found(self, client):
        res = client.get("/api/v1/cases/CASE-NONEXISTENT")
        assert res.status_code == 404

    def test_update_case_endpoint(self, client):
        # Create a case
        payload = {
            "customer_id": "CUST-1003",
            "case_type": "Dormancy Warning",
            "priority": "Low"
        }
        create_res = client.post("/api/v1/cases/", json=payload)
        case_id = create_res.json()["id"]

        # Update status
        update_payload = {
            "status": "Resolved",
            "priority": "High"
        }
        res = client.patch(f"/api/v1/cases/{case_id}", json=update_payload)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "Resolved"
        assert data["priority"] == "High"

    def test_get_case_timeline_endpoint(self, client):
        # Create a case
        payload = {
            "customer_id": "CUST-1004",
            "case_type": "Investment Maturity",
            "priority": "High"
        }
        create_res = client.post("/api/v1/cases/", json=payload)
        case_id = create_res.json()["id"]

        # Get timeline
        res = client.get(f"/api/v1/cases/{case_id}/timeline")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["event"] == "Case Created"

