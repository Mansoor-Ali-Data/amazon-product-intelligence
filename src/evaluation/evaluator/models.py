"""
Data models for retrieval evaluation.

These models represent the outputs of the retrieval evaluation
pipeline. They are independent of any specific vector database
or retrieval implementation.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.enums import QueryCategory


@dataclass(frozen=True, slots=True)
class RetrievedProduct:
    """
    Product returned by the retriever.
    """

    asin: str

    rank: int

    distance: float

    price: float | None

    rating: float | None


@dataclass(frozen=True, slots=True)
class QueryEvaluation:
    """
    Evaluation result for a single benchmark query.
    """

    query_id: str

    query: str

    category: QueryCategory

    retrieved_products: list[RetrievedProduct]

    expected_count: int

    retrieved_count: int

    relevant_retrieved: int

    recall_at_k: float

    precision_at_k: float

    hit_rate: bool

    reciprocal_rank: float


@dataclass(frozen=True, slots=True)
class EvaluationSummary:
    """
    Aggregated evaluation results across the benchmark dataset.
    """

    semantic_results: list[QueryEvaluation]

    metadata_results: list[MetadataEvaluation]

    total_semantic_queries: int

    total_metadata_queries: int

    average_recall_at_k: float

    average_precision_at_k: float

    hit_rate: float

    mean_reciprocal_rank: float

    average_constraint_accuracy: float

    metadata_pass_rate: float


@dataclass(frozen=True, slots=True)
class MetadataEvaluation:
    """
    Evaluation result for one metadata benchmark.
    """

    query_id: str

    query: str

    category: QueryCategory

    retrieved_products: list[RetrievedProduct]

    checked_products: int

    matching_products: int

    violations: int

    constraint_accuracy: float

    passed: bool