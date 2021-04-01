from heliotrope.database.models.hitomi import File, GalleryInfo, Index, Tag
from heliotrope.database.models.requestcount import RequestCount
from heliotrope.utils.hitomi.models import HitomiGalleryInfoModel
from heliotrope.utils.useful import remove_id_and_index_id


async def get_all_request_count():
    if rank_list := await RequestCount.all().values():
        sorted_ranking = sorted(rank_list, key=lambda info: info["count"], reverse=True)
        ranking = {
            "total": len(sorted_ranking),
            "list": sorted_ranking,
        }
        return ranking


async def add_request_count(index: int):
    if index_data := await RequestCount.get_or_none(index=index):
        index_data.count += 1
        await index_data.save()
        return True
    else:
        if galleryinfo := await GalleryInfo.get_or_none(id=index):
            index_data = await RequestCount.create(
                index=index, count=1, title=galleryinfo.title
            )
            await index_data.save()
            return True


async def get_galleryinfo(index: int):
    if galleryinfo := await GalleryInfo.get_or_none(id=index):
        galleryinfo_dict = {
            **(await galleryinfo.first().values())[0],
            "files": remove_id_and_index_id(await galleryinfo.files.all().values()),
            "tags": remove_id_and_index_id(await galleryinfo.tags.all().values()),
        }
        return galleryinfo_dict


async def put_galleryinfo(galleryinfo: HitomiGalleryInfoModel):
    galleyinfo_orm_object = await GalleryInfo.create(
        language_localname=galleryinfo.language_localname,
        language=galleryinfo.language,
        date=galleryinfo.date,
        japanese_title=galleryinfo.japanese_title,
        title=galleryinfo.title,
        id=galleryinfo.galleryid,
        type=galleryinfo.hitomi_type,
    )

    if galleryinfo.files:
        file_orm_object_list = []
        for file_info in galleryinfo.files:
            file_orm_object = File(
                index_id=galleryinfo.galleryid,
                width=file_info.width,
                hash=file_info.hash,
                haswebp=file_info.haswebp,
                name=file_info.name,
                height=file_info.height,
            )
            await file_orm_object.save()
            file_orm_object_list.append(file_orm_object)
        await galleyinfo_orm_object.files.add(*file_orm_object_list)

    if galleryinfo.tags:
        tag_orm_object_list = []
        for tag_info in galleryinfo.tags:
            tag_orm_object = Tag(
                index_id=galleryinfo.galleryid,
                male=tag_info.get("male"),
                female=tag_info.get("female"),
                url=tag_info.get("url"),
            )
            await tag_orm_object.save()
            tag_orm_object_list.append(tag_orm_object)

        await galleyinfo_orm_object.tags.add(*tag_orm_object_list)


async def put_index(index: int):
    await Index.create(index_id=index)


async def get_index():
    return list(
        map(lambda x: int(x["index_id"]), await Index.all().values("index_id")),
    )


async def search_galleryinfo(query: str):
    if search_result_list := await GalleryInfo.filter(title__icontains=query):
        return [
            {
                **(await search_result.first().values())[0],
                "tags": remove_id_and_index_id(await search_result.tags.all().values()),
                "files": remove_id_and_index_id(
                    await search_result.files.all().values()
                ),
            }
            for search_result in search_result_list
        ]
