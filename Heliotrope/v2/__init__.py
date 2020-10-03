import Heliotrope
from sanic.blueprints import Blueprint

from .api import api

version = Blueprint.group(api, url_prefix=f"/v{Heliotrope.version_info.major}")
