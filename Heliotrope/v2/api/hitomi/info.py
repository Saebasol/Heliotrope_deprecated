from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json

from Heliotrope.utils.checker.check import authorized
from Heliotrope.utils.hitomi import hitomi

info = Blueprint("hitomi_info", url_prefix="/info")


@info.route("/<index>")
@authorized()
async def hitomi_info(request, index: int):
    json_ = await hitomi.info(index)
    if not json_:
        return json({"status": 404, "message": "not_found"}, 404)
    else:
        return json(json_)
