from sanic import Blueprint

from .hitomi import hitomi
from .image_proxy import proxy
from .ranking import ranking
from .register import register

api = Blueprint.group(hitomi, proxy, register, ranking, url_prefix="/api")
