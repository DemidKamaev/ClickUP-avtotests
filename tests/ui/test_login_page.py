import allure
from tests.ui.conftest import browser
from pages.login_page import LoginPage
from pages.base_page import BasePage
from pages.board_page import BoardPage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD
from tests.config import TEXT_MY_TITLE


@allure.feature("UI: Авторизация")
class TestLogin(BasePage):
    @allure.desciption("Проверка успешной авторизации в ClickUp")
    def test_login(self, browser):
        with allure.step("Создание новой странице браузера"):
            page = browser.new_page()

        with allure.step("Авторизация с валидными данными"):
            login_page = LoginPage(page)
            login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

        with allure.step("Проверка значений на стенде"):
            board_page = BoardPage(page)
            board_page.assert_text_present_on_page("Home")
            board_page.assert_text_present_on_page(TEXT_MY_TITLE)

    @allure.desciption("Проверка ошибки при некорректном пароле")
    def test_login_invalid_pas(self, browser):
        with allure.step("Создание новой странице браузера"):
            page = browser.new_page()

        with allure.step("Авторизация с неправильным паролем и проверка наличия уведомления"):
            login_page = LoginPage(page)
            login_page.login(CLICKUP_EMAIL, "not-valid0932")
            login_page.assert_text_present_on_page("Incorrect password for this email.")
