import os
from Heliotrope.app import app

headers = {"Authorization": os.environ["Authorization"]}


def test_info_unexpected_response():
    request, response = app.test_client.get(
        "/api/hitomi/info/1111111111111111", headers=headers
    )
    assert response.status == 404


def test_galleryindo_unexpected_response():
    request, response = app.test_client.get(
        "/api/hitomi/galleryinfo/1111111111111111", headers=headers
    )
    assert response.status == 404


def test_list_unexpected_response():
    request, response = app.test_client.get(
        "/api/hitomi/list/1111111111111111", headers=headers
    )
    assert response.status == 404
