import os

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from Heliotrope.utils.database.user_management import user_register

register = Blueprint("register", url_prefix="/register")


@register.route(
    "/",
    methods=["POST"],
)
async def _register(request: Request):
    user_id = request.json.get("user_id")
    api_key = request.json.get("api_key")
    check_header = request.headers.get("Verification")
    if check_header == f"check {os.environ['VERIFI']}":
        return await user_register(user_id, check=True)
    if not user_id or check_header != os.environ["VERIFI"]:
        return json({"status": 400, "message": "bad_request"}, 400)
    return await user_register(user_id, api_key)
