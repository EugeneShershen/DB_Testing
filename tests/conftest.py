import pytest
import json

from pathlib import Path
from src.database import DataBase


@pytest.fixture(scope='module')
def database(request):
    env = request.config.getoption("--env")
    return DataBase(env=env)


@pytest.fixture(scope='module')
def prepare_test_data_cud(request):
    filepath = Path(__file__).parent.parent / "data/tests_data_CUD.json"
    number, table = request.param

    with open(filepath, 'r') as file:
        data = json.load(file)

    if table == 'course':
        return data['courses'][str(number)]

    elif table == 'student':
        return data['students'][str(number)]


@pytest.fixture(scope='module')
def prepare_test_data_search(request):
    filepath = Path(__file__).parent.parent / "data/tests_data_search.json"
    number, table = request.param

    with open(filepath, 'r') as file:
        data = json.load(file)

    if table == 'course':
        return data['courses'][str(number)]

    elif table == 'student':
        res = data['students'][str(number)]
        res['student_info'] = [tuple(student) for student in res['student_info']]
        return res
