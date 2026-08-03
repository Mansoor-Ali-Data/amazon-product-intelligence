"""
LLM-as-a-Judge for end-to-end RAG evaluation.

The judge evaluates a single generated answer using a strict
RAG evaluation rubric. It is responsible only for scoring one
answer and returning structured evaluation results.

Responsibilities
----------------
- Build the judge prompt
- Invoke the LLM judge
- Parse structured evaluation
- Compute overall evaluation score

This module does NOT:
- Retrieve documents
- Execute the RAG pipeline
- Aggregate benchmark results
- Produce reports
"""

from __future__ import annotations

import json


from config.logging import get_logger

from src.evaluation.llm.models import (
    JudgeResult,
    LLMQueryEvaluation,
)

from src.llm.models import LLMResponse

from src.evaluation.llm.prompt_strategy import (
    PromptStrategy,
)
from src.llm.client import LLMClient

from src.evaluation.llm.judge_template import JUDGE_TEMPLATE

from src.llm.models import LLMResponse

logger = get_logger(__name__)


class LLMJudge:
    """
    Evaluate generated answers using an LLM-as-a-Judge.
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the LLM judge.
        """

        self._llm = LLMClient()

    def evaluate(
        self,
        *,
        query_id: str,
        query: str,
        retrieved_context: str,
        ground_truth_answer: str,
        llm_response: LLMResponse,
        prompt_strategy: PromptStrategy,
    ) -> LLMQueryEvaluation:
        """
        Evaluate one generated answer.

        Args:
            query_id:
                Benchmark query identifier.

            query:
                User query.

            retrieved_context:
                Context supplied to the RAG pipeline.

            ground_truth_answer:
                Reference answer.

            generated_answer:
                Answer produced by the RAG system.

            prompt_strategy:
                Prompt strategy being evaluated.

        Returns:
            Structured evaluation result.
        """

        logger.info(
            "Evaluating query '%s' using '%s' strategy.",
            query_id,
            prompt_strategy.value,
        )

        judge_prompt = self._build_prompt(
            query=query,
            retrieved_context=retrieved_context,
            ground_truth_answer=ground_truth_answer,
            generated_answer=llm_response.text,
        )

        llm_response = self._call_judge(
            judge_prompt,
        )

        judge_result = self._parse_response(
            llm_response.text,
        )

        overall_score = self._calculate_overall_score(
            groundedness=judge_result.groundedness,
            answer_relevance=judge_result.answer_relevance,
            semantic_similarity=judge_result.semantic_similarity,
            answer_correctness=judge_result.answer_correctness,
        )

        return LLMQueryEvaluation(
            query_id=query_id,
            query=query,
            prompt_strategy=prompt_strategy,
            answer=llm_response.text,
            groundedness=judge_result.groundedness,
            answer_relevance=judge_result.answer_relevance,
            semantic_similarity=judge_result.semantic_similarity,
            answer_correctness=judge_result.answer_correctness,
            overall_score=overall_score,
            prompt_tokens=llm_response.prompt_tokens,
            completion_tokens=llm_response.completion_tokens,
            total_tokens=llm_response.total_tokens,
            estimated_cost=llm_response.estimated_cost,
            confidence=judge_result.confidence,
            evaluation_reason=judge_result.evaluation_reason,
        )

    def _build_prompt(
        self,
        *,
        query: str,
        retrieved_context: str,
        ground_truth_answer: str,
        generated_answer: str,
    ) -> str:
        """
        Build the judge prompt.
        """

        return JUDGE_TEMPLATE.substitute(
            user_query=query,
            retrieved_context=retrieved_context,
            ground_truth_answer=ground_truth_answer,
            generated_answer=generated_answer,
        )

    def _call_judge(
        self,
        prompt: str,
    ) -> LLMResponse:
        """
        Invoke the LLM judge.
        """

        return self._llm.generate(
            prompt,
        )

    def _parse_response(
    self,
    response: str,
    ) -> JudgeResult:
        """
        Parse the structured JSON returned by the LLM judge.
        """

        try:
            data = json.loads(response)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Judge returned invalid JSON."
            ) from exc

        required_fields = (
            "groundedness",
            "answer_relevance",
            "semantic_similarity",
            "answer_correctness",
            "confidence",
            "evaluation_reason",
        )

        missing = [
            field
            for field in required_fields
            if field not in data
        ]

        if missing:
            raise ValueError(
                f"Judge response missing fields: {missing}"
            )

        # ---------------------------------------------------------
        # Validate metric ranges
        # ---------------------------------------------------------
        for metric in (
            "groundedness",
            "answer_relevance",
            "semantic_similarity",
            "answer_correctness",
            "confidence",
        ):
            value = float(data[metric])

            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"{metric} must be between 0.0 and 1.0."
                )
        return JudgeResult(
            groundedness=float(data["groundedness"]),
            answer_relevance=float(data["answer_relevance"]),
            semantic_similarity=float(data["semantic_similarity"]),
            answer_correctness=float(data["answer_correctness"]),
            confidence=float(data["confidence"]),
            evaluation_reason=str(data["evaluation_reason"]),
        )

    @staticmethod
    def _calculate_overall_score(
        *,
        groundedness: float,
        answer_relevance: float,
        semantic_similarity: float,
        answer_correctness: float,
    ) -> float:
        """
        Compute weighted overall evaluation score.
        """

        score = (
            0.40 * groundedness
            + 0.30 * answer_correctness
            + 0.20 * answer_relevance
            + 0.10 * semantic_similarity
        )

        return round(score, 3)