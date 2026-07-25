"""
Utilities for formatting LLM prompts.

This module is responsible only for converting the user query
and retrieved context into a complete prompt using predefined
templates.

It performs no retrieval, context construction, or LLM inference.
"""

from .templates import PROMPT_TEMPLATE


def format_prompt(
    query: str,
    context: str,
) -> str:
    """
    Format a complete LLM prompt.

    Args:
        query:
            User question.

        context:
            Retrieved context produced by the Context Builder.

    Returns:
        Complete prompt ready for LLM inference.
    """

    return PROMPT_TEMPLATE.substitute(
        query=query,
        context=context,
    )