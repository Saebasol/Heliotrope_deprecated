from asyncio import sleep
from typing import Any, NoReturn

from aiohttp.client import ClientSession

from heliotrope.database.mongo import NoSQLQuery
from heliotrope.database.query import SQLQuery
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.sanic import Heliotrope


class Mirroring(HitomiRequest):
    def __init__(self, heliotrope: Heliotrope, session: ClientSession):
        super().__init__(session)
        self.__heliotrope = heliotrope

    @property
    def sql(self) -> SQLQuery:
        return self.__heliotrope.ctx.sql_query

    @property
    def nosql(self) -> NoSQLQuery:
        return self.__heliotrope.ctx.nosql_query

    @classmethod
    async def setup(cls, **kwargs: Any) -> "Mirroring":
        heliotrope = kwargs.pop("heliotrope")
        session = ClientSession(**kwargs)
        mirroring = cls(heliotrope, session)
        mirroring.session.headers.update(mirroring.headers)
        return mirroring

    async def compare_index_list(self) -> list[int]:
        remote_index_list = await self.fetch_index()
        local_index_list = await self.__heliotrope.ctx.sql_query.get_index()
        return list(set(remote_index_list) - set(local_index_list))

    async def mirroring(self, index_list: list[int]) -> None:
        for index in index_list:
            if galleryinfo := await self.get_galleyinfo(index):
                if not await self.sql.get_galleryinfo(index):
                    await self.sql.add_galleryinfo(galleryinfo)

            if info := await self.get_info(index):
                if not await self.nosql.find_info(index):
                    await self.nosql.insert_info(info.to_dict())

            if index not in await self.sql.get_index():
                await self.sql.add_index(index)

    async def task(self, delay: float) -> NoReturn:
        while True:
            if index_list := await self.compare_index_list():
                await self.mirroring(index_list)

            await sleep(delay)
