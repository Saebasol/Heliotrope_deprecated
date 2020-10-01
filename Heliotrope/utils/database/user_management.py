from sanic.response import json

from Heliotrope.utils.database import User


async def user_register(user_id: int, check: bool = False):
    user_data = await User.get_or_none(user_id=user_id)
    if check:
        if user_data:
            return json({"status": 200, "message": "already_register"}, 200)
        else:
            return json({"status": 404, "message": "not_found"}, 404)
    else:
        if user_data:
            return json({"status": 200, "message": "already_register"}, 200)
        else:
            await User.create(user_id=user_id)
            return json({"status": 201, "message": "successfully"}, 201)
