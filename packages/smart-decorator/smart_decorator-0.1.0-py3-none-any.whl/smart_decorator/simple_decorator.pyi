from collections.abc import Callable
from typing import Protocol, overload
from smart_decorator.types import DecoratorFunctionType

class _SimpleDecorator(Protocol):
    def __call__[**P, T](self, func: Callable[P, T], /) -> Callable[P, T]: ...

class _SimpleDecoratorFactory[**DecoratorArgs](Protocol):
    @overload
    def __call__[
        **P, T
    ](
        self,
        func: Callable[P, T],
        *args: DecoratorArgs.args,
        **kwargs: DecoratorArgs.kwargs,
    ) -> Callable[P, T]: ...
    @overload
    def __call__(
        self, *args: DecoratorArgs.args, **kwargs: DecoratorArgs.kwargs
    ) -> _SimpleDecorator: ...

def simple_decorator[
    DecoratedFunction: Callable, **DecoratorArgs,
](
    dec_func: DecoratorFunctionType[DecoratedFunction, DecoratorArgs, DecoratedFunction]
) -> _SimpleDecoratorFactory[DecoratorArgs]: ...
