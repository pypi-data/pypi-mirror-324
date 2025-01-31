# flake8: noqa

from collections.abc import Callable
from typing import Concatenate


type DecoratorFunctionType[
    DecoratedFunction, **DecoratorArgs, DecoratorReturnType
] = Callable[Concatenate[DecoratedFunction, DecoratorArgs], DecoratorReturnType]

type Method[SelfT, **ArgT, ReturnT] = Callable[Concatenate[SelfT, ArgT], ReturnT]
