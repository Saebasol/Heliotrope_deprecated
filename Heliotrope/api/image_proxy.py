from sanic import Blueprint
from sanic.response import json, raw

from Heliotrope.utils.hitomi.hitomi_requester import image_proxer

proxy = Blueprint("image_proxy", url_prefix="/proxy")


@proxy.route(
    "/<path>",
    methods=["GET"],
)
async def image_proxy(request, path: str):
    r = await image_proxer(path)

    if not isinstance(r, tuple):
        return json({"code": "404", "message": "not_found"}, 404) or r

    return raw(r[0], content_type=r[1])
