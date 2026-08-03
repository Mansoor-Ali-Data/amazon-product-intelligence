"""
Data models for the finalized RAG benchmark.

These models represent the final, human-approved benchmark used
to evaluate the complete RAG pipeline.

The same benchmark is shared by:
- Retrieval evaluation
- LLM generation evaluation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.evaluation.enums import QueryCategory


@dataclass(frozen=True, slots=True)
class ExpectedFilter:
    """
    Expected metadata constraints for filter-based retrieval benchmarks.
    """

    min_price: Optional[float] = None
    max_price: Optional[float] = None

    min_rating: Optional[float] = None
    max_rating: Optional[float] = None


@dataclass(frozen=True, slots=True)
class BenchmarkQuery:
    """
    Single benchmark query used to evaluate the RAG system.

    The retrieval evaluator uses:
    - relevant_asins
    - expected_filter

    The LLM evaluator uses:
    - ground_truth_answer
    """

    # ------------------------------------------------------------------
    # Query information
    # ------------------------------------------------------------------

    query_id: str

    category: QueryCategory

    query: str

    # ------------------------------------------------------------------
    # Retrieval benchmark
    # ------------------------------------------------------------------

    relevant_asins: Optional[list[str]] = None

    expected_filter: Optional[ExpectedFilter] = None

    # ------------------------------------------------------------------
    # LLM benchmark
    # ------------------------------------------------------------------

    ground_truth_answer: Optional[str] = None