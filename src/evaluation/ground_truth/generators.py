"""
Candidate generators for building the retrieval ground truth dataset.

Each generator proposes candidate products for a specific
type of benchmark query.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from src.evaluation.ground_truth.models import (
    CandidateProduct,
    GroundTruthExample,
)


class CandidateGenerator(ABC):
    """
    Base class for candidate generators.
    """

    def generate(
        self,
        example: GroundTruthExample,
        products_df: pd.DataFrame,
    ) -> list[CandidateProduct]:
        """
        Generate candidate products for a query.
        """

        matches = self._filter(
            example,
            products_df,
        )

        return [
            self._to_candidate(row)
            for _, row in matches.iterrows()
        ]

    @abstractmethod
    def _filter(
        self,
        example: GroundTruthExample,
        products_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Return matching products.
        """

    @staticmethod
    def _to_candidate(
        row: pd.Series,
    ) -> CandidateProduct:
        """
        Convert a dataframe row into a CandidateProduct.
        """

        return CandidateProduct(
            asin=row["asin"],
            brand=row["brand_name"],
            title=row["title"],
            price=row["price_value"],
            rating=row["rating_stars"],
        )


class BrandGenerator(CandidateGenerator):
    """
    Candidate generator for brand queries.
    """

    def _filter(
        self,
        example: GroundTruthExample,
        products_df: pd.DataFrame,
    ) -> pd.DataFrame:

        brand = (
            example.query
            .replace("Show me", "")
            .replace("polo shirts.", "")
            .replace("golf shirts.", "")
            .strip()
        )

        return products_df[
            products_df["brand_name"].str.contains(
                brand,
                case=False,
                na=False,
            )
        ]


class KeywordGenerator(CandidateGenerator):
    """
    Candidate generator for keyword/feature queries.
    """

    SEARCH_COLUMNS = (
        "title",
        "about_item",
    )

    def _filter(
        self,
        example: GroundTruthExample,
        products_df: pd.DataFrame,
    ) -> pd.DataFrame:

        mask = pd.Series(
            True,
            index=products_df.index,
        )

        for term in example.search_terms:

            term_mask = pd.Series(
                False,
                index=products_df.index,
            )

            for column in self.SEARCH_COLUMNS:

                text = (
                    products_df[column]
                    .fillna("")
                    .str.lower()
                )

                term_mask |= text.str.contains(
                    term.lower(),
                    regex=False,
                )

            mask &= term_mask

        return products_df[mask]