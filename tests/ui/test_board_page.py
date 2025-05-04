from tests.ui.conftest import sync_browser
from pages.board_page import BoardPage
import allure
from api_clients.task_api import ClickUpClient
from tests.conftest import clickup_client
from tests.config import TEXT_CARD


@allure.feature("UI: Задача на доске")
class TestBoardTask(ClickUpClient):
    @allure.description("Проверка создания задачи через API и удаление через UI")
    def test_delete_task_through_ui(self, sync_browser, create_task_fixture):
        with allure.step("Вход и переход на вкладку доски, используя открывшуюся страницу"):
            board_page = BoardPage(sync_browser)
            board_page.go_to_board_tab()

        with allure.step("Создание задачи через API"):
            response = create_task_fixture
            assert response.status_code == 200, "Задача не создана"

        with allure.step("Удаляем задачу через UI"):
            board_page.delete_the_task()

    @allure.description("Проверка создания задачи через UI и удаления через API")
    def test_ui_create_task(self, sync_browser, clickup_client, get_list_id_fixture):
        with allure.step("Вход и переход на вкладку доски, используя открывшуюся страницу"):
            board_page = BoardPage(sync_browser)
            board_page.go_to_board_tab()

        with allure.step("Создаем задачу через UI"):
            board_page.create_the_task()

        with allure.step("Получить список задач через API"):
            response = clickup_client.get_full_tasks(list_id=get_list_id_fixture)
            assert response.status_code == 200, (f"Статус код: {response.status_code}"
                                                 f"ответ: {response.text}")

        with allure.step("Удаляем задачу через API"):
            data_response = response.json().get('tasks', [])
            task_to_delete = next((item for item in data_response if item['title'] == 'Test_card'), None)

            if task_to_delete is None:
                print(f"Карточка с названием {TEXT_CARD} не найдена")
                return

            task_id = task_to_delete['id']
            delete_response = clickup_client.delete_task(task_id)
            assert delete_response.status_code == 204, (f"Статус код: {delete_response.status_code}"
                                                        f"Ответ: {delete_response.text}")
