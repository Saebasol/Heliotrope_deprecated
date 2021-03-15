from functools import wraps
from typing import Literal, get_args
from sanic.request import Request

from sanic.response import json
from inspect import getfullargspec


def hiyobot_only(f):
    @wraps(f)
    async def decorator_function(request, *args, **kwargs):
        is_hiyobot = True

        if is_hiyobot:
            response = await f(request, *args, **kwargs)
            return response
        return json({"status": 403, "message": "not_authorized"}, 403)

    return decorator_function


def authorized(f):
    @wraps(f)
    async def decorated_function(request, *args, **kwargs):

        is_authorized = True

        if is_authorized:
            response = await f(request, *args, **kwargs)
            return response
        return json({"status": 403, "message": "not_authorized"}, 403)

    return decorated_function


def strict_literal(argument_name: str):
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            full_arg_spec = getfullargspec(f)
            arg_annoration = full_arg_spec.annotations[argument_name]
            if arg_annoration.__origin__ is Literal:
                literal_list = get_args(arg_annoration)
                arg_index = full_arg_spec.args.index(argument_name)

                if arg_index < len(args) and args[arg_index] not in literal_list:
                    raise ValueError(
                        f"Arguments do not match. Expected: {literal_list}"
                    )
                elif recive_arg := kwargs.get(argument_name):
                    if recive_arg not in literal_list:
                        raise ValueError(
                            f"Arguments do not match. Expected: {literal_list}"
                        )

            return await f(*args, **kwargs)

        return decorated_function

    return decorator