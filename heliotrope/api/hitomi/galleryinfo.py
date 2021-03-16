from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

hitomi_galleyinfo = Blueprint("hitomi_list", url_prefix="/galleyinfo")


class HitomiGalleryInfoView(HTTPMethodView):
    async def get(self, request, index):
        return json({"status": 200})


hitomi_galleyinfo.add_route(HitomiGalleryInfoView.as_view(), "<index:int>")