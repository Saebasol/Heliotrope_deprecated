import asyncio
import aioschedule

from Heliotrope.utils.database import User


async def reset_download_count():
    return await User.all().update(download_count=0)


async def reset_scheduler():
    aioschedule.every().day.at("00:00").do(reset_download_count())
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60)