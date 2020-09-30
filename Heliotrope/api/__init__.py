from sanic import Blueprint

from .download import download
from .hitomi import hitomi
from .register import register
from .image_proxy import proxy

api = Blueprint.group(hitomi, download, register, proxy, url_prefix="/api")
