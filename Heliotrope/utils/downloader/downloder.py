import asyncio
import os
import shutil
from typing import Generator

import aiofiles.os as aios
from sanic.response import json

from Heliotrope.utils.database.user_management import Management
from Heliotrope.utils.downloader.core import Core
from Heliotrope.utils.downloader.task_progress import TaskProgress


class Downloader(Core, TaskProgress, Management):
    def __init__(self, index: int, user_id: int):
        Core.__init__(self)
        TaskProgress.__init__(self, user_id)
        Management.__init__(self, user_id)

        self.index = index

    def archive(self):
        shutil.make_archive(
            f"{self.directory}/download/{self.index}/{self.index}",
            "zip",
            f"{self.directory}/image/{self.index}/",
        )

    async def executer(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.archive)

    async def download_viewer(self, tasks_generator: Generator):
        if os.path.exists(f"{self.directory}/image/{self.index}/"):
            total = len(next(os.walk(f"{self.directory}/image/{self.index}/"))[2])
            return json({"status": 200, "message": "already", "total": total}, 200)
        else:
            await aios.mkdir(f"{self.directory}/image/{self.index}")
            tasks_list = list(tasks_generator)
            total = len(tasks_list)
            await tasks_list[0]
            done, _ = await asyncio.wait(tasks_list[1:], return_when="FIRST_COMPLETED")
            if done:
                return json({"status": 200, "message": "pending", "total": total}, 200)
Corutine
    async def download_zip(self, tasks_generator: Generator):
        result = await self.user_download_count_check()

        if result is True:

            count = await self.user_download_count()

            if os.path.exists(
                f"{self.directory}/download/{self.index}/{self.index}.zip"
            ):
                await self.cache_already(
                    self.index,
                    count,
                    "already",
                    f"https://doujinshiman.ga/download/{self.index}/{self.index}.zip",
                )
                return json({"status": 200, "message": "already"})

            elif os.path.exists(f"{self.directory}/image/{self.index}/"):
                await self.executer()

                await self.cache_already(
                    self.index,
                    count,
                    "use_cached",
                    f"https://doujinshiman.ga/download/{self.index}/{self.index}.zip",
                )
                return json({"status": 200, "message": "use_cached"})

            else:
                await aios.mkdir(f"{self.directory}/download/{self.index}")
                await aios.mkdir(f"{self.directory}/image/{self.index}")
                tasks_list = list(tasks_generator)
                task = asyncio.create_task(asyncio.wait(tasks_list), name=self.index)
                await self.cache_task(count, task)

                return json({"status": 200, "message": "pending"}, 200)

        else:
            return result
