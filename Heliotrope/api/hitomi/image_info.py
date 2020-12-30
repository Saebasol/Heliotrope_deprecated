from sanic import Blueprint
from sanic.response import json

from Heliotrope.utils.auth import authorized
from Heliotrope.utils.hitomi import hitomi

images = Blueprint("hitomi_shuffled_image_info", url_prefix="/images")


@images.route("/<index>")
@authorized()
async def hitomi_image(request, index: int):
    image_list = await hitomi.images(index)
    if not image_list:
        return json({"status": 404, "message": "not_found"}, 404)
    return json({"status": 200, "images": image_list})
