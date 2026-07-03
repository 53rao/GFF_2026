"""
retriever.py — RAG Retrieval Wrapper
====================================
Retrieves factual product terms, interest rates, eligibility requirements, and
regulatory disclaimers from ingested SBI documents to ground LLM prompts.

FUTURE IMPLEMENTATION NOTES:
    - Use LangChain or LlamaIndex vector retriever
    - Retrieve top-k document chunks based on product line or customer query
"""

from __future__ import annotations

from typing import List, Dict, Any
from app.config import settings


class RAGRetriever:
    """Retrieves grounded product and policy documentation chunks."""

    def __init__(self) -> None:
        # TODO: Connect to RAG vector index / chunk repository
        pass

    def retrieve_product_docs(self, product_line: str, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Fetches relevant SBI product documentation chunks (e.g. FD rates,
        home loan eligibility rules) matching the query.
        """
        raise NotImplementedError

    def retrieve_policy_guidelines(self, topic: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """
        Fetches internal or regulatory compliance guidelines relevant to `topic`.
        """
        raise NotImplementedError
