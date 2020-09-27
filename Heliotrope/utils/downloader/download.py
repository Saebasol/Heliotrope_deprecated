import asyncio
import os
import shutil

import aiofiles
import aiofiles.os as aios
import aiohttp
from sanic.response import json

from Heliotrope.utils.database.models.user import User
from Heliotrope.utils.hitomi.hitomi import images
from Heliotrope.utils.option import config

headers = {"referer": f"http://{config['domain']}", "User-Agent": config["user_agent"]}

base_directory = os.environ["directory"]


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
                return json({"code": 200, "status": "already", "total": total}, 200)
            else:
                await aios.mkdir(f"{base_directory}/image/{index}")
                total = await compression_or_download(index, img_dicts)
                return json({"code": 200, "status": "pending", "total": total}, 200)

        user_data = await User.get_or_none(user_id=user_id)  # 따로 나눠야함
        if not user_data:
            return json({"code": 403, "status": "need_register"}, 403)
        else:
            count = user_data.download_count
            if count >= 5:
                return json({"code": 429, "status": "Too_many_requests"}, 429)
            else:
                user_data.download_count = count + 1
                await user_data.save()

        if download_bool:
            if os.path.exists(f"{base_directory}/download/{index}/{index}.zip"):
                return json(
                    {
                        "code": 200,
                        "status": "already",
                        "link": f"https://doujinshiman.ga/download/{index}/{index}.zip",
                    },
                    200,
                )
            elif os.path.exists(f"{base_directory}/image/{index}/"):
                shutil.make_archive(
                    f"{base_directory}/download/{index}/{index}",
                    "zip",
                    f"{base_directory}/image/{index}/",
                )
                return json(
                    {
                        "code": 200,
                        "status": "use_cached",
                        "link": f"https://doujinshiman.ga/download/{index}/{index}.zip",
                    },
                    200,
                )
            else:
                await aios.mkdir(f"{base_directory}/download/{index}")
                link = await compression_or_download(index, img_dicts, True)
                return json({"code": 200, "status": "successfully", "link": link}, 200)

    else:
        return json({"code": 404, "status": "not_found"}, 404)


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


async def download_tasks(index: int, img_dicts: dict):
    for img_dict in img_dicts:
        yield downloader(index, img_dict["url"], img_dict["filename"])


async def compression_or_download(index: int, img_dicts: dict, compression=False):
    if compression:
        done, _ = await asyncio.wait(
            [task async for task in download_tasks(index, img_dicts)]
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
        async for task in download_tasks(index, img_dicts):
            total += 1
            asyncio.create_task(task)
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
