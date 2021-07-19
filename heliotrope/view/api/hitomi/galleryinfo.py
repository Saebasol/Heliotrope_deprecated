from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView

from heliotrope.sanic import HeliotropeRequest

hitomi_galleryinfo = Blueprint("hitomi_galleryinfo", url_prefix="/galleryinfo")


class HitomiGalleryinfoView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index: int) -> HTTPResponse:
        return request.app.ctx.response.not_found


# TODO: add_route is partially unknown and as_view is partially unknown Need PR Sanic
hitomi_galleryinfo.add_route(HitomiGalleryinfoView.as_view(), "/<index:int>")  # type: ignore
