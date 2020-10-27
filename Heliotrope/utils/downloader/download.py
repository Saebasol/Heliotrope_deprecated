from sanic.response import json

from Heliotrope.utils.downloader.downloder import Downloader
from Heliotrope.utils.hitomi.hitomi import images


class Download(Downloader):
    def __init__(self, index: int, download_bool: bool, user_id: int = None):
        super().__init__(self, index, user_id)
        self.download_bool = download_bool

    async def check_vaild(self):
        img_dicts = await images(self.index)
        if not img_dicts:
            return None
        else:
            return img_dicts

    def download_tasks_list(self, img_dicts: list) -> list:
        return [
            self.downloader(img_dict["url"], img_dict["filename"])
            for img_dict in img_dicts
        ]

    async def download(self):
        img_dicts = await self.check_vaild()
        if img_dicts:

            task_list = self.download_tasks_list(img_dicts)

            if self.download_bool:
                return await self.download_zip(task_list)
            else:
                return await self.download_viewer(task_list)

        else:
            return json({"status": 404, "message": "not_found"}, 404)
