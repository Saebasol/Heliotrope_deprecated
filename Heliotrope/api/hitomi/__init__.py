from sanic import Blueprint

from .galleryinfo import galleryinfo
from .index import index
from .info import info
from .integrated import integrated
from .list import list_
from .image_info import images

hitomi = Blueprint.group(
    info, galleryinfo, integrated, list_, index, images, url_prefix="/hitomi"
)
