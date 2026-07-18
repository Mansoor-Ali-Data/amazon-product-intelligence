"""
Project-wide logging configuration.

This module provides a centralized logger for the entire project.

Responsibilities:
- Configure consistent logging across all modules.
- Log messages to both the console and a log file.
- Prevent duplicate log handlers when imported multiple times.
- Expose a simple `get_logger()` function for use throughout the project.

Example:
    from config.logging import get_logger

    logger = get_logger(__name__)

    logger.info("Starting preprocessing...")
    logger.warning("Missing values detected.")
    logger.error("Failed to load dataset.")
"""

from pathlib import Path
import logging


# ---------------------------------------------------------------------
# Log Directory
# ---------------------------------------------------------------------
# Ensure the logs directory exists before creating the log file.
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "project.log"


# ---------------------------------------------------------------------
# Log Format
# ---------------------------------------------------------------------
# Example:
# 2026-07-17 09:45:18 | INFO | src.preprocessing | Loaded products dataset
LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ---------------------------------------------------------------------
# Logger Factory
# ---------------------------------------------------------------------
def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger.

    The logger writes messages to both:
        - Console
        - logs/project.log

    If the logger has already been configured, existing handlers are reused
    to avoid duplicate log messages.

    Args:
        name: Typically pass __name__ from the calling module.

    Returns:
        Configured Logger instance.
    """

    logger = logging.getLogger(name)

    # Prevent adding duplicate handlers if this function is called
    # multiple times from the same module.
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT
    )

    # -------------------------------------------------------------
    # Console Handler
    # -------------------------------------------------------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # -------------------------------------------------------------
    # File Handler
    # -------------------------------------------------------------
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Prevent messages from being passed to the root logger,
    # which avoids duplicate log entries.
    logger.propagate = False

    return logger