"""
vector_store.py — Vector Store Client Wrapper (Chroma / Pinecone)
=================================================================
Provides a unified vector database interface for storing semantic embeddings
of customer interaction summaries and querying relevant past interactions.

FUTURE IMPLEMENTATION NOTES:
    - Support ChromaDB (local/HTTP client) or Pinecone based on `settings.VECTOR_STORE_PROVIDER`
    - Provide `upsert_interaction` and `query_similar_interactions`
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from app.config import settings


class VectorStoreClient:
    """Wrapper client for semantic memory vector operations."""

    def __init__(self, provider: Optional[str] = None) -> None:
        self.provider = provider or settings.VECTOR_STORE_PROVIDER
        # TODO: Initialize Chroma or Pinecone SDK client

    def health_check(self) -> bool:
        """Ping vector store backend to ensure connectivity."""
        pass

    def upsert_interaction(
        self,
        customer_id: str,
        interaction_id: str,
        text_summary: str,
        metadata: Dict[str, Any],
        embedding: Optional[List[float]] = None
    ) -> None:
        """
        Stores an interaction embedding vector tagged with customer metadata.
        
        TODO: Generate embedding if missing via LLM provider, then upsert.
        """
        raise NotImplementedError

    def query_similar_interactions(
        self,
        customer_id: str,
        query_text: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Queries past interactions for a specific customer semantically similar
        to `query_text` (e.g. "investment attitude or FD interest").
        """
        raise NotImplementedError
