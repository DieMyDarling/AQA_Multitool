import time
from selene.api import *
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from assist.allure.report import step
from assist.helpers import tool


class BasePage:

    @staticmethod
    @step('Кликнуть на элемент "{name}"')
    def click_on(element, name: str):
        """
        Метод клика по указанному элементу, если он кликабельный.

        :param element: Элемент или локатор (строка), который нужно кликнуть.
                        Если передан объект элемента (selene.api.browser_element), он будет использован напрямую.
                        Если передана строка, то она интерпретируется как локатор для поиска элемента через browser.element().
        :type element: str or selene.api.browser_element
        :param name: Название элемента или страницы, на которую происходит переход.
        :type name: str

        :raises Exception: Если произошла ошибка при переходе, метод вызывает исключение с информацией об ошибке.
        """
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible).hover().click()
        except Exception as e:
            raise Exception(f'Произошла ошибка при клике на элемент: "{name}"\n{str(e)}')

    @staticmethod
    @step('Кликнуть дважды на элемент "{name}"')
    def double_click_on(element, name: str):
        """
        Метод для двойного клика на указанный элемент, если он кликабельный.

        :param element: Элемент или локатор (строка), который нужно дважды кликнуть.
                        Если передан объект элемента (selene.api.browser_element), он будет использован напрямую.
                        Если передана строка, то она интерпретируется как локатор для поиска элемента через browser.element().
        :type element: str or selene.api.browser_element
        :param name: Название элемента или страницы, на которую происходит переход.
        :type name: str

        :raises Exception: Если произошла ошибка при переходе, метод вызывает исключение с информацией об ошибке.
        """
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible).hover().double_click()
        except Exception as e:
            raise Exception(f'Произошла ошибка при двойном клике на элемент: "{name}"\n{str(e)}')

    @staticmethod
    @step('Кликнуть на текст "{text}"')
    def click_on_text(text):
        """
        Кликнуть по элементу, найденному по частичному тексту.

        :param text: Часть текста, по которой будет производиться поиск элемента.
        :type text: str

        :raises Exception: Если произошла ошибка при клике на текст, метод вызывает исключение с информацией об ошибке.
        """
        try:
            browser.element(by.partial_text(text)).hover().click()
        except Exception as e:
            raise Exception(f'Произошла ошибка при клике на текст "{text}"\n{str(e)}')

    @staticmethod
    @step('Переключиться на новое окно')
    def switch_to_new_window(time_to_wait=5):
        """
        Переключается на новое окно браузера и ожидает заданное количество времени перед переключением.

        :param time_to_wait: Время ожидания в секундах перед переключением на новое окно. По умолчанию 5 секунд.
        :type time_to_wait: int, optional
        """
        time.sleep(time_to_wait)
        browser.switch_to_tab(1)

    @staticmethod
    @step('Проверить, что заголовок страницы: "{title}"')
    def check_browser_title(title: str):
        """
        Проверяет, соответствует ли заголовок текущей веб-страницы указанному заголовку.

        :param title: Ожидаемый заголовок страницы.
        :type title: str

        :raises ValueError: Если `title` равен `None`, выбрасывается ошибка "Заголовок страницы не указан".
        """
        if title is None:
            raise ValueError('Заголовок страницы не указан')

        current_title = browser.driver.title
        assert current_title == title, \
            f'Фактический заголовок страницы "{current_title}" не соответствует ожидаемому "{title}"'

    @staticmethod
    @step('Проверить, что текущий URL соответствует "{url}"')
    def check_url(url: str):
        """
        Функция получает текущий URL-адрес страницы и сравнивает его с введённым в параметр.

        :param url: Ожидаемый URL-адрес.
        :type url: str
        """
        current_url = browser.driver.current_url
        assert current_url == url, f'{current_url} does not match {url}'

    @staticmethod
    @step('Проверить, что элемент "{name}" отображается')
    def check_element_is_visible(element, name: str):
        """
        Проверяет видимость элемента на веб-странице.

        :param element: Элемент, который нужно проверить на видимость.
                        Может быть передан как строка (локатор) или объект PageObject.
        :type element: str or WebElement
        :param name: Название элемента для отображения в сообщениях об ошибках.
        :type name: str

        :raises AssertionError: Если элемент не найден или не виден на странице.
        """
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible)
        except Exception as e:
            raise Exception(f'Элемент "{name}" не найден\n{str(e)}')

    @staticmethod
    @step('Ввести текст "{text}" в поле "{name}"')
    def type_text_into_input_field(element, text=None, name=None):
        """
        Ввод текста в указанное поле.

        :param element: Элемент или локатор (строка), представляющий поле ввода.
                        Если передан объект элемента (selene.api.browser_element), он будет использован напрямую.
                        Если передана строка, то она интерпретируется как локатор для поиска элемента через browser.element().
        :type element: str or selene.api.browser_element
        :param text: Текст, который нужно ввести в поле. Если не указан, будет сгенерирован случайный текст.
        :param name: Имя поля ввода. Может быть пустым.
        :type text: str or None

        :raises Exception: Если произошла ошибка при вводе текста, метод вызывает исключение с информацией об ошибке.
        """
        if isinstance(element, str):
            element = browser.element(element)
        if text is None:
            text = tool.random_string()
        try:
            element.should(be.visible).hover().clear().type(text)
        except Exception as e:
            raise Exception(f'Произошла ошибка при вводе текста "{text}" в поле "{name}"\n{str(e)}')

    @staticmethod
    @step('Проверить, что элемент "{name}" не отображается')
    def check_element_is_not_visible(element, name: str):
        """
        Проверяет, что элемент не отображается на странице.

        :param element: Элемент, который нужно проверить на отображение. Может быть передан как строка (локатор) или объект PageObject.
        :type element: str or WebElement
        :param name: Название элемента для отображения в сообщениях об ошибках.
        :type name: str

        :raises AssertionError: Если элемент виден на странице.
        """
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.not_.visible)
        except Exception as e:
            raise Exception(f'Элемент "{name}" присутствует\n{str(e)}')

    @staticmethod
    @step('Проверить, что элемент с текстом "{t}" отображается')
    def check_text_is_visible(text):
        """
        Проверяет видимость элементов с заданным текстом.

        :param text: Текст элемента или список текстов элементов для проверки.
        :type text: str or list

        :raises AssertionError: Если элемент не найден или не виден.
        """
        if isinstance(text, str):
            text = [text]

        for t in text:
            try:
                browser.element(by.partial_text(t)).should(be.visible)
            except Exception as e:
                raise Exception(f'Элемент с текстом "{t}" не найден\n{str(e)}')

    @staticmethod
    @step('Проверить, что элемент с текстом "{t}" не отображается')
    def check_text_is_not_visible(text):
        """
        Проверяет невидимость элементов с заданным текстом.

        :param text: Текст элемента или список текстов элементов для проверки.
        :type text: str or list

        :raises AssertionError: Если элемент виден на странице.
        """
        if isinstance(text, str):
            text = [text]

        for t in text:
            try:
                browser.element(by.partial_text(t)).should(be.not_.visible)
            except Exception as e:
                raise Exception(f'Элемент с текстом "{t}" присутствует\n{str(e)}')

    @staticmethod
    @step('Проверить, что элемент "{name}" содержит текст "{text}"')
    def check_element_contains_text(element, name: str, text: str):
        """
        Проверяет, что элемент содержит указанный текст.

        :param element: Элемент или локатор (строка), который нужно проверить.
                        Если передан объект элемента (selene.api.browser_element), он будет использован напрямую.
                        Если передана строка, то она интерпретируется как локатор для поиска элемента через browser.element().
        :type element: str or selene.api.browser_element
        :param name: Название элемента для отображения в сообщениях об ошибках.
        :type name: str
        :param text: Текст, который должен содержаться в элементе.
        :type text: str

        :raises Exception: Если элемент не содержит указанный текст, метод вызывает исключение с информацией об ошибке.
        """
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible).should(have.text(text))
        except Exception as e:
            raise Exception(f'Элемент "{name}" не содержит текст "{text}"\n{str(e)}')

    @staticmethod
    @step('Кликнуть на элемент с идентификатором "{test_id}"')
    def click_on_id(test_id, name=None):
        """
        Кликает на элемент с указанным идентификатором `id`.

        :param test_id: Идентификатор элемента для клика.
        :type test_id: str
        :param name: Название элемента для отображения в сообщениях об ошибках.
        :type name: str, optional

        :raises Exception: Если произошла ошибка при клике на элемент, метод вызывает исключение с информацией об ошибке.
        """
        try:
            element = browser.element(f'[id="{test_id}"]')
            element.should(be.visible).hover().click()
        except Exception as e:
            msg = f'Произошла ошибка при клике на элемент с идентификатором "{test_id}"'
            if name is not None:
                msg = f'Произошла ошибка при клике на "{name}"'
            raise Exception(f'{msg}: {str(e)}')

    @staticmethod
    @step('Нажать правой кнопкой мыши на элемент "{name}"')
    def right_click(element, name: str):
        """
        Выполняет клик правой кнопкой мыши на указанном элементе.

        :param element: Элемент для выполнения правого клика. Может быть передан как строка (локатор) или объект PageObject.
        :type element: str or WebElement
        :param name: Название элемента для отображения в сообщениях об ошибках.
        :type name: str

        :raises Exception: Если произошла ошибка при выполнении правого клика, метод вызывает исключение с информацией об ошибке.
        """
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible).hover().context_click()
        except Exception as e:
            raise Exception(f'Произошла ошибка при нажатии правой кнопки мыши на элемент "{name}"\n{str(e)}')

    @staticmethod
    @step('Открыть страницу "{url}"')
    def open_page(url: str = None):
        """
        Открывает страницу по указанной ссылке.

        :param url: URL-адрес страницы.
        :type url: str
        """
        if url is None:
            url = config.base_url
        browser.open(url)

    @staticmethod
    @step('Передвинуть слайдер "{name}"')
    def move_slider(element, name: str):
        """
        Передвинуть слайдер.

        :param element: Элемент слайдера.
        :type element: str or WebElement
        :param name: Наименование слайдера.
        :type name: str

        :raises Exception: Если произошла ошибка при передвижении слайдера, метод вызывает исключение с информацией об ошибке.
        """
        driver = browser.driver()  # Используем текущий драйвер из Selene
        try:
            if isinstance(element, str):
                element = driver.find_element(By.XPATH, element)
            action_chains = ActionChains(driver)
            action_chains.click_and_hold(element).move_by_offset(xoffset=200, yoffset=0).release().perform()
        except Exception as e:
            raise Exception(f'Произошла ошибка при передвижении слайдера "{name}"\n{str(e)}')

    @staticmethod
    @step('Очистить поле ввода "{name}"')
    def clear_input_field(element, name: str):
        """
        Очищает поле ввода с помощью нажатий CTRL+A и BACKSPACE.

        :param element: Элемент поле ввода.
        :type element: str or WebElement
        :param name: Наименование поле ввода.
        :type name: str

        :raises Exception: Если произошла ошибка при очистке поля, метод вызывает исключение с информацией об ошибке.
        """
        try:
            if isinstance(element, str):
                element = browser.element(element)
            element.should(be.visible).hover().send_keys(Keys.CONTROL + "a").send_keys(Keys.BACKSPACE)
        except Exception as e:
            raise Exception(f'Произошла ошибка при очистке поля: "{name}"\n{e!s}')
