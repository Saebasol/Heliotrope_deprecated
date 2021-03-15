from heliotrope.utils.requester import RestrictedRequester
from asyncio.locks import Semaphore
from sanic import Sanic

heliotrope = Sanic("heliotrope")


heliotrope.config.concurrency_per_worker = 4
heliotrope.config.FORWARDED_SECRET
heliotrope.config.DB_URL = None
heliotrope.config.SENTRY_DSN = None


@heliotrope.listener("before_server_start")
def init(heliotrope, loop):
    sem = Semaphore(heliotrope.config.concurrency_per_worker, loop=loop)
    heliotrope.request = RestrictedRequester(sem)