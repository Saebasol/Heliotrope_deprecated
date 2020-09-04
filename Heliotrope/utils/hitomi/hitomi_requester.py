from email import header
import json
import aiohttp
from .galleryinfomodel import HitomiGalleryInfoModel, parse_galleryinfo
from .tagsmodel import parse_tags

headers = {
    "referer": "https://hitomi.la",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
}


async def get_galleryinfo(index: int):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(
            f"https://ltn.hitomi.la/galleries/{index}.js", headers=headers
        ) as r:
            if r.status != 200:
                return None
            response = await r.text()
            js_to_json = response.replace("var galleryinfo = ", "")
            return parse_galleryinfo(json.loads(js_to_json))


async def get_gallery(galleryinfomodel: HitomiGalleryInfoModel):
    url = f"https://hitomi.la/{galleryinfomodel.type_}/{galleryinfomodel.title.replace(' ', '-')}-{galleryinfomodel.language_localname}-{galleryinfomodel.galleryid}.html".lower()
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url, headers=headers) as r:
            if r.status != 200:
                return None
            response = await r.text()
            return parse_tags(response, galleryinfomodel.type_)
