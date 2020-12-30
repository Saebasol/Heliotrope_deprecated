async def test_info_unexpected_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/info/1111111111111111")
    assert response.status == 404


async def test_galleryindo_unexpected_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/galleryinfo/1111111111111111")
    assert response.status == 404


async def test_list_unexpected_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/list/1111111111111111")
    assert response.status == 404


async def test_images_unexpected_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/images/1111111111111111")
    assert response.status == 200


async def test_integrated_unexpected_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/integrated/1111111111111111")
    assert response.status == 200


async def test_proxy_unexpected_response(test_cli):
    response = await test_cli.get("/v3/api/proxy/this_is_test")
    assert response.status == 404
