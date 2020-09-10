import pytest

from Heliotrope.app import app as main_app


@pytest.yield_fixture
def app():
    app = main_app
    yield app


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))
