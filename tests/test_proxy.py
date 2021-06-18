def test_get_proxy_hitomi_response(app):
    _, response = app.test_client.get(
        "/v4/api/proxy/tn_smallbigtn_hitomi_la_5_6c_0d2ee87048646232b205bdf1da11240542178c0c58473beb40461aa51d6ee6c5.jpg"
    )
    assert response.status == 200


def test_get_proxy_pixiv_response(app):
    _, response = app.test_client.get(
        "/v4/api/proxy/i_img-original_pximg_net_img_2020_01_28_01_07_34_79136250_p0.jpg"
    )
    assert response.status == 200


def test_get_proxy_bad_request_response(app):
    _, response = app.test_client.get("/v4/api/proxy/test")
    assert response.status == 400
