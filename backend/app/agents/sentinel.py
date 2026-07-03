"""
sentinel.py — Real Rule-Based Signal Detection Agent
====================================================
Analyzes real customer transaction streams, app clickstreams, and holdings data
from data_store to detect actionable financial events and behavioral churn risks.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Any, List, Dict
from app.agents.base_agent import BaseAgent
from app import data_store


class SentinelAgent(BaseAgent):
    """
    Sentinel Agent — real detection engine using rolling averages and threshold checks.
    Genuinely analyzes transaction streams and app login frequency from data_store.py.
    """

    name = "SentinelAgent"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)

    def run(self, customer_id: str) -> List[Dict[str, Any]]:
        """
        Runs real detection heuristics for the specified customer against
        persisted JSON data store. Saves found signals and returns them.
        """
        customer = data_store.get_customer(customer_id)
        if not customer:
            return []

        transactions = data_store.get_transactions(customer_id)
        behavior_events = data_store.get_behavior_events(customer_id)

        detected_signals = []
        now = datetime.utcnow()

        # Helper to parse timestamps
        def parse_ts(ts_str: str) -> datetime:
            try:
                return datetime.strptime(ts_str[:19], "%Y-%m-%dT%H:%M:%S")
            except Exception:
                return now

        # Sort transactions by date ascending
        sorted_txs = sorted(transactions, key=lambda x: parse_ts(x.get("timestamp", "")))

        # -------------------------------------------------------------------
        # Rule 1: LARGE_INFLOW
        # Flag if a single credit transaction in the last 14 days is > ₹5,00,000
        # OR > 3x average historical credit.
        # -------------------------------------------------------------------
        credits = [t for t in sorted_txs if t.get("type", "").upper() == "CREDIT"]
        if credits:
            older_credits = [c for c in credits if (now - parse_ts(c["timestamp"])).days > 14]
            avg_credit = (sum(c["amount"] for c in older_credits) / len(older_credits)) if older_credits else 50000.0

            recent_credits = [c for c in credits if (now - parse_ts(c["timestamp"])).days <= 14]
            for c in recent_credits:
                amt = float(c.get("amount", 0.0))
                if amt >= 500000.0 or (avg_credit > 0 and amt > 3.0 * avg_credit):
                    sig = {
                        "signal_id": f"SIG-{customer_id}-INFLOW-{c.get('id', uuid.uuid4().hex[:6])}",
                        "signal_type": "LARGE_INFLOW",
                        "customer_id": customer_id,
                        "confidence": 0.95,
                        "urgency": 4,
                        "raw_evidence": {
                            "transaction_id": c.get("id"),
                            "amount": amt,
                            "historical_avg_credit": round(avg_credit, 2),
                            "description": c.get("description")
                        },
                        "detected_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
                    detected_signals.append(sig)

        # -------------------------------------------------------------------
        # Rule 2: SPENDING_SPIKE
        # Compare debit spending over the last 7 days vs historical weekly baseline.
        # -------------------------------------------------------------------
        debits = [t for t in sorted_txs if t.get("type", "").upper() == "DEBIT"]
        if debits:
            recent_debits = [d for d in debits if (now - parse_ts(d["timestamp"])).days <= 7]
            older_debits = [d for d in debits if (now - parse_ts(d["timestamp"])).days > 7]

            recent_spend = sum(float(d["amount"]) for d in recent_debits)
            
            # Estimate historical weekly spend
            if older_debits:
                oldest_ts = parse_ts(older_debits[0]["timestamp"])
                weeks = max((now - oldest_ts).days / 7.0, 1.0)
                historical_weekly_avg = sum(float(d["amount"]) for d in older_debits) / weeks
            else:
                historical_weekly_avg = 15000.0

            if recent_spend >= 100000.0 or (historical_weekly_avg > 0 and recent_spend > 3.5 * historical_weekly_avg):
                sig = {
                    "signal_id": f"SIG-{customer_id}-SPIKE-{uuid.uuid4().hex[:6]}",
                    "signal_type": "SPENDING_SPIKE",
                    "customer_id": customer_id,
                    "confidence": 0.92,
                    "urgency": 4,
                    "raw_evidence": {
                        "recent_7d_spending": recent_spend,
                        "historical_weekly_avg": round(historical_weekly_avg, 2),
                        "spike_multiplier": round(recent_spend / historical_weekly_avg, 2) if historical_weekly_avg else 0
                    },
                    "detected_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                detected_signals.append(sig)

        # -------------------------------------------------------------------
        # Rule 3: DORMANCY_WARNING
        # Check days since last app login event.
        # -------------------------------------------------------------------
        logins = [e for e in behavior_events if e.get("event_type") == "APP_LOGIN"]
        if logins:
            sorted_logins = sorted(logins, key=lambda x: parse_ts(x.get("timestamp", "")))
            last_login_ts = parse_ts(sorted_logins[-1]["timestamp"])
            days_inactive = (now - last_login_ts).days
            if days_inactive >= 30:
                sig = {
                    "signal_id": f"SIG-{customer_id}-DORM-{uuid.uuid4().hex[:6]}",
                    "signal_type": "DORMANCY_WARNING",
                    "customer_id": customer_id,
                    "confidence": 0.88,
                    "urgency": 3,
                    "raw_evidence": {
                        "days_inactive": days_inactive,
                        "last_login": sorted_logins[-1].get("timestamp"),
                        "total_historical_logins": len(logins)
                    },
                    "detected_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                detected_signals.append(sig)

        # -------------------------------------------------------------------
        # Rule 4: INVESTMENT_MATURITY_APPROACHING
        # Check customer holdings for upcoming maturities within 30 days.
        # -------------------------------------------------------------------
        for h in customer.get("holdings", []):
            mat_date = h.get("maturity_date")
            if mat_date:
                try:
                    md = datetime.strptime(mat_date, "%Y-%m-%d")
                    days_to_mat = (md - now).days
                    if -5 <= days_to_mat <= 30:
                        sig = {
                            "signal_id": f"SIG-{customer_id}-MAT-{h.get('product_code', 'FD')}",
                            "signal_type": "INVESTMENT_MATURITY_APPROACHING",
                            "customer_id": customer_id,
                            "confidence": 0.99,
                            "urgency": 4,
                            "raw_evidence": {
                                "product_code": h.get("product_code"),
                                "product_name": h.get("product_name"),
                                "maturity_date": mat_date,
                                "days_to_maturity": days_to_mat,
                                "balance": h.get("balance")
                            },
                            "detected_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                        }
                        detected_signals.append(sig)
                except Exception:
                    pass

        # Save all detected signals to JSON data store
        for s in detected_signals:
            data_store.save_signal(s)

        return detected_signals
