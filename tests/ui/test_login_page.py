import allure
from tests.ui.conftest import browser
from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD


@allure.feature("UI: Авторизация")
class TestLogin:
    @allure.desciption("Проверка успешной авторизации в ClickUp")
    def test_login(self, browser):
        with allure.step("Создание новой странице браузера"):
            page = browser.new_page()

        with allure.step("Авторизация с валидными данными"):
            login_page = LoginPage(page)
            login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

    @allure.desciption("Проверка ошибки при некорректном пароле")
    def test_login_invalid_pas(self, browser):
        with allure.step("Создание новой странице браузера"):
            page = browser.new_page()

        with allure.step("Авторизация с неправильным паролем"):
            login_page = LoginPage(page)
            login_page.bad_login(CLICKUP_EMAIL, "not-valid0932")

