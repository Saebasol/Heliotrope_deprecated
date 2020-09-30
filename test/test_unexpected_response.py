import os

headers = {"Authorization": os.environ["Authorization"]}


async def test_info_unexpected_response(test_cli):
    response = await test_cli.get(
        "/v1/api/hitomi/info/1111111111111111", headers=headers
    )
    assert response.status == 404


async def test_galleryindo_unexpected_response(test_cli):
    response = await test_cli.get(
        "/v1/api/hitomi/galleryinfo/1111111111111111", headers=headers
    )
    assert response.status == 404


async def test_list_unexpected_response(test_cli):
    response = await test_cli.get(
        "/v1/api/hitomi/list/1111111111111111", headers=headers
    )
    assert response.status == 404


async def test_thumbnail_unexpected_response(test_cli):
    response = await test_cli.get("/v1/api/proxy/balbalblabla")
    assert response.status == 404
