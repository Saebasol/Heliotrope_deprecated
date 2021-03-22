import pytest
from sanic_testing import TestManager

from heliotrope.server import heliotrope_app


@pytest.fixture
def app():
    TestManager(heliotrope_app)
    return heliotrope_app
