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


async def check_folder(index, download_bool):
    img_links = check_vaild(index)
    if img_links:
        if not download_bool:
            if os.path.exists(f"{base_directory}/image/{index}/"):
                return True
            else:
                link = await compression_or_download(index, img_links)
                return False

        if download_bool:
            if os.path.exists(f"{base_directory}/download/{index}/{index}.zip"):
                return
            else:
                total = await compression_or_download(index, img_links, True)
                return
    else:
        return None


async def downloader(index: int, img_link: str, filename: str):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(img_link, headers=headers) as r:
            async with aiofiles.open(
                f"{base_directory}/image/{index}/{filename}.jpg", mode="wb"
            ) as f:
                await f.write(await r.read())


async def check_vaild(index):
    img_links = await images(index)
    if not img_links:
        return None
    else:
        return img_links


async def download_tasks(index: int, img_links: list):
    filename = 0
    for img_link in img_links:
        filename += 1
        yield downloader(index, img_link, filename)


async def compression_or_download(index: int, img_links: list, compression=False):
    await create_folder(index)

    if compression:
        done, _ = await asyncio.wait(
            [task async for task in download_tasks(index, img_links)]
        )
        if done:
            shutil.make_archive(
                f"{base_directory}/download/{index}/{index}",
                "zip",
                f"{base_directory}/image/{index}/",
            )
            return f"https://doujinshiman.ga/download/{index}/{index}.zip"
    else:
        total = 0
        async for task in download_tasks(index, img_links):
            total += 1
            asyncio.create_task(task)
        return total