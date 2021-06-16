def test_get_proxy_hitomi_response(app):
    _, response = app.test_client.get(
        "/v4/api/proxy/bb_images_hitomi_la_5_58_68d18296183259e5f53047be3196e2fe0c2bc55f4c57b929e9ec129f40d5b585.jpg"
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
