from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json

from Heliotrope.utils.checker.check import authorized
from Heliotrope.utils.hitomi import hitomi

index = Blueprint("hitomi_index_list", url_prefix="/index")


@index.route("/")
@authorized()
async def hitomi_index(request):
    index_list = hitomi.index()
    return json(index_list)
