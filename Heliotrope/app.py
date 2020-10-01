import os

import sentry_sdk
from sanic import Sanic
from sanic.blueprints import Blueprint
from sentry_sdk.integrations.sanic import SanicIntegration
from tortoise.contrib.sanic import register_tortoise

import Heliotrope
from Heliotrope.api import api

sentry_sdk.init(
    dsn=os.environ["sentry"],
    integrations=[SanicIntegration()],
    release=f"heliotrope@{Heliotrope.__version__}",
)

app = Sanic(__name__)
version = Blueprint.group(
    api, url_prefix=f"/v{Heliotrope.version_info.major}"
)  # hardcoding
app.blueprint(version)
app.config.FORWARDED_SECRET = os.environ["forwarded_secret"]
app.config.FALLBACK_ERROR_FORMAT = "json"
register_tortoise(
    app,
    db_url=f"mysql://{os.environ['DB_UNAME']}:{os.environ['DB_PW']}@{os.environ['DB_HOST']}:3306/{os.environ['DB_DBNAME']}",
    modules={"models": ["Heliotrope.utils.database.models"]},
    generate_schemas=True,
)
