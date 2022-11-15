__version__ = "0.1.0"

from .maybe import Just, Maybe, Nothing

__all__: tuple[str, ...] = (
    "Maybe",
    "Just",
    "Nothing",
)
