from Heliotrope.utils.checker.check import authorized
from Heliotrope.utils.downloader.download import check_folder_or_download
from sanic import Blueprint
from sanic.response import json

download = Blueprint("image_download", url_prefix="/download")


@download.route(
    "/",
    methods=["POST"],
)
@authorized()
async def downloader(request):
    index = request.json.get("index")
    download_bool = request.json.get("download")
    if download_bool is None or not index:
        return json({"status": "bad_request"}, 400)

    result = await check_folder_or_download(index, download_bool)

    return result
