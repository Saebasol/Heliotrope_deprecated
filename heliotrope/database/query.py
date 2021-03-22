from heliotrope.database.models.hitomi import GalleryInfo
from heliotrope.database.models.requestcount import RequestCount


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
    def remove_id_and_index_id(tag_or_file_list):
        response_dict_list = []
        for value in tag_or_file_list:
            del value["id"]
            del value["index_id"]
            response_dict_list.append(value)
        return response_dict_list

    if galleryinfo := await GalleryInfo.get_or_none(id=index):
        galleryinfo = {
            "id": galleryinfo.id,
            "language_localname": galleryinfo.language_localname,
            "date": galleryinfo.date,
            "files": remove_id_and_index_id(await galleryinfo.files.all().values()),
            "tags": remove_id_and_index_id(await galleryinfo.tags.all().values()),
            "japanese_title": galleryinfo.japanese_title,
            "title": galleryinfo.title,
            "type": galleryinfo.type,
        }
        return galleryinfo
