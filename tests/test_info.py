def test_get_info_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/info/1496588")
    assert response.status == 200


def test_get_info_unexpected_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/info/0")
    assert response.status == 404
