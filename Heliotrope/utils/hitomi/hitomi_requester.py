import json
import struct
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from Heliotrope.utils.hitomi.galleryinfomodel import parse_galleryinfo
from Heliotrope.utils.hitomi.tagsmodel import parse_tags
from Heliotrope.utils.option import Config, config
from Heliotrope.utils.requester import request
from Heliotrope.utils.shuffle import solve_shuffle_image_url

headers = {"referer": f"http://{config.domain}", "User-Agent": config.user_agent}


async def get_redirect_url(index: int):
    r = await request.get(
        f"https://hitomi.la/galleries/{index}.html", "text", headers=headers
    )
    if r.status != 200:
        return
    soup = BeautifulSoup(r.body, "lxml")
    url = soup.find("a", href=True)["href"]
    type_ = urlparse(url).path.split("/")[1]
    # index = re.search(r"\-([0-9]*)\.html", "url")[1]
    return url, type_


async def get_galleryinfo(index: int):
    r = await request.get(
        f"https://ltn.hitomi.la/galleries/{index}.js", "text", headers=headers
    )
    if r.status != 200:
        return None
    js_to_json = r.body.replace("var galleryinfo = ", "")
    return parse_galleryinfo(json.loads(js_to_json))


async def get_gallery(index: int):
    redirect = await get_redirect_url(index)
    if not redirect:
        return None
    url, type_ = redirect
    r = await request.get(url, headers=headers)
    if r.status != 200:
        return None
    return str(r.url), parse_tags(r.body, type_)


async def image_proxer(shuffled_img_url: str):
    url = solve_shuffle_image_url(shuffled_img_url)

    if not isinstance(url, str):
        return url

    if "pximg" in url:
        headers.update({"referer": "https://pixiv.net"})

    response = await request.get(url, headers=headers)

    if response.status != 200:
        return

    return response.body, response.headers.get("content-type") or "image"


async def fetch_index(opts: Config) -> list:  # thx to seia-soto
    byte_start = (opts.page - 1) * opts.item * 4
    byte_end = byte_start + opts.item * 4 - 1

    r = await request.get(
        f"https://ltn.{opts.domain}/{opts.index_file}",
        headers={
            "User-Agent": opts.user_agent,
            "Range": f"byte={byte_start}-{byte_end}",
            "referer": f"https://{opts.domain}/index-all-${opts.page}.html",
            "origin": f"http://{opts.domain}",
        },
    )

    # len(buffer) % 4 this check 32bit
    total_items = len(r.body) // 4
    return struct.unpack(f">{total_items}i", r.body)
