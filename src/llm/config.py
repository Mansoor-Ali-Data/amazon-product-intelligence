"""
Configuration utilities for the LLM client.

Responsibilities
----------------
- Load LLM configuration
- Read environment variables
- Provide a strongly typed configuration object

This module performs no model initialization or inference.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from config.loader import load_yaml


@dataclass(frozen=True, slots=True)
class RateLimitConfig:
    """
    LLM API rate limit configuration.
    """

    requests_per_minute: int

@dataclass(frozen=True, slots=True)
class LLMPricing:
    """
    Token pricing configuration.
    """

    input_per_million_tokens: float

    output_per_million_tokens: float

@dataclass(frozen=True, slots=True)
class LLMConfig:
    """
    Configuration required to initialize the LLM client.
    """

    provider: str
    model: str
    api_key: str
    temperature: float
    max_output_tokens: int
    pricing: LLMPricing
    rate_limit: RateLimitConfig


def load_llm_config() -> LLMConfig:
    """
    Load the LLM configuration from YAML and environment variables.

    Returns:
        Fully initialized LLM configuration.

    Raises:
        ValueError:
            If the Google API key is not found.
    """

    # ------------------------------------------------------------------
    # Load environment variables
    # ------------------------------------------------------------------
    load_dotenv()

    # ------------------------------------------------------------------
    # Load YAML configuration
    # ------------------------------------------------------------------
    config = load_yaml("llm.yml")["llm"]

    # ------------------------------------------------------------------
    # Load API key
    # ------------------------------------------------------------------
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is not set."
        )

    # ------------------------------------------------------------------
    # Build configuration object
    # ------------------------------------------------------------------
    return LLMConfig(
        provider=config["provider"],
        model=config["model"],
        api_key=api_key,
        temperature=config["temperature"],
        max_output_tokens=config["max_output_tokens"],

        pricing=LLMPricing(
            input_per_million_tokens=config["pricing"][
                "input_per_million_tokens"
            ],
            output_per_million_tokens=config["pricing"][
                "output_per_million_tokens"
            ],
        ),

        rate_limit=RateLimitConfig(
            requests_per_minute=config["rate_limit"][
                "requests_per_minute"
            ],
        ),
    )