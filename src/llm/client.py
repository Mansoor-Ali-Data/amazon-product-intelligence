"""
LLM client implementation.

Responsibilities
----------------
- Initialize the configured LLM provider.
- Send prompts to the configured language model.
- Capture inference metadata.
- Estimate inference cost.
- Return a structured LLM response.
"""

from __future__ import annotations

from time import perf_counter

from google import genai
from google.genai import types

from config.logging import get_logger

from src.llm.models import LLMResponse
from src.llm.rate_limiter import ( 
                          RateLimiter, 
                          get_rate_limiter)

from .config import (
    LLMConfig,
    LLMPricing,
    load_llm_config,
)

logger = get_logger(__name__)


class LLMClient:
    """
    Client for interacting with the configured LLM provider.
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the LLM client.
        """

        self._config: LLMConfig = load_llm_config()

        self._client = genai.Client(
            api_key=self._config.api_key,

        )

        self._rate_limiter = get_rate_limiter(
            self._config.rate_limit.requests_per_minute,
        )

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:
        """
        Generate a response for a prompt.

        Args:
            prompt:
                Fully formatted prompt.

        Returns:
            Structured LLM response.
        """

        logger.info(
            "Generating response using model '%s'.",
            self._config.model,
        )

        logger.info(
            "Waiting for rate limiter..."
        )

        self._rate_limiter.acquire()

        logger.info(
            "Rate limiter granted request."
        )

        start_time = perf_counter()

        try:
            self._rate_limiter.acquire()
            response = self._client.models.generate_content(
                model=self._config.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=self._config.temperature,
                    max_output_tokens=self._config.max_output_tokens,
                ),
            )

            latency = perf_counter() - start_time

            usage = response.usage_metadata

            prompt_tokens = (
                usage.prompt_token_count
                if usage is not None
                else 0
            )

            completion_tokens = (
                usage.candidates_token_count
                if usage is not None
                else 0
            )

            total_tokens = (
                usage.total_token_count
                if usage is not None
                else 0
            )

            finish_reason = None

            if response.candidates:

                candidate = response.candidates[0]

                if candidate.finish_reason is not None:

                    finish_reason = (
                        candidate.finish_reason.name
                    )

            logger.info(
                "LLM response generated successfully."
            )
            logger.info(
                (
                    "LLM usage | "
                    "Prompt=%d | "
                    "Completion=%d | "
                    "Total=%d | "
                    "Cost=$%.6f | "
                    "Latency=%.2fs"
                ),
                prompt_tokens,
                completion_tokens,
                total_tokens,
                self._estimate_cost(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                ),
                latency,
            )
            return LLMResponse(
                text=response.text,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                estimated_cost=self._estimate_cost(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                ),
                latency_seconds=latency,
                model_name=self._config.model,
                finish_reason=finish_reason,
            )

        except Exception:

            logger.exception(
                "LLM generation failed."
            )

            raise

    def _estimate_cost(
        self,
        *,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> float:
        """
        Estimate inference cost in USD.
        """

        input_cost = (
            prompt_tokens
            / 1_000_000
        ) * (
            self._config.pricing.input_per_million_tokens
        )

        output_cost = (
            completion_tokens
            / 1_000_000
        ) * (
            self._config.pricing.output_per_million_tokens
        )

        return input_cost + output_cost