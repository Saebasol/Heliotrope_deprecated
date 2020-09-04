from Heliotrope.app import app

def test_index_unexpected_response():
    request, response = app.test_client.get("/api/hitomi/1111111111111111")
    assert response.status == 404

def test_galleryindo_unexpected_response():
    request, response = app.test_client.get("/api/hitomi/galleryinfo/1111111111111111")
    assert response.status == 404

def test_list_unexpected_response():
    request, response = app.test_client.get("/api/hitomi/list/1111111111111111")
    assert response.status == 404