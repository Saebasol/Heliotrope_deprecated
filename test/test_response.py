import asyncio
import os

headers = {"Authorization": os.environ["Authorization"]}


async def test_info_response(test_cli):
    response = await test_cli.get("/api/hitomi/info/1496588", headers=headers)
    assert response.status == 200


async def test_galleryindo_response(test_cli):
    response = await test_cli.get("/api/hitomi/galleryinfo/1496588", headers=headers)
    assert response.status == 200


async def test_integrated_info_response(test_cli):
    response = await test_cli.get("/api/hitomi/integrated/1496588", headers=headers)
    assert response.status == 200


async def test_list_response(test_cli):
    response = await test_cli.get("/api/hitomi/list/1", headers=headers)
    assert response.status == 200


async def test_register_response(test_cli):
    response = await test_cli.post(
        "/api/register", headers=headers, json={"user_id": 123456789101112131}
    )
    assert response.status == 201


async def test_register_response_already(test_cli):
    response = await test_cli.post(
        "/api/register", headers=headers, json={"user_id": 123456789101112131}
    )
    assert response.status == 200


async def test_download_response(test_cli):
    response = await test_cli.post(
        "/api/download",
        headers=headers,
        json={"download": False, "index": 1, "user_id": 123456789101112131},
    )
    await asyncio.sleep(5)
    assert response.status == 200
    response_json = await response.json()
    assert response_json == {"status": "pending", "total": 2}


async def test_download_response_already(test_cli):
    response = await test_cli.post(
        "/api/download",
        headers=headers,
        json={"download": False, "index": 1, "user_id": 123456789101112131},
    )
    assert response.status == 200
    response_json = await response.json()
    assert response_json == {"status": "already", "total": 2}


async def test_download_zip_response(test_cli):
    response = await test_cli.post(
        "/api/download",
        headers=headers,
        json={"download": True, "index": 1, "user_id": 123456789101112131},
    )
    assert response.status == 200
    response_json = await response.json()
    assert response_json == {
        "status": "use_cached",
        "link": "https://doujinshiman.ga/download/1/1.zip",
    }


async def test_download_zip_response_already(test_cli):
    response = await test_cli.post(
        "/api/download",
        headers=headers,
        json={"download": True, "index": 1, "user_id": 123456789101112131},
    )
    assert response.status == 200
    response_json = await response.json()
    assert response_json == {
        "status": "already",
        "link": "https://doujinshiman.ga/download/1/1.zip",
    }


async def test_thumbnail_response(test_cli):
    info = await test_cli.get("/api/hitomi/info/1496588", headers=headers)
    assert info.status == 200
    info_json = await info.json()
    response = await test_cli.get(f"/proxy/{info_json['thumbnail']}")
    asyncio.sleep(3)
    assert response.status == 200
