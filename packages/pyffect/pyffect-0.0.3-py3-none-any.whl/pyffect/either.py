from __future__ import annotations

import warnings
from typing import Generic, Union, Optional, final

from pyffect._types import E
from pyffect.option import T, NONE, Some, Option


class Either(Generic[T, E]):

    def __init__(self, left: Optional[T], right: Optional[E], *, _force: bool = False) -> None:
        if not _force:
            raise TypeError(
                'Cannot directly initialize, '
                'please use Left or Right.'
            )
        if left is None and right is None:
            raise ValueError('both cannot be none')

        if left is not None and right is not None:
            raise ValueError('both cannot be not none')

        self._left = left
        self._right = right
        self._type = type(self)

    @property
    def isLeft(self) -> bool:
        """Deprecated. Use `is_left` instead."""
        warnings.warn(
            "`isLeft` is deprecated, use `is_left` instead.",
            category=DeprecationWarning,
            stacklevel=2
        )
        return self.is_left

    @property
    def is_left(self) -> bool:
        """The preferred property to check if the value is Left."""
        return self._left is not None

    @property
    def isRight(self) -> bool:
        """Deprecated. Use `is_right` instead."""
        warnings.warn(
            "`isRight` is deprecated, use `is_right` instead.",
            category=DeprecationWarning,
            stacklevel=2  # This makes the warning point to the place where it's called
        )
        return self._right is not None

    @property
    def is_right(self) -> bool:
        """The preferred property to check if the value is Right."""
        return self._right is not None

    @property
    def leftValue(self) -> T:
        """Deprecated. Use `left_value` instead."""
        warnings.warn(
            "`leftValue` is deprecated, use `left_value` instead.",
            category=DeprecationWarning,
            stacklevel=2
        )
        return self.left_value

    @property
    def left_value(self) -> T:
        """The preferred property to access the Left value."""
        if self.is_right:
            raise ValueError('this is not Left')
        if self._left is None:
            raise ValueError('Left value is None, but expected a valid value')
        return self._left

    @property
    def rightValue(self) -> E:
        """Deprecated. Use `right_value` instead."""
        warnings.warn(
            "`rightValue` is deprecated, use `right_value` instead.",
            category=DeprecationWarning,
            stacklevel=2
        )

        return self.right_value

    @property
    def right_value(self) -> E:
        """The preferred property to access the Right value."""
        if self.is_left:
            raise ValueError('this is not Right')
        if self._right is None:
            raise ValueError('Right value is None, but expected a valid value')
        return self._right

    @property
    def toOption(self) -> Option[E]:
        """Deprecated. Use `to_option` instead."""
        warnings.warn(
            "`toOption` is deprecated, use `to_option` instead.",
            category=DeprecationWarning,
            stacklevel=2
        )
        return self.to_option

    @property
    def to_option(self) -> Option[E]:
        if self.is_right:
            if self._right is None:
                raise ValueError('Right value is None, but expected a valid value')
            return Some(self._right)
        else:
            return NONE()

    def __eq__(self, other: Union[Left, Right]):  # type: ignore
        return isinstance(other, self._type) and (self._left == other._left and self._right == other._right)


@final
class Left(Either[E, T]):
    def __init__(self, value: E) -> None:
        if value is None:
            raise ValueError('Left value cannot be None')
        super().__init__(right=None, left=value, _force=True)


@final
class Right(Either[E, T]):
    def __init__(self, value: T) -> None:
        if value is None:
            raise ValueError('Right value cannot be None')
        super().__init__(right=value, left=None, _force=True)
