from types import SimpleNamespace

from sanic.app import Sanic
from sanic.request import Request
from sanic.config import Config
from heliotrope.database.query import ORMQuery
from heliotrope.response import Response


class HeliotropeContext(SimpleNamespace):
    orm_query = ORMQuery()
    response = Response()


class Heliotrope(Sanic):
    ctx: HeliotropeContext
    config: Config


class HeliotropeRequest(Request):
    app: Heliotrope