from sanic.blueprints import Blueprint

from heliotrope import version_info
from heliotrope.routes.api.count import request_count
from heliotrope.routes.api.hitomi import hitomi_endpoint

heliotrope_api_endpoint = Blueprint.group(
    hitomi_endpoint,
    request_count,
    url_prefix="/api",
    version=f"v{version_info.major}",
)
