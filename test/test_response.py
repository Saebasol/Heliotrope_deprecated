import asyncio
import os


async def test_info_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/info/1496588")
    assert response.status == 200


async def test_galleryindo_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/galleryinfo/1496588")
    assert response.status == 200


async def test_integrated_info_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/integrated/1496588")
    assert response.status == 200


async def test_list_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/list/1")
    assert response.status == 200


async def test_index_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/index")
    assert response.status == 200
