from sanic import Blueprint

from .hitomi import hitomi

api = Blueprint.group(hitomi, url_prefix="/api")
