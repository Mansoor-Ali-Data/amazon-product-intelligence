"""
Domain models for the RAG pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.llm.prompt_strategy import PromptStrategy
from src.llm.models import LLMResponse
from src.retrieval.models import RetrievedChunk


@dataclass(frozen=True, slots=True)
class RAGResponse:
    """
    Response returned by the RAG pipeline.

    Attributes
    ----------
    query:
        Original user query.

    prompt_strategy:
        Prompt strategy used to construct the final prompt.

    llm_response:
        Structured response returned by the LLM.

    retrieved_chunks:
        Chunks retrieved from the hybrid retriever.
    """

    query: str

    prompt_strategy: PromptStrategy

    llm_response: LLMResponse

    retrieved_chunks: list[RetrievedChunk]