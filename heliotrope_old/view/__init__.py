from heliotrope.view.about import heliotrope_about
from heliotrope.view.api import heliotrope_api
from sanic.blueprints import Blueprint

heliotrope_view = Blueprint.group(heliotrope_api, heliotrope_about)
