from sanic import Blueprint

from .download import download
from .hitomi import hitomi
from .register import register
from .image_proxy import proxy
from .progress import progress

api = Blueprint.group(hitomi, download, register, proxy, progress, url_prefix="/api")
