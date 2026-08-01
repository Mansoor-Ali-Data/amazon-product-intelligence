"""
Persistent storage for the BM25 lexical index.

Responsibilities
----------------
- Save the BM25 index to disk.
- Load the BM25 index from disk.
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

from rank_bm25 import BM25Okapi

from config.loader import load_yaml
from src.indexing.bm25_models import BM25IndexData


class BM25Store:
    """
    Persistent storage for the BM25 lexical index.
    """

    def __init__(
        self,
    ) -> None:

        self._config = self._load_config()

        self._persist_directory = Path(
            self._config["persist_directory"]
        )

        self._persist_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._index_path = (
            self._persist_directory
            / self._config["file_name"]
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def save(
        self,
        bm25: BM25Okapi,
        index_data: BM25IndexData,
    ) -> Path:
        """
        Persist the BM25 index.

        Parameters
        ----------
        bm25:
            BM25 lexical index.

        index_data:
            Corpus used to build the index.

        Returns
        -------
        Path
            Saved file path.
        """

        payload = {
            "bm25": bm25,
            "index_data": index_data,
        }

        with self._index_path.open(
            mode="wb",
        ) as file:

            pickle.dump(
                payload,
                file,
            )

        return self._index_path

    def load(
        self,
    ) -> tuple[
        BM25Okapi,
        BM25IndexData,
    ]:
        """
        Load the persisted BM25 index.

        Returns
        -------
        tuple
            BM25 index and corpus.
        """

        if not self._index_path.exists():

            raise FileNotFoundError(
                f"BM25 index not found: {self._index_path}"
            )

        with self._index_path.open(
            mode="rb",
        ) as file:

            payload: dict[str, Any] = pickle.load(
                file,
            )

        return (
            payload["bm25"],
            payload["index_data"],
        )

    def exists(
        self,
    ) -> bool:
        """
        Check whether the BM25 index exists.
        """

        return self._index_path.exists()

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_config(
    ) -> dict[str, Any]:
        """
        Load BM25 store configuration.
        """

        return load_yaml(
            "bm25_store.yaml",
        )["bm25_store"]