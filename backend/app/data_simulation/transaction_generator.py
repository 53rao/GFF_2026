"""
transaction_generator.py — Synthetic Transaction Stream Generator
=================================================================
Uses Faker and randomized banking heuristics to generate realistic financial
transaction event streams for testing Sentinel detection thresholds.
"""

from __future__ import annotations

from typing import List, Dict, Any
# TODO: from faker import Faker


def generate_synthetic_transactions(customer_id: str, count: int = 20) -> List[Dict[str, Any]]:
    """
    Generates realistic historical transactions (UPI, NEFT, ATM, POS, Salary)
    including occasional anomaly events (large inflows or spending spikes).
    """
    raise NotImplementedError
