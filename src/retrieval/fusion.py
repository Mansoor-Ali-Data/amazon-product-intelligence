"""
Reciprocal Rank Fusion (RRF).

Combines multiple ranked retrieval results into a single ranking.
"""

from __future__ import annotations

from src.retrieval.models import RetrievedChunk


class ReciprocalRankFusion:
    """
    Fuse multiple ranked retrieval results using Reciprocal Rank Fusion.
    """

    def __init__(
        self,
        k: int = 60,
    ) -> None:
        """
        Initialize the fusion algorithm.

        Args:
            k: Rank constant used in the RRF formula.
        """
        self._k = k

    def fuse(
        self,
        rankings: list[list[RetrievedChunk]],
    ) -> list[RetrievedChunk]:
        """
        Fuse multiple ranked retrieval lists.

        Args:
            rankings: Ranked retrieval results from different retrievers.

        Returns:
            A single fused ranking.
        """

        scores = self._accumulate_scores(
            rankings,
        )

        return self._sort_results(
            scores,
        )

    def _accumulate_scores(
        self,
        rankings: list[list[RetrievedChunk]],
    ) -> dict[str, tuple[RetrievedChunk, float]]:
        """
        Accumulate RRF scores for each product.

        Returns:
            Mapping from ASIN to (RetrievedChunk, fused_score).
        """

        fused: dict[
            str,
            tuple[RetrievedChunk, float],
        ] = {}

        for ranking in rankings:

            for chunk in ranking:

                score = (
                    1.0
                    / (
                        self._k
                        + chunk.rank
                    )
                )

                if chunk.asin in fused:

                    existing_chunk, existing_score = (
                        fused[chunk.asin]
                    )

                    fused[chunk.asin] = (
                        existing_chunk,
                        existing_score + score,
                    )

                else:

                    fused[chunk.asin] = (
                        chunk,
                        score,
                    )

        return fused

    def _sort_results(
        self,
        scores: dict[
            str,
            tuple[RetrievedChunk, float],
        ],
    ) -> list[RetrievedChunk]:
        """
        Sort products by fused score.

        Returns:
            Final fused ranking.
        """

        ranked = sorted(
            scores.values(),
            key=lambda item: item[1],
            reverse=True,
        )

        results: list[RetrievedChunk] = []

        for rank, (chunk, _) in enumerate(
            ranked,
            start=1,
        ):

            results.append(
                RetrievedChunk(
                    id=chunk.id,
                    text=chunk.text,
                    metadata=chunk.metadata,
                    distance=chunk.distance,
                    rank=rank,
                    asin=chunk.asin,
                    chunk_index=chunk.chunk_index,
                )
            )

        return results