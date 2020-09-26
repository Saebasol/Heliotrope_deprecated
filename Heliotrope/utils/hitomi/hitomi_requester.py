import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import aiohttp

from Heliotrope.utils.hitomi.galleryinfomodel import parse_galleryinfo
from Heliotrope.utils.hitomi.tagsmodel import parse_tags
from Heliotrope.utils.option import config

headers = {"referer": f"http://{config['domain']}", "User-Agent": config["user_agent"]}


async def get_redirect_url(index: int):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(
            f"https://hitomi.la/galleries/{index}.html", headers=headers
        ) as r:
            if r.status != 200:
                return
            response = await r.text()
            soup = BeautifulSoup(response, "lxml")
            url = soup.find("a", href=True)["href"]
            type_ = urlparse(url).path.split("/")[1]
            # index = re.search(r"\-([0-9]*)\.html", "url")[1]
            return url, type_


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


async def get_gallery(index: int):
    redirect = await get_redirect_url(index)
    if not redirect:
        return None
    else:
        url, type_ = redirect
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url, headers=headers) as r:
            if r.status != 200:
                return None
            response = await r.text()
            return str(r.url), parse_tags(response, type_)