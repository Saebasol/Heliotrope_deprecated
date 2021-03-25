from heliotrope.api.about import heliotrope_about
from sanic.blueprints import Blueprint

from heliotrope import version_info
from heliotrope.api.count import request_count
from heliotrope.api.hitomi import hitomi_endpoint

heliotrope_endpoint = Blueprint.group(
    hitomi_endpoint,
    request_count,
    heliotrope_about,
    url_prefix="/api",
    version=f"v{version_info.major}",
)
