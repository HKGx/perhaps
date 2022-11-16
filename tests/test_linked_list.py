from __future__ import annotations

from typing import Generic, Iterator, TypeVar

from perhaps import Just, Maybe, Nothing

T = TypeVar("T")


class Node(Generic[T]):
    value: T
    next: Maybe[Node]

    def __init__(self, value: T, parent: Maybe[Node] = Nothing()) -> None:
        self.value = value
        self.next = Nothing()

        # TODO: Make this prettier
        if parent != Nothing():
            parent.unwrap().next = Just(self)

    def __repr__(self) -> str:
        # FIXME: This repr is recursive, it may not be a good idea
        return f"Node({self.value!r}) -> {self.next!r}"


class LinkedList(Generic[T], Iterator[Node[T]]):
    head: Node[T]
    current: Maybe[Node[T]]

    def __init__(self, head: Node[T]) -> None:
        self.head = head
        self.current = Just(self.head)

    def __next__(self) -> Node[T]:
        result = self.current.unwrap(lambda: StopIteration)
        self.current = result.next
        return result

    def __repr__(self) -> str:
        return f"LinkedList({self.head!r})"
