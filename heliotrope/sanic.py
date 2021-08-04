from types import SimpleNamespace

from sanic.app import Sanic
from sanic.config import Config
from sanic.request import Request

from heliotrope.database.mongo import NoSQLQuery
from heliotrope.database.query import SQLQuery
from heliotrope.request.base import BaseRequest
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.response import Response


class HeliotropeContext(SimpleNamespace):
    sql_query: SQLQuery
    nosql_query: NoSQLQuery
    response: Response
    hitomi_request: HitomiRequest
    base_request: BaseRequest


class Heliotrope(Sanic):
    ctx: HeliotropeContext
    config: Config


class HeliotropeRequest(Request):
    app: Heliotrope
    args: property
