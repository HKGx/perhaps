from typing import cast

import pytest

from perhaps import Just, Maybe, Nothing


def test_create_just():
    assert Just(1) == Just(1)
    assert Just(1) != Just(2)
    assert Just(1) != Nothing()


def test_create_nothing():
    assert Nothing() == Nothing()
    assert Nothing() != Just(1)


def test_unwrap_or_else():
    assert Just(1).unwrap_or_else(lambda: 2) == 1
    assert Nothing().unwrap_or_else(lambda: 2) == 2


def test_map():
    assert Just(1).map(lambda x: x + 1) == Just(2)
    assert Nothing().map(lambda x: x + 1) == Nothing()


def test_lift2():
    assert Just(1).lift2(lambda x, y: x + y, Just(2)) == Just(3)
    assert (
        Just(1).lift2(lambda x, y: x + y, Nothing[int]()) == Nothing()
    )  # annotation for Nothing is required here, though most often it can be inferred
    assert Nothing().lift2(lambda x, y: x + y, Just(2)) == Nothing()
    maybe1 = cast(Maybe[int], Nothing())
    assert maybe1.lift2(lambda x, y: x + y, Just(2)) == Nothing()
    maybe2 = cast(Maybe[int], Just(3))
    assert maybe1.lift2(lambda x, y: x + y, maybe2) == Nothing()
    assert maybe2.lift2(lambda x, y: x * y, maybe2) == Just(9)


def test_bind():
    assert Just(1).bind(lambda x: Just(x + 1)) == Just(2)
    assert Nothing().bind(lambda x: Just(x + 1)) == Nothing()


def test_and_then():
    assert Just(1).and_then(lambda x: Just(x + 1)) == Just(1).bind(
        lambda x: Just(x + 1)
    )
    assert Nothing().and_then(lambda x: Just(x + 1)) == Nothing().bind(
        lambda x: Just(x + 1)
    )


def test_and():
    assert Just(1) & Just(2) == Just(2)
    assert Just(1) & Nothing() == Nothing()
    # `and` has lower precedence than `!=`
    # so this is equivalent to `Nothing() and (Just(2)) != Nothing())`
    # `and` short-circuits, so the second operand is not evaluated
    # so this is equivalent to simply `Nothing()`
    # this may be surprising, so please use `&` instead
    assert not (Nothing() and Just(2) != Nothing())
    assert Nothing() & Just(2) == Nothing()
    assert Nothing() & Nothing() == Nothing()


def test_or():
    assert Just(1) | Just(2) == Just(1)
    assert Just(1) | Nothing() == Just(1)
    assert Nothing() | Just(2) == Just(2)
    assert Nothing() | Nothing() == Nothing()


def test_unwrap():
    assert Just(1).unwrap() == 1
    with pytest.raises(ValueError):
        Nothing().unwrap()
    with pytest.raises(TypeError):
        Nothing().unwrap(lambda: TypeError("oops"))


def test_unwrap_or():
    assert Just(1).unwrap_or(2) == 1
    assert Nothing().unwrap_or(2) == 2


def test_filter():
    assert Just(1).filter(lambda x: x > 1) == Nothing()
    assert Just(1).filter(lambda x: x < 1) == Nothing()
    assert Just(1).filter(lambda x: x == 1) == Just(1)


def test_from_try():
    assert Maybe.from_try(lambda: 1 / 1, ZeroDivisionError) == Just(1)
    assert Maybe.from_try(lambda: 1 / 0, ZeroDivisionError) == Nothing()


def test_from_optional():
    assert Maybe.from_optional(1) == Just(1)
    assert Maybe.from_optional(None) == Nothing()


def test_to_optional():
    assert Just(1).to_optional() == 1
    assert Nothing().to_optional() == None


def test_is_operator():
    assert Nothing() is Nothing()
    assert Just(1) is not Just(1)
    assert Just(1) is not Nothing()
    assert Nothing() is not Just(1)
