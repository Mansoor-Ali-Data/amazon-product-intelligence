"""
Utilities for manual validation of LLM-as-a-Judge evaluations.

The validator helps engineers inspect the quality of the judge by
sampling representative evaluation results.

Responsibilities
----------------
- Surface the highest-scoring evaluations.
- Surface the lowest-scoring evaluations.
- Select random evaluation samples.
- Support manual inspection of judge reasoning.

This module performs no evaluation or scoring.
"""

from __future__ import annotations

import random

from src.evaluation.llm.models import (
    LLMEvaluationSummary,
    LLMQueryEvaluation,
)

class LLMValidator:
    """
    Utilities for manually validating LLM judge outputs.
    """


    def validate(
        self,
        summary: LLMEvaluationSummary,
        *,
        top_n: int = 5,
        random_n: int = 5,
    ) -> str:
        """
        Generate a manual validation report.
        """

    def validate(
        self,
        summary: LLMEvaluationSummary,
        *,
        top_n: int = 5,
        random_n: int = 5,
    ) -> str:

        evaluations = []

        for strategy in summary.strategy_results:

            evaluations.extend(
                strategy.query_results
            )

        lines = []

        lines.append("=" * 100)
        lines.append("LLM Judge Manual Validation")
        lines.append("=" * 100)
        lines.append("")

        lines.extend(
            self._section(
                "Highest Scoring Evaluations",
                self.sample_best(
                    evaluations,
                    top_n,
                ),
            )
        )

        lines.extend(
            self._section(
                "Lowest Scoring Evaluations",
                self.sample_worst(
                    evaluations,
                    top_n,
                ),
            )
        )

        lines.extend(
            self._section(
                "Random Evaluation Samples",
                self.sample_random(
                    evaluations,
                    random_n,
                ),
            )
        )

        return "\n".join(lines)


    def sample_best(
        self,
        evaluations: list[LLMQueryEvaluation],
        n: int,
    ) -> list[LLMQueryEvaluation]:
        """
        Return the highest scoring evaluations.
        """

        return sorted(
            evaluations,
            key=lambda result: result.overall_score,
            reverse=True,
        )[:n]

    def sample_best(
        self,
        evaluations: list[LLMQueryEvaluation],
        n: int,
    ) -> list[LLMQueryEvaluation]:
        """
        Return the highest scoring evaluations.
        """

        return sorted(
            evaluations,
            key=lambda result: result.overall_score,
            reverse=True,
        )[:n]


    def _section(
        self,
        title: str,
        evaluations: list[LLMQueryEvaluation],
    ) -> list[str]:
        """
        Format one validation section.
        """

        lines = []

        lines.append("=" * 100)
        lines.append(title)
        lines.append("=" * 100)
        lines.append("")

        for evaluation in evaluations:

            lines.extend(
                self._evaluation(
                    evaluation,
                )
            )

        return lines


    def _evaluation(
        self,
        evaluation: LLMQueryEvaluation,
    ) -> list[str]:
        """
        Format one evaluation for manual review.
        """

        return [
            f"Query ID           : {evaluation.query_id}",
            f"Prompt Strategy    : {evaluation.prompt_strategy.value}",
            f"Query              : {evaluation.query}",
            "",
            f"Overall Score      : {evaluation.overall_score:.3f}",
            f"Groundedness       : {evaluation.groundedness:.3f}",
            f"Answer Relevance   : {evaluation.answer_relevance:.3f}",
            f"Semantic Similarity: {evaluation.semantic_similarity:.3f}",
            f"Answer Correctness : {evaluation.answer_correctness:.3f}",
            f"Confidence         : {evaluation.confidence:.3f}",
            "",
            "Generated Answer",
            "-" * 100,
            evaluation.answer,
            "",
            "Judge Reasoning",
            "-" * 100,
            evaluation.evaluation_reason,
            "",
            "=" * 100,
            "",
        ]