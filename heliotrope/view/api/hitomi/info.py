from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

from heliotrope.sanic import HeliotropeRequest

hitomi_info = Blueprint("hitomi_info", url_prefix="/info")


class HitomiInfoView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index_id: int) -> HTTPResponse:
        if info := await request.app.ctx.nosql_query.find_info(index_id):
            return json("status", 200, **info)

        return request.app.ctx.response.not_found


# TODO: add_route is partially unknown and as_view is partially unknown Need PR Sanic
hitomi_info.add_route(HitomiInfoView.as_view(), "/<index_id:int>")  # type: ignore
