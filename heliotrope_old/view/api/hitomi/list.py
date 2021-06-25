from heliotrope.database.query import get_info_list
from heliotrope.utils.response import not_found
from heliotrope.utils.typed import HeliotropeRequest
from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

hitomi_list = Blueprint("hitomi_list", url_prefix="/list")


class HitomiListView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index: int):
        start_at_zero = index - 1

        if start_at_zero < 0:
            return not_found

        info_list = await get_info_list(request.app.ctx.mongo, start_at_zero)

        return json({"status": 200, "list": info_list})


hitomi_list.add_route(HitomiListView.as_view(), "/<index:int>")
