from sanic import Blueprint

from .hitomi import hitomi
from .download import download

api = Blueprint.group(hitomi, download, url_prefix="/api")
