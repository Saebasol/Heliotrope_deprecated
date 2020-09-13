from sanic import Blueprint
from sanic.response import json

from Heliotrope.utils.checker.check import authorized
from Heliotrope.utils.database import user_register

register = Blueprint("register", url_prefix="/register")


@register.route(
    "/",
    methods=["POST"],
)
@authorized()
async def api_register(request):
    user_id = request.json.get("user_id")
    if not user_id:
        return json({"status": "bad_request"}, 400)

    result = user_register(user_id)

    return result
