import asyncio

from Heliotrope.utils.downloader.download import downloader, download_compression


class DownloadQueue(asyncio.Queue):
    def __init__(self, queue_list: list, index: int, maxsize: int = 0) -> None:
        super().__init__(maxsize)
        self.queue_list = queue_list
        self.index = index
        self.completed = 0
        self.total = self.qsize()

    async def make_queue(self) -> None:
        for dl_queue in self.queue_list:
            await self.put(
                downloader(self.index, dl_queue["url"], dl_queue["filename"])
            )

    async def worker(self) -> None:
        download_task = await self.get()
        await download_task
        self.task_done()
        self.completed += 1

    async def start_download(self, compression: bool = False):
        if compression:
            return asyncio.create_task(
                download_compression(self.queue_list, self.index)
            )
        else:
            for _ in self.total:
                await self.worker()
