from sanic import Blueprint
from Heliotrope.utils.hitomi import hitomi
from sanic.exceptions import abort
from sanic.response import json

info = Blueprint("hitomi_info", url_prefix="/info")


@info.route("/<index>")
async def hitomi_info(request, index: int):
    json_ = await hitomi.info(index)
    if not json_:
        return abort(404)
    else:
        return json(json_)