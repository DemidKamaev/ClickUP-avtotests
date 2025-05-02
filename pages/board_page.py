from pages.base_page import BasePage
from api_clients.task_api import ClickUpClient
from tests.ui.conftest import create_task_api_for_ui, create_data_card
from tests.config import WORKSPACE_ID, FOLDER_ID


class BoardPage(BasePage):
    WORKSPACE_TEXT = "Clickup-тесты"
    HOME_TEXT = "Home"
    INBOX_TEXT = "Inbox"

    BOARD_BTN_SELECTOR = '[data-test="data-view-item__view-id-body-Board"]'
    ADD_TASK_BTN_SELECTOR = '[data-test="board-group__create-task-button__Add Task"]'
    TASK_INPUT_LOCATOR = '[data-test="quick-create-task-panel__panel-board__input"]'
    SAVE_TASK_BTN_SELECTOR = '[data-test="quick-create-task-panel__panel-board__enter-button"]'
    TASK_MENU_BTN_SELECTOR = '[data-test="board-actions-menu__ellipsis__Test_card"]'
    DELETE_BUTTON_SELECT = '[data-test="quick-actions-menu__delete-task"]'

    def __init__(self, page):
        super().__init__(page)
        self._endpoint = "90151065503/v/l/2kypr5wz-255"

    def go_to_board_tab(self):
        self.wait_for_selector_and_click(self.BOARD_BTN_SELECTOR)
        self.assert_text_not_on_page("in progress")

    def create_the_task(self):
        self.assert_url_is_correct("https://app.clickup.com/90151065503/v/b/li/901510167328")
        self.wait_for_selector_and_click(self.ADD_TASK_BTN_SELECTOR)
        self.wait_for_selector_and_type(self.TASK_INPUT_LOCATOR, "Test_card", 100)
        self.wait_for_selector_and_click(self.SAVE_TASK_BTN_SELECTOR)
        self.assert_text_present_on_page("Created")

    def delete_the_task(self):
        self.hover_selector('.open-task-clickable-area[_ngcontent-ng-c17472219]')
        self.wait_for_selector_and_click(self.TASK_MENU_BTN_SELECTOR)
        self.wait_for_selector_and_click(self.DELETE_BUTTON_SELECT)
        self.assert_text_not_on_page("Task moved to trash")






    # как собрать полный урл с team_id?
    # понять иерархию для корректного написания скелета
    # в боард указать корректный адрес с team_id (Или название в Spaces)
    # создаем таску через фикстуру
    # находим таску по названию + тянем селектор по удалению таски

    # класс Боард нужен для того, чтобы мы могли открыть страницу с team_id,
    # где лежать наши таски

    # Как найти селектор или название созданной задачи через апи,
    # чтобы удалить задачу через ui
