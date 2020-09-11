from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json

from Heliotrope.utils.checker.check import authorized
from Heliotrope.utils.hitomi import hitomi

galleryinfo = Blueprint("hitomi_galleryinfo", url_prefix="/galleryinfo")


@galleryinfo.route("/<index>")
@authorized()
async def hitomi_galleryinfo(request, index: int):
    json_ = await hitomi.galleryinfo(index)
    if not json_:
        return json({"status":"not_found"}, 404)
    else:
        return json(json_)
