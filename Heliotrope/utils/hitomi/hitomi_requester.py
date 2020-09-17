import re
import json

import aiohttp

from Heliotrope.utils.hitomi.galleryinfomodel import (
    HitomiGalleryInfoModel,
    parse_galleryinfo,
)
from Heliotrope.utils.hitomi.tagsmodel import parse_tags
from Heliotrope.utils.option import config

headers = {"referer": f"http://{config['domain']}", "User-Agent": config["user_agent"]}


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
    url_title = re.sub(
        r"(\"|\'|\%|\(|\)|\{|\}|\[|\]|\<|\>)", "-", galleryinfomodel.title
    ).replace(" ", "-")
    url = f"https://hitomi.la/{galleryinfomodel.type_ if galleryinfomodel.type_.lower() != 'artistcg' else 'cg'}/{url_title}-{galleryinfomodel.language_localname}-{galleryinfomodel.galleryid}.html".lower()
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url, headers=headers) as r:
            if r.status != 200:
                return None
            response = await r.text()
            return parse_tags(response, galleryinfomodel.type_)
