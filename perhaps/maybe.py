from abc import ABC, abstractmethod
from typing import Callable, NoReturn, Optional, Tuple, Type, TypeGuard, Union, overload


class Maybe[T](ABC):
    __slots__ = ()

    value: Union[T, NoReturn]

    @abstractmethod
    def map[R](self, f: Callable[[T], R]) -> "Maybe[R]":
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
    def map_nothing(self, f: Callable[[], T]) -> "Just[T]":
        """
        Returns new Just, that has a default value if Maybe was Nothing.

        Functionally the same as `Maybe[T] or Just[T]`

        >>> Just(1).map_nothing(lambda: 5)
        Just(1)
        >>> Nothing().map_nothing(lambda: 5)
        Just(5)
        >>> Maybe.from_optional(None).map_nothing(lambda: 5)
        Just(5)
        """
        ...

    @abstractmethod
    def _lift2[R, U](self, f: Callable[[T, R], U], other: "Maybe[R]") -> "Maybe[U]":
        """
        Prefer using Maybe.lift2 instead of this method.

        Given a function that takes two arguments, and another Maybe, apply the
        function to the value of this Maybe and the other Maybe, if they both
        have values.

        Analogous to the `Option::zip_wth` in Rust and the `liftA2` in Haskell.

        >>> Just(1)._lift2(lambda x, y: x + y, Just(2))
        Just(3)

        >>> Just(1)._lift2(lambda x, y: x + y, Nothing())
        Nothing()

        >>> Nothing()._lift2(lambda x, y: x + y, Just(2))
        Nothing()

        """
        ...

    @abstractmethod
    def bind[R](self, f: Callable[[T], "Maybe[R]"]) -> "Maybe[R]":
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
    def and_then[R](self, f: Callable[[T], "Maybe[R]"]) -> "Maybe[R]":
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
    def filter_typed[R](self, f: Callable[[T], TypeGuard[R]]) -> "Maybe[R]":
        """
        Filter the value of the Maybe, if it has one, based on a type guard.
        """
        ...

    @abstractmethod
    def filter(self, f: Callable[[T], bool]) -> "Maybe[T]":
        """
        Filter the value of the Maybe, returning Nothing if the predicate returns False.

        Analogous to `Option::filter` in Rust.

        >>> Just(1).filter(lambda x: x > 1)
        Nothing()
        >>> Just(1).filter(lambda x: x < 1)
        Nothing()
        >>> Just(1).filter(lambda x: x == 1)
        Just(1)
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
    def __or__[R](self, other: "Maybe[R]") -> Union["Maybe[T]", "Maybe[R]"]:
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

    @staticmethod
    def lift2[
        A, B, R
    ](
        operation: Callable[[A, B], R],
    ) -> Callable[
        ["Maybe[A]", "Maybe[B]"], "Maybe[R]"
    ]:
        """
        Given a binary function and two Maybe objects, apply the function to the values of the Maybe objects, if they both have values.

        This method is analogous to the `Option::zip_with` in Rust and the `liftA2` in Haskell.

        Usage:
        >>> Maybe.lift2(lambda x, y: x + y)(Just(5), Just(7))
        Just(12)

        >>> Maybe.lift2(lambda x, y: x + y)(Just(5), Nothing())
        Nothing()

        >>> Maybe.lift2(lambda x, y: x + y)(Nothing(), Just(7))
        Nothing()
        """

        def lifted(left: "Maybe[A]", right: "Maybe[B]") -> "Maybe[R]":
            return left._lift2(operation, right)

        return lifted


class Just[T](Maybe[T]):
    __match_args__ = ("value",)
    __slots__ = ("value",)

    value: T

    def __init__(self, value: T):
        self.value = value

    def map[R](self, f: Callable[[T], R]) -> "Just[R]":
        return Just(f(self.value))

    def map_nothing(self, f: Callable[[], T]) -> "Just[T]":
        return self or Just(f())

    @overload
    def _lift2[R, U](self, f: Callable[[T, R], U], other: "Just[R]") -> "Just[U]":
        ...

    @overload
    def _lift2[R, U](self, f: Callable[[T, R], U], other: "Nothing[R]") -> "Nothing[U]":
        ...

    @overload
    def _lift2[R, U](self, f: Callable[[T, R], U], other: "Maybe[R]") -> "Maybe[U]":
        ...

    def _lift2[R, U](self, f: Callable[[T, R], U], other: Maybe[R]) -> Maybe[U]:
        return other.map(lambda x: f(self.value, x))

    def bind[R](self, f: Callable[[T], Maybe[R]]) -> Maybe[R]:
        return f(self.value)

    def and_then[R](self, f: Callable[[T], Maybe[R]]) -> Maybe[R]:
        return self.bind(f)

    def unwrap(
        self, f: Optional[Callable[[], Union[Exception, Type[Exception]]]] = None
    ) -> T:
        return self.value

    def unwrap_or(self, default: T) -> T:
        return self.value

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return self.value

    def filter_typed[R](self, f: Callable[[T], TypeGuard[R]]) -> Maybe[R]:
        if f(self.value):
            return Just(self.value)
        return Nothing()

    def filter(self, f: Callable[[T], bool]) -> Maybe[T]:
        return self if f(self.value) else Nothing()

    def to_optional(self) -> T:
        return self.value

    @overload
    def __and__[R](self, other: "Just[R]") -> "Just[R]":
        ...

    @overload
    def __and__[R](self, other: "Nothing[R]") -> "Nothing[R]":
        ...

    @overload
    def __and__[R](self, other: Maybe[R]) -> Union[Maybe[T], Maybe[R]]:
        ...

    def __and__[R](self, other: Maybe[R]) -> Union[Maybe[T], Maybe[R]]:
        return other

    @overload
    def __or__(self, other: "Just") -> "Just[T]":
        ...

    @overload
    def __or__(self, other: "Nothing") -> "Just[T]":
        ...

    @overload
    def __or__[R](self, other: Maybe[R]) -> Union[Maybe[T], Maybe[R]]:
        ...

    def __or__[R](self, other: Maybe[R]) -> Union[Maybe[T], Maybe[R]]:
        return self

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Just) and self.value == other.value

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"Just({self.value!r})"


class Nothing[T](Maybe[T]):
    __match_args__ = ()
    __slots__ = ()

    instance: Optional["Nothing[T]"] = None

    def __new__(cls) -> "Nothing[T]":
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def map[R](self, f: Callable[[T], R]) -> "Nothing[R]":
        return Nothing()

    def map_nothing(self, f: Callable[[], T]) -> "Just[T]":
        return Just(f())

    def _lift2[R, U](self, f: Callable[[T, R], U], other: Maybe[R]) -> Maybe[U]:
        return Nothing()

    def bind[R](self, f: Callable[[T], Maybe[R]]) -> "Nothing[R]":
        return Nothing()

    def and_then[R](self, f: Callable[[T], Maybe[R]]) -> "Nothing[R]":
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

    def filter_typed[R](self, f: Callable[[T], TypeGuard[R]]) -> "Nothing[R]":
        return Nothing()

    def filter(self, f: Callable[[T], bool]) -> "Nothing[T]":
        return Nothing()

    def to_optional(self) -> None:
        return None

    @overload
    def __and__(self, other: "Just") -> "Nothing[T]":
        ...

    @overload
    def __and__[R](self, other: "Nothing[R]") -> "Nothing[R]":
        ...

    def __and__[R](self, other: Maybe[R]) -> Union["Nothing[T]", Maybe[R]]:
        return other if isinstance(other, Nothing) else self

    @overload
    def __or__[R](self, other: "Just[R]") -> "Just[R]":
        ...

    @overload
    def __or__[R](self, other: "Nothing[R]") -> "Nothing[R]":
        ...

    def __or__[R](self, other: Maybe[R]) -> Union["Nothing[T]", Maybe[R]]:
        return other

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Nothing)

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Nothing()"
