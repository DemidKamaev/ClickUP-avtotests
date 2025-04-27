import pytest
import requests
import allure
from config import BASE_URL
from api_clients.task_api import ClickUpClient
from utils.helpers import CLICKUP_API_KEY
from faker import Faker


faker = Faker()


@pytest.fixture(scope="session")
def clickup_client():
    return ClickUpClient(
        base_url=BASE_URL,
        api_token=CLICKUP_API_KEY
    )


@pytest.fixture()
def get_list_id_fixture(clickup_client):
    return clickup_client.get_list_id


@pytest.fixture()
def create_data():
    with allure.step("Генерация валидных данных для создание новой task"):
        return {
            "name": faker.word(),
            "description": faker.word(),
            "status": "in progress"
        }


@pytest.fixture()
def create_task_fixture(clickup_client, get_list_id_fixture, create_data):
    yield
    list_id = get_list_id_fixture
    response = clickup_client.create_task(list_id, create_data)

    if response is None:
        raise ValueError("Ответ равен None, проверить API client")

    data_response = response.json()
    task_id = data_response['id']

    delete_response = clickup_client.delete_task(task_id)
    assert delete_response.status_code == 204, (f"Status code: {delete_response.status_code}, "
                                                f"Response: {delete_response.text}")

    get_response = clickup_client.get_task(task_id)
    assert get_response.status_code == 404, (f"Status code: {get_response.status_code}, "
                                             f"Response: {get_response.text}")
    get_data = get_response.json()
    assert 'err' in get_data, "Key 'err' not found in response"
    assert get_data['err'] == "Task not found, deleted", f"Value 'err': {get_data['err']}"
    assert 'ECODE' in get_data, "Key 'ECODE' not found in response"
    assert get_data['ECODE'] == "ITEM_013", f"Value 'ECODE': {get_data['ECODE']}"


@pytest.fixture()
def update_data():
    """Генерация данных для созданной task"""
    return {
        "name": faker.word().capitalize(),
        "description": faker.sentence(nb_words=5)
    }


@pytest.fixture()
def create_negative_data():
    """Генерация c некорректным типом данных для создание новой task"""
    return {
        "name": 32023,
        "description": faker.sentence(nb_words=5)
    }


@pytest.fixture()
def invalid_update_data():
    """Генерация данных для созданной task"""
    return {
        "name": 54503,
    }


# @pytest.fixture(scope="session")
# def get_team_id():
#     """Матрешка для получения list_id"""
#     get_responce = requests.get(BaseApi.BASE_URL_GET_TEAM_ID, headers=BaseApi.HEADERS)
#     assert get_responce.status_code == 200, (f"Status code: {get_responce.status_code}, "
#                                              f"Responce: {get_responce.text}")
#
#     team_data = get_responce.json()
#
#     if isinstance(team_data['teams'], list) and len(team_data['teams']) > 0:
#         team_id = team_data['teams'][0]['id']
#     else:
#         raise ValueError("No teams found in the responce")
#
#     return team_id
#
#
# def get_space_id(get_team_id):
#     team_id = get_team_id
#
#     URL = f"https://api.clickup.com/v2/team/{team_id}/space"
#     get_responce = requests.get(URL, headers=BaseApi.HEADERS)
#     assert get_responce.status_code == 200, (f"Status code: {get_responce.status_code}, "
#                                              f"Responce: {get_responce.text}")
#
#     space_data = get_responce.json()
#
#     if isinstance(space_data['spaces'], list) and len(space_data) > 0:
#         space_id = space_data['spaces'][0]['id']
#     else:
#         raise ValueError("No spaces found in the responce")
#
#     return space_id