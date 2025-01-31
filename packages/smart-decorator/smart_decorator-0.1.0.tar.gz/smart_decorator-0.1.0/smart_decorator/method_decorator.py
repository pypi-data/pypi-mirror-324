from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property, update_wrapper, wraps
from smart_decorator._decorator_factory import create_decorator_factory
from smart_decorator.types import UNSET


def method_decorator(dec_func):

    return create_decorator_factory(dec_func, DecoratedMethod)


@dataclass
class DecoratedMethod:
    dec_func: Callable
    wrapped: Callable
    dec_args: tuple
    dec_kwargs: dict
    __name__: str = ""
    __qualname__: str = ""

    def __post_init__(self):
        update_wrapper(self, self.wrapped)

    def __call__(self, *args, **kwargs):
        return self.decorated_non_method(*args, **kwargs)

    def __get__(self, obj, objtype):
        func = self.wrapped
        dec_func = self.dec_func
        d_args = self.dec_args
        d_kwds = self.dec_kwargs
        if obj is not None:
            return dec_func(bind_method(func, obj, objtype), *d_args, **d_kwds)
        else:

            @wraps(func)
            def unbound_method_wrapper(self, *args, **kwds):
                if not isinstance(self, objtype):
                    raise TypeError(
                        f'Parameter "self" must be of type {objtype.__name__}'
                    )
                return dec_func(bind_method(func, obj, objtype), *d_args, **d_kwds)(
                    *args, **kwds
                )

            return unbound_method_wrapper

    def __set_name__(self, owner, name: str):
        self.__name__ = name
        self.__qualname__ = f"{owner.__qualname__}.{name}"

    @cached_property
    def decorated_non_method(self):
        return self.dec_func(self.wrapped, *self.dec_args, **self.dec_kwargs)


def bind_method(func, obj, objtype):
    return func.__get__(obj, objtype)
