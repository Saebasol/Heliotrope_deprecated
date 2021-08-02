from dataclasses import dataclass
from typing import Any, Literal, Optional
from aiohttp.client import ClientSession
from types import TracebackType

from multidict import CIMultiDictProxy
from yarl import URL


@dataclass
class Response:
    status: int
    returned: Any
    url: URL
    headers: CIMultiDictProxy[str]


class BaseRequest:
    def __init__(self, session: Optional[ClientSession] = None) -> None:
        self.session = session

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    async def __aenter__(self) -> "BaseRequest":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        url: str,
        return_method: Literal["json", "text", "read"] = "json",
        **kwargs: Any
    ) -> Response:
        if not self.session:
            self.session = ClientSession()

        async with self.session.request(method, url, **kwargs) as r:
            return Response(
                r.status,
                await getattr(r, return_method)(),
                r.url,
                r.headers,
            )

    async def get(
        self,
        url: str,
        return_method: Literal["json", "text", "read"] = "json",
        **kwargs: Any
    ) -> Response:
        return await self.request("GET", url, return_method, **kwargs)

    async def post(
        self,
        url: str,
        return_method: Literal["json", "text", "read"] = "json",
        **kwargs: Any
    ) -> Response:
        return await self.request("POST", url, return_method, **kwargs)