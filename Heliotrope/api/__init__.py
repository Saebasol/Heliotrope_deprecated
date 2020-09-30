from sanic import Blueprint

from .download import download
from .hitomi import hitomi
from .image_proxy import proxy
from .progress import progress
from .register import register

api = Blueprint.group(hitomi, download, register, proxy, progress, url_prefix="/api")
