from selene.api import browser, by

from model.user import user_for_main
from tools.web.pages.base_page import BasePage


class LoginPage(BasePage):
    input_login = browser.element(by.id('user-name'))
    input_password = browser.element(by.id('password'))
    button_login = browser.element(by.id('login-button'))

    def open_page(self, url: str = None):
        self.open_page(url='https://www.saucedemo.com/')
        self.check_browser_title(title='Swag Labs')


    def fill_auth_form(self, username=None, password=None):
        """
        1. Перейти на сайт
        2. Заполнить данные пользователя в форме авторизации
        3. Нажать на кнопку "Войти"
        """

        if username is None and password is None:
            username = user_for_main.username
            password = user_for_main.password

        self.type_text_into_input_field(element=self.input_login,
                                        name='Поле ввода "Введите почту"',
                                        text=username)
        self.type_text_into_input_field(element=self.input_password,
                                        name='Поле ввода "Ваш пароль"',
                                        text=password)

    def press_login_button(self):
        self.click_on(element=self.button_login, name='Кнопка "Войти"')
        self.check_url(url='https://www.saucedemo.com/inventory.html')
