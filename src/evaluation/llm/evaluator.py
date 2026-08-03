"""
Responsibilities:
- Evaluate the complete RAG pipeline using benchmark queries.
- Execute the RAG pipeline for each prompt strategy.
- Invoke the LLM-as-a-Judge to evaluate generated answers.
- Aggregate query-level evaluation metrics into strategy-level summaries.
- Compare prompt strategies and select the best-performing prompt.
"""


from __future__ import annotations

from statistics import mean

from config.logging import get_logger

from src.evaluation.benchmark import BENCHMARKS
from src.evaluation.benchmark_models import BenchmarkQuery
from src.evaluation.llm.judge import LLMJudge
from src.evaluation.llm.models import (
    LLMEvaluationSummary,
    LLMQueryEvaluation,
    PromptStrategySummary,
)
from src.evaluation.llm.prompt_strategy import PromptStrategy
from src.pipeline.rag_pipeline import RAGPipeline

logger = get_logger(__name__)


class LLMEvaluator:
    """
    Evaluate the complete RAG pipeline using an LLM-as-a-Judge.
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize evaluation components.
        """

        self._pipeline = RAGPipeline()

        self._judge = LLMJudge()    


    def evaluate_all(
        self,
    )  -> LLMEvaluationSummary:
        """
        Evaluate every prompt strategy.
        """

        logger.info(
            "Starting LLM evaluation."
        )

        strategy_results = []

        for strategy in PromptStrategy:

            logger.info(
                "Evaluating '%s' prompt strategy.",
                strategy.value,
            )

            strategy_results.append(
                self._evaluate_strategy(
                    strategy,
                )
            )

        selected_prompt, selection_reason = (
            self._select_best_prompt(
                strategy_results,
            )
        )

        logger.info(
            "LLM evaluation completed."
        )

        return LLMEvaluationSummary(
            strategy_results=strategy_results,
            selected_prompt=selected_prompt,
            selection_reason=selection_reason,
        )


    def _evaluate_strategy(
        self,
        strategy: PromptStrategy,
    ) -> PromptStrategySummary:
        """
        Evaluate one prompt strategy.
        """

        query_results = []

        benchmarks = [
            benchmark
            for benchmark in BENCHMARKS
            if benchmark.ground_truth_answer is not None
        ]

        for benchmark in benchmarks:

            query_results.append(
                self._evaluate_query(
                    benchmark,
                    strategy,
                )
            )

        return self._build_summary(
            strategy,
            query_results,
        )

    def _evaluate_query(
        self,
        benchmark: BenchmarkQuery,
        strategy: PromptStrategy,
    ) -> LLMQueryEvaluation:
        """
        Evaluate one benchmark query.
        """

        rag_response = self._pipeline.ask(
            query=benchmark.query,
            prompt_strategy=strategy,
        )

        retrieved_context = "\n\n".join(
            chunk.text
            for chunk in rag_response.retrieved_chunks
        )

        return self._judge.evaluate(
            query_id=benchmark.query_id,
            query=benchmark.query,
            retrieved_context=retrieved_context,
            ground_truth_answer=benchmark.ground_truth_answer,
            llm_response=rag_response.llm_response,
            prompt_strategy=strategy,
        )

    def _build_summary(
        self,
        strategy: PromptStrategy,
        query_results: list[LLMQueryEvaluation],
    ) -> PromptStrategySummary:
        """
        Aggregate query evaluation results.
        """

        return PromptStrategySummary(
            prompt_strategy=strategy,
            query_results=query_results,
            average_groundedness=mean(
                r.groundedness
                for r in query_results
            ),
            average_answer_relevance=mean(
                r.answer_relevance
                for r in query_results
            ),
            average_semantic_similarity=mean(
                r.semantic_similarity
                for r in query_results
            ),
            average_answer_correctness=mean(
                r.answer_correctness
                for r in query_results
            ),
            average_overall_score=mean(
                r.overall_score
                for r in query_results
            ),
            average_prompt_tokens=mean(
                r.prompt_tokens
                for r in query_results
            ),
            average_completion_tokens=mean(
                r.completion_tokens
                for r in query_results
            ),
            average_total_tokens=mean(
                r.total_tokens
                for r in query_results
            ),
            total_estimated_cost=sum(
                r.estimated_cost
                for r in query_results
            ),
        )


    def _select_best_prompt(
        self,
        summaries: list[PromptStrategySummary],
    ) -> tuple[PromptStrategy, str]:
        """
        Select the best prompt strategy.
        """

        max_cost = max(
            summary.total_estimated_cost
            for summary in summaries
        )

        scored = []

        for summary in summaries:

            if max_cost == 0:

                cost_score = 1.0

            else:

                cost_score = (
                    1.0
                    - (
                        summary.total_estimated_cost
                        / max_cost
                    )
                )

            score = (
                0.50 * summary.average_overall_score
                + 0.25 * summary.average_groundedness
                + 0.15 * summary.average_answer_correctness
                + 0.10 * cost_score
            )

            scored.append(
                (
                    score,
                    summary,
                )
            )

        _, winner = max(
            scored,
            key=lambda item: item[0],
        )

        reason = (
            f"Selected '{winner.prompt_strategy.value}' "
            "because it achieved the highest weighted "
            "evaluation score while balancing answer "
            "quality, groundedness, correctness, and "
            "cost efficiency."
        )

        return (
            winner.prompt_strategy,
            reason,
        )