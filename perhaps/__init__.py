__version__ = "0.3.2"

from typing import Tuple

from .maybe import Just, Maybe, Nothing

__all__: Tuple[str, ...] = (
    "Maybe",
    "Just",
    "Nothing",
)
