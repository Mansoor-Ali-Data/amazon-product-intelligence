"""
Models for retrieval evaluation.

These dataclasses represent the results produced during retrieval
benchmarking.

The evaluator computes one EvaluationResult for each benchmark query
and aggregates them into an EvaluationSummary.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.retrieval.dataset import (
    BenchmarkType,
    QueryCategory,
)


@dataclass(frozen=True, slots=True)
class EvaluationProduct:
    """
    Product used during retrieval evaluation.

    This model represents both:

    - Expected products (ground truth)
    - Retrieved products

    Similarity score is only populated for retrieved products.
    """

    asin: str
    brand: str
    title: str

    price: float | None
    rating: float | None

    distance: float | None = None


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    """
    Retrieval evaluation result for a single benchmark query.
    """

    query: str
    benchmark: BenchmarkType
    category: QueryCategory

    expected_products: list[EvaluationProduct]
    retrieved_products: list[EvaluationProduct]

    hit_rate: float
    precision_at_k: float
    recall_at_k: float
    reciprocal_rank: float


@dataclass(frozen=True, slots=True)
class EvaluationSummary:
    """
    Aggregate retrieval evaluation metrics across the benchmark dataset.
    """

    average_hit_rate: float
    average_precision_at_k: float
    average_recall_at_k: float
    mean_reciprocal_rank: float

    results: list[EvaluationResult]