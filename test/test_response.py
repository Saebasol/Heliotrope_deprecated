from Heliotrope.app import app


def test_info_response():
    request, response = app.test_client.get("/api/hitomi/info/1496588")
    assert response.status == 200


def test_galleryindo_response():
    request, response = app.test_client.get("/api/hitomi/galleryinfo/1496588")
    assert response.status == 200


def test_integrated_info_response():
    request, response = app.test_client.get("/api/hitomi/integrated/1496588")
    assert response.status == 200


def test_list_response():
    request, response = app.test_client.get("/api/hitomi/list/1")
    assert response.status == 200