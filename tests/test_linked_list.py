from __future__ import annotations

from typing import Iterator

import pytest

from perhaps import Just, Maybe, Nothing


class Node[T]:
    value: T
    next: Maybe[Node[T]]

    def __init__(self, value: T, parent: Maybe[Node[T]] = Nothing()) -> None:
        self.value = value
        self.next = Nothing()

        # TODO: Make this prettier
        if parent != Nothing():
            parent.unwrap().next = Just(self)

    def __repr__(self) -> str:
        # FIXME: This repr is recursive, it may not be a good idea
        return f"Node({self.value!r}) -> {self.next!r}"


class LinkedList[T](Iterator[Node[T]]):
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


def test_nodes():
    node1 = Node("first")
    node2 = Node("second", parent=Just(node1))
    node3 = Node("third", parent=Just(node2))

    assert node1.next == Just(node2)
    assert node2.next == Just(node3)
    assert node3.next == Nothing()


def test_linked_list():
    node1 = Node("first")
    node2 = Node("second", parent=Just(node1))
    node3 = Node("third", parent=Just(node2))

    llist = LinkedList(node1)

    assert next(llist) == node1
    assert next(llist) == node2
    assert next(llist) == node3
    with pytest.raises(StopIteration):
        next(llist)
