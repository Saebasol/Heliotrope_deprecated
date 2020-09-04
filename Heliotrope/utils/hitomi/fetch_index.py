import struct

import aiohttp


async def fetch_index(opts: dict) -> list:  # thx to seia-soto
    byte_start = (opts["page"] - 1) * opts["item"] * 4
    byte_end = byte_start + opts["item"] * 4 - 1

    async with aiohttp.ClientSession() as cs:
        async with cs.get(
            f'https://ltn.{opts["domain"]}/{opts["index_file"]}',
            headers={
                "User-Agent": opts["user_agent"],
                "Range": f"byte={byte_start}-{byte_end}",
                "referer": f"https://{opts['domain']}/index-all-${opts['page']}.html",
                "origin": f"http://{opts['domain']}",
            },
        ) as r:
            buffer = await r.read()

    # len(buffer) % 4 this check 32bit
    total_items = len(buffer) // 4
    return struct.unpack(f">{total_items}i", buffer)
