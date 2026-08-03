"""
Run retrieval evaluation.

Evaluates all retrieval methods, generates a comparison report,
and writes the report to disk.
"""

from __future__ import annotations

from src.bm25_store.store import BM25Store
from src.evaluation.evaluator.evaluator import RetrievalEvaluator
from src.evaluation.evaluator.metadata_evaluation import MetadataEvaluator
from src.evaluation.evaluator.reporter import EvaluationReporter
from src.evaluation.evaluator.semantic_evaluation import SemanticEvaluator
from src.evaluation.evaluator.writer import EvaluationWriter
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.fusion import ReciprocalRankFusion
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore


def main() -> None:
    """
    Execute retrieval evaluation.
    """

    # ------------------------------------------------------------------
    # Build Retrievers
    # ------------------------------------------------------------------

    dense_retriever = Retriever(
        vector_store=VectorStore(),
    )

    bm25_retriever = BM25Retriever(
        store=BM25Store(),
    )

    hybrid_retriever = HybridRetriever(
        dense_retriever=dense_retriever,
        bm25_retriever=bm25_retriever,
        fusion=ReciprocalRankFusion(),
    )

    # ------------------------------------------------------------------
    # Semantic Evaluators
    # ------------------------------------------------------------------

    semantic_evaluators = [

        SemanticEvaluator(
            retriever=dense_retriever,
            retrieval_method="Dense",
        ),

        SemanticEvaluator(
            retriever=bm25_retriever,
            retrieval_method="BM25",
        ),

        SemanticEvaluator(
            retriever=hybrid_retriever,
            retrieval_method="Hybrid",
        ),
    ]

    # ------------------------------------------------------------------
    # Metadata Evaluators
    # ------------------------------------------------------------------

    metadata_evaluators = [

        MetadataEvaluator(
            retriever=dense_retriever,
            retrieval_method="Dense",
        ),

        MetadataEvaluator(
            retriever=bm25_retriever,
            retrieval_method="BM25",
        ),

        MetadataEvaluator(
            retriever=hybrid_retriever,
            retrieval_method="Hybrid",
        ),
    ]

    # ------------------------------------------------------------------
    # Evaluate
    # ------------------------------------------------------------------

    evaluator = RetrievalEvaluator(
        semantic_evaluators=semantic_evaluators,
        metadata_evaluators=metadata_evaluators,
    )

    summary = evaluator.evaluate_all()

    # ------------------------------------------------------------------
    # Generate Report
    # ------------------------------------------------------------------

    reporter = EvaluationReporter()

    report = reporter.generate(
        summary,
    )

    # ------------------------------------------------------------------
    # Persist Report
    # ------------------------------------------------------------------

    writer = EvaluationWriter()

    writer.write_report(
        report,
    )

    print(report)


if __name__ == "__main__":
    main()