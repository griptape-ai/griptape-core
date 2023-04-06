import functools
from schema import Schema


def action(name: str, schema: Schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.is_action = True
        wrapper.name = name
        wrapper.schema = schema

        return wrapper
    return decorator
