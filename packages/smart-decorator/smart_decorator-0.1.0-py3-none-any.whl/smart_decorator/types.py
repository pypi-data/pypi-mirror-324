import sys
from typing import TYPE_CHECKING


if sys.version_info >= (3, 12) or TYPE_CHECKING:

    from smart_decorator._types import (
        Method as Method,
        DecoratorFunctionType as DecoratorFunctionType,
    )

else:

    class _GenericType:
        def __getitem__(self, item):
            return Method

    Method = DecoratorFunctionType = _GenericType()

UNSET = object()
