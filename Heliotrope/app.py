import os

import sentry_sdk
from sanic import Sanic
from sentry_sdk.integrations.sanic import SanicIntegration
from tortoise.contrib.sanic import register_tortoise

from Heliotrope.api import api
from Heliotrope.utils import database

sentry_sdk.init(
    dsn=os.environ["sentry"],
    integrations=[SanicIntegration()],
)

app = Sanic(__name__)
app.blueprint(api)
register_tortoise(
    app,
    db_url=f"mysql://{os.environ['DB_UNAME']}:{os.environ['DB_PW']}@{os.environ['DB_HOST']}:3306/{os.environ['DB_DBNAME']}",
    modules={"models": ["Heliotrope.utils.database.models"]},
    generate_schemas=True,
)
