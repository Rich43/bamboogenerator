import logging
from typing import Optional


def setup_logging(
    filename: Optional[str] = None,
    level: int = logging.INFO,
    format: str = "%(asctime)s - %(levelname)s - %(message)s",
) -> None:
    """Configure basic logging for examples and utilities."""
    logging.basicConfig(filename=filename, level=level, format=format)

