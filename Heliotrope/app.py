import os

import sentry_sdk
from sanic import Sanic
from sentry_sdk.integrations.sanic import SanicIntegration

from Heliotrope.api import api
from Heliotrope.utils import database

sentry_sdk.init(
    dsn=os.environ["sentry"],
    integrations=[SanicIntegration()],
)

app = Sanic(__name__)
app.blueprint(api)


@app.listener("before_server_start")
async def setup_db(app, loop):
    await database.init()


@app.listener("after_server_stop")
async def close_db(app, loop):
    await database.close()