from inspect import signature

from pydantic import BaseModel, ValidationError
from functools import wraps


def strict(func):
    annotations = func.__annotations__
    if 'return' in annotations:
        del annotations['return']

    class ArgsModel(BaseModel):
        __annotations__ = annotations

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_sig = signature(func)  # get func params and values
        bound_args = func_sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        try:
            ArgsModel(**bound_args.arguments)
        except ValidationError as e:
            raise TypeError(f'Error validation args to func sum_two: {e}')
        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b
