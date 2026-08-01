"""
Builder for the BM25 lexical search index.

Converts a BM25IndexData corpus into a BM25Okapi index.
"""

from __future__ import annotations

from rank_bm25 import BM25Okapi

from src.indexing.bm25_models import BM25IndexData


class BM25StoreBuilder:
    """
    Builds a BM25 lexical search index.
    """

    def build(
        self,
        index_data: BM25IndexData,
    ) -> BM25Okapi:
        """
        Build a BM25Okapi index.

        Parameters
        ----------
        index_data:
            BM25 corpus generated during the indexing pipeline.

        Returns
        -------
        BM25Okapi
            Ready-to-use BM25 index.
        """

        self._validate(index_data)

        return BM25Okapi(
            corpus=index_data.tokenized_documents,
        )

    @staticmethod
    def _validate(
        index_data: BM25IndexData,
    ) -> None:
        """
        Validate the BM25 corpus before building the index.
        """

        if not index_data.documents:
            raise ValueError(
                "BM25 corpus is empty."
            )

        document_count = len(index_data.documents)

        if len(index_data.tokenized_documents) != document_count:
            raise ValueError(
                "Mismatch between documents and tokenized documents."
            )

        if len(index_data.chunk_ids) != document_count:
            raise ValueError(
                "Mismatch between documents and chunk IDs."
            )

        if len(index_data.metadatas) != document_count:
            raise ValueError(
                "Mismatch between documents and metadata."
            )