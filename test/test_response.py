import os
from Heliotrope.app import app
import time

headers = {"Authorization": os.environ["Authorization"]}


def test_info_response():
    request, response = app.test_client.get("/api/hitomi/info/1496588", headers=headers)
    assert response.status == 200


def test_galleryindo_response():
    request, response = app.test_client.get(
        "/api/hitomi/galleryinfo/1496588", headers=headers
    )
    assert response.status == 200


def test_integrated_info_response():
    request, response = app.test_client.get(
        "/api/hitomi/integrated/1496588", headers=headers
    )
    assert response.status == 200


def test_list_response():
    request, response = app.test_client.get("/api/hitomi/list/1", headers=headers)
    assert response.status == 200


def test_download_response():
    request, response = app.test_client.post(
        "/api/download", headers=headers, json={"download": False, "index": 1}
    )
    assert (
        response.status == 200
        and response.json["status"] == "pending"
        and response.json["total"] == 2
    )


def test_download_response_already():
    time.sleep(10)
    request, response = app.test_client.post(
        "/api/download", headers=headers, json={"download": False, "index": 1}
    )
    assert (
        response.status == 200
        and response.json["status"] == "already"
        and response.json["total"] == 2
    )


def test_download_zip_response():
    request, response = app.test_client.post(
        "/api/download", headers=headers, json={"download": True, "index": 1}
    )
    assert (
        response.status == 200
        and response.json["status"] == "use_cached"
        and response.json["link"] == "https://doujinshiman.ga/download/1/1.zip"
    )


def test_download_zip_response_already():
    request, response = app.test_client.post(
        "/api/download", headers=headers, json={"download": True, "index": 1}
    )
    assert (
        response.status == 200
        and response.json["status"] == "already"
        and response.json["link"] == "https://doujinshiman.ga/download/1/1.zip"
    )