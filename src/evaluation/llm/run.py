"""
Entry point for LLM evaluation.

Runs the complete prompt strategy benchmark,
generates a human-readable report, and writes
the results to disk.

Responsibilities
----------------
- Execute the LLM evaluation pipeline.
- Generate the evaluation report.
- Persist the report.

This module performs orchestration only.
"""


from __future__ import annotations

from config.logging import get_logger

from src.evaluation.llm.evaluator import LLMEvaluator
from src.evaluation.llm.reporter import LLMEvaluationReporter
from src.evaluation.llm.writer import EvaluationWriter

logger = get_logger(__name__)


def main() -> None:
    """
    Run the complete LLM evaluation pipeline.
    """

    logger.info(
        "Starting LLM evaluation."
    )

    evaluator = LLMEvaluator()

    reporter = LLMEvaluationReporter()

    write = EvaluationWriter()

    summary = evaluator.evaluate_all()

    report = reporter.generate(
        summary,
    )

    write.write_report(
        report=report,
        file_name="llm_evaluation_report",
    )

    logger.info(
        "LLM evaluation completed successfully."
    )

    print()

    print("=" * 80)

    print("LLM evaluation completed successfully.")

    print(
        "Report saved to "
        "outputs/evaluation/llm_evaluation_report.txt"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()