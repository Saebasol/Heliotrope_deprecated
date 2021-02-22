import os

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from Heliotrope.utils.database.ranking_management import add_count, view_ranking

ranking = Blueprint("ranking", url_prefix="/ranking")


@ranking.route(
    "/",
    methods=["POST"]
)
async def _ranking(request):
    index = request.json.get("index")
    check_header = request.headers.get("Verification")
    if check_header == f"check {os.environ['VERIFI']}":
        return await add_count(index, check=True)
    if not index or check_header != os.environ['VERIFI']:
        return json({"status": 400, "message": "bad_request"}, 400)
    return await add_count(index)


@ranking.route(
    "/",
    methods=["GET"]
)
async def _view_ranking(request):
    check_header = request.headers.get("Verification")

    if check_header == f"check {os.environ['VERIFI']}":
        return await view_ranking(check=True)
    else:
        return json({"status": 400, "message": "bad_request"}, 400)
