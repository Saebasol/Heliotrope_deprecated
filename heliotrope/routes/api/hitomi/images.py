from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from heliotrope.database.query import get_galleryinfo
from heliotrope.utils.hitomi.common import image_url_from_image
from heliotrope.utils.hitomi.models import HitomiGalleryInfoModel, HitomiImageModel
from heliotrope.utils.response import not_found
from heliotrope.utils.shuffle import shuffle_image_url
from heliotrope.utils.typed import HeliotropeRequest

hitomi_images = Blueprint("hitomi_images", url_prefix="/images")


class HitomiImagesInfoView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index):
        galleryinfo_json = await get_galleryinfo(index)
        if not galleryinfo_json:
            files = (
                await request.app.ctx.hitomi_requester.get_galleryinfo(index)
            ).files
            if not files:
                return not_found
        else:
            files = HitomiImageModel.image_model_generator(galleryinfo_json["files"])
        return json(
            {
                "files": [
                    {
                        "name": file["name"],
                        "image": shuffle_image_url(
                            image_url_from_image(
                                int(index), HitomiImageModel(file), True
                            )
                        ),
                    }
                    for file in files
                ]
            }
        )


hitomi_images.add_route(HitomiImagesInfoView.as_view(), "/<index:int>")
