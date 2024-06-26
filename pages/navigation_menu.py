from selene.api import *

from pages.base_page import BasePage


class NavigationMenu(BasePage):
    button_burger_menu = browser.element(by.id('react-burger-menu-btn'))

    def open_burger_menu(self):
        self.click_on(element=self.button_burger_menu, name='Кнопка "Бургер меню"')
        self.check_text_is_visible(text='All items')

    def close_burger_menu(self):
        self.click_on(element=self.button_burger_menu, name='Кнопка "Бургер меню"')
        self.check_text_is_not_visible(text='All items')