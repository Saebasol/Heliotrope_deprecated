from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

hitomi_images = Blueprint("hitomi_images", url_prefix="/images")


class HitomiImagesInfoView(HTTPMethodView):
    async def get(self, request, index):
        return json({"status": 200})


hitomi_images.add_route(HitomiImagesInfoView.as_view(), "/<index:int>")
