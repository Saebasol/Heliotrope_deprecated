from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

from heliotrope.sanic import HeliotropeRequest

hitomi_search = Blueprint("hitomi_search", url_prefix="/search")


class HitomiSearchView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest) -> HTTPResponse:
        offset = (
            int(offset) - 1
            if (offset := request.args.get("offset"))
            and (offset.isdigit())
            and not (int(offset) - 1 < 0)
            else 0
        )

        if (query := request.args.get("q")) and (
            search_result := await request.app.ctx.nosql_query.search_info_list(
                query, offset
            )
        ):
            result, count = search_result
            return json(
                {
                    "status": 200,
                    "result": result,
                    "count": count,
                }
            )

        return request.app.ctx.response.not_found


# TODO: add_route is partially unknown and as_view is partially unknown Need PR Sanic
hitomi_search.add_route(HitomiSearchView.as_view(), "")  # type: ignore
