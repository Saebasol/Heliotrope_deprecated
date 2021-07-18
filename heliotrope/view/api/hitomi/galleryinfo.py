from heliotrope.server import HeliotropeRequest

from sanic.blueprints import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import HTTPResponse

hitomi_galleryinfo = Blueprint("hitomi_galleryinfo", url_prefix="/galleryinfo")


class HitomiGalleryInfoView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest) -> HTTPResponse:
        return request.app.ctx.response.not_found


# TODO: add_route is partially unknown and as_view is partially unknown Need PR Sanic
hitomi_galleryinfo.add_route(HitomiGalleryInfoView.as_view(), "/<index:int>")  # type: ignore
