from sanic import Blueprint

from .galleryinfo import galleryinfo
from .info import info
from .integrated import integrated
from .list import list_
from .index import index

hitomi = Blueprint.group(
    info, galleryinfo, integrated, list_, index, url_prefix="/hitomi"
)
