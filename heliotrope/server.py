from asyncio.events import AbstractEventLoop
from heliotrope.response import Response
from heliotrope.database.query import ORMQuery

from sanic.app import Sanic

from tortoise import Tortoise


from heliotrope import __version__
from heliotrope.sanic import Heliotrope
from heliotrope.view import view
from os import environ, getenv
from sentry_sdk import init
from sentry_sdk.integrations.sanic import SanicIntegration

heliotrope = Sanic("heliotrope")

# NOTE: Will fixed
heliotrope.blueprint(view)  # type: ignore


async def setup_heliotrope(heliotrope: Heliotrope) -> None:
    heliotrope.config.FALLBACK_ERROR_FORMAT = "json"
    # heliotrope.config.MONGO_DB_URL = environ["MONGO_DB_URL"]
    heliotrope.config.HIYOBOT_SECRET = environ["HIYOBOT_SECRET"]
    await Tortoise.init(
        db_url=environ["DB_URL"],
        modules={"models": ["heliotrope.database.models.hitomi"]},
    )
    await Tortoise.generate_schemas()
    heliotrope.ctx.orm_query = ORMQuery()
    heliotrope.ctx.response = Response()
    if getenv("IS_TEST"):
        init(
            dsn=environ["SENTRY_DSN"],
            integrations=[SanicIntegration()],
            release=f"heliotrope@{__version__}",
        )
        heliotrope.config.FORWARDED_SECRET = environ["FORWARDED_SECRET"]


# TODO: Type hint
@heliotrope.main_process_start  # type: ignore
async def start(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    await setup_heliotrope(heliotrope)


# TODO: Type hint
@heliotrope.main_process_stop  # type: ignore
async def stop(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    await Tortoise.close_connections()