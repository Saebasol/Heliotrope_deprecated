import pytest

from sanic_testing import TestManager
from heliotrope.server import heliotrope


@pytest.fixture
def app():
    TestManager(heliotrope)
    return heliotrope