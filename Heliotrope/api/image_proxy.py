import asyncio
import aiohttp

from sanic import Blueprint
from sanic import response

from Heliotrope.utils.shuffle import solve_shuffle_image_url
from Heliotrope.utils.option import config

# https://github.com/kijk2869/discodo/blob/v1.0.5b/discodo/node/server/server.py#L44
class StreamSender:
    def __init__(
        self, session: aiohttp.ClientSession, response: aiohttp.ClientResponse
    ):
        self.loop = asyncio.get_event_loop()
        self.session = session
        self.response = response

    def __del__(self):
        if self.response:
            self.response.close()
        self.loop.create_task(self.session.close())

    @classmethod
    async def create(
        cls,
        url: str,
    ):
        headers = {
            "referer": f"http://{config.domain}",
            "User-Agent": config.user_agent,
        }
        if "pximg" in url:
            headers.update({"referer": "https://pixiv.net"})

        session = aiohttp.ClientSession()
        response = await session.get(url, headers=headers)

        return cls(session, response)

    async def send(self, response: response.StreamingHTTPResponse):
        try:
            async for data, _ in self.response.content.iter_chunks():
                try:
                    await response.write(data)
                except:
                    break
        except:
            pass
        finally:
            self.__del__()


proxy = Blueprint("image_proxy", url_prefix="/proxy")


@proxy.route(
    "/<path>",
    methods=["GET"],
)
async def image_proxy(request, path: str):
    url = solve_shuffle_image_url(path)

    if not isinstance(url, str):
        return url

    sender = await StreamSender.create(url)

    if sender.response.status != 200:
        return response.json({"code": "404", "message": "not_found"}, 404)

    return response.stream(
        sender.send, content_type_=sender.response.headers.get("content-type_")
    )
