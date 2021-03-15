from multidict import CIMultiDictProxy
from yarl import URL
from heliotrope.utils.decorators import strict_literal
from aiohttp import ClientSession
from asyncio.locks import Semaphore
from typing import Any, Literal


class Response:
    def __init__(
        self,
        status: int,
        reason: str,
        body: Any,
        url: URL,
        headers: CIMultiDictProxy[str],
    ):
        self.status = status
        self.reason = reason
        self.body = body
        self.url = url
        self.headers = headers


class RestrictedRequester:
    def __init__(self, semapore: Semaphore) -> None:
        self.semapore = semapore

    @strict_literal("return_method")
    async def request(
        self,
        method: str,
        url: str,
        return_method: Literal["read", "text", "json"],
        **kwargs: Any
    ):
        async with ClientSession() as cs:
            async with self.semapore, cs.request(method, url, **kwargs) as r:
                return Response(
                    r.status,
                    r.reason,
                    await getattr(r, return_method)(),
                    r.url,
                    r.headers,
                )

    @strict_literal("return_method")
    async def get(self, url, return_method: Literal["read", "text", "json"]):
        return await self.request("GET", url, return_method)

    @strict_literal("return_method")
    async def post(self, url, return_method: Literal["read", "text", "json"]):
        return await self.request("POST", url, return_method)
