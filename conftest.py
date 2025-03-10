import pytest

from src.database import DataBase


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="local", help="Environment to run test against (local, docker)")


@pytest.fixture(scope='module')
def database(request):
    env = request.config.getoption("--env")
    return DataBase(env=env)
