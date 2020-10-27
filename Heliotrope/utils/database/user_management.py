from sanic.response import json

from Heliotrope.utils.database import User


class Management:
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def user_register(self, check: bool = False):
        user_data = await User.get_or_none(user_id=self.user_id)
        if check:
            if user_data:
                return json({"status": 200, "message": "already_register"}, 200)
            else:
                return json({"status": 404, "message": "not_found"}, 404)
        else:
            if user_data:
                return json({"status": 200, "message": "already_register"}, 200)
            else:
                await User.create(user_id=self.user_id)
                return json({"status": 201, "message": "successfully"}, 201)

    async def user_download_count_check(self):
        user_data = await User.get_or_none(user_id=self.user_id)
        if not user_data:
            return json({"status": 403, "message": "need_register"}, 403)
        else:
            if user_data.download_count >= 5:
                return json({"status": 429, "message": "Too_many_requests"}, 429)
            else:
                return True

    async def user_download_count(self):
        user_data = await User.get_or_none(user_id=self.user_id)
        user_data.download_count += 1
        await user_data.save()
        return 5 - user_data.download_count
