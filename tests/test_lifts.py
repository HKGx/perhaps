from perhaps import Just, Maybe, Nothing


def test_liftA2():
    combine = Maybe.lift2(int.__add__)
    result = combine(Just(5), Just(7))
    assert result == Just(12)

    result = combine(Just(5), Nothing())
    assert result == Nothing()

    result = combine(Nothing(), Nothing())
    assert result == Nothing()


def test_liftA2_str():
    combine = Maybe.lift2(str.__add__)
    result = combine(Just("abc"), Just("def"))
    assert result == Just("abcdef")

    result = combine(Just("abc"), Nothing())
    assert result == Nothing()

    result = combine(Nothing(), Nothing())
    assert result == Nothing()


def test_lift2():
    result = Just(5)._lift2(int.__add__, Just(7))
    assert result == Just(12)

    result = Just(5)._lift2(int.__add__, Nothing())
    assert result == Nothing()

    result = Nothing()._lift2(int.__add__, Nothing())
    assert result == Nothing()
