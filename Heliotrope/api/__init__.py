from sanic import Blueprint

from .download import download
from .hitomi import hitomi
from .register import register

api = Blueprint.group(hitomi, download, register, url_prefix="/api")
