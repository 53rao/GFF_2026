"""
policy_rules.py — Structured Banking Policy & Compliance Rules
==============================================================
Contains structured rule configurations evaluated by PolicyAgent before any
customer outreach occurs.
"""

from __future__ import annotations

from typing import Dict, Any, List

POLICY_RULES: Dict[str, Any] = {
    "TRAI_CALL_WINDOW": {
        "start_time_ist": "09:00",
        "end_time_ist": "21:00",
        "allowed_days": ["MON", "TUE", "WED", "THU", "FRI", "SAT"],
    },
    "RBI_FREQUENCY_LIMITS": {
        "max_unsolicited_contacts_per_month": 4,
        "cooling_off_hours_after_decline": 48,
    },
    "DPDP_CONSENT_REQUIREMENTS": {
        "mandatory_purpose_codes": ["INVESTMENT_ADVISORY", "CROSS_SELL_LOAN"],
    },
    "SEBI_DISCLAIMERS": {
        "mutual_funds": "Mutual fund investments are subject to market risks, read all scheme related documents carefully.",
    }
}
