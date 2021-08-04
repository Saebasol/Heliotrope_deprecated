# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false

from typing import Any, Optional, cast

from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore


class NoSQLQuery:
    def __init__(self, mongo_db_url: str) -> None:
        self.__collection = AsyncIOMotorClient(mongo_db_url).hitomi.info

    async def get_info_list(
        self, offset: int = 0, limit: int = 15
    ) -> list[dict[str, Any]]:
        return cast(
            list[dict[str, Any]],
            await self.__collection.find({}, {"_id": 0})
            .sort("index", -1)
            .skip(offset)
            .limit(limit)
            .to_list(15),
        )

    async def search_info_list(
        self, query: str, offset: int = 0, limit: int = 15
    ) -> Optional[tuple[int, dict[str, Any]]]:
        search_query = {"$search": {"text": {"query": query, "path": "title"}}}

        if count := (
            await self.__collection.aggregate(
                [search_query, {"$count": "count"}]
            ).to_list(1)
        ):
            result = await self.__collection.aggregate(
                [
                    search_query,
                    {"$skip": offset},
                    {"$limit": limit},
                    {"$project": {"_id": 0}},
                ]
            ).to_list(15)

            return result, count[0]["count"]

        return None

    async def find_info(self, index: int) -> dict[str, Any]:
        return cast(dict[str, Any], await self.__collection.find_one({"index": index}))

    async def insert_info(self, info: dict[str, Any]) -> None:
        return cast(None, await self.__collection.insert_one(info))
