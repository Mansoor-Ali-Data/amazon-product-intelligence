"""
Build complete LLM prompts.

The Prompt Builder transforms a user query and retrieved context
into a complete prompt ready for LLM inference.

This module performs no retrieval, context construction,
or model inference.
"""

from .formatter import format_prompt


class PromptBuilder:
    """
    Build complete prompts for the LLM.
    """

    def build(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Build an LLM-ready prompt.

        Args:
            query:
                User question.

            context:
                Retrieved context.

        Returns:
            Prompt string.
        """

        return format_prompt(
            query=query,
            context=context,
        )