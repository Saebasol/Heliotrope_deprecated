from sanic import Blueprint, response
from sanic.response import json

from Heliotrope.utils.checker.check import authorized
from Heliotrope.utils.downloader.task_progress import TaskProgress

progress = Blueprint("download_progress", url_prefix="/progress")
task_progress = TaskProgress()


@progress.route(
    "/<user_id>",
    methods=["GET"],
)
@authorized()
async def image_progress(request, user_id: str):
    info_list = []
    if await task_progress.cache.exists(user_id):
        task_list = await task_progress.cache.get(user_id)
        task_info = [
            {
                "index": task_dict["task_name"],
                "count": task_dict["count"],
                "task_status": "completed" if task_dict["task"].done() else "pending",
                "link": f"https://doujinshiman.ga/download/{task_dict['task_name']}/{task_dict['task_name']}.zip"
                if task_dict["task"].done()
                else None,
            }
            for task_dict in task_list
        ]
        info_list.extend(task_info)

    if await task_progress.cache.exists(f"{user_id}_already"):
        already_info = await task_progress.cache.get(f"{user_id}_already")
        info_list.extend(already_info)

    if info_list:
        return json({"code": 200, "info": info_list})
    else:
        return json({"code": 404, "status": "not_found"})