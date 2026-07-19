from dataclasses import dataclass
from typing import Any


@dataclass
class Chunk:
    """
    Represents a single chunk generated from a rich product document.

    Each chunk contains a portion of the original document text
    together with metadata inherited from its parent document.
    """

    id: str
    text: str
    metadata: dict[str, Any]