from collections.abc import Callable
from typing import Any, Concatenate, Never, Protocol, overload
from smart_decorator.types import DecoratorFunctionType, Method
from smart_decorator.smart_decorator import _SmartDecoratorFactory

def method_decorator[
    **InArgT,
    InRetT, **OutArgT,
    OutRetT, **DecArgT,
](
    dec_func: DecoratorFunctionType[
        Callable[InArgT, InRetT],
        DecArgT,
        Callable[OutArgT, OutRetT],
    ]
) -> _MethodDecoratorFactory[
    InArgT,
    InRetT,
    OutArgT,
    OutRetT,
    DecArgT,
]: ...

class _MethodDecoratorFactory[**InArgT, InRetT, **OutArgT, OutRetT, **DecArgT](
    Protocol
):
    @overload  # func is a method, or it has at least 1 positional argument.
    #           we don't know yet which one!
    def __call__[
        FirstArgOrSelfT
    ](
        self,
        func: Method[FirstArgOrSelfT, InArgT, InRetT],
        /,
        *args: DecArgT.args,
        **kwargs: DecArgT.kwargs,
    ) -> DecoratedMethod[FirstArgOrSelfT, OutArgT, OutRetT]: ...
    @overload  # if func has no positional arguments
    def __call__(
        self,
        func: Callable[InArgT, InRetT],
        /,
        *args: DecArgT.args,
        **kwargs: DecArgT.kwargs,
    ) -> _DecoratedFunctionNotMethod[OutArgT, OutRetT]: ...
    @overload  # called without func (decorator factory style)
    def __call__(
        self, /, *args: DecArgT.args, **kwargs: DecArgT.kwargs
    ) -> _MethodDecorator[InArgT, InRetT, OutArgT, OutRetT]: ...

class _MethodDecorator[**InArgT, InRetT, **OutArgT, OutRetT](Protocol):
    @overload
    def __call__[
        FirstArgOrSelfT
    ](self, func: Method[FirstArgOrSelfT, InArgT, InRetT], /) -> DecoratedMethod[
        FirstArgOrSelfT, OutArgT, OutRetT
    ]: ...
    @overload
    def __call__(
        self, func: Callable[InArgT, InRetT], /
    ) -> _DecoratedFunctionNotMethod[OutArgT, OutRetT]: ...

class DecoratedMethod[FirstArgOrSelfT, **ArgsType, ReturnType](Protocol):
    def __call__(  # Not a method. first_arg is just a normal arg.
        self,
        first_arg: FirstArgOrSelfT,
        /,
        *args: ArgsType.args,
        **kwargs: ArgsType.kwargs,
    ) -> ReturnType: ...
    @overload  # Create an unbound method.
    def __get__(
        self, instance: None, owner: Any = None
    ) -> Callable[Concatenate[FirstArgOrSelfT, ArgsType], ReturnType]: ...
    @overload  # Create a bound method.
    def __get__(
        self, instance: FirstArgOrSelfT, owner: Any = None
    ) -> Callable[ArgsType, ReturnType]: ...

class _DecoratedFunctionNotMethod[**ArgT, RetT](Protocol):
    def __call__(self, *args: ArgT.args, **kwargs: ArgT.kwargs) -> RetT: ...
    def __get__(self, obj, obj_type) -> _NeverFunc: ...

class _NeverFunc(Protocol):
    def __call__(__self, self: Never, *args: Never, **kwargs: Never) -> Never: ...
