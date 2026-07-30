"""
Entry point for retrieval evaluation.
"""

from __future__ import annotations

from src.evaluation.evaluator.evaluator import RetrievalEvaluator
from src.evaluation.evaluator.reporter import EvaluationReporter
from src.evaluation.evaluator.writer import EvaluationWriter
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore


def main() -> None:
    """
    Run the retrieval evaluation pipeline.
    """

    print()
    print("=" * 100)
    print("Retrieval Evaluation")
    print("=" * 100)
    print()

    # ---------------------------------------------------------
    # Initialize Components
    # ---------------------------------------------------------

    print("Loading vector store...")

    vector_store = VectorStore()

    print("Initializing retriever...")

    retriever = Retriever(
        vector_store=vector_store,
    )

    print("Initializing evaluator...")

    evaluator = RetrievalEvaluator(
        retriever=retriever,
    )

    print("Running benchmark evaluation...")
    print()

    # ---------------------------------------------------------
    # Run Evaluation
    # ---------------------------------------------------------

    summary = evaluator.evaluate_all()

    # ---------------------------------------------------------
    # Generate Report
    # ---------------------------------------------------------

    reporter = EvaluationReporter()

    report = reporter.generate(
        summary,
    )

    # ---------------------------------------------------------
    # Write Report
    # ---------------------------------------------------------

    writer = EvaluationWriter()

    report_path = writer.write_report(
        report=report,
    )

    # ---------------------------------------------------------
    # Display Results
    # ---------------------------------------------------------

    print(report)

    print()
    print("=" * 100)
    print("Evaluation Complete")
    print("=" * 100)
    print(f"Report saved to: {report_path}")
    print()


if __name__ == "__main__":
    main()