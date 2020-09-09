import os
from Heliotrope.app import app

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