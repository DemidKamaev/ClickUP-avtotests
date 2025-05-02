import time

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = 'login'

    USER_NAME_SELECTOR = '#login-email-input'
    PASSWORD_SELECTOR = '#login-password-input'
    LOG_BUTTON_SELECTOR = 'button[data-test="login-submit"]'

    def login(self, username, password):
        self.navigate_to()
        self.wait_for_selector_and_type(self.USER_NAME_SELECTOR, username, 100)
        self.wait_for_selector_and_type(self.PASSWORD_SELECTOR, password, 100)
        self.wait_for_selector_and_click(self.LOG_BUTTON_SELECTOR)
        time.sleep(5)
        self.assert_text_present_on_page('Clickup-тесты')
        self.assert_text_present_on_page('Team Space')

    def bad_login(self, username, password):
        self.navigate_to()
        self.wait_for_selector_and_type(self.USER_NAME_SELECTOR, username, 100)
        self.wait_for_selector_and_type(self.PASSWORD_SELECTOR, password, 100)
        self.assert_text_present_on_page("Incorrect password for this email.")
