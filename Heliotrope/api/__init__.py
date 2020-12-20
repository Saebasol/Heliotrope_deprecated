from sanic import Blueprint

from .hitomi import hitomi
from .image_proxy import proxy

api = Blueprint.group(hitomi, proxy, url_prefix="/api")
