from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from heliotrope.database.query import get_galleryinfo
from heliotrope.utils.response import not_found
from heliotrope.utils.typed import HeliotropeRequest

hitomi_galleyinfo = Blueprint("hitomi_galleyinfo", url_prefix="/galleryinfo")


class HitomiGalleryInfoView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index: int):
        if galleryinfo := await get_galleryinfo(index):
            galleryinfo.update({"status": 200})
            return json(galleryinfo)
        return not_found


hitomi_galleyinfo.add_route(HitomiGalleryInfoView.as_view(), "/<index:int>")
