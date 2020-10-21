import asyncio

from Heliotrope.utils.hitomi.common import image_model_generator, image_url_from_image
from Heliotrope.utils.hitomi.fetch_index import fetch_index
from Heliotrope.utils.hitomi.hitomi_requester import get_gallery, get_galleryinfo
from Heliotrope.utils.option import config


async def info(index: int):
    arg = await get_gallery(index)
    if not arg:
        return None
    else:
        url, tags = arg

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
    galleryinfomodel = await get_galleryinfo(index)

    if not galleryinfomodel:
        return None

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
    galleryinfomodel = await get_galleryinfo(index)
    _, tags = await get_gallery(index)

    if not galleryinfomodel:
        gi = None
    else:
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

    if not tags:
        ts = None
    else:
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


async def images(index: int):
    galleryinfomodel = await get_galleryinfo(index)
    if not galleryinfomodel:
        return None
    images = [
        {
            "url": image_url_from_image(index, img, False),
            "filename": img.name,
        }
        for img in image_model_generator(galleryinfomodel.files)
    ]
    return images


async def index():
    return await fetch_index(config)
