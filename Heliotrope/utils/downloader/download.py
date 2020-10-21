import asyncio
import os
import shutil

import aiofiles
import aiofiles.os as aios
import aiohttp
from sanic.response import json

from Heliotrope.utils.database.user_management import (
    user_download_count,
    user_download_count_check,
)
from Heliotrope.utils.downloader.task_progress import TaskProgress
from Heliotrope.utils.hitomi.hitomi import images
from Heliotrope.utils.image import convert_to_png
from Heliotrope.utils.option import config

headers = {"referer": f"http://{config['domain']}", "User-Agent": config["user_agent"]}

base_directory = os.environ["directory"]

task_progress = TaskProgress()


async def create_folder():
    if not os.path.exists(f"{base_directory}/image"):
        await aios.mkdir(f"{base_directory}/image")

    if not os.path.exists(f"{base_directory}/download"):
        await aios.mkdir(f"{base_directory}/download")

    if not os.path.exists(f"{base_directory}/thumbnail"):
        await aios.mkdir(f"{base_directory}/thumbnail")


async def check_folder_and_download(index, download_bool, user_id=None):
    await create_folder()
    img_dicts = await check_vaild(index)
    if img_dicts:

        if not download_bool:
            if os.path.exists(f"{base_directory}/image/{index}/"):
                total = len(next(os.walk(f"{base_directory}/image/{index}/"))[2])
                return json({"status": 200, "message": "already", "total": total}, 200)
            else:
                await aios.mkdir(f"{base_directory}/image/{index}")
                total = await compression_or_download(user_id, index, img_dicts)
                return json({"status": 200, "message": "pending", "total": total}, 200)
        result = await user_download_count_check(user_id)

        if result is True:
            count = await user_download_count(user_id)

            if download_bool:
                if os.path.exists(f"{base_directory}/download/{index}/{index}.zip"):
                    await task_progress.cache_already(
                        user_id,
                        index,
                        count,
                        "already",
                        f"https://doujinshiman.ga/download/{index}/{index}.zip",
                    )

                    return json({"status": 200, "message": "pending"})
                elif os.path.exists(f"{base_directory}/image/{index}/"):
                    await executer(index)
                    await task_progress.cache_already(
                        user_id,
                        index,
                        count,
                        "use_cached",
                        f"https://doujinshiman.ga/download/{index}/{index}.zip",
                    )

                    return json({"status": 200, "message": "pending"})

                else:
                    await aios.mkdir(f"{base_directory}/download/{index}")
                    await aios.mkdir(f"{base_directory}/image/{index}")
                    await compression_or_download(
                        user_id, index, img_dicts, count, True
                    )
                    return json({"status": 200, "message": "pending"}, 200)
        else:
            return result

    else:
        return json({"status": 404, "message": "not_found"}, 404)


async def downloader(index: int, img_link: str, filename: str):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(img_link, headers=headers) as r:
            async with aiofiles.open(
                f"{base_directory}/image/{index}/{filename}", mode="wb"
            ) as f:
                await f.write(await r.read())


async def check_vaild(index):
    img_dicts = await images(index)
    if not img_dicts:
        return None
    else:
        return img_dicts


def download_tasks(index: int, img_dicts: list):
    for img_dict in img_dicts:
        yield downloader(index, img_dict["url"], img_dict["filename"])


def archive(index):
    shutil.make_archive(
        f"{base_directory}/download/{index}/{index}",
        "zip",
        f"{base_directory}/image/{index}/",
    )


async def convert(index):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, convert_to_png, f"{base_directory}/image/{index}")
    return loop


async def executer(index):
    loop = await convert(index)
    return await loop.run_in_executor(None, archive, index)


async def download_compression(task_list, index):
    done, _ = await asyncio.wait(task_list)
    if done:
        return await executer(index)


async def compression_or_download(
    user_id: int,
    index: int,
    img_dicts: list,
    count: int = None,
    compression: bool = False,
):
    task_list = list(download_tasks(index, img_dicts))
    if compression:
        task = asyncio.create_task(download_compression(task_list, index), name=index)
        await task_progress.cache_task(user_id, count, task)
        return
    else:
        total = len(img_dicts)
        done, _ = await asyncio.wait(
            task_list,
            return_when="FIRST_COMPLETED",
        )
        if done:
            await convert(index)
            return total


async def thumbnail_cache(img_path: str):
    if "thumbnail" not in img_path and "_" not in img_path:
        return
    path = img_path.replace("thumbnail", "").replace("_", "/")
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://tn.hitomi.la{path}", headers=headers) as r:
            if r.status != 200:
                return
            await create_folder()
            async with aiofiles.open(
                f"{base_directory}/thumbnail/{img_path}", mode="wb"
            ) as f:
                await f.write(await r.read())
                return True
