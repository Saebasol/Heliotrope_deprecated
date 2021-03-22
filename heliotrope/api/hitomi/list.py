from asyncio.tasks import gather

from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from heliotrope.utils.typed import HeliotropeRequest

hitomi_list = Blueprint("hitomi_list", url_prefix="/list")


class HitomiListView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index: int):
        hitomi_index_list = await request.app.ctx.hitomi_requester.fetch_index(index)
        split_index_list = [
            hitomi_index_list[i * 15 : (i + 1) * 15]
            for i in range((len(hitomi_index_list) + 15 - 1) // 15)
        ]
        if len(split_index_list) < index + 1:
            return

        info_list = await gather(
            *[
                request.app.ctx.hitomi_requester.get_info_using_index(index)
                for index in split_index_list[index]
            ]
        )

        return json({"status": 200, "list": info_list})


hitomi_list.add_route(HitomiListView.as_view(), "/<index:int>")
