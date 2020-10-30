import asyncio
import os

headers = {"Authorization": os.environ["Authorization"]}


async def test_info_response(test_cli):
    response = await test_cli.get("/v2/api/hitomi/info/1496588", headers=headers)
    assert response.status == 200


async def test_galleryindo_response(test_cli):
    response = await test_cli.get("/v2/api/hitomi/galleryinfo/1496588", headers=headers)
    assert response.status == 200


async def test_integrated_info_response(test_cli):
    response = await test_cli.get("/v2/api/hitomi/integrated/1496588", headers=headers)
    assert response.status == 200


async def test_list_response(test_cli):
    response = await test_cli.get("/v2/api/hitomi/list/1", headers=headers)
    assert response.status == 200


async def test_index_response(test_cli):
    response = await test_cli.get("/v2/api/hitomi/index", headers=headers)
    assert response.status == 200


async def test_register_response(test_cli):
    response = await test_cli.post(
        "/v2/api/register",
        headers=headers,
        json={"user_id": 123456789101112131, "check": False},
    )
    assert response.status == 201


async def test_register_response_already(test_cli):
    response = await test_cli.post(
        "/v2/api/register",
        headers=headers,
        json={"user_id": 123456789101112131, "check": True},
    )
    assert response.status == 200


async def test_download_response(test_cli):
    response = await test_cli.post(
        "/v2/api/download",
        headers=headers,
        json={"download": False, "index": 1496588, "user_id": 123456789101112131},
    )
    await asyncio.sleep(5)
    assert response.status == 200
    response_json = await response.json()
    assert response_json == {"status": 200, "message": "pending", "total": 207}


async def test_download_response_already(test_cli):
    response = await test_cli.post(
        "/v2/api/download",
        headers=headers,
        json={"download": False, "index": 1496588, "user_id": 123456789101112131},
    )
    assert response.status == 200
    response_json = await response.json()
    assert response_json == {"status": 200, "message": "already", "total": 207}


async def test_download_zip_response(test_cli):
    response = await test_cli.post(
        "/v2/api/download",
        headers=headers,
        json={"download": True, "index": 1496588, "user_id": 123456789101112131},
    )
    assert response.status == 200
    response_json = await response.json()
    assert response_json == {"status": 200, "message": "use_cached"}


async def test_download_zip_response_already(test_cli):
    response = await test_cli.post(
        "/v2/api/download",
        headers=headers,
        json={"download": True, "index": 1496588, "user_id": 123456789101112131},
    )
    assert response.status == 200
    response_json = await response.json()
    assert response_json == {"status": 200, "message": "already"}


async def test_progress_response(test_cli):
    response = await test_cli.get(
        "/v2/api/progress/123456789101112131",
        headers=headers,
    )
    assert response.status == 200
    response_json = await response.json()
    assert response_json == {
        "status": 200,
        "info": [
            {
                "index": 1496588,
                "count": 4,
                "task_status": "use_cached",
                "link": "https://doujinshiman.ga/download/1/1.zip",
            },
            {
                "index": 1496588,
                "count": 3,
                "task_status": "already",
                "link": "https://doujinshiman.ga/download/1/1.zip",
            },
        ],
    }


async def test_thumbnail_response(test_cli):
    info = await test_cli.get("/v2/api/hitomi/info/1496588", headers=headers)
    assert info.status == 200
    info_json = await info.json()
    response = await test_cli.get(f"/v2/api/proxy/{info_json['thumbnail']}")
    asyncio.sleep(3)
    assert response.status == 200
