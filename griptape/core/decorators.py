import functools
from schema import Schema, And, Use


def action(config: dict):
    __config_schema().validate(config)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.is_action = True
        wrapper.config = config

        return wrapper
    return decorator


def __config_schema() -> Schema:
    return Schema({
        "name": str,
        "description": str,
        "value_schema": Schema
    }, ignore_extra_keys=True)
