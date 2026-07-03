"""
ingest.py — Document Ingestion Pipeline (Placeholder)
=====================================================
Processes raw PDF, Markdown, and text documents from `app/rag/documents/`,
splits them into chunks, computes embeddings, and indexes them for RAG retrieval.

FUTURE IMPLEMENTATION NOTES:
    - Use RecursiveCharacterTextSplitter with configurable chunk size/overlap
    - Store chunk metadata (source file, product category, version date)
"""

from __future__ import annotations

from typing import List
from pathlib import Path
from app.config import settings


def ingest_documents(source_dir: str = "backend/app/rag/documents") -> int:
    """
    Reads all documents in `source_dir`, chunks them, generates embeddings,
    and upserts into the RAG vector index.
    
    Returns:
        Number of chunks successfully indexed.
    """
    raise NotImplementedError
