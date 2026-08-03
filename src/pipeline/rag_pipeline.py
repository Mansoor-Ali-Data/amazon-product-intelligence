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
from time import perf_counter
from src.context_builder.builder import ContextBuilder
from src.llm.client import LLMClient
from src.prompt_builder.builder import PromptBuilder
from src.vector_store.chroma_store import VectorStore
from src.bm25_store.store import BM25Store
from src.evaluation.llm.prompt_strategy import PromptStrategy
from src.retrieval.retriever import Retriever
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.fusion import ReciprocalRankFusion
from src.pipeline.models import RAGResponse
from collections.abc import Callable
from src.monitoring.collector import TelemetryCollector
from src.monitoring.writer import MonitoringWriter
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

        self._telemetry_collector = TelemetryCollector()
        self._monitoring_writer = MonitoringWriter()
        # --------------------------------------------------------------
        # Dense Retriever
        # --------------------------------------------------------------

        self._vector_store = VectorStore()

        dense_retriever = Retriever(
            vector_store=self._vector_store,
        )

        # --------------------------------------------------------------
        # BM25 Retriever
        # --------------------------------------------------------------

        bm25_store = BM25Store()

        bm25_retriever = BM25Retriever(
            store=bm25_store,
        )

        # --------------------------------------------------------------
        # Production Retriever
        # --------------------------------------------------------------

        self._production_retriever = HybridRetriever(
            dense_retriever=dense_retriever,
            bm25_retriever=bm25_retriever,
            fusion=ReciprocalRankFusion(),
        )

        self._context_builder = ContextBuilder()

        self._prompt_builder = PromptBuilder()

        self._llm = LLMClient()

       
    

    def ask(
        self,
        query: str,
        top_k: int = 3,
        prompt_strategy: PromptStrategy = PromptStrategy.BASELINE,
        progress_callback: Callable[[str], None] | None = None,
    ) -> RAGResponse:
        """
        Answer a user question using Retrieval-Augmented Generation.

        Args:
            query:
                User question.

            top_k:
                Number of chunks to retrieve.

            prompt_strategy:
                Prompt construction strategy.

            progress_callback:
                Optional callback used by the UI to display progress.

        Returns:
            Generated RAG response.
        """

        logger.info(
            "Starting RAG pipeline for query: '%s'",
            query,
        )

        pipeline_start = perf_counter()

        # --------------------------------------------------------------
        # Retrieve relevant chunks
        # --------------------------------------------------------------

        retrieval_start = perf_counter()

        if progress_callback:
            progress_callback("🔍 Retrieving relevant products...")

        retrieved_chunks = self._production_retriever.retrieve(
            query=query,
            top_k=top_k,
        )

        retrieval_latency_seconds = (
            perf_counter() - retrieval_start
        )

        logger.info(
            "Retrieved %d chunks.",
            len(retrieved_chunks),
        )

        # --------------------------------------------------------------
        # Build LLM context
        # --------------------------------------------------------------

        context_start = perf_counter()

        if progress_callback:
            progress_callback("🧠 Building LLM context...")

        context = self._context_builder.build(
            retrieved_chunks,
        )

        context_latency_seconds = (
            perf_counter() - context_start
        )

        logger.info(
            "Context built successfully.",
        )

        # --------------------------------------------------------------
        # Build prompt
        # --------------------------------------------------------------

        prompt_start = perf_counter()

        if progress_callback:
            progress_callback("📝 Constructing prompt...")

        prompt = self._prompt_builder.build(
            query=query,
            context=context,
            strategy=prompt_strategy,
        )

        prompt_latency_seconds = (
            perf_counter() - prompt_start
        )

        logger.info(
            "Prompt built successfully using '%s' strategy.",
            prompt_strategy.value,
        )

        # --------------------------------------------------------------
        # Generate response
        # --------------------------------------------------------------

        if progress_callback:
            progress_callback("🤖 Generating answer...")

        llm_response = self._llm.generate(
            prompt,
        )

        total_latency_seconds = (
            perf_counter() - pipeline_start
        )

        # --------------------------------------------------------------
        # Build pipeline response
        # --------------------------------------------------------------

        rag_response = RAGResponse(
            query=query,
            prompt_strategy=prompt_strategy,
            llm_response=llm_response,
            retrieved_chunks=retrieved_chunks,
        )

        # --------------------------------------------------------------
        # Monitoring
        # --------------------------------------------------------------

        telemetry = self._telemetry_collector.collect(
            rag_response=rag_response,
            retrieval_latency_seconds=retrieval_latency_seconds,
            context_latency_seconds=context_latency_seconds,
            prompt_latency_seconds=prompt_latency_seconds,
            total_latency_seconds=total_latency_seconds,
        )

        self._monitoring_writer.write_telemetry(
            telemetry,
        )

        logger.info(
            "RAG pipeline completed successfully."
        )

        return rag_response