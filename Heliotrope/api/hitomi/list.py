from sanic import Blueprint
from sanic.response import json

from Heliotrope.utils.auth import authorized
from Heliotrope.utils.hitomi import hitomi

list_ = Blueprint("hitomi_list", url_prefix="/list")


@list_.route("/<num>")
@authorized()
async def hitomi_list(request, num: int):
    hitomi_info_list = await hitomi.list_(int(num) - 1)
    if not hitomi_info_list:
        return json({"status": 404, "message": "not_found"}, 404)
    else:
        return json(hitomi_info_list)
