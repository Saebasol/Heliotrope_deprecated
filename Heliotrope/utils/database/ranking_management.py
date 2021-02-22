from sanic.response import json

from Heliotrope.utils.database import Ranking


async def add_count(index, check=False):
    index_data = await Ranking.get_or_none(index=index)
    if check:
        if index_data:
            index_data.count += 1
            await index_data.save()
            return json({"status": 200, "message": "successfully"}, 200)
        else:
            ranking = await Ranking.create(index=index, count=1)
            await ranking.save()
            return json({"status": 201, "message": "successfully"}, 201)
    else:
        return json({"status": 400, "message": "bad_request"}, 400)


async def view_ranking(check=False):
    if check:
        rank_list = await Ranking.all().values('index', 'count')
        sorted_ranking = sorted(rank_list, key=lambda info: info['count'], reverse=True)
        ranking = {"count": len(sorted_ranking) - 1, "list": sorted_ranking}
        return json(ranking, 200)
    else:
        return json({"status": 400, "message": "bad_request"}, 400)
