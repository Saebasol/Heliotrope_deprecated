from heliotrope.view.api.hitomi.galleryinfo import hitomi_galleyinfo
from heliotrope.view.api.hitomi.images import hitomi_images
from heliotrope.view.api.hitomi.info import hitomi_info
from heliotrope.view.api.hitomi.list import hitomi_list
from heliotrope.view.api.hitomi.search import hitomi_search
from sanic.blueprints import Blueprint

hitomi_endpoint = Blueprint.group(
    hitomi_galleyinfo,
    hitomi_images,
    hitomi_info,
    hitomi_list,
    hitomi_search,
    url_prefix="/hitomi",
)
