import allure
import pytest
from api_clients.task_api import ClickUpClient
import requests
from tests.conftest import create_data, update_data, get_list_id_fixture, clickup_client
from utils.helpers import CLICKUP_API_KEY
import time


@allure.feature("Тестирование  API в ClickUp")
class TestApi(ClickUpClient):

    @allure.title("Создание и удаление задачи c использованием фикстур")
    @allure.description(
        "Создание новой задачи, проверка полей, удаление и проверка удаления"
    )
    def test_create_task(self, create_task_fixture, create_data):
        with allure.step("Create new task"):
            create_response = create_task_fixture
            assert create_response.status_code == 200, (f"Status code: {create_response.status_code}, "
                                                        f"responce: {create_response.text}")
            task_data = create_response.json()
            task_id = task_data['id']

        with allure.step("Проверка совпадения имени задачи"):
            assert task_data['name'] == create_data['name'], (
                f"Имя задачи не совпадает: ожидалось {create_data['name']}, "
                f"получено {task_data['name']}"
            )

        with allure.step("Проверка совпадания описания задачи"):
            assert task_data['description'] == create_data['description'], (
                f"Имя задачи не совпадает: ожидалось {task_data['name']}, "
                f"получено {task_data['name']}"
            )

        if 'status' in task_data:
            with allure.step("Проверка совпадаения статуса по задачи"):
                assert task_data['status']['status'] == create_data['status'], (
                    f"Статус задачи не совпадает: {task_data['status']['status']}"
                )

    @allure.description("Получение таски и проверка полей")
    def test_get_task(self, clickup_client, create_task_fixture):
        with allure.step("Получение созданной task"):
            response = create_task_fixture
            assert response.status_code == 200, (f"Status code: {response.status_code}, "
                                                 f"response: {response.text}")
            data_response = response.json()
            task_id = data_response['id']

            get_response = clickup_client.get_task(task_id)
            assert get_response.status_code == 200, (f"Status code: {get_response.status_code}, "
                                                     f"response: {get_response.text}")
            get_data = get_response.json()
            assert task_id == get_data['id']

        with allure.step("Проверка совпадения обязательных полей во вложенном словаре status"):
            assert isinstance(get_data['status'], dict), f"Другой тип данных: {type(get_data['status'])}"

            assert len(get_data['status']['id']) > 0, "Нет значения по ключу 'id' в dict['status']"
            assert isinstance(get_data['status']['id'], str), (f"Другой тип данных: "
                                                               f"{type(get_data['status']['id'])}")
            assert get_data['status']['id'] == data_response['status']['id'], (f"Другое значение по ключу 'id': "
                                                                               f"{get_data['status']['id']}")

            assert isinstance(get_data['status']['status'], str), (f"Другой тип данных: "
                                                                   f"{get_data['status']['status']}")
            assert len(get_data['status']['status']) > 0, "Нет значения по ключу 'status' в dict['status']"
            assert get_data['status']['status'] == data_response['status']['status'], (
                f"Value for key 'status': {get_data['status']['status']}")

            assert isinstance(get_data['status']['color'], str), (f"Другой тип данных: "
                                                                  f"{type(get_data['status']['color'])}")
            assert len(get_data['status']['color']) > 0, "Нет значения по ключу 'color' в dict['status']"
            assert get_data['status']['color'] == data_response['status']['color'], (
                f"Value for key 'color': {get_data['status']['color']}")

            assert isinstance(get_data['status']['orderindex'], int), (f"Другой тип данных: "
                                                                       f"{type(get_data['status']['orderindex'])}")
            assert get_data['status']['orderindex'] == 0, "Нет значения в dict['status']"

            assert isinstance(get_data['status']['type'], str), (f"Другой тип данных: "
                                                                 f"{type(get_data['status']['type'])}")
            assert len(get_data['status']['type']) > 0, "Нет значения по ключу 'type' в словаре dict['status']"

    @allure.description("Обновление таски и проверка полей")
    def test_update_task(self, clickup_client, create_task_fixture, update_data):
        with allure.step("Проверка обновления task"):
            response = create_task_fixture
            assert response.status_code == 200, (f"Status code: {response.status_code}, "
                                                 f"response: {response.text}")
            data_response = response.json()
            task_id = data_response['id']

            put_response = clickup_client.update_task(task_id, update_data)
            assert put_response.status_code == 200, (f"Status code: {response.status_code}, "
                                                     f"response: {response.text}")
            data_put = put_response.json()
            if task_id == data_put['id']:
                assert data_put['name'] == update_data['name'], f"Название задачи не обновилось: {data_put['name']}"
                assert data_put['description'] == update_data['description'], (f"Описание задачи не обновилось: "
                                                                               f"{data_put['description']}")
            assert data_put['status']['id'] == data_response['status']['id'], (f"Другое значение по ключу 'id': "
                                                                               f"{data_put['status']['id']}")

    @pytest.mark.parametrize("create_task_fixture_negative, expected_status", [
        ({"name": 58484, "description": "Valid description", "status": "to do"}, 400),
        ({"name": True, "description": "Error for key", "status": "to do"}, 400),
        ({"name": "Valid name", "description": "Valid description", "status": "Open"}, 400)
    ], indirect=["create_task_fixture_negative"])
    def test_create_task_invalid_params(self, create_task_fixture_negative, expected_status):
        with allure.step(f"Проверка создания такси при невалидных данных"):
            response = create_task_fixture_negative
            assert response.status_code == expected_status, (
                f"Ожидаемый код ответа: {expected_status}, "
                f"Получен статус код: {response.status_code}, "
                f"Ответ: {response.text}"
            )

    @allure.description("Попытка получения несуществующей таски")
    def test_get_task_invalid_task_id(self, create_task_fixture, clickup_client):
        with allure.step(f"Проверка получение такси при невалидных данных"):
            response = create_task_fixture
            assert response.status_code == 200, (f"Status code: {response.status_code}, "
                                                 f"response: {response.text}")
            data_response = response.json()
            task_id = data_response['id']

            if task_id in data_response:
                get_response = clickup_client.get_task("86c39m3u")
                assert get_response.status_code == 401, (f"Status code: {get_response.status_code}, "
                                                         f"response: {get_response.text}")
                get_data = get_response.json()
                assert 'err' in get_data, "Key 'err' not found in responce"
                assert get_data['err'] == "Team not authorized", f"Value 'err': {get_data['err']}"
                assert 'ECODE' in get_data, "Key 'ECODE' not found in responce"
                assert get_data['ECODE'] == "OAUTH_027", f"Value 'ECODE': {get_data['ECODE']}"

    @allure.description("Попытка обновления с некорректным task_id")
    def test_update_task_invalid_id(self, create_task_fixture, clickup_client, update_data):
        with allure.step("Добавление несуществующего task_id"):
            response = create_task_fixture
            assert response.status_code == 200, (f"Status code: {response.status_code}, "
                                                 f"response: {response.text}")
            data_response = response.json()
            task_id = data_response['id']

            if task_id in data_response:
                put_response = clickup_client.update_task("86c39m3_id", update_data)
                assert put_response.status_code == 401, (f"Status code: {put_response.status_code}, "
                                                         f"Responce: {put_response.text}")
                assert "Oauth token not found" in put_response.text, "Нет сообщения в ответе"

    @allure.description("Попытка обновления с невалидными данными")
    def test_update_task_invalid_data(self, create_task_fixture, clickup_client, invalid_update_data):
        with allure.step("Отправка невалидных данных"):
            response = create_task_fixture
            assert response.status_code == 200, (f"Status code: {response.status_code}, "
                                                 f"response: {response.text}")
            data_response = response.json()
            task_id = data_response['id']

            if task_id in data_response:
                put_response = clickup_client.update_task(task_id, invalid_update_data)
                assert put_response.status_code == 200, (f"Status code: {put_response.status_code}, "
                                                         f"Responce: {put_response.text}")
                data_put = put_response.json()
                assert "name" in data_put, f"Response: {data_put.text}"
                assert "description" in data_put, f"В ответе нет ключа 'description': {data_put.text}"

    @allure.description("Попытка удаления несуществующим task_id")
    def test_delete_invalid_task_id(self, clickup_client, create_task_fixture):
        with allure.step("Использование невалидного ID"):
            response = create_task_fixture
            assert response.status_code == 200, (f"Status code: {response.status_code}, "
                                                 f"response: {response.text}")

            data_response = response.json()
            task_id = data_response['id']

            if task_id in data_response:
                delete_response = clickup_client.delete_task("36wniw_id")
                assert delete_response.status_code == 401, (f"Status code: {delete_response.status_code}, "
                                                            f"Responce: {delete_response.text}")

                data_delete = data_response.json()
                assert "Team not authorized" in data_delete, f"Response: {data_delete.text}"

    # @pytest.fixture(scope='function')
    # def test_replace_get_on_post_task_(self, create_data):
    #     post_responce = requests.post(f"{self.BASE_URL}/api/v2/list/{self.LIST_ID}/task",
    #                                   json=create_data, headers=self.HEADERS_POST)
    #     assert post_responce.status_code == 200, (f"Status code: {post_responce.status_code}, "
    #                                               f"Responce: {post_responce.text}")
    #     post_data = post_responce.json()
    #     assert len(post_data['id']) > 0, "Not found new id"
    #     task_id = post_data['id']
    #
    #     get_responce = requests.post(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert get_responce.status_code == 404, (f"Status code: {get_responce.status_code}, "
    #                                              f"Responce: {get_responce.text}")
    #     assert "<pre>Cannot POST" in get_responce.text, "Error message not found responce"
    #
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 204, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
    # @pytest.fixture(scope='function')
    # def test_invalid_time_get_task_(self, create_data):
    #     TIMEOUT_GET = 1
    #
    #     post_responce = requests.post(f"{self.BASE_URL}/api/v2/list/{self.LIST_ID}/task",
    #                                   json=create_data, headers=self.HEADERS_POST)
    #     assert post_responce.status_code == 200, (f"Status code: {post_responce.status_code}, "
    #                                               f"Responce: {post_responce.text}")
    #     post_data = post_responce.json()
    #     assert len(post_data['id']) > 0, "Not found new id"
    #     task_id = post_data['id']
    #
    #     start_time = time.time()
    #     get_responce = requests.get(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     end_time = time.time()
    #
    #     responce_time = end_time - start_time
    #
    #     assert get_responce.status_code == 404, (f"Status code: {get_responce.status_code}, "
    #                                              f"Responce: {get_responce.text}")
    #     assert "<pre>Cannot POST" in get_responce.text, "Error message not found responce"
    #
    #     assert responce_time < TIMEOUT_GET, f"Get request crashed due to timeout: {responce_time: .2f} seconds"
    #
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 204, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
    # @pytest.fixture(scope='function')
    # def test_negative_update_data_task(self, create_data, invalid_update_data):
    #     post_responce = requests.post(f"{self.BASE_URL}/api/v2/list/{self.LIST_ID}/task",
    #                                   json=create_data, headers=self.HEADERS_POST)
    #     assert post_responce.status_code == 200, (f"Status code: {post_responce.status_code}, "
    #                                               f"Responce: {post_responce.text}")
    #
    #     post_data = post_responce.json()
    #     task_id = post_data['id']
    #
    #     put_responce = requests.put(f"{self.BASE_URL}/api/v2/task/{task_id}",
    #                                 headers=self.HEADERS_POST, json=invalid_update_data)
    #     assert put_responce.status_code == 400, (f"Status code: {put_responce.status_code}, "
    #                                              f"Responce: {put_responce.text}")
    #
    #     assert 'err' in post_data, "Key 'err' not found in responce"
    #     assert post_data['err'] == "Task name invalid", f"Value 'err': {post_data['err']}"
    #     assert 'ECODE' in post_data, "Key 'ECODE' not found in responce"
    #     assert post_data['ECODE'] == "INPUT_005", f"Value 'ECODE': {post_data['ECODE']}"
    #
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 204, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
    # @pytest.fixture(scope='function')
    # def test_invalid_headers_update_task(self, create_data, invalid_update_data):
    #     post_responce = requests.post(f"{self.BASE_URL}/api/v2/list/{self.LIST_ID}/task",
    #                                   json=create_data, headers=self.HEADERS_POST)
    #     assert post_responce.status_code == 200, (f"Status code: {post_responce.status_code}, "
    #                                               f"Responce: {post_responce.text}")
    #
    #     post_data = post_responce.json()
    #     task_id = post_data['id']
    #
    #     headers = {"Accept": "application/json",
    #                "Content-Type": "text/html",
    #                "Authorization": [CLICKUP_API_KEY]}
    #
    #     put_responce = requests.put(f"{self.BASE_URL}/api/v2/task/{task_id}",
    #                                 headers=headers, json=invalid_update_data)
    #     assert put_responce.status_code == 200, (f"Status code: {put_responce.status_code}, "
    #                                              f"Responce: {put_responce.text}")
    #
    #     put_data = put_responce.json()
    #     assert task_id == put_data['id'], f"Value key 'id': {put_data['id']}"
    #     assert put_data['name'] != invalid_update_data['name'], f"Value key 'name': {put_data['name']}"
    #
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 204, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
    # @pytest.fixture(scope='function')
    # def test_invalid_task_id_delete_task(self, create_data):
    #     post_responce = requests.post(f"{self.BASE_URL}/api/v2/list/{self.LIST_ID}/task",
    #                                   json=create_data, headers=self.HEADERS_POST)
    #     assert post_responce.status_code == 200, (f"Status code: {post_responce.status_code}, "
    #                                               f"Responce: {post_responce.text}")
    #     post_data = post_responce.json()
    #     task_id = post_data['id']
    #
    #     invalid_task_id = "86c35"
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{invalid_task_id}", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 401, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
    #     get_responce = requests.get(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert get_responce.status_code == 200, (f"Status code: {get_responce.status_code}, "
    #                                              f"Responce: {get_responce.text}")
    #     get_data = get_responce.json()
    #     assert get_data['id'] == task_id, f"Value for key 'id': {get_data['id']}"
    #     assert get_data['name'] == post_data['name'], f"Value for key 'name': {get_data['name']}"
    #
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 204, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
    #     get_responce = requests.get(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert get_responce.status_code == 404, (f"Status code: {delete_responce.status_code}, "
    #                                              f"Responce: {delete_responce.text}")
    #
    # @pytest.fixture(scope='function')
    # def test_invalid_url_delete_task(self, create_data):
    #     post_responce = requests.post(f"{self.BASE_URL}/api/v2/list/{self.LIST_ID}/task",
    #                                   json=create_data, headers=self.HEADERS_POST)
    #     assert post_responce.status_code == 200, (f"Status code: {post_responce.status_code}, "
    #                                               f"Responce: {post_responce.text}")
    #     post_data = post_responce.json()
    #     task_id = post_data['id']
    #
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{task_id}/team", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 404, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
    #     assert "<pre>Cannot DELETE" in delete_responce.text, "Error message not found responce"
    #
    #     get_responce = requests.get(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert get_responce.status_code == 200, (f"Status code: {get_responce.status_code}, "
    #                                              f"Responce: {get_responce.text}")
    #     get_data = get_responce.json()
    #     assert get_data['id'] == task_id, f"Value for key 'id': {get_data['id']}"
    #     assert get_data['name'] == post_data['name'], f"Value for key 'name': {get_data['name']}"
    #
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 204, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
    #     get_responce = requests.get(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert get_responce.status_code == 404, (f"Status code: {delete_responce.status_code}, "
    #                                              f"Responce: {delete_responce.text}")
