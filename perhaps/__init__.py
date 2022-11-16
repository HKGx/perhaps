from importlib.metadata import version
from typing import Tuple

from .maybe import Just, Maybe, Nothing

__version__ = version("perhaps")

__all__: Tuple[str, ...] = (
    "Maybe",
    "Just",
    "Nothing",
)
