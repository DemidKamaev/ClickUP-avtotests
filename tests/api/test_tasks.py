import allure
import pytest
from api_clients.task_api import ClickUpClient
import requests
from tests.conftest import create_data, update_data, get_list_id_fixture, clickup_client
from utils.helpers import CLICKUP_API_KEY
import time


@allure.feature("Тестирование  API в ClickUp")
class TestApi:

    @allure.title("Создание и удаление задачи c использованием фикстур")
    @allure.description(
        "Create task, check fields task, Delete task, check delete task"
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

        with allure.step("Проверка совпадаения описания задачи"):
            assert task_data['description'] == create_data['description'], (
                f"Имя задачи не совпадает: ожидалось {task_data['name']}, "
                f"получено {task_data['name']}"
            )

        return task_id

    # @pytest.fixture(scope='function')
    # def test_task(self, create_data, get_list_id):
    #     list_id = get_list_id
    #
    #     item_response = requests.post(f"{self.BASE_URL}/api/v2/list/{list_id}/task",
    #                                   json=create_data, headers=self.HEADERS_POST)
    #     assert item_response.status_code == 200, (f"Status code: {item_response.status_code}, "
    #                                               f"responce: {item_response.text}")
    #     item_data = item_response.json()
    #     assert item_data['name'] == create_data['name'], f"not found is name: {create_data['name']}"
    #     assert item_data['description'] == create_data['description'], (f"not found is description: "
    #                                                                     f"{create_data['description']}")
    #
    #     assert len(item_data['id']) > 0, "No value entry for key id"
    #     assert isinstance(item_data['id'], str), f"Object not found or object not type str: {item_data['id']}"
    #
    #     assert isinstance(item_data['status'], dict), f"Object not found or object not type dict: {item_data['status']}"
    #     assert len(item_data['status']['id']) > 0, "No value entry for key id in dict['status']"
    #     assert isinstance(item_data['status']['id'], str), (f"Object not found or object not type str: "
    #                                                         f"{item_data['status']['id']}")
    #
    #     assert isinstance(item_data['status']['status'], str), (f"Object not found or object not type str: "
    #                                                             f"{item_data['status']['status']}")
    #     assert len(item_data['status']['status']) > 0, "No value entry for key status in dict['status']"
    #
    #     assert isinstance(item_data['status']['color'], str), (f"Object not found or object not type str: "
    #                                                            f"{item_data['status']['color']}")
    #     assert len(item_data['status']['color']) > 0, "No value entry for key color in dict['status']"
    #
    #     assert isinstance(item_data['status']['orderindex'], int), (f"Object not found or object not type int: "
    #                                                                 f"{item_data['status']['orderindex']}")
    #     assert item_data['status']['orderindex'] == 0, "No value entry for key orderindex in dict['status']"
    #
    #     assert isinstance(item_data['status']['type'], str), (f"Object not found or object not type str: "
    #                                                           f"{item_data['status']['type']}")
    #     assert len(item_data['status']['type']) > 0, "No value entry for key type in dict['status']"
    #
    #     assert 'creator' in item_data, "Key 'creator' not found in dict"
    #     assert isinstance(item_data['creator'], dict), (f"Object not found or object not type dict:"
    #                                                     f"{item_data['creator']}")
    #
    #     assert isinstance(item_data['creator']['id'], int), (f"Object not found or object not type int: "
    #                                                          f"{item_data['creator']['id']}")
    #
    #     assert isinstance(item_data['creator']['username'], str), (f"Object not found or object not type dict: "
    #                                                                f"{item_data['creator']['username']}")
    #     assert len(item_data['creator']['username']) > 0, "No value entry for key username in dict['creator']"
    #
    #     assert isinstance(item_data['creator']['color'], str), (f"Object not found or object not type dict: "
    #                                                             f"{item_data['creator']['color']}")
    #     assert item_data['creator']['color'] == "", "No value entry for key color in dict['creator']"
    #
    #     # Пакет с email не устанавливается
    #     # assert isinstance(item_data['creator']['email'], email), (f"Object not found or object not type dict: "
    #     #                                                           f"{item_data['creator']['email']}")
    #     # assert len(item_data['creator']['email']) > 0, "No value entry for key email in dict['creator']"
    #
    #     profile_picture = item_data['creator']['profilePicture']
    #     assert isinstance(profile_picture, str) or profile_picture is None, \
    #         (f"Если profilePicture не строка и не равен None, поднимется исключение: "
    #          f"{item_data['creator']['profilePicture']}")
    #     # assert item_data['creator']['profilePicture'] is , "No value entry for key profilePicture in dict"
    #     # task_id = item_data['id']
    #     assert isinstance(item_data['list'], dict), f"type 'list': {type(item_data['list'])}"
    #     assert isinstance(item_data['list']['id'], str), f"type 'id': {type(item_data['list']['id'])}"
    #     assert len(item_data['list']['id']) > 0, f"value key 'id' not found: {item_data['list']['id']}"
    #
    #     assert isinstance(item_data['folder'], dict), f"type 'folder': {type(item_data['folder'])}"
    #     assert isinstance(item_data['folder']['id'], str), f"type 'id': {type(item_data['folder']['id'])}"
    #     assert len(item_data['folder']['id']) > 0, f"value key 'id' not found: {item_data['folder']['id']}"
    #
    #     assert isinstance(item_data['space'], dict), f"type 'space': {type(item_data['space'])}"
    #     assert isinstance(item_data['space']['id'], str), f"type 'id': {type(item_data['space']['id'])}"
    #     assert len(item_data['space']['id']) > 0, f"value key 'id' not found: {item_data['space']['id']}"
    #
    # @pytest.fixture(scope='function')
    # def test_get_task(self, test_create_task, create_data):
    #     self.item_data = test_create_task
    #     task_id = self.item_data['id']
    #
    #     item_response = requests.get(f"{self.BASE_URL}/api/v2/task/{task_id}",
    #                                  headers=self.HEADERS_GET)
    #     assert item_response.status_code == 200, (f"Status code: {item_response.status_code}, "
    #                                               f"Responce: {item_response.text}")
    #     get_data = item_response.json()
    #     assert task_id == get_data['id'], f"Value for key id: {get_data['id']}"
    #     assert len(get_data['id']) > 0, "No value entry for key id"
    #     assert isinstance(get_data['id'], str), f"Object not found or object not type str: {get_data['id']}"
    #
    #     assert get_data['name'] == self.item_data['name'], f"Value for key name: {get_data['name']}"
    #     assert get_data['description'] == self.item_data['description'], (f"Value for key 'description': "
    #                                                                       f"{get_data['description']}")
    #
    #     assert isinstance(get_data['status'], dict), (f"Object not found or object not type dict: "
    #                                                   f"{type(get_data['status'])}")
    #
    #     assert len(get_data['status']['id']) > 0, "No value entry for key id in dict['status']"
    #     assert isinstance(get_data['status']['id'], str), (f"Object not found or object not type str: "
    #                                                        f"{get_data['status']['id']}")
    #     assert get_data['status']['id'] == self.item_data['status']['id'], (f"Value for key 'id': "
    #                                                                         f"{type(get_data['status']['id'])}")
    #
    #     assert isinstance(get_data['status']['status'], str), (f"Object not found or object not type str: "
    #                                                            f"{get_data['status']['status']}")
    #     assert len(get_data['status']['status']) > 0, "No value entry for key status in dict['status']"
    #     assert get_data['status']['status'] == self.item_data['status']['status'], (f"Value for key 'status': "
    #                                                                                 f"{get_data['status']['status']}")
    #     assert isinstance(get_data['status']['color'], str), (f"Object not found or object not type str: "
    #                                                           f"{type(get_data['status']['color'])}")
    #     assert len(get_data['status']['color']) > 0, "No value entry for key color in dict['status']"
    #     assert get_data['status']['color'] == self.item_data['status']['color'], (f"Value for key 'color': "
    #                                                                               f"{get_data['status']['color']}")
    #
    #     assert isinstance(get_data['status']['orderindex'], int), (f"Object not found or object not type int: "
    #                                                                f"{type(get_data['status']['orderindex'])}")
    #     assert get_data['status']['orderindex'] == 0, "No value entry for key orderindex in dict['status']"
    #     assert get_data['status']['orderindex'] == self.item_data['status']['orderindex'], \
    #         f"Value for key 'color': {get_data['status']['orderindex']}"
    #
    #     assert isinstance(get_data['status']['type'], str), (f"Object not found or object not type str: "
    #                                                          f"{type(get_data['status']['type'])}")
    #     assert len(get_data['status']['type']) > 0, "No value entry for key type in dict['status']"
    #     assert get_data['status']['type'] == self.item_data['status']['type'], (f"Value for key 'color': "
    #                                                                             f"{get_data['status']['type']}")
    #
    #     assert 'creator' in get_data, "Key 'creator' not found in dict"
    #     assert get_data['creator']['id'] == self.item_data['creator']['id'], f"Value id: {get_data['creator']['id']}"
    #     assert get_data['creator']['username'] == self.item_data['creator']['username'], \
    #         f"Value username: {get_data['creator']['username']}"
    #     assert get_data['creator']['color'] == self.item_data['creator']['color'], \
    #         f"Value color: {get_data['creator']['color']}"
    #     assert get_data['creator']['profilePicture'] == self.item_data['creator']['profilePicture'], \
    #         f"Value profilePicture: {get_data['creator']['profilePicture']}"
    #
    #     assert isinstance(get_data['list'], dict), f"type 'list': {type(get_data['list'])}"
    #     assert get_data['list']['id'] == self.item_data['list']['id'], f"value for key 'id': {get_data['list']['id']}"
    #
    #     assert isinstance(get_data['folder'], dict), f"type 'folder': {type(get_data['folder'])}"
    #     assert get_data['folder']['id'] == self.item_data['folder']['id'], \
    #         f"value for key 'id': {get_data['folder']['id']}"
    #
    #     assert isinstance(get_data['space'], dict), f"type 'space': {type(get_data['space'])}"
    #     assert get_data['space']['id'] == self.item_data['space']['id'], (f"value for key 'id': "
    #                                                                       f"{get_data['space']['id']}")
    #
    #     return get_data
    #
    # @pytest.fixture(scope='function')
    # def test_update_task(self, test_create_task, create_data, update_data, test_get_task):
    #     self.item_data = test_create_task
    #     self.get_data = test_get_task
    #     task_id = self.item_data['id']
    #
    #     put_response = requests.put(f"{self.BASE_URL}/api/v2/task/{task_id}",
    #                                 headers=self.HEADERS_POST, json=update_data)
    #     assert put_response.status_code == 200, (f"Status code: {put_response.status_code}, "
    #                                              f"Responce: {put_response.text}")
    #
    #     put_data = put_response.json()
    #     assert task_id == put_data['id'], f"Value for key id: {put_data['id']}"
    #     assert len(put_data['id']) == 1, "No value entry for key id or there are duplicates"
    #     assert isinstance(put_data['id'], str), f"Object not found or object not type str: {put_data['id']}"
    #
    #     assert put_data['name'] == update_data['name'], f"Value for key name: {put_data['name']}"
    #     assert put_data['description'] == update_data['description'], (f"Value for key 'description': "
    #                                                                    f"{put_data['description']}")
    #
    #     assert isinstance(put_data['status'], dict), (f"Object not found or object not type dict: "
    #                                                   f"{type(put_data['status'])}")
    #
    #     assert len(put_data['status']['id']) > 0, "No value entry for key id in dict['status']"
    #     assert isinstance(put_data['status']['id'], str), (f"Object not found or object not type str: "
    #                                                        f"{put_data['status']['id']}")
    #     assert put_data['status']['id'] == self.get_data['status']['id'], (f"Value for key 'id': "
    #                                                                        f"{type(put_data['status']['id'])}")
    #
    #     assert isinstance(put_data['status']['status'], str), (f"Object not found or object not type str: "
    #                                                            f"{put_data['status']['status']}")
    #     assert len(put_data['status']['status']) > 0, "No value entry for key status in dict['status']"
    #     assert put_data['status']['status'] == self.get_data['status']['status'], (f"Value for key 'status': "
    #                                                                                f"{put_data['status']['status']}")
    #     assert isinstance(put_data['status']['color'], str), (f"Object not found or object not type str: "
    #                                                           f"{type(put_data['status']['color'])}")
    #     assert len(put_data['status']['color']) > 0, "No value entry for key color in dict['status']"
    #     assert put_data['status']['color'] == self.get_data['status']['color'], (f"Value for key 'color': "
    #                                                                              f"{put_data['status']['color']}")
    #
    #     assert isinstance(put_data['status']['orderindex'], int), (f"Object not found or object not type int: "
    #                                                                f"{type(put_data['status']['orderindex'])}")
    #     assert put_data['status']['orderindex'] == 0, "No value entry for key orderindex in dict['status']"
    #     assert put_data['status']['orderindex'] == self.get_data['status']['orderindex'], \
    #         f"Value for key 'color': {put_data['status']['orderindex']}"
    #
    #     assert isinstance(put_data['status']['type'], str), (f"Object not found or object not type str: "
    #                                                          f"{type(put_data['status']['type'])}")
    #     assert len(put_data['status']['type']) > 0, "No value entry for key type in dict['status']"
    #     assert put_data['status']['type'] == self.get_data['status']['type'], (f"Value for key 'color': "
    #                                                                            f"{put_data['status']['type']}")
    #
    #     assert 'creator' in put_data, "Key 'creator' not found in dict"
    #     assert put_data['creator']['id'] == self.get_data['creator']['id'], f"Value id: {put_data['creator']['id']}"
    #     assert put_data['creator']['username'] == self.get_data['creator']['username'], \
    #         f"Value username: {put_data['creator']['username']}"
    #     assert put_data['creator']['color'] == self.get_data['creator']['color'], \
    #         f"Value color: {put_data['creator']['color']}"
    #     assert put_data['creator']['profilePicture'] == self.get_data['creator']['profilePicture'], \
    #         f"Value profilePicture: {put_data['creator']['profilePicture']}"
    #
    #     assert 'custom_fields' in put_data, "Key 'custom_fields' not found in dict"
    #     assert isinstance(put_data['custom_fields'], str), (f"Object not type dict: "
    #                                                         f"{type(put_data['custom_fields'])}")
    #
    #     assert isinstance(put_data['list'], dict), f"type 'list': {type(put_data['list'])}"
    #     assert put_data['list']['id'] == self.get_data['list']['id'], f"value for key 'id': {put_data['list']['id']}"
    #
    #     assert isinstance(put_data['folder'], dict), f"type 'folder': {type(put_data['folder'])}"
    #     assert put_data['folder']['id'] == self.get_data['folder']['id'], \
    #         f"value for key 'id': {put_data['folder']['id']}"
    #
    #     assert isinstance(put_data['space'], dict), f"type 'space': {type(put_data['space'])}"
    #     assert put_data['space']['id'] == self.get_data['space']['id'], (f"value for key 'id': "
    #                                                                      f"{put_data['space']['id']}")
    #
    # @pytest.fixture(scope='function')
    # def test_delete_task(self, test_create_task):
    #     self.item_data = test_create_task
    #     task_id = self.item_data['id']
    #
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 204, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
    #     get_responce = requests.get(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert get_responce.status_code == 404, (f"Status code: {delete_responce.status_code}, "
    #                                              f"Responce: {delete_responce.text}")
    #     get_data = get_responce.json()
    #     assert 'err' in get_data, "Key 'err' not found in responce"
    #     assert get_data['err'] == "Task not found, deleted", f"Value 'err': {get_data['err']}"
    #     assert 'ECODE' in get_data, "Key 'ECODE' not found in responce"
    #     assert get_data['ECODE'] == "ITEM_013", f"Value 'ECODE': {get_data['ECODE']}"
    #
    # @pytest.fixture(scope='function')
    # def test_negative_create_task(self, create_data):
    #     LIST_ID = "9015"
    #     post_responce = requests.post(f"{self.BASE_URL}//api/v2/list/{LIST_ID}/task",
    #                                   json=create_data, headers=self.HEADERS_POST)
    #     assert post_responce.status_code == 401, (f"Status code: {post_responce.status_code}, "
    #                                               f"Responce: {post_responce.text}")
    #
    #     post_data = post_responce.json()
    #     assert 'err' in post_data, "Key 'err' not found in responce"
    #     assert post_data['err'] == "Team not autorizated", f"Value 'err': {post_data['err']}"
    #     assert 'ECODE' in post_data, "Key 'ECODE' not found in responce"
    #     assert post_data['ECODE'] == "OAUTH_027", f"Value 'ECODE': {post_data['ECODE']}"
    #
    # @pytest.fixture(scope='function')
    # def test_negative_create_task_2(self, create_negative_data):
    #     post_responce_2 = requests.post(f"{self.BASE_URL}//api/v2/list/{self.LIST_ID}/task",
    #                                     json=create_negative_data, headers=self.HEADERS_POST)
    #     assert post_responce_2.status_code == 400, (f"Status code: {post_responce_2.status_code}, "
    #                                                 f"Responce: {post_responce_2.text}")
    #
    #     post_data_2 = post_responce_2.json()
    #     assert 'err' in post_data_2, "Key 'err' not found in responce"
    #     assert post_data_2['err'] == "Task name invalid", f"Value 'err': {post_data_2['err']}"
    #     assert 'ECODE' in post_data_2, "Key 'ECODE' not found in responce"
    #     assert post_data_2['ECODE'] == "INPUT_005", f"Value 'ECODE': {post_data_2['ECODE']}"
    #
    # @pytest.fixture(scope='function')
    # def test_negative_create_task_3(self, create_data):
    #     post_responce_3 = requests.post(f"{self.BASE_URL}//api/v2/list/{self.LIST_ID}/tasks",
    #                                     json=create_data, headers=self.HEADERS_POST)
    #     assert post_responce_3.status_code == 404, (f"Status code: {post_responce_3.status_code}, "
    #                                                 f"Responce: {post_responce_3.text}")
    #
    #     assert "<pre>Cannot POST" in post_responce_3.text, "Error message not found responce"
    #
    # @pytest.fixture(scope='function')
    # def test_invalid_url_get_task(self, create_data):
    #     post_responce = requests.post(f"{self.BASE_URL}/api/v2/list/{self.LIST_ID}/task",
    #                                   json=create_data, headers=self.HEADERS_POST)
    #     assert post_responce.status_code == 200, (f"Status code: {post_responce.status_code}, "
    #                                               f"Responce: {post_responce.text}")
    #     post_data = post_responce.json()
    #     assert len(post_data['id']) > 0, "Not found new id"
    #     task_id = post_data['id']
    #
    #     get_responce = requests.get(f"{self.BASE_URL}/api/v2/task_id/{task_id}", headers=self.HEADERS_GET)
    #     assert get_responce.status_code == 404, (f"Status code: {get_responce.status_code}, "
    #                                              f"Responce: {get_responce.text}")
    #     assert 'err' in post_data, "Key 'err' not found in responce"
    #     assert post_data['err'] == "Route not found", f"Value 'err': {post_data['err']}"
    #     assert 'ECODE' in post_data, "Key 'ECODE' not found in responce"
    #     assert post_data['ECODE'] == "APP_001", f"Value 'ECODE': {post_data['ECODE']}"
    #
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 204, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
    # @pytest.fixture(scope='function')
    # def test_invalid_list_id_get_task(self, create_data):
    #     post_responce = requests.post(f"{self.BASE_URL}/api/v2/list/{self.LIST_ID}/task",
    #                                   json=create_data, headers=self.HEADERS_POST)
    #     assert post_responce.status_code == 200, (f"Status code: {post_responce.status_code}, "
    #                                               f"Responce: {post_responce.text}")
    #     post_data = post_responce.json()
    #     assert len(post_data['id']) > 0, "Not found new id"
    #     task_id = post_data['id']
    #
    #     get_responce = requests.get(f"{self.BASE_URL}/api/v2/task/9xh", headers=self.HEADERS_GET)
    #     assert get_responce.status_code == 401, (f"Status code: {get_responce.status_code}, "
    #                                              f"Responce: {get_responce.text}")
    #     assert 'err' in post_data, "Key 'err' not found in responce"
    #     assert post_data['err'] == "Team not authorized", f"Value 'err': {post_data['err']}"
    #     assert 'ECODE' in post_data, "Key 'ECODE' not found in responce"
    #     assert post_data['ECODE'] == "OAUTH_027", f"Value 'ECODE': {post_data['ECODE']}"
    #
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 204, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
    # @pytest.fixture(scope='function')
    # def test_invalid_token_get_task(self, create_data):
    #     post_responce = requests.post(f"{self.BASE_URL}/api/v2/list/{self.LIST_ID}/task",
    #                                   json=create_data, headers=self.HEADERS_POST)
    #     assert post_responce.status_code == 200, (f"Status code: {post_responce.status_code}, "
    #                                               f"Responce: {post_responce.text}")
    #     post_data = post_responce.json()
    #     assert len(post_data['id']) > 0, "Not found new id"
    #     task_id = post_data['id']
    #
    #     get_responce = requests.get(f"{self.BASE_URL}/api/v2/task/{task_id}",
    #                                 headers={"Accept": "application/json",
    #                                          "Authorization": "pk_182684312_A1I55W7P84F4B9HFKIGU3L32NEF654"})
    #     assert get_responce.status_code == 401, (f"Status code: {get_responce.status_code}, "
    #                                              f"Responce: {get_responce.text}")
    #     assert 'err' in post_data, "Key 'err' not found in responce"
    #     assert post_data['err'] == "Token invalid", f"Value 'err': {post_data['err']}"
    #     assert 'ECODE' in post_data, "Key 'ECODE' not found in responce"
    #     assert post_data['ECODE'] == "OAUTH_027", f"Value 'ECODE': {post_data['ECODE']}"
    #
    #     delete_responce = requests.delete(f"{self.BASE_URL}/api/v2/task/{task_id}", headers=self.HEADERS_GET)
    #     assert delete_responce.status_code == 204, (f"Status code: {delete_responce.status_code}, "
    #                                                 f"Responce: {delete_responce.text}")
    #
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
