"""
Prompt strategy definitions for LLM evaluation.

This module defines the supported prompting strategies that can
be benchmarked during end-to-end LLM evaluation.
"""

from __future__ import annotations

from enum import Enum


class PromptStrategy(str, Enum):
    """
    Supported prompt strategies.

    These strategies are evaluated using the same:
    - Hybrid Retriever
    - Retrieved Context
    - LLM

    Only the prompt template changes.
    """

    BASELINE = "baseline"

    STRUCTURED = "structured"