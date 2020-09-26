from sanic import Blueprint
from sanic import response
from sanic.response import json

from Heliotrope.utils.downloader.download import thumbnail_cache


proxy = Blueprint("image_proxy", url_prefix="/proxy")


@proxy.route(
    "/<path>",
    methods=["GET"],
)
async def image_proxy(request, path: str):
    cached = await thumbnail_cache(path)
    if cached:
        return await response.file(f"/var/www/proxy{path}")
    else:
        return json({"status": "not_found"}, 404)
