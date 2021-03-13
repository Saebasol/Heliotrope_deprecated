from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

hitomi_list = Blueprint("hitomi_list", url_prefix="/list")


class HitomiListView(HTTPMethodView):
    async def get(self, request, index):
        return json({"status": 200})


hitomi_list.add_route(HitomiListView.as_view(), "<index:int>")
