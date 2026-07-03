"""
memory_schema.py — Structured Memory Representation Schema
==========================================================
Defines the schema for long-term customer context stored across both SQL
databases and vector search indexes (Chroma/Pinecone).

Ensures longitudinal consistency when MemoryAgent stores or queries interactions.
"""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class InteractionSummary(BaseModel):
    """Represents a single past interaction summary stored in vector memory."""
    interaction_id: str
    case_id: Optional[str] = None
    timestamp: str
    channel: str
    hypothesis_product: str
    outcome_type: str
    sentiment: str
    key_takeaway: str
    embedding_vector: Optional[List[float]] = None


class CustomerPreferenceProfile(BaseModel):
    """Customer channel preferences, contact restrictions, and best timing."""
    preferred_channel: str = "voice"
    secondary_channel: str = "sms"
    opt_out_categories: List[str] = Field(default_factory=list)
    dnd_registered: bool = False
    preferred_time_window_ist: str = "14:00-18:00"


class CustomerMemoryRecord(BaseModel):
    """Aggregate customer 360 memory record returned by MemoryAgent."""
    customer_id: str
    cif_number: str
    full_name: str
    segment: str
    preferences: CustomerPreferenceProfile
    recent_interactions: List[InteractionSummary] = Field(default_factory=list)
    semantic_summary: Optional[str] = None
