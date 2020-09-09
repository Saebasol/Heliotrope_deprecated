import os
import asyncio
import shutil

import aiohttp

import aiofiles
import aiofiles.os as aios

from Heliotrope.utils.hitomi.hitomi import images
from Heliotrope.utils.option import config

headers = {"referer": f"http://{config['domain']}", "User-Agent": config["user_agent"]}

base_directory = "/var/www"


async def create_folder(index):
    if not os.path.exists(f"{base_directory}/image"):
        await aios.mkdir(f"{base_directory}/image")

    if not os.path.exists(f"{base_directory}/download"):
        await aios.mkdir(f"{base_directory}/download")

    if not os.path.exists(f"{base_directory}/image/{index}/"):
        await aios.mkdir(f"{base_directory}/image/{index}/")


async def downloader(index: int, img_link: str, filename: str):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(img_link, headers=headers) as r:
            async with aiofiles.open(
                f"{base_directory}/image/{index}/{filename}.jpg", mode="wb"
            ) as f:
                await f.write(await r.read())


async def download_tasks(index: int):
    img_links = await images(index)
    filename = 0
    for img_link in img_links:
        filename += 1
        yield downloader(index, img_link, filename)


async def compression_or_download(index: int, compression=False):
    await create_folder(index)

    if compression:
        done, _ = await asyncio.wait(list(await download_tasks(index)))
        if done:
            shutil.make_archive(
                f"{base_directory}/download/{index}/{index}",
                "zip",
                f"{base_directory}/image/{index}/",
            )
            return f"https://doujinshiman.ga/download/{index}/{index}.zip"
    else:
        async for task in download_tasks(index):
            asyncio.create_task(task)
        total = len(list(await download_tasks(index)))
        return total