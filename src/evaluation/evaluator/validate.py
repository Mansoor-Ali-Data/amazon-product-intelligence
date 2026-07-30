"""
Validate the Retrieval Evaluation framework.

Runs smoke tests to ensure all evaluation components are
correctly configured and working together.
"""

from __future__ import annotations

from src.evaluation.benchmark import BENCHMARKS
from src.evaluation.evaluator.evaluator import RetrievalEvaluator
from src.evaluation.evaluator.reporter import EvaluationReporter
from src.evaluation.evaluator.writer import EvaluationWriter
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore


def _check(
    condition: bool,
    success: str,
    failure: str,
) -> None:
    """
    Print validation result.
    """

    if condition:
        print(f"✓ {success}")
    else:
        raise RuntimeError(failure)


def main() -> None:
    """
    Run retrieval evaluation validation.
    """

    print()
    print("=" * 100)
    print("Retrieval Evaluation Validation")
    print("=" * 100)
    print()

    # ---------------------------------------------------------
    # Benchmark Dataset
    # ---------------------------------------------------------

    _check(
        len(BENCHMARKS) > 0,
        f"Loaded {len(BENCHMARKS)} benchmark queries.",
        "Benchmark dataset is empty.",
    )

    # ---------------------------------------------------------
    # Vector Store
    # ---------------------------------------------------------

    vector_store = VectorStore()

    _check(
        vector_store is not None,
        "Vector store initialized.",
        "Failed to initialize vector store.",
    )

    # ---------------------------------------------------------
    # Retriever
    # ---------------------------------------------------------

    retriever = Retriever(
        vector_store=vector_store,
    )

    _check(
        retriever is not None,
        "Retriever initialized.",
        "Failed to initialize retriever.",
    )

    # ---------------------------------------------------------
    # Evaluator
    # ---------------------------------------------------------

    evaluator = RetrievalEvaluator(
        retriever=retriever,
    )

    summary = evaluator.evaluate_all()

    _check(
        len(summary.semantic_results)
        == summary.total_semantic_queries,
        "All semantic benchmarks evaluated.",
        "Semantic evaluation count mismatch.",
    )

    _check(
        len(summary.metadata_results)
        == summary.total_metadata_queries,
        "All metadata benchmarks evaluated.",
        "Metadata evaluation count mismatch.",
    )

    # ---------------------------------------------------------
    # Semantic Metric Checks
    # ---------------------------------------------------------

    print()
    print("Checking semantic metrics...")
    print()

    for result in summary.semantic_results:

        _check(
            0.0 <= result.precision_at_k <= 1.0,
            f"{result.query_id:<30} Precision@K",
            f"Invalid Precision@K for '{result.query_id}'.",
        )

        _check(
            0.0 <= result.recall_at_k <= 1.0,
            f"{result.query_id:<30} Recall@K",
            f"Invalid Recall@K for '{result.query_id}'.",
        )

        _check(
            isinstance(result.hit_rate, bool),
            f"{result.query_id:<30} Hit Rate",
            f"Invalid Hit Rate for '{result.query_id}'.",
        )

        _check(
            0.0 <= result.reciprocal_rank <= 1.0,
            f"{result.query_id:<30} Reciprocal Rank",
            f"Invalid Reciprocal Rank for '{result.query_id}'.",
        )

    # ---------------------------------------------------------
    # Metadata Metric Checks
    # ---------------------------------------------------------

    print()
    print("Checking metadata metrics...")
    print()

    for result in summary.metadata_results:

        _check(
            0.0 <= result.constraint_accuracy <= 1.0,
            f"{result.query_id:<30} Constraint Accuracy",
            f"Invalid Constraint Accuracy for '{result.query_id}'.",
        )

        _check(
            isinstance(result.passed, bool),
            f"{result.query_id:<30} Pass Status",
            f"Invalid pass status for '{result.query_id}'.",
        )

    # ---------------------------------------------------------
    # Summary Metrics
    # ---------------------------------------------------------

    print()
    print("Checking summary metrics...")
    print()

    _check(
        0.0 <= summary.average_precision_at_k <= 1.0,
        "Average Precision@K",
        "Invalid average Precision@K.",
    )

    _check(
        0.0 <= summary.average_recall_at_k <= 1.0,
        "Average Recall@K",
        "Invalid average Recall@K.",
    )

    _check(
        0.0 <= summary.hit_rate <= 1.0,
        "Average Hit Rate",
        "Invalid average Hit Rate.",
    )

    _check(
        0.0 <= summary.mean_reciprocal_rank <= 1.0,
        "Mean Reciprocal Rank",
        "Invalid Mean Reciprocal Rank.",
    )

    _check(
        0.0 <= summary.average_constraint_accuracy <= 1.0,
        "Average Constraint Accuracy",
        "Invalid average constraint accuracy.",
    )

    _check(
        0.0 <= summary.metadata_pass_rate <= 1.0,
        "Metadata Pass Rate",
        "Invalid metadata pass rate.",
    )

    # ---------------------------------------------------------
    # Reporter
    # ---------------------------------------------------------

    reporter = EvaluationReporter()

    report = reporter.generate(
        summary,
    )

    _check(
        len(report) > 0,
        "Report generated.",
        "Failed to generate report.",
    )

    # ---------------------------------------------------------
    # Writer
    # ---------------------------------------------------------

    writer = EvaluationWriter()

    report_path = writer.write_report(
        report,
        file_name="validation_report",
    )

    _check(
        report_path.exists(),
        f"Validation report written to '{report_path}'.",
        "Failed to write validation report.",
    )

    print()
    print("=" * 100)
    print("Validation Passed")
    print("=" * 100)


if __name__ == "__main__":
    main()