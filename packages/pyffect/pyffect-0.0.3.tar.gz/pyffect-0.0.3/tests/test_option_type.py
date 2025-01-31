import pytest

from pyffect import Some, NONE, Option


def test_option():
    assert Some(7).is_defined is True
    assert Some(7).is_empty is False
    assert NONE().is_defined is False
    assert NONE().is_empty is True
    assert Some(6).value == 6
    with pytest.raises(ValueError):
        assert NONE().value

    assert Some(6).get_or_else(5) == 6
    assert NONE().get_or_else(5) == 5
    assert NONE().get_or_else(None) is None
    assert NONE() == NONE()
    assert NONE() != Some(6)
    assert Some(5) != Some(6)
    assert Some(5) == Some(5)
    assert Option.of(5).is_defined
    assert Option.of(None).is_empty


