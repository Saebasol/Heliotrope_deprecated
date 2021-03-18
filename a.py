import asyncio
from asyncio.locks import Semaphore

from aiohttp.client import ClientSession

from heliotrope.utils.requester import HitomiRequester, RestrictedRequester


async def main():

    sem = Semaphore()
    hitomi_session = ClientSession()

    request = RestrictedRequester(sem)
    print(request.semaphore)
    print(request.session)

    hitomi_requester = HitomiRequester(hitomi_session)

    print(request.semaphore)
    print(request.session)
    print("=========")
    print(hitomi_requester.semaphore)
    print(hitomi_requester.session)


asyncio.run(main())
