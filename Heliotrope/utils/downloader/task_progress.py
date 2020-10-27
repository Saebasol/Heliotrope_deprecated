import asyncio

import aiocache


class TaskProgress:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.cache = aiocache.Cache()

    async def cache_task(self, count: int, task: asyncio.Task):
        task_dict_list = [{"task_name": task.get_name(), "count": count, "task": task}]
        if await self.cache.exists(self.user_id):
            already_in_list = await self.cache.get(self.user_id)
            already_in_list.extend(task_dict_list)
            await self.cache.set(self.user_id, already_in_list)
        else:
            await self.cache.set(self.user_id, task_dict_list)

    async def cache_already(self, index, count, status, link):
        already_dict_list = [
            {"index": index, "count": count, "task_status": status, "link": link}
        ]
        if await self.cache.exists(f"{self.user_id}_already"):
            already_in_list = await self.cache.get(f"{self.user_id}_already")
            already_in_list.extend(already_dict_list)
            await self.cache.set(f"{self.user_id}_already", already_in_list)
        else:
            await self.cache.set(f"{self.user_id}_already", already_dict_list)
