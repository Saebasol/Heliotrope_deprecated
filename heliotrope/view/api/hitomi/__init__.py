from sanic.blueprints import Blueprint

from heliotrope.view.api.hitomi.galleryinfo import hitomi_galleryinfo

# NOTE: Will fixed
hitomi_endpoint = Blueprint.group(hitomi_galleryinfo, url_prefix="/hitomi")