async def test_info_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/info/1496588")
    assert response.status == 200


async def test_galleryindo_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/galleryinfo/1496588")
    assert response.status == 200


async def test_integrated_info_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/integrated/1496588")
    assert response.status == 200


async def test_list_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/list/1")
    assert response.status == 200


async def test_index_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/index")
    assert response.status == 200


async def test_images_response(test_cli):
    response = await test_cli.get("/v3/api/hitomi/images/1496588")
    assert response.status == 200


async def test_proxy_reponse(test_cli):
    response = await test_cli.get(
        "/v3/api/proxy/bb_images_hitomi_la_3_b2_7c731d3025aecf74205b1b188c36d65c124ca5bc0a2e81edcf28125aa9df5b23.png"
    )
    assert response.status == 200
