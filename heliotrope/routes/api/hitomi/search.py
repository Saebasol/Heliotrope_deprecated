from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from heliotrope.database.query import search_galleryinfo
from heliotrope.utils.hitomi.models import HitomiGalleryInfoModel
from heliotrope.utils.response import not_found
from heliotrope.utils.typed import HeliotropeRequest

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
            search_result := await search_galleryinfo(query, offset)
        ):
            result, count = search_result
            if (is_true := request.args.get("raw")) and (is_true.lower() == "true"):
                return json({"status": 200, "result": result, "count": count})
            return json(
                {
                    "status": 200,
                    "result": list(
                        map(
                            lambda parsed_galleryinfo_model: {
                                "language_localname": parsed_galleryinfo_model.language_localname,
                                "language": parsed_galleryinfo_model.language,
                                "date": parsed_galleryinfo_model.date,
                                "files": parsed_galleryinfo_model.files,
                                "tags": parsed_galleryinfo_model.tags,
                                "japanese_title": parsed_galleryinfo_model.japanese_title,
                                "title": parsed_galleryinfo_model.title,
                                "id": parsed_galleryinfo_model.galleryid,
                                "type": parsed_galleryinfo_model.hitomi_type,
                            },
                            map(
                                lambda raw_result: HitomiGalleryInfoModel.parse_galleryinfo(
                                    raw_result, True
                                ),
                                result,
                            ),
                        )
                    ),
                    "count": count,
                }
            )

        return not_found


hitomi_search.add_route(HitomiSearchView.as_view(), "")
