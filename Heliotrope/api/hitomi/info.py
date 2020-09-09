from sanic import Blueprint
from Heliotrope.utils.hitomi import hitomi
from sanic.exceptions import abort
from sanic.response import json
from Heliotrope.utils.checker.check import authorized

info = Blueprint("hitomi_info", url_prefix="/info")


@info.route("/<index>")
@authorized()
async def hitomi_info(request, index: int):
    json_ = await hitomi.info(index)
    if not json_:
        return abort(404)
    else:
        return json(json_)