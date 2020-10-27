from sanic import Blueprint
from sanic.response import json

from Heliotrope.utils.checker.check import authorized
from Heliotrope.utils.database import Management

register = Blueprint("register", url_prefix="/register")


@register.route(
    "/",
    methods=["POST"],
)
@authorized()
async def api_register(request):
    user_id = request.json.get("user_id")
    check = request.json.get("check")
    if not user_id or check is None:
        return json({"status": 400, "message": "bad_request"}, 400)

    db = Management(user_id)
    result = await db.user_register(check)

    return result
