from sanic import Blueprint
from Heliotrope.utils.hitomi import hitomi
from sanic.exceptions import abort
from sanic.response import json
from Heliotrope.utils.checker.check import authorized

galleryinfo = Blueprint("hitomi_galleryinfo", url_prefix="/galleryinfo")


@galleryinfo.route("/<index>")
@authorized()
async def hitomi_galleryinfo(request, index: int):
    json_ = await hitomi.galleryinfo(index)
    if not json_:
        return abort(404)
    else:
        return json(json_)
