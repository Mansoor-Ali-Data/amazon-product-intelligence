"""
Validation script for the monitoring subsystem.
"""

from __future__ import annotations

from pathlib import Path

from config.logging import get_logger

from src.pipeline.rag_pipeline import RAGPipeline

logger = get_logger(__name__)


def main() -> None:
    """
    Validate the monitoring subsystem.
    """

    logger.info(
        "Starting monitoring validation."
    )

    pipeline = RAGPipeline()

    rag_response = pipeline.ask(
        query="Recommend a golf polo shirt.",
    )

    # ---------------------------------------------------------
    # Validate RAG response
    # ---------------------------------------------------------

    assert rag_response.query

    assert rag_response.prompt_strategy

    assert rag_response.retrieved_chunks

    assert rag_response.llm_response.text

    assert rag_response.llm_response.prompt_tokens > 0

    assert rag_response.llm_response.completion_tokens >= 0

    assert rag_response.llm_response.total_tokens > 0

    assert rag_response.llm_response.estimated_cost >= 0

    assert rag_response.llm_response.latency_seconds > 0

    # ---------------------------------------------------------
    # Validate telemetry output
    # ---------------------------------------------------------

    telemetry_file = Path(
        "outputs/monitoring/telemetry.jsonl"
    )

    assert telemetry_file.exists()

    assert telemetry_file.stat().st_size > 0

    logger.info(
        "Monitoring validation completed successfully."
    )

    print()

    print("=" * 80)
    print("Monitoring Validation")
    print("=" * 80)

    print(
        f"Query                 : {rag_response.query}"
    )

    print(
        f"Prompt Strategy       : "
        f"{rag_response.prompt_strategy.value}"
    )

    print(
        f"Retrieved Chunks      : "
        f"{len(rag_response.retrieved_chunks)}"
    )

    print(
        f"Total Tokens          : "
        f"{rag_response.llm_response.total_tokens}"
    )

    print(
        f"Estimated Cost        : "
        f"${rag_response.llm_response.estimated_cost:.6f}"
    )

    print(
        f"LLM Latency           : "
        f"{rag_response.llm_response.latency_seconds:.2f}s"
    )

    print()

    print(
        "✓ Telemetry written automatically."
    )

    print(
        "✓ Telemetry file exists."
    )

    print()

    print("=" * 80)
    print("Validation completed successfully.")
    print("=" * 80)


if __name__ == "__main__":
    main()