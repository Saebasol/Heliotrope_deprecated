from sanic import Blueprint

from .galleryinfo import galleryinfo
from .info import info
from .integrated import integrated
from .list import list_

hitomi = Blueprint.group(info, galleryinfo, integrated, list_, url_prefix="/hitomi")
