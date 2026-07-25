"""
RAG pipeline orchestration.

The RAGPipeline coordinates the end-to-end retrieval-augmented
generation workflow by composing the project's existing components.

Responsibilities
----------------
- Retrieve relevant chunks
- Build LLM context
- Build the final prompt
- Generate an answer using the configured LLM

This module contains orchestration logic only.
"""

from __future__ import annotations

from config.logging import get_logger

from src.context_builder.builder import ContextBuilder
from src.llm.client import LLMClient
from src.prompt_builder.builder import PromptBuilder
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore

logger = get_logger(__name__)


class RAGPipeline:
    """
    End-to-end Retrieval-Augmented Generation pipeline.
    """

    def __init__(self) -> None:
        """
        Initialize all pipeline components.
        """

        logger.info("Initializing RAG pipeline.")

        self._vector_store = VectorStore()

        self._retriever = Retriever(
            self._vector_store,
        )

        self._context_builder = ContextBuilder()

        self._prompt_builder = PromptBuilder()

        self._llm = LLMClient()

    def ask(
        self,
        query: str,
        top_k: int = 3,
    ) -> str:
        """
        Answer a user question using Retrieval-Augmented Generation.

        Args:
            query:
                User question.

            top_k:
                Number of chunks to retrieve.

        Returns:
            Generated answer.
        """

        logger.info(
            "Starting RAG pipeline for query: '%s'",
            query,
        )

        # --------------------------------------------------------------
        # Retrieve relevant chunks
        # --------------------------------------------------------------

        chunks = self._retriever.retrieve(
            query=query,
            top_k=top_k,
        )

        logger.info(
            "Retrieved %d chunks.",
            len(chunks),
        )

        # --------------------------------------------------------------
        # Build LLM context
        # --------------------------------------------------------------

        context = self._context_builder.build(
            chunks,
        )

        logger.info(
            "Context built successfully.",
        )

        # --------------------------------------------------------------
        # Build prompt
        # --------------------------------------------------------------

        prompt = self._prompt_builder.build(
            query=query,
            context=context,
        )

        logger.info(
            "Prompt built successfully.",
        )

        # --------------------------------------------------------------
        # Generate response
        # --------------------------------------------------------------

        answer = self._llm.generate(
            prompt,
        )

        logger.info(
            "RAG pipeline completed successfully.",
        )

        return answer