from sanic import Blueprint
from sanic.response import response

from Heliotrope.utils.downloader.download import thumbnail_cache


proxy = Blueprint("image_proxy", url_prefix="/proxy")


@proxy.route(
    "/<path>",
    methods=["GET"],
)
async def image_proxy(request, path: str):
    await thumbnail_cache(path)
    return await response.file(f"/var/www{path}")
