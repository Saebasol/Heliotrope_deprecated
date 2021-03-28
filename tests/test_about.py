def test_get_count_html_response(app):
    _, response = app.test_client.get("/about")
    assert response.status == 200
    assert "text/html" in response.content_type


def test_get_count_json_response(app):
    for param in ["True", "true"]:
        _, response = app.test_client.get("/v4/api/count", params={"json": param})
        assert response.status == 200
        assert "application/json" in response.content_type
