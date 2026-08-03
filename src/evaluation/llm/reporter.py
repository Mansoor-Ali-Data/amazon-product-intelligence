"""
Reporting utilities for LLM evaluation.

Formats prompt strategy evaluation results into a
human-readable report suitable for benchmarking,
comparison, and manual review.

Responsibilities
----------------
- Present strategy-level evaluation summaries.
- Compare prompt strategies side-by-side.
- Display the selected prompt strategy and justification.
- Format query-level evaluation results.
- Report token usage and estimated inference cost.

This module performs presentation only.

"""
from __future__ import annotations

from src.evaluation.llm.models import (
    LLMEvaluationSummary,
    LLMQueryEvaluation,
    PromptStrategySummary,
)
from src.evaluation.llm.prompt_strategy import (
    PromptStrategy,
)

class LLMEvaluationReporter:
    """
    Formats LLM evaluation results.
    """

    LINE_WIDTH = 100


    def generate(
        self,
        summary: LLMEvaluationSummary,
    ) -> str:
        """
        Generate a complete LLM evaluation report.
        """

        lines: list[str] = []

        lines.append("=" * self.LINE_WIDTH)
        lines.append("LLM Evaluation Report")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        # ---------------------------------------------------------
        # Strategy summaries
        # ---------------------------------------------------------

        for strategy in summary.strategy_results:

            lines.extend(
                self._strategy_summary(
                    strategy,
                )
            )

            lines.append("")

        # ---------------------------------------------------------
        # Comparison
        # ---------------------------------------------------------

        lines.append("=" * self.LINE_WIDTH)
        lines.append("Prompt Strategy Comparison")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        lines.extend(
            self._comparison(
                summary,
            )
        )

        lines.append("")

        # ---------------------------------------------------------
        # Winner
        # ---------------------------------------------------------

        lines.append("=" * self.LINE_WIDTH)
        lines.append("Selected Prompt Strategy")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        lines.extend(
            self._selected_prompt(
                summary,
            )
        )

        # ---------------------------------------------------------
        # Query Results
        # ---------------------------------------------------------

        for strategy in summary.strategy_results:

            lines.append("")
            lines.append("=" * self.LINE_WIDTH)

            lines.append(
                f"{strategy.prompt_strategy.value.title()} Query Results"
            )

            lines.append("=" * self.LINE_WIDTH)
            lines.append("")

            for result in strategy.query_results:

                lines.extend(
                    self._query_result(
                        result,
                    )
                )

        return "\n".join(lines)

    def _strategy_summary(
        self,
        summary: PromptStrategySummary,
    ) -> list[str]:
        """
        Format one prompt strategy summary.
        """

        return [
            "=" * self.LINE_WIDTH,
            f"{summary.prompt_strategy.value.title()} Summary",
            "=" * self.LINE_WIDTH,
            "",
            f"Queries                     : {len(summary.query_results)}",
            f"Groundedness                : {summary.average_groundedness:.3f}",
            f"Answer Relevance            : {summary.average_answer_relevance:.3f}",
            f"Semantic Similarity         : {summary.average_semantic_similarity:.3f}",
            f"Answer Correctness          : {summary.average_answer_correctness:.3f}",
            f"Overall Score              : {summary.average_overall_score:.3f}",
            f"Average Prompt Tokens      : {summary.average_prompt_tokens:.1f}",
            f"Average Completion Tokens  : {summary.average_completion_tokens:.1f}",
            f"Average Total Tokens       : {summary.average_total_tokens:.1f}",
            f"Total Estimated Cost       : {self._format_cost(summary.total_estimated_cost)}",
        ]  

    def _comparison(
        self,
        summary: LLMEvaluationSummary,
    ) -> list[str]:
        """
        Compare prompt strategies.
        """

        lines: list[str] = []

        strategies = {
            result.prompt_strategy: result
            for result in summary.strategy_results
        }

        baseline = strategies[PromptStrategy.BASELINE]
        structured = strategies[PromptStrategy.STRUCTURED]

        header = (
            f"{'Metric':<30}"
            f"{'Baseline':>15}"
            f"{'Structured':>15}"
        )

        lines.append(header)
        lines.append("-" * len(header))

        rows = [
            (
                "Groundedness",
                baseline.average_groundedness,
                structured.average_groundedness,
            ),
            (
                "Answer Relevance",
                baseline.average_answer_relevance,
                structured.average_answer_relevance,
            ),
            (
                "Semantic Similarity",
                baseline.average_semantic_similarity,
                structured.average_semantic_similarity,
            ),
            (
                "Answer Correctness",
                baseline.average_answer_correctness,
                structured.average_answer_correctness,
            ),
            (
                "Overall Score",
                baseline.average_overall_score,
                structured.average_overall_score,
            ),
        ]

        for metric, base, structured_value in rows:

            lines.append(
                f"{metric:<30}"
                f"{base:>15.3f}"
                f"{structured_value:>15.3f}"
            )

        lines.append("")
        lines.append(
            f"{'Total Cost':<30}"
            f"{self._format_cost(baseline.total_estimated_cost):>15}"
            f"{self._format_cost(structured.total_estimated_cost):>15}"
        )

        return lines  

    def _selected_prompt(
        self,
        summary: LLMEvaluationSummary,
    ) -> list[str]:
        """
        Format selected prompt strategy.
        """

        return [
            f"Winner : {summary.selected_prompt.value}",
            "",
            "Reason",
            "-" * self.LINE_WIDTH,
            summary.selection_reason,
        ]
    

    def _query_result(
        self,
        evaluation: LLMQueryEvaluation,
    ) -> list[str]:
        """
        Format one query evaluation.
        """

        lines: list[str] = []

        lines.append(f"Query ID          : {evaluation.query_id}")
        lines.append(f"Prompt Strategy   : {evaluation.prompt_strategy.value}")
        lines.append(f"Query             : {evaluation.query}")

        lines.append("")

        lines.append("Evaluation Metrics")
        lines.append("-" * self.LINE_WIDTH)

        lines.append(
            f"Groundedness            : {evaluation.groundedness:.3f}"
        )

        lines.append(
            f"Answer Relevance        : {evaluation.answer_relevance:.3f}"
        )

        lines.append(
            f"Semantic Similarity     : {evaluation.semantic_similarity:.3f}"
        )

        lines.append(
            f"Answer Correctness      : {evaluation.answer_correctness:.3f}"
        )

        lines.append(
            f"Overall Score           : {evaluation.overall_score:.3f}"
        )

        lines.append(
            f"Confidence              : {evaluation.confidence:.3f}"
        )

        lines.append("")

        lines.append("Token Usage")
        lines.append("-" * self.LINE_WIDTH)

        lines.append(
            f"Prompt Tokens           : {evaluation.prompt_tokens}"
        )

        lines.append(
            f"Completion Tokens       : {evaluation.completion_tokens}"
        )

        lines.append(
            f"Total Tokens            : {evaluation.total_tokens}"
        )

        lines.append(
            f"Estimated Cost          : {self._format_cost(evaluation.estimated_cost)}"
        )

        lines.append("")

        lines.append("Judge Reasoning")
        lines.append("-" * self.LINE_WIDTH)

        lines.append(evaluation.evaluation_reason)

        lines.append("")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        return lines


    @staticmethod
    def _format_cost(
        cost: float,
    ) -> str:
        """
        Format estimated inference cost.
        """

        return f"${cost:.6f}"