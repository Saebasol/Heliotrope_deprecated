from sanic.response import json

from Heliotrope.utils.database import User


async def user_register(user_id, api_key=None, check=False):
    user_data = await User.get_or_none(user_id=int(user_id))
    if check:
        if user_data:
            return json(
                {
                    "status": 200,
                    "message": "already_register",
                    "api_key": user_data.api_key,
                },
                200,
            )
        return json({"status": 404, "message": "not_found"}, 404)
    if user_data:
        return json({"status": 200, "message": "already_register"}, 200)
    user = await User.create(user_id=user_id, api_key=api_key)
    await user.save()
    return json({"status": 201, "message": "successfully"}, 201)
