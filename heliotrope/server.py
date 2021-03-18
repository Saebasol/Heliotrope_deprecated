import os

from aiohttp.client import ClientSession
from sanic import Sanic

from heliotrope.utils.requester import HitomiRequester

heliotrope = Sanic("heliotrope")

if not os.environ.get("TEST"):
    heliotrope.config.FORWARDED_SECRET = os.environ["FORWARDED_SECRET"]
    heliotrope.config.DB_URL = os.environ["DB_URL"]
    heliotrope.config.SENTRY_DSN = os.environ["SENTRY_DSN"]


@heliotrope.listener("before_server_start")
def init(heliotrope, loop):
    hitomi_session = ClientSession(loop=loop)
    heliotrope.hitomi_requester = HitomiRequester(hitomi_session)


@heliotrope.listener("after_server_stop")
def finish(heliotrope, loop):
    loop.run_until_complete(heliotrope.hitomi_session.close())
    loop.close()
