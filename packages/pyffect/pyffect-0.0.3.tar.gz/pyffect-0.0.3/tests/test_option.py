import pytest


from pyffect import NONE, Some, Option


# Assuming the Option class and its children (Some, NONE) are defined as above

def test_is_empty_deprecation_warning():
    option = Some(10)

    # Check if accessing isEmpty raises a deprecation warning
    with pytest.deprecated_call():
        _ = option.isEmpty  # Accessing the deprecated property


def test_is_defined_deprecation_warning():
    option = Some(10)

    # Check if accessing isDefined raises a deprecation warning
    with pytest.deprecated_call():
        _ = option.isDefined  # Accessing the deprecated property


def test_get_or_else_deprecation_warning():
    option = Some(10)

    # Check if accessing getOrElse raises a deprecation warning
    with pytest.deprecated_call():
        _ = option.getOrElse(5)  # Accessing the deprecated property


def test_from_value_deprecation_warning():
    # Check if accessing fromValue raises a deprecation warning
    with pytest.deprecated_call():
        _ = Option.fromValue(10)  # Accessing the deprecated class method


def test_is_empty_property():
    none = NONE()
    some = Some(10)

    # Test new property
    assert none.is_empty is True
    assert some.is_empty is False


def test_is_defined_property():
    none = NONE()
    some = Some(10)

    # Test new property
    assert none.is_defined is False
    assert some.is_defined is True


def test_get_or_else_property():
    none = NONE()
    some = Some(10)

    # Test new method
    assert none.get_or_else(5) == 5
    assert some.get_or_else(5) == 10


def test_from_value_property():
    # Test new class method
    none = Option.of(None)
    some = Option.of(10)
    assert isinstance(none, NONE)
    assert isinstance(some, Some)
    assert some._value == 10
