from typing import Iterable, Iterator, Union

from perhaps import Just, Maybe, Nothing


class Peekable[T](Iterator[T]):
    current: Maybe[T]
    source: Iterator[T]

    def __init__(self, source: Union[Iterator[T], Iterable[T]]):
        self.source = iter(source)
        self.current = Maybe.from_try(lambda: next(self.source), StopIteration)

    def peek(self) -> Maybe[T]:
        return self.current

    def __next__(self) -> T:
        result = self.current.unwrap(lambda: StopIteration)
        self.current = Maybe.from_try(lambda: next(self.source), StopIteration)
        return result


def test_peekable_iterator():
    peekable = Peekable([1, 2, 3])
    assert peekable.peek() == Just(1)
    assert next(peekable) == 1
    assert peekable.peek() == Just(2)
    assert next(peekable) == 2
    assert peekable.peek() == Just(3)
    assert next(peekable) == 3
    assert peekable.peek() == Nothing()


def test_peekable_to_list():
    peekable = Peekable([1, 2, 3])
    assert list(peekable) == [1, 2, 3]
