from sanic.response import json
from Heliotrope.utils.database import User


async def check_user(user_id):
    user_data = await User.get_or_none(user_id=user_id)
    if not user_data:
        return json({"status": "need_register"}, 403)
    else:
        count = user_data.download_count
        if count >= 5:
            return json({"status": "Too_many_requests"}, 429)
        else:
            user_data.download_count = count + 1
            await user_data.save()


async def user_register(user_id):
    user_data = await User.get_or_none(user_id=user_id)
    if user_data:
        return json({"status": "already_register"}, 200)
    else:
        await User.create(user_id=user_id)
        return json({"status": "successfully"}, 201)