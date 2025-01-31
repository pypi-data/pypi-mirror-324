from functools import update_wrapper
from types import FunctionType


def safe_wraps(wrapper, wrapped):
    if (
        wrapper is not wrapped
        and isinstance(wrapper, (FunctionType, type))
        and (isinstance(wrapper, type(wrapped)) or isinstance(wrapped, type(wrapper)))
    ):
        try:
            update_wrapper(wrapper, wrapped)
        except (AttributeError, TypeError, KeyError):
            pass
    return wrapper
