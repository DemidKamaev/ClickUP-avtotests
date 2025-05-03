import pytest
import allure
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD


@pytest.fixture(scope='session')
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=500)

    yield browser

    with allure.step("Выход из аккаунта"):
        browser.close()
        playwright.stop()


@pytest.fixture(scope='session')
def sync_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    login_page = LoginPage(page)

    with allure.step("Вход в систему"):
        login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

    yield page

    with allure.step("Выход из аккаунта"):
        page.click('[data-test="user-main-settings-menu__dropdown-toggle"]')
        page.click('[data-test="dropdown-list-item__Log out"]')
        browser.close()
        playwright.stop()


@pytest.fixture()
def create_data_card():
    with allure.step("Генерация валидных данных для создание новой такси"):
        return {
            "name": "Test_card",
            "description": "For delete_test",
            "status": "in progress"
        }
