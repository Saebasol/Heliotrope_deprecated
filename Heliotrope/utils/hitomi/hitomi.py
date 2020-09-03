from .common import *
from .galleryinfomodel import *
from .hitomi_requester import *
from .tagsmodel import *


async def info(number: int):
    galleryinfomodel = await get_galleryinfo(number)
    tags = await get_gallery(galleryinfomodel)
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


async def images(number: int):
    galleryinfomodel = await get_galleryinfo(number)
    return [
        image_url_from_image(number, img_model, False)
        for img_model in image_model_generator(galleryinfomodel.files)
    ]

