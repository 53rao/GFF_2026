"""
data_store.py — Thread-safe JSON Data Store
===========================================
Single module for reading and writing persisted JSON data files.
Ensures thread safety with threading.Lock() around write operations and
reads live disk data on every call.
"""

import json
import os
import threading
from typing import List, Dict, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

_lock = threading.Lock()


def _read_json(filename: str) -> Any:
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return [] if filename != "customer_memory.json" else {}
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return [] if filename != "customer_memory.json" else {}


def _write_json(filename: str, data: Any) -> None:
    filepath = os.path.join(DATA_DIR, filename)
    with _lock:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


# ---------------------------------------------------------------------------
# Customers
# ---------------------------------------------------------------------------

def get_all_customers() -> List[Dict[str, Any]]:
    return _read_json("customers.json")


def get_customer(customer_id: str) -> Optional[Dict[str, Any]]:
    customers = get_all_customers()
    for c in customers:
        if c.get("id") == customer_id or c.get("cif_number") == customer_id:
            return c
    return None


# ---------------------------------------------------------------------------
# Transactions & Behavior
# ---------------------------------------------------------------------------

def get_transactions(customer_id: str) -> List[Dict[str, Any]]:
    txs = _read_json("transactions.json")
    return [t for t in txs if t.get("customer_id") == customer_id]


def get_behavior_events(customer_id: str) -> List[Dict[str, Any]]:
    events = _read_json("behavior_events.json")
    return [e for e in events if e.get("customer_id") == customer_id]


def get_policy_rules() -> List[Dict[str, Any]]:
    return _read_json("policy_rules.json")


# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------

def get_signals(customer_id: Optional[str] = None) -> List[Dict[str, Any]]:
    signals = _read_json("signals.json")
    if customer_id:
        return [s for s in signals if s.get("customer_id") == customer_id]
    return signals


def save_signal(signal: Dict[str, Any]) -> Dict[str, Any]:
    with _lock:
        signals = _read_json("signals.json")
        # Check if signal with same id already exists
        updated = False
        for i, s in enumerate(signals):
            if s.get("signal_id") == signal.get("signal_id") or (
                s.get("customer_id") == signal.get("customer_id") and s.get("signal_type") == signal.get("signal_type")
            ):
                signals[i] = signal
                updated = True
                break
        if not updated:
            signals.append(signal)
        with open(os.path.join(DATA_DIR, "signals.json"), "w", encoding="utf-8") as f:
            json.dump(signals, f, indent=2)
    return signal


# ---------------------------------------------------------------------------
# Hypotheses
# ---------------------------------------------------------------------------

def get_hypotheses(customer_id: Optional[str] = None) -> List[Dict[str, Any]]:
    hypotheses = _read_json("hypotheses.json")
    if customer_id:
        return [h for h in hypotheses if h.get("customer_id") == customer_id]
    return hypotheses


def save_hypothesis(hypothesis: Dict[str, Any]) -> Dict[str, Any]:
    with _lock:
        hypotheses = _read_json("hypotheses.json")
        updated = False
        for i, h in enumerate(hypotheses):
            if h.get("hypothesis_id") == hypothesis.get("hypothesis_id"):
                hypotheses[i] = hypothesis
                updated = True
                break
        if not updated:
            hypotheses.append(hypothesis)
        with open(os.path.join(DATA_DIR, "hypotheses.json"), "w", encoding="utf-8") as f:
            json.dump(hypotheses, f, indent=2)
    return hypothesis


# ---------------------------------------------------------------------------
# Engagement Cases
# ---------------------------------------------------------------------------

def get_engagement_cases(status: Optional[str] = None) -> List[Dict[str, Any]]:
    cases = _read_json("cases.json")
    if status:
        return [c for c in cases if c.get("status", "").lower() == status.lower()]
    return cases


def save_engagement_case(case: Dict[str, Any]) -> Dict[str, Any]:
    with _lock:
        cases = _read_json("cases.json")
        updated = False
        for i, c in enumerate(cases):
            if c.get("id") == case.get("id") or c.get("case_id") == case.get("id"):
                cases[i] = case
                updated = True
                break
        if not updated:
            cases.append(case)
        with open(os.path.join(DATA_DIR, "cases.json"), "w", encoding="utf-8") as f:
            json.dump(cases, f, indent=2)
    return case


# ---------------------------------------------------------------------------
# Customer Memory
# ---------------------------------------------------------------------------

def get_customer_memory(customer_id: str) -> Dict[str, Any]:
    memory = _read_json("customer_memory.json")
    return memory.get(customer_id, {})


def update_customer_memory(customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    with _lock:
        memory = _read_json("customer_memory.json")
        current = memory.get(customer_id, {})
        current.update(data)
        memory[customer_id] = current
        with open(os.path.join(DATA_DIR, "customer_memory.json"), "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)
    return current


# ---------------------------------------------------------------------------
# Transcripts & Engagement Outcomes
# ---------------------------------------------------------------------------

def get_call_transcripts(customer_id: Optional[str] = None) -> List[Dict[str, Any]]:
    transcripts = _read_json("call_transcripts.json")
    if customer_id:
        return [t for t in transcripts if t.get("customer_id") == customer_id]
    return transcripts


def save_call_transcript(transcript: Dict[str, Any]) -> Dict[str, Any]:
    with _lock:
        transcripts = _read_json("call_transcripts.json")
        updated = False
        for i, t in enumerate(transcripts):
            if t.get("call_sid") == transcript.get("call_sid"):
                transcripts[i] = transcript
                updated = True
                break
        if not updated:
            transcripts.append(transcript)
        with open(os.path.join(DATA_DIR, "call_transcripts.json"), "w", encoding="utf-8") as f:
            json.dump(transcripts, f, indent=2)
    return transcript


def get_engagement_outcomes(customer_id: Optional[str] = None) -> List[Dict[str, Any]]:
    outcomes = _read_json("engagement_outcomes.json")
    if customer_id:
        return [o for o in outcomes if o.get("customer_id") == customer_id]
    return outcomes


def save_engagement_outcome(outcome: Dict[str, Any]) -> Dict[str, Any]:
    with _lock:
        outcomes = _read_json("engagement_outcomes.json")
        outcomes.append(outcome)
        with open(os.path.join(DATA_DIR, "engagement_outcomes.json"), "w", encoding="utf-8") as f:
            json.dump(outcomes, f, indent=2)
    return outcome

