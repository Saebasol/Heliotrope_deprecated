from sanic import Blueprint

from .info import info
from .galleryinfo import galleryinfo
from .integrated import integrated
from .list import list_

hitomi = Blueprint.group(info, galleryinfo, integrated, list_, url_prefix="/hitomi")
