from asyncio.tasks import gather
from typing import Any, cast

from heliotrope.hitomi.models import HitomiGalleryinfo

from heliotrope.database.models.hitomi import File, GalleryInfo, Index, Tag


class ORMQuery:
    async def add_galleryinfo(self, hitomi_galleryinfo: HitomiGalleryinfo) -> None:
        """
        Add a new galleryinfo to the database.
        """
        # Cast to dict[str, Any] because Typeddict is immutable
        hitomi_galleryinfo_dict = cast(dict[str, Any], hitomi_galleryinfo.to_dict())

        files = hitomi_galleryinfo_dict.pop("files")
        tags = hitomi_galleryinfo_dict.pop("tags")
        galleryinfo_orm_object = await GalleryInfo.create(**hitomi_galleryinfo_dict)

        if files:
            # Make File ORM objects
            file_orm_object_list = [
                File(**{"index_id": hitomi_galleryinfo.id, **file}) for file in files
            ]
            # Save File ORM objects
            await gather(
                *[file_orm_object.save() for file_orm_object in file_orm_object_list]
            )

            # MTM Field so add in galleryinfo.files
            await galleryinfo_orm_object.files.add(*file_orm_object_list)

        if tags:
            # Make Tag ORM objects
            tag_orm_object_list = [
                Tag(**{"index_id": hitomi_galleryinfo.id, **tag}) for tag in tags
            ]
            # Save Tag ORM objects
            await gather(
                *[tag_orm_object.save() for tag_orm_object in tag_orm_object_list]
            )
            # MTM Field so add in galleryinfo.tags
            await galleryinfo_orm_object.tags.add(*tag_orm_object_list)
        # Save galleryinfo ORM object
        await galleryinfo_orm_object.save()

    async def get_galleryinfo(self, index_id: int) -> HitomiGalleryinfo:
        ...

    async def add_index(self, index: int) -> None:
        await Index.create(index_id=index)

    async def get_index(self) -> list[int]:
        return list(
            map(int, await Index.all().values_list("index_id", flat=True)),
        )

    async def get_sorted_index(self) -> list[int]:
        return sorted(await self.get_index(), reverse=True)

    async def search_galleryinfo(
        self, query: str, offset: int = 0, limit: int = 15, include_files: bool = False
    ) -> None:
        ...
