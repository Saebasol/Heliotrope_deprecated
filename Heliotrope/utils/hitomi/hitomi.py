import asyncio
from typing import Optional, Union

from Heliotrope.utils.hitomi.common import HitomiImageModel, image_url_from_image
from Heliotrope.utils.hitomi.hitomi_requester import (
    fetch_index,
    get_gallery,
    get_galleryinfo,
)
from Heliotrope.utils.option import config
from Heliotrope.utils.shuffle import shuffle_image_url


async def info(index: int):
    if response := await get_gallery(index):
        url, tags = response

        data = {
            "status": 200,
            "title": {"value": tags.title, "url": url},
            "galleryid": index,
            "thumbnail": tags.thumbnail,
            "artist": tags.artist,
            "group": tags.group,
            "type": tags.type_,
            "language": tags.language,
            "series": tags.series,
            "characters": tags.characters,
            "tags": tags.tags,
        }

        return data


async def galleryinfo(index: int):
    if galleryinfomodel := await get_galleryinfo(index):
        data = {
            "status": 200,
            "language_localname": galleryinfomodel.language_localname,
            "language": galleryinfomodel.language,
            "date": galleryinfomodel.date,
            "files": galleryinfomodel.files,
            "tags": galleryinfomodel.tags,
            "japanese_title": galleryinfomodel.japanese_title,
            "title": galleryinfomodel.title,
            "id": galleryinfomodel.galleryid,
            "type": galleryinfomodel.type_,
        }

        return data


async def integrated_info(index: int):
    if galleryinfomodel := await get_galleryinfo(index):
        gi = {
            "language_localname": galleryinfomodel.language_localname,
            "language": galleryinfomodel.language,
            "date": galleryinfomodel.date,
            "files": galleryinfomodel.files,
            "tags": galleryinfomodel.tags,
            "japanese_title": galleryinfomodel.japanese_title,
            "title": galleryinfomodel.title,
            "id": galleryinfomodel.galleryid,
            "type": galleryinfomodel.type_,
        }
    else:
        gi = None

    if response := await get_gallery(index):
        _, tags = response
        ts = {
            "title": tags.title,
            "artist": tags.artist,
            "group": tags.group,
            "type": tags.type_,
            "language": tags.language,
            "series": tags.series,
            "characters": tags.characters,
            "tags": tags.tags,
        }
    else:
        ts = None

    data = {
        "data": [
            {
                "status": 200,
                "galleryinfo": gi,
                "tags": ts,
            }
        ]
    }

    return data


async def list_(num: int):
    index_list = await fetch_index(config)
    split_index_list = [
        index_list[i * 15 : (i + 1) * 15]
        for i in range((len(index_list) + 15 - 1) // 15)
    ]

    if len(split_index_list) < num + 1:
        return None

    done, _ = await asyncio.wait([info(index) for index in split_index_list[num]])
    info_list = [d.result() for d in done]
    data = {"status": 200, "list": info_list}

    return data


async def images(index: int) -> Optional[Union[list[dict[str, str]]]]:
    if galleryinfomodel := await get_galleryinfo(index):
        if galleryinfomodel.files:
            images = [
                {
                    "url": f"https://doujinshiman.ga/v3/api/proxy/{shuffle_image_url(image_url_from_image(index, img, True))}",
                    "filename": img.name,
                }
                for img in HitomiImageModel.image_model_generator(
                    galleryinfomodel.files
                )
            ]
            return images

    return None


async def index():
    return await fetch_index(config)
