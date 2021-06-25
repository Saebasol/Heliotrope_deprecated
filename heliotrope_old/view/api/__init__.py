from heliotrope import version_info
from heliotrope.view.api.count import heliotrope_request_count
from heliotrope.view.api.hitomi import hitomi_endpoint
from heliotrope.view.api.proxy import heliotrope_image_proxy
from sanic.blueprints import Blueprint

heliotrope_api = Blueprint.group(
    hitomi_endpoint,
    heliotrope_request_count,
    heliotrope_image_proxy,
    url_prefix="/api",
    version=f"v{version_info.major}",
)
