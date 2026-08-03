"""
Data models for the monitoring module.

Responsibilities
----------------
- Define monitoring data structures.
- Represent pipeline telemetry.
- Represent user feedback.

This module contains no business logic, file I/O,
or dashboard functionality.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelemetryRecord:
    """
    Represents telemetry collected from a single
    RAG pipeline execution.
    """

    timestamp: str

    query: str
    prompt_strategy: str

    status: str
    error_message: str | None

    retrieval_latency_seconds: float
    context_latency_seconds: float
    prompt_latency_seconds: float
    llm_latency_seconds: float
    total_latency_seconds: float

    retrieved_chunks: int
    unique_products: int

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    estimated_cost: float


@dataclass(frozen=True, slots=True)
class FeedbackRecord:
    """
    Represents user feedback for a generated response.
    """

    timestamp: str

    query: str

    helpful: bool

    comment: str | None