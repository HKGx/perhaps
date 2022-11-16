from __future__ import annotations

from typing import TypeVar, Iterator, Generic

from perhaps import Maybe, Just, Nothing


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


def main():
    node_1 = Node("first")
    node_2 = Node("second", parent=Just(node_1))
    node_3 = Node("third", parent=Just(node_2))

    llist = LinkedList(node_1)

    for i in llist:
        print(i.value)


if __name__ == "__main__":
    main()
