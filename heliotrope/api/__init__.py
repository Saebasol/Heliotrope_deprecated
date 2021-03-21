from sanic.blueprints import Blueprint

from heliotrope.api.hitomi import hitomi_endpoint
from heliotrope.api.count import request_count

heliotrope_endpoint = Blueprint.group(hitomi_endpoint, request_count, url_prefix="/api")
