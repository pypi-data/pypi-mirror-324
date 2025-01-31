# Test Cases
import pytest

from pyffect import Right, Left, NONE, Some


def test_left_creation():
    left = Left(10)
    assert left.is_left
    assert not left.is_right
    assert left.left_value == 10
    with pytest.raises(ValueError):
        left.right_value


def test_right_creation():
    right = Right(20)
    assert right.is_right
    assert not right.is_left
    assert right.right_value == 20
    with pytest.raises(ValueError):
        right.left_value


def test_deprecated_isLeft_warning():
    left = Left(10)

    with pytest.deprecated_call():
        _ = left.isLeft  # Accessing the deprecated property


def test_deprecated_isRight_warning():
    right = Right(20)

    # Check if accessing isRight raises a deprecation warning
    with pytest.deprecated_call():
        _ = right.isRight  # Accessing the deprecated property


def test_deprecated_leftValue_warning():
    left = Left(10)

    # Check if accessing leftValue raises a deprecation warning
    with pytest.deprecated_call():
        _ = left.leftValue  # Accessing the deprecated property


def test_deprecated_rightValue_warning():
    right = Right(20)

    # Check if accessing rightValue raises a deprecation warning
    with pytest.deprecated_call():
        _ = right.rightValue  # Accessing the deprecated property


def test_deprecated_toOption_warning():
    right = Right(20)

    # Check if accessing toOption raises a deprecation warning
    with pytest.deprecated_call():
        _ = right.toOption  # Accessing the deprecated property


def test_is_left_property():
    left = Left(10)
    assert left.is_left is True
    right = Right(20)
    assert right.is_left is False


def test_is_right_property():
    left = Left(10)
    assert left.is_right is False
    right = Right(20)
    assert right.is_right is True


def test_left_value_property():
    left = Left(10)
    assert left.left_value == 10
    with pytest.raises(ValueError):
        left.right_value


def test_right_value_property():
    right = Right(20)
    assert right.right_value == 20
    with pytest.raises(ValueError):
        right.left_value


def test_to_option_property():
    left = Left(10)
    assert isinstance(left.to_option, NONE)
    right = Right(20)
    assert isinstance(right.to_option, Some)
