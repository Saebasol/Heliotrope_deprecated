import os
from functools import wraps

from sanic.response import json


def check_request_for_authorization_status(request):
    token = request.headers.get("Authorization")
    if not token or token not in os.environ["Authorization"]:
        return False
    else:
        return True


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = check_request_for_authorization_status(request)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({"status": 403, "message": "not_authorized"}, 403)

        return decorated_function

    return decorator
