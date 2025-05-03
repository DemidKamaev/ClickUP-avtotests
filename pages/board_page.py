from pages.base_page import BasePage
from tests.config import BOARD_ID, TEAM_ID, FOLDER_ID, CARD_ID, TEXT_CARD


class BoardPage(BasePage):
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
        self._endpoint = f"{TEAM_ID}/v/l/{BOARD_ID}"

    def go_to_board_tab(self):
        self.wait_for_selector_and_click(self.BOARD_BTN_SELECTOR)
        self.assert_text_not_on_page("in progress")

    def create_the_task(self):
        self.assert_url_is_correct(f"https://app.clickup.com/{TEAM_ID}/v/b/li/{FOLDER_ID}")
        self.wait_for_selector_and_click(self.ADD_TASK_BTN_SELECTOR)
        self.wait_for_selector_and_type(self.TASK_INPUT_LOCATOR, TEXT_CARD, 100)
        self.wait_for_selector_and_click(self.SAVE_TASK_BTN_SELECTOR)
        self.assert_text_present_on_page("Created")
        self.assert_text_present_on_page("Test_card")

    def delete_the_task(self):
        self.hover_selector(f'.open-task-clickable-area[_ngcontent-ng-{CARD_ID}]')
        self.wait_for_selector_and_click(self.TASK_MENU_BTN_SELECTOR)
        self.wait_for_selector_and_click(self.DELETE_BUTTON_SELECT)
        self.assert_text_present_on_page("Task moved to trash")
        self.assert_text_not_on_page("Test_card")
