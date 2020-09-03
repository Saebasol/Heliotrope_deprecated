import json
import aiohttp
from .galleryinfomodel import HitomiGalleryInfoModel, parse_galleryinfo
from .tagsmodel import parse_tags


async def get_galleryinfo(number: int):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://ltn.hitomi.la/galleries/{number}.js") as r:
            response = await r.text()
            js_to_json = response.replace("var galleryinfo = ", "")
            return parse_galleryinfo(json.loads(js_to_json))


async def get_gallery(galleryinfomodel: HitomiGalleryInfoModel):
    url = f"https://hitomi.la/{galleryinfomodel.type_}/{galleryinfomodel.title.replace(' ', '-')}-{galleryinfomodel.language_localname}-{galleryinfomodel.galleryid}.html"
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            response = await r.text()
            return parse_tags(response)