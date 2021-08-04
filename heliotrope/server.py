from asyncio.events import AbstractEventLoop
from os import environ, getenv

from aiohttp.client import ClientSession
from sanic.app import Sanic
from sentry_sdk import init
from sentry_sdk.integrations.sanic import SanicIntegration
from tortoise import Tortoise

from heliotrope import __version__
from heliotrope.database.mongo import NoSQLQuery
from heliotrope.database.query import SQLQuery
from heliotrope.request.base import BaseRequest
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.response import Response
from heliotrope.sanic import Heliotrope
from heliotrope.tasks.mirroring import Mirroring
from heliotrope.view import view

heliotrope = Sanic("heliotrope")

# NOTE: Will fixed
heliotrope.blueprint(view)  # type: ignore


async def setup_heliotrope(heliotrope: Heliotrope) -> None:
    if not getenv("IS_TEST"):
        init(
            dsn=environ["SENTRY_DSN"],
            integrations=[SanicIntegration()],
            release=f"heliotrope@{__version__}",
        )
        heliotrope.config.FORWARDED_SECRET = environ["FORWARDED_SECRET"]

    heliotrope.config.FALLBACK_ERROR_FORMAT = "json"
    heliotrope.ctx.nosql_query = NoSQLQuery(environ["MONGO_DB_URL"])
    await Tortoise.init(
        db_url=environ["DB_URL"],
        modules={"models": ["heliotrope.database.models.hitomi"]},
    )
    await Tortoise.generate_schemas()
    heliotrope.ctx.sql_query = SQLQuery()


# TODO: Type hint
@heliotrope.main_process_start  # type: ignore
async def start(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    await setup_heliotrope(heliotrope)
    heliotrope.ctx.response = Response()
    heliotrope.ctx.hitomi_request = await HitomiRequest.setup()
    heliotrope.ctx.base_request = BaseRequest(ClientSession())
    heliotrope.add_task(Mirroring.setup(heliotrope=heliotrope))


# TODO: Type hint
@heliotrope.main_process_stop  # type: ignore
async def stop(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    await Tortoise.close_connections()
