"""
Data models for end-to-end LLM evaluation.

These models represent the outputs of prompt strategy evaluation.
They are independent of any specific LLM provider or prompt template.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.llm.prompt_strategy import PromptStrategy

@dataclass(frozen=True, slots=True)
class LLMQueryEvaluation:
    """
    Evaluation result for a single benchmark query.
    """

    query_id: str

    query: str

    prompt_strategy: PromptStrategy

    answer: str

    groundedness: float

    answer_relevance: float

    semantic_similarity: float

    answer_correctness: float

    overall_score: float

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int

    estimated_cost: float

    confidence: float

    evaluation_reason: str


@dataclass(frozen=True, slots=True)
class PromptStrategySummary:
    """
    Aggregated metrics for one prompt strategy.
    """

    prompt_strategy: PromptStrategy

    query_results: list[LLMQueryEvaluation]

    average_groundedness: float

    average_answer_relevance: float

    average_semantic_similarity: float

    average_answer_correctness: float

    average_overall_score: float

    average_prompt_tokens: float

    average_completion_tokens: float

    average_total_tokens: float

    total_estimated_cost: float


@dataclass(frozen=True, slots=True)
class LLMEvaluationSummary:
    """
    Overall benchmark evaluation.
    """

    strategy_results: list[PromptStrategySummary]

    selected_prompt: PromptStrategy

    selection_reason: str


@dataclass(frozen=True, slots=True)
class JudgeResult:
    """
    Structured output returned by the LLM judge.

    This model represents the parsed JSON returned by the
    LLM-as-a-Judge before it is converted into a
    LLMQueryEvaluation.
    """

    groundedness: float

    answer_relevance: float

    semantic_similarity: float

    answer_correctness: float

    confidence: float

    evaluation_reason: str