from sanic import Sanic
from sanic.exceptions import abort
from sanic.response import json

from Heliotrope.utils.hitomi import hitomi

app = Sanic(__name__)


@app.route("/api/hitomi/<index>")
async def info(request, index: int):
    json_ = await hitomi.info(index)
    if not json_:
        return abort(404)
    else:
        return json(json_)


@app.route("/api/hitomi/galleryinfo/<index>")
async def galleryinfo(request, index: int):
    json_ = await hitomi.galleryinfo(index)
    if not json_:
        return abort(404)
    else:
        return json(json_)


@app.route("/api/hitomi/integrated/<index>")
async def inte_info(request, index: int):
    json_ = await hitomi.integrated_info(index)
    return json(json_)
