import os

import aiofiles
import aiofiles.os as aios
import aiohttp

from Heliotrope.utils import option


class Core:
    def __init__(self):
        self._directory = os.environ["directory"]
        self._headers = {
            "referer": f"http://{option.config['domain']}",
            "User-Agent": option.config["user_agent"],
        }

    @property
    def directory(self):
        return self._directory

    @property
    def headers(self):
        return self._headers

    async def create_folder(self):
        if not os.path.exists(f"{self.directory}/image"):
            await aios.mkdir(f"{self.directory}/image")

        if not os.path.exists(f"{self.directory}/download"):
            await aios.mkdir(f"{self.directory}/download")

        if not os.path.exists(f"{self.directory}/thumbnail"):
            await aios.mkdir(f"{self.directory}/thumbnail")

    async def downloader(self, index: int, img_link: str, filename: str) -> None:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(img_link, headers=self.headers) as r:
                async with aiofiles.open(
                    f"{self.directory}/image/{index}/{filename}", mode="wb"
                ) as f:
                    await f.write(await r.read())

    async def thumbnail_cache(self, img_path: str) -> True:
        if "thumbnail" not in img_path and "_" not in img_path:
            return
        path = img_path.replace("thumbnail", "").replace("_", "/")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://tn.hitomi.la{path}", headers=self.headers) as r:
                if r.status != 200:
                    return
                await self.create_folder()
                async with aiofiles.open(
                    f"{self.directory}/thumbnail/{img_path}", mode="wb"
                ) as f:
                    await f.write(await r.read())
                    return True
