from sanic import Blueprint
from sanic.response import json

from Heliotrope.utils.checker.check import authorized
from Heliotrope.utils.downloader.download import Download

download = Blueprint("image_download", url_prefix="/download")


@download.route(
    "/",
    methods=["POST"],
)
@authorized()
async def api_download(request):
    index = request.json.get("index")
    user_id = request.json.get("user_id")
    download_bool = request.json.get("download")
    if download_bool is None or not index or not user_id:
        return json({"status": 400, "message": "bad_request"}, 400)
    else:
        download = Download(index, download_bool, user_id)
        return await download.download()
