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
        ...

    @abstractmethod
    def or_else(self, f: Callable[[], T]) -> T:
        ...

    @abstractmethod
    def unwrap(
        self, f: Optional[Callable[[], Union[Exception, Type[Exception]]]] = None
    ) -> Union[T, NoReturn]:
        ...

    @abstractmethod
    def to_optional(self) -> Optional[T]:
        ...

    @classmethod
    def from_optional(cls, value: Optional[T]) -> "Maybe[T]":
        return Just(value) if value is not None else Nothing()

    @classmethod
    def from_try(
        cls,
        f: Callable[[], T],
        exc: Union[Type[Exception], Tuple[Type[Exception], ...]] = (),
    ) -> "Maybe[T]":
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
    def __repr__(self) -> str:
        ...


class Just(Generic[T], Maybe[T]):
    __match_args__ = ("value",)

    value: T

    def __init__(self, value: T):
        self.value = value

    def map(self, f: Callable[[T], R]) -> "Just[R]":
        return Just(f(self.value))

    def or_else(self, f: Callable[[], T]) -> T:
        return self.value

    def unwrap(
        self, f: Optional[Callable[[], Union[Exception, Type[Exception]]]] = None
    ) -> T:
        return self.value

    def to_optional(self) -> T:
        return self.value

    @overload
    def __and__(self, other: "Just[R]") -> "Just[R]":
        ...

    @overload
    def __and__(self, other: "Nothing[R]") -> "Nothing[R]":
        ...

    def __and__(self, other: "Maybe[R]") -> Union["Maybe[T]", "Maybe[R]"]:
        return other

    @overload
    def __or__(self, other: "Just") -> "Just[T]":
        ...

    @overload
    def __or__(self, other: "Nothing") -> "Just[T]":
        ...

    def __or__(self, other: "Maybe[R]") -> Union["Maybe[T]", "Maybe[R]"]:
        return self

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Just) and self.value == other.value

    def __repr__(self) -> str:
        return f"Just({self.value!r})"


class Nothing(Generic[T], Maybe[T]):
    __match_args__ = ()

    def map(self, f: Callable[[T], R]) -> "Nothing[R]":
        return Nothing()

    def or_else(self, f: Callable[[], T]) -> T:
        return f()

    def unwrap(
        self, f: Optional[Callable[[], Union[Exception, Type[Exception]]]] = None
    ) -> NoReturn:
        if f:
            raise f()
        raise ValueError("Tried to unwrap Nothing")

    def to_optional(self) -> None:
        return None

    @overload
    def __and__(self, other: "Just") -> "Nothing[T]":
        ...

    @overload
    def __and__(self, other: "Nothing") -> "Nothing[T]":
        ...

    def __and__(self, other: "Maybe[R]") -> Union["Nothing[T]", "Maybe[R]"]:
        return self

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

    def __repr__(self) -> str:
        return "Nothing()"
