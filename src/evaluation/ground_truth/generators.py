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
        Generate candidate products for a benchmark query.
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

    SEARCH_COLUMNS = [
        "title",
        "about_item",
        "product_description",
    ]

    def _filter(
        self,
        example: GroundTruthExample,
        products_df: pd.DataFrame,
    ) -> pd.DataFrame:

        keywords = (
            example.query.lower()
            .replace("show", "")
            .replace("recommend", "")
            .replace("polo shirts", "")
            .replace("golf shirts", "")
            .replace("shirt", "")
            .split()
        )

        mask = pd.Series(
            False,
            index=products_df.index,
        )

        for column in self.SEARCH_COLUMNS:

            text = (
                products_df[column]
                .fillna("")
                .str.lower()
            )

            for keyword in keywords:
                mask |= text.str.contains(
                    keyword,
                    regex=False,
                )

        return products_df[mask]


class PriceGenerator(CandidateGenerator):
    """
    Candidate generator for price queries.
    """

    def _filter(
        self,
        example: GroundTruthExample,
        products_df: pd.DataFrame,
    ) -> pd.DataFrame:

        query = example.query.lower()

        if "under $20" in query:
            return products_df[
                products_df["price_value"] < 20
            ]

        if "under $30" in query:
            return products_df[
                products_df["price_value"] < 30
            ]

        return pd.DataFrame(columns=products_df.columns)


class RatingGenerator(CandidateGenerator):
    """
    Candidate generator for rating queries.
    """

    def _filter(
        self,
        example: GroundTruthExample,
        products_df: pd.DataFrame,
    ) -> pd.DataFrame:

        query = example.query.lower()

        if "above 4.5" in query:
            return products_df[
                products_df["rating_stars"] >= 4.5
            ]

        if "highest rated" in query:

            return (
                products_df.sort_values(
                    "rating_stars",
                    ascending=False,
                )
                .head(20)
            )

        return pd.DataFrame(columns=products_df.columns)