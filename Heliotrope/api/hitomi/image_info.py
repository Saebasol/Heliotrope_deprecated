from sanic import Blueprint
from sanic.response import json


from Heliotrope.utils.hitomi import hitomi
from Heliotrope.utils.auth import authorized

images = Blueprint("hitomi_shuffled_image_info", url_prefix="/images")


@images.route("/<index>")
@authorized()
async def hitomi_image(request, index: int):
    image_list = await hitomi.images(index)
    return json({"images": image_list})
