from asyncio.events import AbstractEventLoop

from sanic.app import Sanic

from heliotrope.sanic import Heliotrope, HeliotropeContext
from heliotrope.view import view

heliotrope = Sanic("heliotrope")

# NOTE: Will fixed
heliotrope.blueprint(view)  # type: ignore


# TODO: Type hint
@heliotrope.main_process_start  # type: ignore
async def start(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    heliotrope.ctx = HeliotropeContext()
