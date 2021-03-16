from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView
from heliotrope.utils.decorators import hiyobot_only

request_count = Blueprint("request_count", url_prefix="/count")


class RequestCountView(HTTPMethodView):
    @hiyobot_only
    async def get(self, request):
        return json({"status": 200})

    @hiyobot_only
    async def porst(self, request):
        return json({"status": 200})


request_count.add_route(RequestCountView.as_view(), "/")