
from heliotrope.hitomi.models import  HitomiGalleryInfo,

from heliotrope.database.models.hitomi import File, GalleryInfo, Tag


class ORMQuery:
    async def add_galleryinfo(self, hitomi_galleryinfo: HitomiGalleryInfo) -> None:
        hitomi_galleryinfo_dict = hitomi_galleryinfo.to_dict()
        files = hitomi_galleryinfo_dict.pop("files")
        tags = hitomi_galleryinfo_dict.pop("tags")
        galleryinfo_orm_object = await GalleryInfo.create(**hitomi_galleryinfo_dict)

        if files:
            for file in files:
                file_orm_object = File(**{"index_id": hitomi_galleryinfo.id, **file})
                await file_orm_object.save()
                await galleryinfo_orm_object.files.add(file_orm_object)

        if tags:
            for tag in tags:
                tag_orm_object = Tag(**{"index_id": hitomi_galleryinfo.id, **tag})
                await tag_orm_object.save()
                await galleryinfo_orm_object.tags.add(tag_orm_object)

        await galleryinfo_orm_object.save()
