from heliotrope.database.models.requestcount import RequestCount


async def get_all_request_count():
    rank_list = await RequestCount.all().values("index", "count")
    sorted_ranking = sorted(rank_list, key=lambda info: info["count"], reverse=True)
    ranking = {
        "total": len(sorted_ranking),
        "list": sorted_ranking,
    }
    return ranking


async def add_request_count(index):
    if index_data := await RequestCount.get_or_none(index=index):
        index_data.count += 1
        await index_data.save()
    else:
        index_data = await RequestCount.create(index=index, count=1)
        await index_data.save()
