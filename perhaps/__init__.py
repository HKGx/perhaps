__version__ = "0.1.0"

from typing import Tuple

from .maybe import Just, Maybe, Nothing

__all__: Tuple[str, ...] = (
    "Maybe",
    "Just",
    "Nothing",
)
