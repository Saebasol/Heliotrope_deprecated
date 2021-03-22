def test_get_count_unexpected_response(app):
    _, response = app.test_client.get("/v4/api/count")
    assert response.status == 404


def test_post_count_response(app):
    _, response = app.test_client.post("/v4/api/count", json={"index": 1496588})
    assert response.status == 200


def test_get_count_response(app):
    _, response = app.test_client.get("/v4/api/count")
    assert response.status == 200


def test_post_count_unexpected_response(app):
    _, response = app.test_client.post("/v4/api/count", json={"index": 0})
    assert response.status == 400
