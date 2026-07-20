"""
Utility functions for loading project configuration files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


# Directory containing all project configuration files
CONFIG_DIR = Path(__file__).parent


def load_yaml(filename: str) -> dict[str, Any]:
    """
    Load a YAML configuration file from the project's config directory.

    Args:
        filename: Name of the YAML file (e.g. "vector_store.yaml").

    Returns:
        Parsed YAML configuration as a dictionary.

    Raises:
        FileNotFoundError:
            If the configuration file does not exist.

        ValueError:
            If the YAML file is empty.

        yaml.YAMLError:
            If the YAML syntax is invalid.
    """

    config_path = CONFIG_DIR / filename

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if config is None:
        raise ValueError(
            f"Configuration file '{filename}' is empty."
        )

    return config