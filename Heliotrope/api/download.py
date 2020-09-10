from Heliotrope.utils.checker.check import authorized
from Heliotrope.utils.downloader.download import check_vaild, compression_or_download
from sanic import Blueprint
from sanic.response import json
from Heliotrope.utils.hitomi import hitomi

download = Blueprint("image_download", url_prefix="/download")


@download.route(
    "/",
    methods=["POST"],
)
@authorized()
async def downloader(request):
    download_bool = request.json.get("download")
    index = request.json.get("index")
    if not download_bool or not index:
        return json({"status": "bad_request"}, 400)
    