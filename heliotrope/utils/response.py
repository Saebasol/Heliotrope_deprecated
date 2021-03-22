from sanic.response import json

not_found = json({"status": 404, "message": "not_found"}, 404)
