import os
from functools import wraps

from nacl.encoding import Base64Encoder
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey
from sanic.response import json


async def check_request_for_authorization_status(request):
    api_key: str = request.headers.get("Authorization")
    if not api_key:
        return False
    else:
        verify = VerifyKey(
            "+h1d9bCXPTmJl71Ek80xxr31P0Fzjt+qMNfR9c37WMA=".encode(),
            encoder=Base64Encoder,
        )
        try:
            verify.verify(api_key.encode(), encoder=Base64Encoder)
        except BadSignatureError:
            return False
        else:
            return True


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if os.environ.get("TEST_FLAG"):
                is_authorized = True
            else:
                is_authorized = await check_request_for_authorization_status(request)

            if is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json({"status": 403, "message": "not_authorized"}, 403)

        return decorated_function

    return decorator
