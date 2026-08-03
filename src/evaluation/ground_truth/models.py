"""
Data models used by the Benchmark Builder.

These models define benchmark queries and candidate products
used to construct the final RAG benchmark dataset before
manual review and approval.

The generated benchmark is shared by:
- Retrieval evaluation
- LLM generation evaluation
"""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.enums import QueryCategory


@dataclass(frozen=True, slots=True)
class GroundTruthExample:
    """
    Represents a single benchmark example.

    This model is used during benchmark generation before
    producing the finalized benchmark dataset.
    """

    # ------------------------------------------------------------------
    # Query information
    # ------------------------------------------------------------------

    id: str

    query: str

    category: QueryCategory

    description: str

    search_terms: list[str]

    # ------------------------------------------------------------------
    # Retrieval benchmark
    # ------------------------------------------------------------------

    relevant_asins: list[str]

    # ------------------------------------------------------------------
    # LLM benchmark
    # ------------------------------------------------------------------

    ground_truth_answer: str | None = None


@dataclass(frozen=True, slots=True)
class GroundTruthDataset:
    """
    Collection of ground truth examples.

    This dataset is used to construct the finalized benchmark
    shared by both retrieval and LLM evaluation.
    """

    examples: list[GroundTruthExample]


@dataclass(frozen=True, slots=True)
class CandidateProduct:
    """
    Candidate product proposed for a benchmark query.

    Human reviewers inspect these candidates before approving
    them into the final benchmark dataset.
    """

    asin: str

    brand: str

    title: str

    price: float | None

    rating: float | None