import pytest
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
def update_data():
    with allure.step("Генерация данных для созданной task"):
        return {
            "name": faker.word().capitalize(),
            "description": faker.sentence(nb_words=5)
        }


@pytest.fixture()
def invalid_data():
    """Генерация данных для созданной task"""
    return {
        "name": 54503,
    }


@pytest.fixture()
def create_task_fixture(clickup_client, get_list_id_fixture, create_data):
    list_id = get_list_id_fixture
    response = clickup_client.create_task(list_id, create_data)

    if response is None:
        raise ValueError("Ответ равен None, проверить API client")

    data_response = response.json()
    task_id = data_response['id']
    yield response

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
def create_task_fixture_negative(clickup_client, get_list_id_fixture, request):
    list_id = get_list_id_fixture
    data = request.param
    response = clickup_client.create_task(list_id, data)

    if response is None:
        raise ValueError("Ответ равен None, проверить API client")

    yield response

    if response.status_code == 200:
        data_response = response.json()
        task_id = data_response['id']
        delete_response = clickup_client.delete_task(task_id)
        assert delete_response.status_code == 204, (f"Status code: {delete_response.status_code}, "
                                                    f"Response: {delete_response.text}")

        get_response = clickup_client.get_task(task_id)
        assert get_response.status_code == 404, (f"Status code: {get_response.status_code}, "
                                                 f"Response: {get_response.text}")



@pytest.fixture()
def create_negative_data():
    """Генерация c некорректным типом данных для создание новой task"""
    return {
        "name": 32023,
        "description": faker.sentence(nb_words=5)
    }
