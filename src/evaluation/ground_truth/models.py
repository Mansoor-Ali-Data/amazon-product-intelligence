"""
Data models for the retrieval ground truth dataset.

The ground truth dataset defines benchmark queries and their
expected relevant products. It serves as the reference dataset
for retrieval evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.enums import QueryCategory


@dataclass(frozen=True, slots=True)
class GroundTruthExample:
    """
    Represents a single retrieval benchmark example.

    Attributes
    ----------
    query:
        Natural language user query.

    expected_asins:
        ASINs considered relevant for this query.

    category:
        Query category used for reporting and analysis.

    description:
        Human-readable explanation of what this benchmark
        example evaluates.
    """
    id: str

    query: str

    relevant_asins: list[str]

    category: QueryCategory

    description: str

    search_terms: list[str]


@dataclass(frozen=True, slots=True)
class GroundTruthDataset:
    """
    Collection of benchmark examples.

    This dataset is used as the reference for retrieval
    evaluation.
    """

    examples: list[GroundTruthExample]


@dataclass(frozen=True, slots=True)
class CandidateProduct:
    """
    Candidate product proposed for a benchmark query.

    This model is used during ground truth generation.
    Human reviewers inspect these candidates before
    approving them into the benchmark dataset.
    """

    asin: str

    brand: str

    title: str

    price: float | None

    rating: float | None