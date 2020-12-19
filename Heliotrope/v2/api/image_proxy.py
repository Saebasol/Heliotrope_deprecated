from sanic import Blueprint, response
from sanic.response import json

proxy = Blueprint("image_proxy", url_prefix="/proxy")


@proxy.route(
    "/<path>",
    methods=["GET"],
)
async def image_proxy(request, path: str):
    core = Core()
    cached = await core.thumbnail_cache(path)
    if cached:
        return await response.file(f"{core.directory}/thumbnail/{path}")
    else:
        return json({"status": 404, "message": "not_found"}, 404)
