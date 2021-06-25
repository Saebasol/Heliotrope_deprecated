from heliotrope.database.query import search_galleryinfo, search_info_list
from heliotrope.utils.hitomi.models import HitomiGalleryInfoModel
from heliotrope.utils.response import not_found
from heliotrope.utils.typed import HeliotropeRequest
from heliotrope.utils.useful import is_raw, parse_raw_galleryinfo_list
from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

hitomi_search = Blueprint("hitomi_search", url_prefix="/search")


class HitomiSearchView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest):
        offset = (
            int(offset) - 1
            if (offset := request.args.get("offset"))
            and (offset.isdigit())
            and not (int(offset) - 1 < 0)
            else 0
        )

        if (query := request.args.get("q")) and (
            search_result := await search_info_list(
                request.app.ctx.mongo, query, offset
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

        return not_found


hitomi_search.add_route(HitomiSearchView.as_view(), "")
