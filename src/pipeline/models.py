"""
Data models for the RAG pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.retrieval.models import RetrievedChunk


@dataclass(slots=True)
class RAGResponse:
    """
    Represents the output of the RAG pipeline.

    Contains both the generated answer and the retrieved
    evidence used to produce that answer.
    """

    answer: str
    retrieved_chunks: list[RetrievedChunk]