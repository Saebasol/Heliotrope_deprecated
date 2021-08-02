from sanic.blueprints import Blueprint

from heliotrope import version_info
from heliotrope.view.api.hitomi import hitomi_endpoint

# NOTE: Will fixed
api_endpoint = Blueprint.group(
    hitomi_endpoint, url_prefix="/api", version=version_info.major
)
