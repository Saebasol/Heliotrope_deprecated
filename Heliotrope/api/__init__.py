from sanic import Blueprint

from .hitomi import hitomi
from .image_proxy import proxy
from .register import register

api = Blueprint.group(hitomi, proxy, register, url_prefix="/api")
