"""
Ground truth builder.

Coordinates the generation of candidate products for benchmark
queries by selecting the appropriate candidate generator.
"""

from __future__ import annotations

from src.data.data_loader import load_processed_data

from src.evaluation.enums import QueryCategory
from src.evaluation.ground_truth.generators import (
    BrandGenerator,
    CandidateGenerator,
    KeywordGenerator,)

from src.evaluation.ground_truth.models import (
    CandidateProduct,
    GroundTruthExample,
)


class GroundTruthBuilder:
    """
    Builds candidate products for ground truth benchmark queries.
    """

    def __init__(self) -> None:
        """
        Initialize the ground truth builder.
        """

        self._products_df, _ = load_processed_data()

        self._generators: dict[
            QueryCategory,
            CandidateGenerator,
        ] = {
            QueryCategory.BRAND: BrandGenerator(),
            QueryCategory.RECOMMENDATION: KeywordGenerator(),
        }

    def build(
        self,
        example: GroundTruthExample,
    ) -> list[CandidateProduct]:
        """
        Build candidate products for a benchmark query.

        Parameters
        ----------
        example:
            Benchmark query.

        Returns
        -------
        list[CandidateProduct]
            Candidate products proposed for the query.
        """

        generator = self._get_generator(
            example.category,
        )

        return generator.generate(
            example,
            self._products_df,
        )

    def build_all(
        self,
        examples: list[GroundTruthExample],
    ) -> dict[str, list[CandidateProduct]]:
        """
        Build candidate products for multiple benchmark queries.

        Parameters
        ----------
        examples:
            Benchmark queries.

        Returns
        -------
        dict[str, list[CandidateProduct]]
            Mapping from query id to candidate products.
        """

        return {
            example.id: self.build(example)
            for example in examples
        }

    def _get_generator(
        self,
        category: QueryCategory,
    ) -> CandidateGenerator:
        """
        Return the generator responsible for a query category.

        Raises
        ------
        ValueError
            If no generator is registered.
        """

        try:
            return self._generators[category]

        except KeyError as error:
            raise ValueError(
                f"No generator registered for category '{category}'."
            ) from error