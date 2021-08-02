from sanic.blueprints import Blueprint

from heliotrope.view.api.hitomi.galleryinfo import hitomi_galleryinfo
from heliotrope.view.api.hitomi.images import hitomi_images

# NOTE: Will fixed
hitomi_endpoint = Blueprint.group(
    hitomi_galleryinfo, hitomi_images, url_prefix="/hitomi"
)
