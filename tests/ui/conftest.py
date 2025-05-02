import pytest
import allure
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD
from api_clients.task_api import ClickUpClient


@pytest.fixture(scope='session')
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    yield browser

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


@pytest.fixture()
def create_task_api_for_ui(clickup_client, get_list_id_fixture, create_data_card):
    list_id = get_list_id_fixture
    response = clickup_client.create_task(list_id, create_data_card)

    if response is None:
        raise ValueError("Ответ равен None, проверить API client")

    yield response


@pytest.fixture()
def authorized_user():
    with allure.step("Запуск браузера и авторизация через UI"):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        login_page = LoginPage(page)

        with allure.step("Вход в систему"):
            login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

    yield page

    with allure.step("Выход из аккаунта"):
        page.click('')
        page.click('')
        browser.close()
        playwright.stop()

