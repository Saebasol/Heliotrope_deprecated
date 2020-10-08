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


async def user_download_count_check(user_id: int):
    user_data = await User.get_or_none(user_id=user_id)  # 따로 나눠야함
    if not user_data:
        return json({"status": 403, "message": "need_register"}, 403)
    else:
        count = user_data.download_count
        if count >= 5:
            return json({"status": 429, "message": "Too_many_requests"}, 429)
        else:
            return True


async def user_download_count(user_id: int):
    user_data = await User.get_or_none(user_id=user_id)
    count = user_data.download_count
    user_data.download_count = count + 1
    await user_data.save()
    return 5 - user_data.download_count
