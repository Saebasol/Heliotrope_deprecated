from sanic.response import json

not_found = json({"status": 404, "message": "not_found"}, 404)

bad_request = json({"status": 404, "message": "bad_request"}, 400)
