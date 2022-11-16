from abc import ABC, abstractmethod
from typing import (
    Callable,
    Generic,
    NoReturn,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

T = TypeVar("T")
R = TypeVar("R")


class Maybe(Generic[T], ABC):
    value: Union[T, NoReturn]

    @abstractmethod
    def map(self, f: Callable[[T], R]) -> "Maybe[R]":
        """
        Apply a function to the value of the Maybe, if it has one.

        Analogous to the `Option::map` in Rust.

        >>> Just(1).map(lambda x: x + 1)
        Just(2)
        >>> Nothing().map(lambda x: x + 1)
        Nothing()
        >>> Maybe.from_optional(None).map(lambda x: x + 1)
        Nothing()
        """
        ...

    @abstractmethod
    def bind(self, f: Callable[[T], "Maybe[R]"]) -> "Maybe[R]":
        """
        Apply a function to the value of the Maybe, if it has one.

        Analogous to the `Option::and_then` in Rust and the `bind` in Haskell.

        >>> Just(1).bind(lambda x: Just(x + 1))
        Just(2)
        >>> Nothing().bind(lambda x: Just(x + 1))
        Nothing()
        """
        ...

    @abstractmethod
    def and_then(self, f: Callable[[T], "Maybe[R]"]) -> "Maybe[R]":
        """
        Alias for `bind` if you prefer the Rust naming.
        """
        ...

    @abstractmethod
    def unwrap(
        self, f: Optional[Callable[[], Union[Exception, Type[Exception]]]] = None
    ) -> Union[T, NoReturn]:
        """
        Unwrap the value, or raise an exception if it is Nothing.

        Custom exceptions can be raised by passing a callable that returns an exception or exception type.

        Analogous to `Option::unwrap` in Rust.

        >>> Just(1).unwrap()
        1
        >>> Nothing().unwrap()
        Traceback (most recent call last):
            ...
        ValueError: Tried to unwrap Nothing
        """
        ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """
        Unwrap the value or return the default value.


        Analogous to `Option::unwrap_or` in Rust.

        >>> Just(1).unwrap_or(2)
        1
        >>> Nothing().unwrap_or(2)
        2

        """
        ...

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """
        Unwrap the value or return the result of the function.
        Allows for lazy evaluation of the default value.

        Analogous to `Option::unwrap_or_else` in Rust.

        >>> Nothing().unwrap_or_else(lambda: 1)
        1
        >>> Just(1).unwrap_or_else(lambda: 2)
        1

        """
        ...

    @abstractmethod
    def to_optional(self) -> Optional[T]:
        """
        Convert to an Optional.

        >>> Just(1).to_optional()
        1
        >>> Nothing().to_optional()
        None
        """
        ...

    @classmethod
    def from_optional(cls, value: Optional[T]) -> "Maybe[T]":
        """
        Convert from an Optional.

        >>> Maybe.from_optional(1)
        Just(1)
        >>> Maybe.from_optional(None)
        Nothing()
        """
        return Just(value) if value is not None else Nothing()

    @classmethod
    def from_try(
        cls,
        f: Callable[[], T],
        exc: Union[Type[Exception], Tuple[Type[Exception], ...]],
    ) -> "Maybe[T]":
        """
        Convert from a function that may raise an exception.

        Exception types can be passed as a tuple to catch multiple exceptions.

        >>> Maybe.from_try(lambda: 1 / 1, ZeroDivisionError)
        Just(1)
        >>> Maybe.from_try(lambda: 1 / 0, ZeroDivisionError)
        Nothing()
        """
        try:
            return Just(f())
        except exc:
            return Nothing()

    @abstractmethod
    def __and__(self, other: "Maybe[R]") -> Union["Maybe[T]", "Maybe[R]"]:
        ...

    @abstractmethod
    def __or__(self, other: "Maybe[R]") -> Union["Maybe[T]", "Maybe[R]"]:
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...

    @abstractmethod
    def __bool__(self) -> bool:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...


class Just(Generic[T], Maybe[T]):
    __match_args__ = ("value",)

    value: T

    def __init__(self, value: T):
        self.value = value

    def map(self, f: Callable[[T], R]) -> "Just[R]":
        return Just(f(self.value))

    def bind(self, f: Callable[[T], "Maybe[R]"]) -> "Maybe[R]":
        return f(self.value)

    def and_then(self, f: Callable[[T], "Maybe[R]"]) -> "Maybe[R]":
        return self.bind(f)

    def unwrap(
        self, f: Optional[Callable[[], Union[Exception, Type[Exception]]]] = None
    ) -> T:
        return self.value

    def unwrap_or(self, default: T) -> T:
        return self.value

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return self.value

    def to_optional(self) -> T:
        return self.value

    @overload
    def __and__(self, other: "Just[R]") -> "Just[R]":
        ...

    @overload
    def __and__(self, other: "Nothing[R]") -> "Nothing[R]":
        ...

    @overload
    def __and__(self, other: "Maybe[R]") -> Union["Maybe[T]", "Maybe[R]"]:
        ...

    def __and__(self, other: "Maybe[R]") -> Union["Maybe[T]", "Maybe[R]"]:
        return other

    @overload
    def __or__(self, other: "Just") -> "Just[T]":
        ...

    @overload
    def __or__(self, other: "Nothing") -> "Just[T]":
        ...

    @overload
    def __or__(self, other: "Maybe[R]") -> Union["Maybe[T]", "Maybe[R]"]:
        ...

    def __or__(self, other: "Maybe[R]") -> Union["Maybe[T]", "Maybe[R]"]:
        return self

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Just) and self.value == other.value

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"Just({self.value!r})"


class Nothing(Generic[T], Maybe[T]):
    __match_args__ = ()

    instance: Optional["Nothing[T]"] = None

    def __new__(cls) -> "Nothing[T]":
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def map(self, f: Callable[[T], R]) -> "Nothing[R]":
        return Nothing()

    def bind(self, f: Callable[[T], "Maybe[R]"]) -> "Nothing[R]":
        return Nothing()

    def and_then(self, f: Callable[[T], "Maybe[R]"]) -> "Nothing[R]":
        return self.bind(f)

    def unwrap(
        self, f: Optional[Callable[[], Union[Exception, Type[Exception]]]] = None
    ) -> NoReturn:
        if f:
            raise f()
        raise ValueError("Tried to unwrap Nothing")

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return f()

    def to_optional(self) -> None:
        return None

    @overload
    def __and__(self, other: "Just") -> "Nothing[T]":
        ...

    @overload
    def __and__(self, other: "Nothing[R]") -> "Nothing[R]":
        ...

    def __and__(self, other: "Maybe[R]") -> Union["Nothing[T]", "Maybe[R]"]:
        return other if isinstance(other, Nothing) else self

    @overload
    def __or__(self, other: "Just[R]") -> "Just[R]":
        ...

    @overload
    def __or__(self, other: "Nothing[R]") -> "Nothing[R]":
        ...

    def __or__(self, other: "Maybe[R]") -> Union["Nothing[T]", "Maybe[R]"]:
        return other

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Nothing)

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Nothing()"
