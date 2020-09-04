from importlib.metadata import files
from .common import *
from .galleryinfomodel import *
from .hitomi_requester import *
from .tagsmodel import *
from .fetch_index import *

config = {
    "domain": "hitomi.la",
    "mode": "index",
    "index_file": "index-korean.nozomi",
    "page": 1,
    "item": 25,
    "language": "en",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "proxy": "",
}


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

    data = {"data": [{"galleryinfo": gi, "tags": ts,}]}

    return data


async def images(index: int):
    galleryinfomodel = await get_galleryinfo(index)
    return [
        image_url_from_image(index, img_model, False)
        for img_model in image_model_generator(galleryinfomodel.files)
    ]


async def index(config):
    return await fetch_index(config)
