import allure
import requests
from utils.helpers import CLICKUP_API_KEY
from tests.conftest import create_data


class ClickUpClient:
    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Authorization": api_token
        })
        self.session_2 = requests.Session()
        self.session_2.headers.update({
            "Accept": "application/json",
            "Content_Type": "application/json",
            "Authorization": api_token
        })

    @allure.step("Получение team id")
    def get_team_id(self):
        response = self.session.get(f"{self.base_url}/api/v2/team")
        response_json = response.json()

        try:
            team_id = response_json['teams'][0]['id']
            return team_id
        except (KeyError, IndexError) as e:
            raise ValueError("Не удалось получить team_id из response_json") from e

    @allure.step("Получение space id")
    def get_space_id(self):
        team_id = self.get_team_id()

        response = self.session.get(f"{self.base_url}/api/v2/team/{team_id}/space")
        response_json = response.json()

        try:
            space_id = response_json['spaces'][0]['id']
            return space_id
        except (KeyError, IndexError) as e:
            raise ValueError("Не удалось получить space_id из response_json") from e

    @allure.step("Получение folder_id")
    def get_folder_id(self):
        space_id = self.get_space_id

        response = self.session.get(f"{self.base_url}/api/v2/space/{space_id}/folder")
        response_json = response.json()

        try:
            folder_id = response_json['folders'][0]['id']
            return folder_id
        except (KeyError, IndexError) as e:
            raise ValueError("Не удалось получить folder_id из response_json") from e

    @allure.step("Получение list_id")
    def get_list_id(self):
        folder_id = self.get_folder_id

        response = self.session.get(f"{self.base_url}/api/v2/folder/{folder_id}/list")
        response_json = response.json()

        try:
            list_id = response_json['lists'][0]['id']
            return list_id
        except (KeyError, IndexError) as e:
            raise ValueError("Не удалось получить list_id из response_json") from e

    @allure.step("Создание task")
    def create_task(self, list_id, create_data):
        return self.session_2.post(f"{self.base_url}/api/v2/list/{list_id}/task", json=create_data)

    @allure.step("Получение task")
    def get_task(self, task_id):
        return self.session.get(f"{self.base_url}/api/v2/task/{task_id}")

    @allure.step("Обновление task")
    def update_task(self, task_id, update_data):
        return self.session_2.put(f"{self.base_url}/api/v2/task/{task_id}", json=update_data)

    @allure.step("Удаление task")
    def delete_task(self, task_id):
        return self.session.delete(f"{self.base_url}/api/v2/task/{task_id}")



    # BASE_URL = 'https://api.clickup.com'
    # HEADERS_POST = {"Accept": "application/json",
    #                 "Content-Type": "application/json",
    #                 "Authorization": [CLICKUP_API_KEY]}
    #
    # HEADERS_GET = {"Accept": "application/json",
    #                "Authorization": [CLICKUP_API_KEY]}
    #
    # TEAM_ID = "90151065503"
    # SPACE_ID = "90154117382"
    # FOLDER_ID = "90156319403"
    # LIST_ID = "901510167328"

    # def __init__(self):
    #     self._endpoint = ""
    #
    # def _get_full_url(self):
    #     return f"{self.__BASE_URL}/{self._endpoint}"

    # Дернуть матрешку для получения list_id

