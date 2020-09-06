import os

import sentry_sdk
from sanic import Sanic
from sentry_sdk.integrations.sanic import SanicIntegration
from Heliotrope.api import api

sentry_sdk.init(
    dsn=os.environ["sentry"],
    integrations=[SanicIntegration()],
)

app = Sanic(__name__)
app.blueprint(api)
