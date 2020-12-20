import os

import sentry_sdk
from sanic import Sanic
from sanic.blueprints import Blueprint
from sentry_sdk.integrations.sanic import SanicIntegration

import Heliotrope
from Heliotrope.api import api

sentry_sdk.init(
    dsn=os.environ["sentry"],
    integrations=[SanicIntegration()],
    release=f"heliotrope@{Heliotrope.__version__}",
)

app = Sanic(__name__)
app.blueprint(Blueprint.group(api, url_prefix=f"/v{Heliotrope.version_info.major}"))

app.config.FORWARDED_SECRET = os.environ["forwarded_secret"]
app.config.FALLBACK_ERROR_FORMAT = "json"
