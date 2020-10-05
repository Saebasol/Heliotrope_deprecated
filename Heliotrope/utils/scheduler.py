import asyncio

import aioschedule

from Heliotrope.utils.database import User


async def job():
    await User.all().update(download_count=0)


async def reset_scheduler():
    aioschedule.every().day.at("00:00").do(job_func=job)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60)
