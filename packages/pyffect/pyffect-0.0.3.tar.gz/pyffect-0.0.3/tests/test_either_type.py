import pytest

from pyffect import Either, Some, NONE, Right, Left


def sendRight(value: Either[str, int]):
    assert value.is_right
    assert value.to_option == Some(5)


def sendLeft(value: Either[str, int]):
    assert value.is_left
    assert value.to_option == NONE()


def test_either():
    with pytest.raises(TypeError):
        assert Either(5, "6")

    assert Right(5).is_left is False
    assert Right(5).is_right is True
    assert Left("test").is_left is True
    assert Left("test").is_right is False

    sendRight(Right(5))
    sendLeft(Left("5"))

    assert Right(5).right_value == 5

    with pytest.raises(ValueError):
        assert Right(5).left_value

    assert Left("test").left_value == "test"

    with pytest.raises(ValueError):
        assert Left("test").right_value

    assert Left("5") == Left("5")
    assert Left("5") != Left("6")
    assert Left("5") != Left(5)
    assert Left("5") != Right("5")
    assert Right("5") == Right("5")
    assert Right("5") != Right("6")
