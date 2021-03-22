import os
from asyncio.events import AbstractEventLoop

from aiohttp.client import ClientSession
from sanic import Sanic
from sanic_cors import CORS
from sentry_sdk import init
from sentry_sdk.integrations.sanic import SanicIntegration
from tortoise.contrib.sanic import register_tortoise

import heliotrope
from heliotrope.api import heliotrope_endpoint
from heliotrope.utils.requester import HitomiRequester
from heliotrope.utils.typed import Heliotrope

heliotrope_app = Sanic("heliotrope")
CORS(heliotrope_app, origins=["https://doujinshiman.ga"])
heliotrope_app.blueprint(heliotrope_endpoint)

if not os.environ.get("BYPASS"):
    heliotrope_app.config.DB_URL = os.environ["DB_URL"]
    if not os.environ.get("IS_TEST"):
        heliotrope_app.config.SENTRY_DSN = os.environ["SENTRY_DSN"]
        heliotrope_app.config.FORWARDED_SECRET = os.environ["FORWARDED_SECRET"]
        init(
            dsn=heliotrope_app.config.SENTRY_DSN,
            integrations=[SanicIntegration()],
            release=f"heliotrope@{heliotrope.__version__}",
        )

    register_tortoise(
        heliotrope_app,
        db_url=heliotrope_app.config.DB_URL,
        modules={
            "models": [
                "heliotrope.database.models.hitomi",
                "heliotrope.database.models.requestcount",
            ]
        },
        generate_schemas=True,
    )


@heliotrope_app.listener("before_server_start")
async def init(heliotrope: Heliotrope, loop: AbstractEventLoop):
    hitomi_session = ClientSession(loop=loop)
    heliotrope.ctx.hitomi_requester = HitomiRequester(hitomi_session)


@heliotrope_app.listener("after_server_stop")
async def finish(heliotrope: Heliotrope, loop: AbstractEventLoop):
    await heliotrope.ctx.hitomi_requester.session.close()
