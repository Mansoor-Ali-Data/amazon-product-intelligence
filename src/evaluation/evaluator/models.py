"""
Data models for retrieval evaluation.

These models represent the outputs of the retrieval evaluation
pipeline. They are independent of any specific vector database
or retrieval implementation.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.enums import QueryCategory


# ----------------------------------------------------------------------
# Retrieved Products
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RetrievedProduct:
    """
    Product returned by a retriever.
    """

    asin: str

    rank: int

    distance: float

    price: float | None

    rating: float | None


# ----------------------------------------------------------------------
# Semantic Evaluation
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class QueryEvaluation:
    """
    Evaluation result for a single semantic benchmark query.
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


# ----------------------------------------------------------------------
# Metadata Evaluation
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MetadataEvaluation:
    """
    Evaluation result for a single metadata benchmark query.
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


# ----------------------------------------------------------------------
# Retrieval Method Summary
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RetrievalMethodSummary:
    """
    Aggregated evaluation results for one retrieval method.

    Examples
    --------
    - Dense
    - BM25
    - Hybrid
    """

    retrieval_method: str

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


# ----------------------------------------------------------------------
# Overall Evaluation Summary
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class EvaluationSummary:
    """
    Comparison of multiple retrieval methods.
    """

    retrieval_methods: list[RetrievalMethodSummary]