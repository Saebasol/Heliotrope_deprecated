import sentry_sdk
from sanic import Sanic
from sanic.exceptions import abort
from sanic.response import json
from sentry_sdk.integrations.sanic import SanicIntegration

from Heliotrope.utils.hitomi import hitomi

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    integrations=[SanicIntegration()],
)

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


@app.route("/api/hitomi/list/<num>")
async def list_(request, num: int):
    hitomi_info_list = await hitomi.list_(int(num) - 1)
    return json(hitomi_info_list)