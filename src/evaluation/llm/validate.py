"""
Validation entry point for the LLM evaluation subsystem.

Runs a lightweight end-to-end validation to ensure all major
components of the LLM evaluation pipeline are correctly
integrated.

Responsibilities
----------------
- Execute a single prompt strategy evaluation.
- Validate RAG pipeline execution.
- Validate prompt construction.
- Validate LLM judge integration.
- Validate report generation.

This module is intended for development and integration
testing. It does NOT execute the complete benchmark.
"""

from __future__ import annotations

from config.logging import get_logger

from src.evaluation.llm.evaluator import LLMEvaluator
from src.evaluation.llm.prompt_strategy import PromptStrategy
from src.evaluation.llm.reporter import LLMEvaluationReporter

logger = get_logger(__name__)



def main() -> None:
    """
    Run a lightweight validation of the LLM evaluation
    subsystem.
    """

    logger.info(
        "Starting LLM evaluation validation."
    )

    evaluator = LLMEvaluator()

    reporter = LLMEvaluationReporter()

    logger.info(
        "Validating '%s' prompt strategy.",
        PromptStrategy.BASELINE.value,
    )

    strategy_summary = evaluator._evaluate_strategy(
        PromptStrategy.BASELINE,
    )

    report_lines = reporter._strategy_summary(
        strategy_summary,
    )

    # ---------------------------------------------------------
    # Assertions
    # ---------------------------------------------------------
    assert (
        strategy_summary.total_queries == 6
    ), "Unexpected number of benchmark queries."

    assert (
        0.0
        <= strategy_summary.average_groundedness
        <= 1.0
    ), "Groundedness score out of range."

    assert (
        0.0
        <= strategy_summary.average_answer_relevance
        <= 1.0
    ), "Answer relevance score out of range."

    assert (
        0.0
        <= strategy_summary.average_semantic_similarity
        <= 1.0
    ), "Semantic similarity score out of range."

    assert (
        0.0
        <= strategy_summary.average_answer_correctness
        <= 1.0
    ), "Answer correctness score out of range."

    assert (
        0.0
        <= strategy_summary.overall_score
        <= 1.0
    ), "Overall score out of range."

    assert (
        strategy_summary.average_prompt_tokens > 0
    ), "Prompt token count must be positive."

    assert (
        strategy_summary.average_completion_tokens > 0
    ), "Completion token count must be positive."

    assert (
        strategy_summary.average_total_tokens > 0
    ), "Total token count must be positive."

    assert (
        strategy_summary.total_estimated_cost > 0.0
    ), "Estimated cost must be positive."
    

    print()

    print("=" * 80)
    print("LLM Evaluation Validation")
    print("=" * 80)
    print()

    print(
        f"Prompt Strategy : {PromptStrategy.BASELINE.value}"
    )

    print()

    print("\n".join(report_lines))

    print()

    print("=" * 80)
    print("Validation completed successfully.")
    print("=" * 80)

    logger.info(
        "LLM evaluation validation completed successfully."
    )


if __name__ == "__main__":
    main()