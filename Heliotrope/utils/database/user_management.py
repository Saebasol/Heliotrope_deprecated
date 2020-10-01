from sanic.response import json

from Heliotrope.utils.database import User


async def user_register(user_id: int, check: bool = False):
    user_data = await User.get_or_none(user_id=user_id)
    if check:
        if user_data:
            return json({"code": 200, "status": "already_register"}, 200)
        else:
            return json({"code": 404, "status": "not_found"}, 404)
    else:
        if user_data:
            return json({"code": 200, "status": "already_register"}, 200)
        else:
            await User.create(user_id=user_id)
            return json({"code": 201, "ststus": "successfully"}, 201)
