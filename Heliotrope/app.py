import os

import sentry_sdk
from sanic import Sanic
from sanic.blueprints import Blueprint
from sentry_sdk.integrations.sanic import SanicIntegration
from tortoise.contrib.sanic import register_tortoise

import Heliotrope
from Heliotrope.api import api

sentry_sdk.init(
    dsn=None
    if os.environ.get("TEST_FLAG")
    else "https://aad296bf8e654dbc84b7919b13485227@o440492.ingest.sentry.io/5417505",
    integrations=[SanicIntegration()],
    release=f"heliotrope@{Heliotrope.__version__}",
)

app = Sanic(__name__)
app.blueprint(Blueprint.group(api, url_prefix=f"/v{Heliotrope.version_info.major}"))

if not os.environ.get("TEST_FLAG"):
    app.config.FORWARDED_SECRET = os.environ["forwarded_secret"]
    register_tortoise(
        app,
        db_url=os.environ["DB_URL"],
        modules={"models": ["Heliotrope.utils.database.models"]},
        generate_schemas=True,
    )

app.config.FALLBACK_ERROR_FORMAT = "json"
