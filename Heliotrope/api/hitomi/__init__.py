from sanic import Blueprint

from .galleryinfo import galleryinfo
from .image_info import images
from .index import index
from .info import info
from .integrated import integrated
from .list import list_

hitomi = Blueprint.group(
    info, galleryinfo, integrated, list_, index, images, url_prefix="/hitomi"
)
