from Heliotrope.utils.hitomi.common import image_model_generator, image_url_from_image
import asyncio

from Heliotrope.utils.hitomi.fetch_index import fetch_index
from Heliotrope.utils.hitomi.hitomi_requester import get_gallery, get_galleryinfo
from Heliotrope.utils.option import config


async def info(index: int):
    galleryinfomodel = await get_galleryinfo(index)
    if not galleryinfomodel:
        return None
    tags = await get_gallery(galleryinfomodel)
    if not tags:
        return None

    data = {
        "title": tags.title,
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
    tags = await get_gallery(galleryinfomodel)

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
    data = {"list": info_list}

    return data


async def images(index: int):
    galleryinfomodel = await get_galleryinfo(index)
    images = [
        image_url_from_image(index, img, True)
        for img in image_model_generator(galleryinfomodel.files)
    ]  # 추후에 파일 이름 변경예정
    return images