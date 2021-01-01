import os
from functools import wraps

from sanic.response import json

from Heliotrope.utils.database.user_management import user_register


def check_request_for_authorization_status(request):
    token = request.headers.get("Authorization")
    in_database = user_register(token, check=True)
    if not token or not in_database:
        return False
    else:
        return True


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = check_request_for_authorization_status(request)

            if os.environ.get("TEST_FLAG") or is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json({"status": 403, "message": "not_authorized"}, 403)

        return decorated_function

    return decorator
