import asyncio


class DownloadQueue(asyncio.Queue):
    def __init__(self, index: int, maxsize: int = 0) -> None:
        super().__init__(maxsize)
        self.index = index
        self.completed = 0
        self._total = self.qsize()

    @property
    def total(self):
        return self._total

    async def make_queue(self, queue_list: list) -> None:
        for dl_queue in queue_list:
            await self.put(dl_queue)

    async def worker(self) -> None:
        download_task = await self.get()
        await download_task
        self.task_done()
        self.completed += 1

    async def start_download(self):
        return [self.worker() for _ in range(self.total)]
