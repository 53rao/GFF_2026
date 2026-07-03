"""
behavior_generator.py — Synthetic App-Behavior Stream Generator
===============================================================
Generates simulated mobile app (YONO) and internet banking clickstream events,
login frequencies, feature navigation, and session drop-offs.
"""

from __future__ import annotations

from typing import List, Dict, Any


def generate_behavior_events(customer_id: str, days_back: int = 30) -> List[Dict[str, Any]]:
    """
    Simulates app telemetry events to test Sentinel churn and dormancy detectors.
    """
    raise NotImplementedError
