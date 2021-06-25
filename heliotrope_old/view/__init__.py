from sanic.blueprints import Blueprint

from heliotrope.view.about import heliotrope_about
from heliotrope.view.api import heliotrope_api

heliotrope_view = Blueprint.group(heliotrope_api, heliotrope_about)
