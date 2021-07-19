from asyncio.events import AbstractEventLoop

from sanic.app import Sanic

from tortoise.contrib.sanic import register_tortoise

from heliotrope import __version__
from heliotrope.sanic import Heliotrope, HeliotropeContext
from heliotrope.view import view
from os import environ
from sentry_sdk import init
from sentry_sdk.integrations.sanic import SanicIntegration

heliotrope = Sanic("heliotrope")

# NOTE: Will fixed
heliotrope.blueprint(view)  # type: ignore


def setup_heliotrope(heliotrope: Heliotrope) -> None:
    heliotrope.config.FALLBACK_ERROR_FORMAT = "json"
    heliotrope.config.MONGO_DB_URL = environ["MONGO_DB_URL"]
    heliotrope.config.HIYOBOT_SECRET = environ["HIYOBOT_SECRET"]
    register_tortoise(
        heliotrope,
        db_url=environ["DB_URL"],
        modules={
            "models": [
                "heliotrope.database.models.hitomi",
                "heliotrope.database.models.requestcount",
            ]
        },
        generate_schemas=True,
    )
    if not environ["IS_TEST"]:
        init(
            dsn=environ["SENTRY_DSN"],
            integrations=[SanicIntegration()],
            release=f"heliotrope@{__version__}",
        )
        heliotrope.config.FORWARDED_SECRET = environ["FORWARDED_SECRET"]


# TODO: Type hint
@heliotrope.main_process_start  # type: ignore
async def start(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    heliotrope.ctx = HeliotropeContext()


# TODO: Type hint
@heliotrope.main_process_stop  # type: ignore
async def stop(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    pass