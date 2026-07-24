"""
Build LLM-ready context from retrieved chunks.

The Context Builder transforms retrieval results into a clean textual
context that will later be injected into the LLM prompt.

This module performs no retrieval, filtering, or prompt construction.
"""

from __future__ import annotations

from src.retrieval.models import RetrievedChunk


class ContextBuilder:
    """
    Build a textual context from retrieved chunks.
    """

    def build(
        self,
        chunks: list[RetrievedChunk],
    ) -> str:
        """
        Build an LLM-ready context string.

        Parameters
        ----------
        chunks:
            Retrieved chunks returned by the Retriever.

        Returns
        -------
        str
            Context string for the Prompt Builder.
        """

        sections: list[str] = []

        for index, chunk in enumerate(chunks, start=1):

            section = (
                    f"Retrieved Context {index}\n"
                    f"{'=' * 80}\n"
                    f"ASIN: {chunk.asin}\n"
                    f"Brand: {chunk.metadata.get('brand_name', 'Unknown')}\n\n"
                    f"{chunk.text.strip()}"
            )

            sections.append(section)

        return "\n\n" + ("\n\n" + ("-" * 80) + "\n\n").join(sections)