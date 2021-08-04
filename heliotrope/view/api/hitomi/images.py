from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

from heliotrope.hitomi.common import image_url_from_image
from heliotrope.hitomi.models import HitomiFiles
from heliotrope.sanic import HeliotropeRequest
from heliotrope.shuffle import shuffle_image_url

hitomi_images = Blueprint("hitomi_images", url_prefix="/images")


class HitomiImagesView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index_id: int) -> HTTPResponse:
        if galleryinfo := await request.app.ctx.sql_query.get_galleryinfo(index_id):
            return json(
                {
                    "status": 200,
                    "files": [
                        {
                            "name": file.name,
                            "url": shuffle_image_url(
                                image_url_from_image(index_id, file, True)
                            ),
                        }
                        for file in map(HitomiFiles, galleryinfo["files"])
                    ],
                }
            )
        return request.app.ctx.response.not_found


# TODO: add_route is partially unknown and as_view is partially unknown Need PR Sanic
hitomi_images.add_route(HitomiImagesView.as_view(), "/<index_id:int>")  # type: ignore
