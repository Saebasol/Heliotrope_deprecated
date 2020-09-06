from sanic import Blueprint
from Heliotrope.utils.hitomi import hitomi
from sanic.exceptions import abort
from sanic.response import json

list_ = Blueprint("hitomi_list", url_prefix="/list")


@list_.route("/<num>")
async def hitomi_list(request, num: int):
    hitomi_info_list = await hitomi.list_(int(num) - 1)
    if not hitomi_info_list:
        return abort(404)
    else:
        return json(hitomi_info_list)
