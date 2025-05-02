from tests.ui.conftest import browser
from pages.board_page import BoardPage
import allure
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD
from api_clients.task_api import ClickUpClient
from tests.conftest import clickup_client


@allure.feature("UI: Задача на доске")
class TestBoardTask(ClickUpClient):
    @allure.description("Проверка создания задачи через API и удаление через UI")
    def test_delete_task_through_ui(self, browser, create_task_api_for_ui, authorized_user):
        with allure.step("Создание задачи через API"):
            response = create_task_api_for_ui
            assert response.status_code == 200, "Задача не создана"

        with allure.step("Переходим на вкладку доски"):
            board_page = BoardPage(authorized_user)
            board_page.go_to_board_tab()

        with allure.step("Удаляем задачу через UI"):
            board_page.delete_the_task()

    @allure.description("Проверка создания задачи через UI и удаления через API")
    def test_ui_create_task(self, authorized_user, clickup_client, get_list_id_fixture):
        with allure.step("Переходим на вкладку доски"):
            board_page = BoardPage(authorized_user)
            board_page.go_to_board_tab()

        with allure.step("Создаем задачу через UI"):
            board_page.create_the_task()

        with allure.step("Получить список задач через API"):
            response = clickup_client.get_full_tasks(list_id=get_list_id_fixture)
            assert response.status_code == 200, (f"Статус код: {response.status_code}"
                                                 f"ответ: {response.text}")

        with allure.step("Удаляем задачу через API"):
            data_response = response.json()
            task_id = data_response['tasks'][0]['id']
            delete_response = clickup_client.delete_task(task_id)
            assert delete_response.status_code == 204, (f"Статус код: {delete_response.status_code}"
                                                        f"ответ: {delete_response.text}")






