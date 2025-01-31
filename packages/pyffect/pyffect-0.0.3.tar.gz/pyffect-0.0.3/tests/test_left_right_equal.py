from pyffect import Left, Right


def test_left_equality_same_value():
    left1 = Left(10)
    left2 = Left(10)
    assert left1 == left2  # Same value should be equal

def test_left_equality_different_value():
    left1 = Left(10)
    left2 = Left(20)
    assert left1 != left2  # Different values should not be equal

def test_right_equality_same_value():
    right1 = Right(10)
    right2 = Right(10)
    assert right1 == right2  # Same value should be equal

def test_right_equality_different_value():
    right1 = Right(10)
    right2 = Right(20)
    assert right1 != right2  # Different values should not be equal

def test_left_right_inequality():
    left = Left(10)
    right = Right(10)
    assert left != right  # Left and Right should not be equal

def test_same_type_diff_value():
    left = Left(10)
    right = Right(10)
    assert left != right  # Different types (Left vs Right) should not be equal

def test_different_type_comparison():
    left = Left(10)
    not_a_either = 10  # Just an integer, not an instance of Either
    assert left != not_a_either  # Left is not equal to an object of another type
