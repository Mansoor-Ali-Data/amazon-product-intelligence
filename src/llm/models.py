"""
Domain models for LLM inference.

These models represent structured responses returned by
language models and are shared across the RAG pipeline,
evaluation framework, and monitoring components.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LLMResponse:
    """
    Structured response returned by an LLM.

    Attributes
    ----------
    text:
        Generated response.

    prompt_tokens:
        Number of prompt tokens.

    completion_tokens:
        Number of generated tokens.

    total_tokens:
        Total token usage.

    estimated_cost:
        Estimated inference cost in USD.

    latency_seconds:
        End-to-end inference latency.

    model_name:
        Model used for generation.

    finish_reason:
        Model termination reason.
    """

    text: str

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int

    estimated_cost: float

    latency_seconds: float

    model_name: str

    finish_reason: str | None = None


@property
def latency_ms(
    self,
) -> float:
    """
    Inference latency expressed in milliseconds.

    This convenience property avoids repeated conversions
    from seconds to milliseconds throughout the application.
    """

    return self.latency_seconds * 1000