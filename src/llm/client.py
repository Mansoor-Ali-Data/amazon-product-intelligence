"""
LLM client implementation.

Responsibilities
----------------
- Initialize the configured LLM provider
- Send prompts to the model
- Return generated text

This module hides provider-specific implementation details
from the rest of the application.
"""

from __future__ import annotations

from google import genai
from google.genai import types

from config.logging import get_logger

from .config import (
    LLMConfig,
    load_llm_config,
)

logger = get_logger(__name__)


class LLMClient:
    """
    Client for interacting with the configured LLM provider.
    """

    def __init__(self) -> None:
        """
        Initialize the LLM client.
        """

        self._config: LLMConfig = load_llm_config()

        self._client = genai.Client(
            api_key=self._config.api_key,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response for a prompt.

        Args:
            prompt:
                Fully formatted prompt.

        Returns:
            Generated response text.
        """

        logger.info(
            "Generating response using model '%s'.",
            self._config.model,
        )

        try:

            response = self._client.models.generate_content(
                model=self._config.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=self._config.temperature,
                    max_output_tokens=self._config.max_output_tokens,
                ),
            )

            logger.info("LLM response generated successfully.")

            return response.text.strip()

        except Exception:

            logger.exception(
                "LLM generation failed."
            )

            raise