import asyncio
import os
import shutil

import aiofiles.os as aios
from sanic.response import json

from Heliotrope.utils.database.user_management import Management
from Heliotrope.utils.downloader.core import Core
from Heliotrope.utils.downloader.queue import DownloadQueue
from Heliotrope.utils.downloader.task_progress import TaskProgress


class Downloader(Core, TaskProgress, Management, DownloadQueue):
    def __init__(self, index: int, user_id: int):
        Core.__init__(self)
        TaskProgress.__init__(self, user_id)
        Management.__init__(self, user_id)
        DownloadQueue.__init__(self, index)

    def archive(self):
        shutil.make_archive(
            f"{self.directory}/download/{self.index}/{self.index}",
            "zip",
            f"{self.directory}/image/{self.index}/",
        )

    async def executer(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.archive, self.index)

    async def download_viewer(self, tasks_list: list):
        if os.path.exists(f"{self.directory}/image/{self.index}/"):
            total = len(next(os.walk(f"{self.directory}/image/{self.index}/"))[2])
            return json({"status": 200, "message": "already", "total": total}, 200)
        else:
            await aios.mkdir(f"{self.directory}/image/{self.index}")
            total = len(tasks_list)
            await self.make_queue(tasks_list)
            tasks = await self.start_download()
            await tasks[0]
            asyncio.create_task(asyncio.wait(tasks[1:]))
            return json({"status": 200, "message": "pending", "total": total}, 200)

    async def download_zip(self, task_list):
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

                await self.make_queue(task_list)
                tasks = await self.start_download()

                task = asyncio.create_task(asyncio.wait(tasks), name=self.index)
                await self.cache_task(count, task)

                return json({"status": 200, "message": "pending"}, 200)

        else:
            return result
