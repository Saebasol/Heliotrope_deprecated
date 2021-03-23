from sanic.blueprints import Blueprint

from heliotrope.api.hitomi.galleryinfo import hitomi_galleyinfo
from heliotrope.api.hitomi.images import hitomi_images
from heliotrope.api.hitomi.info import hitomi_info
from heliotrope.api.hitomi.list import hitomi_list

hitomi_endpoint = Blueprint.group(
    hitomi_galleyinfo,
    hitomi_images,
    hitomi_info,
    hitomi_list,
    url_prefix="/hitomi",
)
