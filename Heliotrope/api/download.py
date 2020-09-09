from Heliotrope.utils.checker.check import authorized
from crypt import methods
from Heliotrope.utils.downloader.download import compression_or_download
from sanic import Blueprint
from sanic.response import json
from Heliotrope.utils.hitomi import hitomi

download = Blueprint("image_download", url_prefix="/download")


@download.route("/", methods=["POST"])
@authorized()
async def downloader(request):
    download_bool = request.body.get("download")
    index = request.body.get("index")
    if download_bool is None or index is None:
        return json({"status": "bad_request"}, 400)
    elif not download_bool:
        link = await compression_or_download(index)
        return json({"status": "successfully", "link": link})
    elif download_bool:
        total = await compression_or_download(index, True)
        return json({"status": "pending", "total": total})
