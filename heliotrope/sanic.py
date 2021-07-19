from types import SimpleNamespace

from sanic.app import Sanic
from sanic.request import Request

from heliotrope.database.query import ORMQuery
from heliotrope.response import Response


class HeliotropeContext(SimpleNamespace):
    orm_query = ORMQuery()
    response = Response()


class Heliotrope(Sanic):
    ctx: HeliotropeContext


class HeliotropeRequest(Request):
    app: Heliotrope