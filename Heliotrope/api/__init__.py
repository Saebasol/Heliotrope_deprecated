from sanic import Blueprint

from .download import download
from .hitomi import hitomi

api = Blueprint.group(hitomi, download, url_prefix="/api")
