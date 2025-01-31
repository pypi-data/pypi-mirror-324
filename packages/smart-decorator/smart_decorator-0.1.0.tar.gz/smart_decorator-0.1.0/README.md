# Smart Decorator

A static-typed library for creating decorators.


```python
from smart_decorator import simple_decorator

_events = {}

@simple_decorator
def register(callback, *, event_type: str = 'normal'):
    _events[event_type] = callback
    return callback


@register # Parentheses optional
def on_normal():
    print('an event happened!')

@register(event_type='error')
def on_error():
    print('an error!')

# can be used as a normal function, too
def on_close():
    print('closing!')

register(on_close, event_type='close')

```


## Documentation

### ```@simple_decorator```

Turn a function into a smart decorator, as shown above. The decorator must accept a func, and some optional keyword arguments. Simple decorators must either return the func unchanged, or a wrapper with the *same signature* (see @decorator for signature morphing!).

```python

@simple_decorator
def my_function(func, *, option1, option2 = ...):
    def wrapper(*args, **kwargs):
        ... # do something
        return func(*args, **kwargs)
    return wrapper
```


### ```@decorator```

The same as ```@simple_decorator``` but the decorator can return anything, such as a function with a different signature. Decorators declared this way should ideally be static-typed.

```python

@decorator
def inject_foo[**P, R](
    func: Callable[Concatenate[str, P], R], # static-typing to inject a parameter
    *,
    what_to_inject: str = 'foo'
) -> Callable[P, R]:
    
    def wrapper_func(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(what_to_inject, *args, **kwargs)

    return wrapper_func


@inject_foo
def add_stuff(what: str, cool: str) -> str:
    return what + cool

assert add_stuff('bar') == 'foobar'


```