import time
from selene.api import *
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from assist.helpers import tool
# from assist.allure.report import step
from assist.allure.custom_step import step



class BasePage:

    @staticmethod
    @step('Кликнуть на элемент')
    def click_on(element, name: str):
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible).hover().click()
        except Exception as e:
            raise Exception(f'Произошла ошибка при клике на элемент: "{name}"\n{str(e)}')

    @staticmethod
    @step('Кликнуть дважды на элемент')
    def double_click_on(element, name: str):
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible).hover().double_click()
        except Exception as e:
            raise Exception(f'Произошла ошибка при двойном клике на элемент: "{name}"\n{str(e)}')

    @staticmethod
    @step('Кликнуть на текст')
    def click_on_text(text):
        try:
            browser.element(by.partial_text(text)).hover().click()
        except Exception as e:
            raise Exception(f'Произошла ошибка при клике на текст "{text}"\n{str(e)}')

    @staticmethod
    @step('Переключиться на новое окно')
    def switch_to_new_window(time_to_wait=5):
        time.sleep(time_to_wait)
        browser.switch_to_tab(1)

    @staticmethod
    @step('Проверить заголовок страницы')
    def check_browser_title(title: str):
        if title is None:
            raise ValueError('Заголовок страницы не указан')

        current_title = browser.driver.title
        assert current_title == title, \
            f'Фактический заголовок страницы "{current_title}" не соответствует ожидаемому "{title}"'

    @staticmethod
    @step('Проверить текущий URL')
    def check_url(url: str):
        current_url = browser.driver.current_url
        assert current_url == url, f'{current_url} does not match {url}'

    @staticmethod
    @step('Проверить, что элемент отображается')
    def check_element_is_visible(element, name: str):
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible)
        except Exception as e:
            raise Exception(f'Элемент "{name}" не найден\n{str(e)}')

    @staticmethod
    @step('Ввести текст в поле')
    def type_text_into_input_field(element, text=None, name=None):
        if isinstance(element, str):
            element = browser.element(element)
        if text is None:
            text = tool.random_string()
        try:
            element.should(be.visible).hover().clear().type(text)
        except Exception as e:
            if name:
                raise Exception(f'Произошла ошибка при вводе текста "{text}" в поле "{name}"\n{str(e)}')
            else:
                raise Exception(f'Произошла ошибка при вводе текста "{text}"\n{str(e)}')

    @staticmethod
    @step('Проверить, что элемент не отображается')
    def check_element_is_not_visible(element, name: str):
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.not_.visible)
        except Exception as e:
            raise Exception(f'Элемент "{name}" присутствует\n{str(e)}')

    @staticmethod
    @step('Проверить, что элемент с текстом отображается')
    def check_text_is_visible(text):
        if isinstance(text, str):
            text = [text]
        for t in text:
            try:
                browser.element(by.partial_text(t)).should(be.visible)
            except Exception as e:
                raise Exception(f'Элемент с текстом "{t}" не найден\n{str(e)}')

    @staticmethod
    @step('Проверить, что элемент с текстом не отображается')
    def check_text_is_not_visible(text):
        if isinstance(text, str):
            text = [text]

        for t in text:
            try:
                browser.element(by.partial_text(t)).should(be.not_.visible)
            except Exception as e:
                raise Exception(f'Элемент с текстом "{t}" присутствует\n{str(e)}')

    @staticmethod
    @step('Проверить, что элемент содержит текст')
    def check_element_contains_text(element, name: str, text: str):
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible).should(have.text(text))
        except Exception as e:
            raise Exception(f'Элемент "{name}" не содержит текст "{text}"\n{str(e)}')

    @staticmethod
    @step('Кликнуть на элемент с идентификаторо')
    def click_on_id(test_id, name=None):
        try:
            element = browser.element(f'[id="{test_id}"]')
            element.should(be.visible).hover().click()
        except Exception as e:
            msg = f'Произошла ошибка при клике на элемент с идентификатором "{test_id}"'
            if name:
                msg = f'Произошла ошибка при клике на "{name}"'
            raise Exception(f'{msg}: {str(e)}')

    @staticmethod
    @step('Нажать правой кнопкой мыши на элемент')
    def right_click(element, name: str):
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible).hover().context_click()
        except Exception as e:
            raise Exception(f'Произошла ошибка при нажатии правой кнопки мыши на элемент "{name}"\n{str(e)}')

    @staticmethod
    @step('Открыть страницу')
    def open_page(url: str = config.base_url):
        browser.open(url)

    @staticmethod
    @step('Передвинуть слайдер')
    def move_slider(element, name: str):
        driver = browser.driver()  # Используем текущий драйвер из Selene
        try:
            if isinstance(element, str):
                element = driver.find_element(By.XPATH, element)
            action_chains = ActionChains(driver)
            action_chains.click_and_hold(element).move_by_offset(xoffset=200, yoffset=0).release().perform()
        except Exception as e:
            raise Exception(f'Произошла ошибка при передвижении слайдера "{name}"\n{str(e)}')

    @staticmethod
    @step('Очистить поле ввода')
    def clear_input_field(element, name: str):
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible).hover().send_keys(Keys.CONTROL + "a").send_keys(Keys.BACKSPACE)
        except Exception as e:
            raise Exception(f'Произошла ошибка при очистке поля: "{name}"\n{e!s}')
