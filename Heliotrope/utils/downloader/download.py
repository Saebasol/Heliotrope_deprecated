from sanic.response import json

from Heliotrope.utils.downloader.downloder import Downloader
from Heliotrope.utils.hitomi.hitomi import images


class Download(Downloader):
    def __init__(self, index: int, download_bool: bool, user_id: int = None):
        super().__init__(index, user_id)
        self.download_bool = download_bool

    async def check_vaild(self):
        img_dicts = await images(self.index)
        if not img_dicts:
            return None
        else:
            return img_dicts

    def download_tasks_list(self, img_dicts: list) -> list:
        for img_dict in img_dicts:
            yield self.downloader(self.index, img_dict["url"], img_dict["filename"])

    async def download(self):
        img_dicts = await self.check_vaild()
        if img_dicts:
            await self.create_folder()
            if self.download_bool:
                return await self.download_zip(self.download_tasks_list(img_dicts))
            else:
                return await self.download_viewer(self.download_tasks_list(img_dicts))

        else:
            return json({"status": 404, "message": "not_found"}, 404)
