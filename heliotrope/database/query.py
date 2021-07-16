from asyncio.tasks import gather
from typing import Any, cast

from heliotrope.hitomi.models import HitomiGalleryInfo

from heliotrope.database.models.hitomi import File, GalleryInfo, Tag


class ORMQuery:
    async def add_galleryinfo(self, hitomi_galleryinfo: HitomiGalleryInfo) -> None:
        hitomi_galleryinfo_dict = cast(dict[str, Any], hitomi_galleryinfo.to_dict())

        files = hitomi_galleryinfo_dict.pop("files")
        tags = hitomi_galleryinfo_dict.pop("tags")
        galleryinfo_orm_object = await GalleryInfo.create(**hitomi_galleryinfo_dict)

        if files:
            file_orm_object_list = [
                File(**{"index_id": hitomi_galleryinfo.id, **file}) for file in files
            ]
            await gather(
                *[file_orm_object.save() for file_orm_object in file_orm_object_list]
            )

            await galleryinfo_orm_object.files.add(*file_orm_object_list)

        if tags:
            tag_orm_object_list = [
                Tag(**{"index_id": hitomi_galleryinfo.id, **tag}) for tag in tags
            ]
            await gather(
                *[tag_orm_object.save() for tag_orm_object in tag_orm_object_list]
            )

            await galleryinfo_orm_object.tags.add(*tag_orm_object_list)

        await galleryinfo_orm_object.save()
