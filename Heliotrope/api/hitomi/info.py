from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

hitomi_info = Blueprint("hitomi_info", url_prefix="/info")


class HitomiInfoView(HTTPMethodView):
    async def get(self, request, index):
        return json({"status": 200})


hitomi_info.add_route(HitomiInfoView.as_view(), "<index:int>")
