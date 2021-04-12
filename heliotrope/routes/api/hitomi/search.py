from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from heliotrope.database.query import search_galleryinfo
from heliotrope.utils.response import not_found
from heliotrope.utils.typed import HeliotropeRequest

hitomi_search = Blueprint("hitomi_search", url_prefix="/search")


class HitomiSearchView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest):
        if (query := request.args.get("q")) and (
            result := await search_galleryinfo(query)
        ):
            return json({"status": 200, "result": result})

        return not_found


hitomi_search.add_route(HitomiSearchView.as_view(), "")
