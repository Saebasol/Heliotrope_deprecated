import os

from sanic import Blueprint
from sanic.response import json

from Heliotrope.utils.database.user_management import user_register

register = Blueprint("register", url_prefix="/register")


@register.route(
    "/",
    methods=["POST"],
)
async def _register(request):
    user_id = request.json.get("user_id")
    check_header = request.headers.get("Verification")
    if not user_id or check_header != os.environ["VERIFI"]:
        return json({"status": 400, "message": "bad_request"}, 400)
    else:
        return await user_register(user_id)
