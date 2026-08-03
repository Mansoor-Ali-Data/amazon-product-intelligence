"""
Prompt formatting utilities.
"""

from __future__ import annotations

from src.evaluation.llm.prompt_strategy import PromptStrategy

from .templates import PROMPT_TEMPLATES


def format_prompt(
    query: str,
    context: str,
    strategy: PromptStrategy = PromptStrategy.BASELINE,
) -> str:
    """
    Format an LLM prompt.

    Args:
        query:
            User question.

        context:
            Retrieved context.

        strategy:
            Prompt strategy to use.

    Returns:
        Formatted prompt.
    """

    template = PROMPT_TEMPLATES[strategy]

    return template.substitute(
        query=query,
        context=context,
    )