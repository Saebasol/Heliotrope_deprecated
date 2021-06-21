import json
from dataclasses import dataclass
from struct import unpack
from typing import Any, Literal
from urllib.parse import urlparse

from aiohttp import ClientSession
from aiohttp.typedefs import StrOrURL
from multidict import CIMultiDictProxy
from yarl import URL


@dataclass
class Response:
    status: int
    reason: str
    body: Any
    url: URL
    headers: CIMultiDictProxy[str]


class SessionRequester:
    def __init__(self, session: ClientSession = None) -> None:
        self.session = session

    async def request(
        self,
        method: str,
        url: StrOrURL,
        return_method: Literal["read", "text", "json"],
        **kwargs: Any,
    ):
        if not self.session:
            raise RuntimeError("Need ClientSession")
        async with self.session.request(method, url, **kwargs) as r:
            return Response(
                r.status,
                r.reason,
                await getattr(r, return_method)(),
                r.url,
                r.headers,
            )

    async def get(
        self,
        url: StrOrURL,
        return_method: Literal["read", "text", "json"],
        **kwargs: Any,
    ):
        return await self.request("GET", url, return_method, **kwargs)

    async def post(
        self,
        url: StrOrURL,
        return_method: Literal["read", "text", "json"],
        **kwargs: Any,
    ):
        return await self.request("POST", url, return_method, **kwargs)


# class SemaphoreRequester:
#     def __init__(self, semaphore: Semaphore = None) -> None:
#         self.semaphore = semaphore

#
#     async def request(
#         self,
#         method: str,
#         url: StrOrURL,
#         return_method: Literal["read", "text", "json"],
#         **kwargs: Any,
#     ):
#         if not self.semaphore:
#             raise RuntimeError("Need Semaphore")
#         async with ClientSession() as cs:
#             async with self.semaphore, cs.request(method, url, **kwargs) as r:
#                 return Response(
#                     r.status,
#                     r.reason,
#                     await getattr(r, return_method)(),
#                     r.url,
#                     r.headers,
#                 )

#
#     async def get(
#         self,
#         url: StrOrURL,
#         return_method: Literal["read", "text", "json"],
#         **kwargs: Any,
#     ):
#         return await self.request("GET", url, return_method, **kwargs)

#
#     async def post(
#         self,
#         url: StrOrURL,
#         return_method: Literal["read", "text", "json"],
#         **kwargs: Any,
#     ):
#         return await self.request("POST", url, return_method, **kwargs)
