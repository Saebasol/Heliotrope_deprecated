from asyncio.events import AbstractEventLoop

from sanic.app import Sanic
from sanic.request import Request

from types import SimpleNamespace
from heliotrope.database.query import ORMQuery

heliotrope = Sanic("heliotrope")


class HeliotropeContext(SimpleNamespace):
    orm_query = ORMQuery()


class Heliotrope(Sanic):
    ctx: HeliotropeContext


class HeliotropeRequest(Request):
    app: Heliotrope


# TODO: Type hint
@heliotrope.main_process_start  # type: ignore
async def start(heliotrope: Heliotrope, loop: AbstractEventLoop):
    heliotrope.ctx = HeliotropeContext()
