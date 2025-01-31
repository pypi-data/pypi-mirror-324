from typing import Any, Callable

from smart_decorator._decorator_factory import create_decorator_factory
from smart_decorator.types import UNSET
from smart_decorator.utils import safe_wraps


def decorator(dec_func):

    def wrapper_factory(
        dec_func: Callable, wrapped: Callable, dec_args: tuple, dec_kwargs: dict
    ) -> Any:
        return safe_wraps(dec_func(wrapped, *dec_args, **dec_kwargs), wrapped)

    return create_decorator_factory(dec_func, wrapper_factory=wrapper_factory)
