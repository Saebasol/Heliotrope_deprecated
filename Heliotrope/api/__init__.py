from sanic import Blueprint

from .hitomi import hitomi
from .image_proxy import proxy
from .register import register
from .ranking import ranking

api = Blueprint.group(hitomi, proxy, register, ranking, url_prefix="/api")
