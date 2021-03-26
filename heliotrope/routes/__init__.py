from sanic.blueprints import Blueprint

from heliotrope.routes.about import heliotrope_about
from heliotrope.routes.api import heliotrope_api_endpoint

heliotrope_routes = Blueprint.group(heliotrope_api_endpoint, heliotrope_about)
