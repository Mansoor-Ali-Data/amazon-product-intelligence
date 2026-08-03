"""
Telemetry collector.

Responsibilities
----------------
- Collect monitoring information from a completed
  RAG pipeline execution.
- Construct TelemetryRecord objects.
- Remain independent of storage and visualization.

This module performs no file I/O.
"""

from __future__ import annotations

from datetime import UTC, datetime

from src.llm.models import LLMResponse
from src.monitoring.models import TelemetryRecord
from src.pipeline.models import RAGResponse


class TelemetryCollector:
    """
    Builds telemetry records from pipeline outputs.
    """

    def collect(
        self,
        rag_response: RAGResponse,
        retrieval_latency_seconds: float,
        context_latency_seconds: float,
        prompt_latency_seconds: float,
        total_latency_seconds: float,
        status: str = "success",
        error_message: str | None = None,
    ) -> TelemetryRecord:
        """
        Build a telemetry record for a completed pipeline request.

        Args:
            rag_response:
                Final RAG pipeline response.

            retrieval_latency_seconds:
                Time spent retrieving documents.

            context_latency_seconds:
                Time spent constructing context.

            prompt_latency_seconds:
                Time spent building the final prompt.

            total_latency_seconds:
                End-to-end pipeline latency.

            status:
                Pipeline execution status.

            error_message:
                Optional failure reason.

        Returns:
            TelemetryRecord.
        """

        llm_response: LLMResponse = rag_response.llm_response

        return TelemetryRecord(
            timestamp=datetime.now(UTC).isoformat(),
            query=rag_response.query,
            prompt_strategy=rag_response.prompt_strategy.value,
            status=status,
            error_message=error_message,
            retrieval_latency_seconds=retrieval_latency_seconds,
            context_latency_seconds=context_latency_seconds,
            prompt_latency_seconds=prompt_latency_seconds,
            llm_latency_seconds=llm_response.latency_seconds,
            total_latency_seconds=total_latency_seconds,
            retrieved_chunks=len(rag_response.retrieved_chunks),
            unique_products=len(
                {
                    chunk.asin
                    for chunk in rag_response.retrieved_chunks
                }
            ),
            prompt_tokens=llm_response.prompt_tokens,
            completion_tokens=llm_response.completion_tokens,
            total_tokens=llm_response.total_tokens,
            estimated_cost=llm_response.estimated_cost,
        )