from collections.abc import Callable
from functools import wraps
from typing import Any, Protocol, TypeVar

from smart_decorator.types import UNSET


class WrapperFactory(Protocol):
    def __call__(
        self,
        /,
        dec_func: Callable,
        wrapped: Callable,
        dec_args: tuple,
        dec_kwargs: dict,
    ) -> Any: ...


def create_decorator_factory(dec_func: Callable, wrapper_factory: WrapperFactory):
    @wraps(dec_func)
    def smart_decorator_factory(func_or_pos_arg=UNSET, *args, **kwargs):

        if callable(func_or_pos_arg):
            # called as a simple decorator or a normal function

            return wrapper_factory(
                dec_func=dec_func,
                wrapped=func_or_pos_arg,
                dec_args=args,
                dec_kwargs=kwargs,
            )

        elif args and callable(args[0]):
            # To avoid ambiguity between @decorator and @decorator(argument),
            # we require the positional arguments to not be callable.
            raise TypeError(
                f"Positional argument in {dec_func.__name__} must not be callable"
            )
        elif func_or_pos_arg is UNSET:
            # called as a decorator factory with no positional arguments

            def _smart_decorator(func):
                return wrapper_factory(
                    dec_func=dec_func,
                    wrapped=func,
                    dec_args=args,
                    dec_kwargs=kwargs,
                )

            return _smart_decorator
        else:
            # called as a decorator factory with positional arguments
            def _smart_decorator(func):
                return wrapper_factory(
                    dec_func=dec_func,
                    wrapped=func,
                    dec_args=(func_or_pos_arg, *args),
                    dec_kwargs=kwargs,
                )

            return _smart_decorator

    return smart_decorator_factory
