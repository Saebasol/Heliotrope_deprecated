from sanic.response import json

from Heliotrope.utils.database import User


async def user_register(user_id, check=False):
    user_data = await User.get_or_none(user_id=int(user_id))
    if check:
        if user_data:
            return True
        else:
            return False
    if user_data:
        return json({"status": 200, "message": "already_register"}, 200)
    else:
        await User.create(user_id=user_id)
        return json({"status": 201, "message": "successfully"}, 201)
