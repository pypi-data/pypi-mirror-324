from collections.abc import Callable
from typing import Protocol, overload
from smart_decorator.types import DecoratorFunctionType

def decorator[
    DecoratedFunction: Callable, **DecoratorArgs, DecoratorReturnType = DecoratedFunction
](
    dec_func: DecoratorFunctionType[DecoratedFunction, DecoratorArgs, DecoratorReturnType]
) -> _SmartDecoratorFactory[DecoratedFunction, DecoratorArgs, DecoratorReturnType]: ...


class _SmartDecoratorFactory[
    DecoratedFunction, **DecoratorArgs, DecoratorReturnType
    ](Protocol):
    
    @overload
    def __call__(
        self,
        func: DecoratedFunction,
        *args: DecoratorArgs.args,
        **kwargs: DecoratorArgs.kwargs
    ) -> DecoratorReturnType: ...
    @overload
    def __call__(
        self,
        *args: DecoratorArgs.args,
        **kwargs: DecoratorArgs.kwargs
    ) -> Callable[[DecoratedFunction], DecoratorReturnType]:
        ...



