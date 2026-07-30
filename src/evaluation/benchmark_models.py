"""
Data models for the finalized retrieval benchmark.

Unlike the GroundTruthExample used during candidate generation,
these models represent the final, human-approved benchmark used
by the retrieval evaluator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.evaluation.enums import QueryCategory


@dataclass(frozen=True)
class ExpectedFilter:
    """Expected metadata constraints for filter-based retrieval benchmarks."""

    min_price: Optional[float] = None
    max_price: Optional[float] = None

    min_rating: Optional[float] = None
    max_rating: Optional[float] = None


@dataclass(frozen=True)
class BenchmarkQuery:
    """Single retrieval benchmark."""

    query_id: str
    category: QueryCategory
    query: str

    # Semantic retrieval benchmark
    relevant_asins: Optional[list[str]] = None

    # Metadata retrieval benchmark
    expected_filter: Optional[ExpectedFilter] = None