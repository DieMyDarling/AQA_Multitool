import time

from allure import step
from selene.api import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from tools.helpers import tool


class BasePage:

    @staticmethod
    def click_on(element, name: str):
        """
        Метод для перехода к указанному элементу, если он кликабельный.

        :param element: Элемент или локатор (строка), который нужно кликнуть.
                        Если передан объект элемента (selene.api.browser_element), он будет использован напрямую.
                        Если передана строка, то она интерпретируется как локатор для поиска элемента через browser.element().
        :type element: str or selene.api.browser_element
        :param name: Название элемента или страницы, на которую происходит переход.
        :type name: str

        :raises Exception: Если произошла ошибка при переходе, метод вызывает исключение с информацией об ошибке.
        """
        with step(f'Кликнуть на "{name}"'):
            try:
                if isinstance(element, str):
                    element = browser.element(element)
                element.should(be.visible).hover().click()
            except Exception as e:
                raise Exception(f'Произошла ошибка при клике на элемент: "{name}"\n{str(e)}')

    @staticmethod
    def double_click_on(element, name: str):
        """
        Метод для перехода к указанному элементу, если он кликабельный.

        :param element: Элемент или локатор (строка), который нужно кликнуть.
                        Если передан объект элемента (selene.api.browser_element), он будет использован напрямую.
                        Если передана строка, то она интерпретируется как локатор для поиска элемента через browser.element().
        :type element: str or selene.api.browser_element
        :param name: Название элемента или страницы, на которую происходит переход.
        :type name: str

        :raises Exception: Если произошла ошибка при переходе, метод вызывает исключение с информацией об ошибке.
        """
        with step(f'Кликнуть на "{name}"'):
            try:
                if isinstance(element, str):
                    element = browser.element(element)
                element.should(be.visible).hover().double_click()
            except Exception as e:
                raise Exception(f'Произошла ошибка при двойном клике на элемент: "{name}"\n{str(e)}')

    @staticmethod
    def click_on_text(text):
        """
        Кликнуть по элементу, найденному по частичному тексту.

        :param text: Часть текста, по которой будет производиться поиск элемента.
        :type text: str

        :raises Exception: Если произошла ошибка при клике на текст, метод вызывает исключение с информацией об ошибке.
        """
        with step(f'Кликнуть на текст "{text}"'):
            try:
                browser.element(by.partial_text(text)).hover().click()
            except Exception as e:
                raise Exception(f'Произошла ошибка при клике на текст "{text}"\n{str(e)}')

    @staticmethod
    def switch_to_new_window(time_to_wait=5):
        """
        Переключается на новое окно браузера и ожидает заданное количество времени перед переключением.

        :param time_to_wait: Время ожидания в секундах перед переключением на новое окно. По умолчанию 5 секунд.
        :type time_to_wait: int, optional
        """
        with step('Переключиться на открывшееся окно'):
            time.sleep(time_to_wait)
            browser.switch_to_tab(1)

    @staticmethod
    def check_browser_title(title: str):
        """
        Проверяет, соответствует ли заголовок текущей веб-страницы указанному заголовку.

        :param title: Ожидаемый заголовок страницы.
        :type title: str

        :raises ValueError: Если `title` равен `None`, выбрасывается ошибка "Заголовок страницы не указан".
        """
        with step(f'Проверить, что заголовок страницы: "{title}"'):
            if title is None:
                raise ValueError('Заголовок страницы не указан')

        current_title = browser.driver.title
        assert current_title == title, \
            f'Фактический заголовок страницы "{current_title}" не соответствует ожидаемому "{title}"'

    @staticmethod
    def check_url(url: str):
        """
        Функция получает текущий URL-адрес страницы и сравнивает его с введённым в параметр.

        :param url: Ожидаемый URL-адрес.
        :type url: str
        """
        with step(f'Проверить, что текущий url {url}'):
            current_url = browser.driver.current_url
            assert current_url == url, f'{current_url} does not match {url}'

    @staticmethod
    def check_element_is_visible(element, name: str):
        """
        Проверяет видимость элемента на веб-странице.

        :param element: Элемент, который нужно проверить на видимость.
                        Может быть передан как строка (локатор) или объект PageObject.
        :type element: str or WebElement
        :param name: Название элемента для отображения в сообщениях об ошибках.
        :type name: str

        :raises AssertionError: Если элемент не найден или не виден на странице.

        Пример использования:
        check_element_is_visible('button.submit', 'Кнопка отправки формы')
        """
        with step(f'Проверить что элемент "{name}" отображается'):
            try:
                if isinstance(element, str):
                    # Если элемент передан в виде строки, ищем его с помощью локатора
                    element = browser.element(element)
                # Проверяем, что элемент виден
                element.should(be.visible)
            except Exception as e:
                raise Exception(f'"Элемент" "{name}" не найден\n{str(e)}')

    @staticmethod
    def type_text_into_input_field(element, text=None, name=None):
        """
        Ввод текста в указанное поле.

        :param element: Элемент или локатор (строка), представляющий поле ввода.
                        Если передан объект элемента (selene.api.browser_element), он будет использован напрямую.
                        Если передана строка, то она интерпретируется как локатор для поиска элемента через browser.element().
        :type element: str or selene.api.browser_element
        :param text: Текст, который нужно ввести в поле. Если не указан, будет сгенерирован случайный текст.
        :param name: Имя поля ввода. Может быть пустым
        :type text: str or None

        :raises Exception: Если произошла ошибка при вводе текста, метод вызывает исключение с информацией об ошибке.
        """
        if isinstance(element, str):
            element = browser.element(element)
        if text is None:
            text = tool.random_string()
        try:
            if name is not None:
                with step(f'Ввести текст "{text}" в поле "{name}"'):
                    element.should(be.visible).hover().clear().type(text)
            else:
                with step(f'Ввести текст "{text}"'):
                    element.should(be.visible).hover().clear().type(text)
        except Exception as e:
            if name is not None:
                raise Exception(f'Произошла ошибка при вводе текста "{text}" в поле "{name}"\n{str(e)}')
            else:
                raise Exception(f'Произошла ошибка при вводе текста "{text}"\n{str(e)}')

    @staticmethod
    def check_element_is_not_visible(element, name: str):
        """
        Проверяет, что элемент не отображается на странице.

        Аргументы:
        - element: Элемент, который нужно проверить на отображение. Может быть передан как строка (локатор) или объект PageObject.
        - name: Название элемента для отображения в сообщениях об ошибках.

        Исключения:
        - AssertionError: Если элемент виден на странице.
        """
        with step(f'Проверить что элемент "{name}" не отображается'):
            try:
                if isinstance(element, str):
                    element = browser.element(element)
                element.should(be.not_.visible)
            except Exception as e:
                raise Exception(f'"Элемент" "{name}" присутствует\n{str(e)}')

    @staticmethod
    def check_text_is_visible(text):
        """
        Проверяет видимость элементов с заданным текстом.

        Args:
            text (str or list): Текст элемента или список текстов элементов для проверки.
        Raises:
            AssertionError: Если элемент не найден или не видим.
        Examples:
            # Проверка видимости элемента с текстом 'Привет'
            check_text_is_visible('Привет')

            # Проверка видимости нескольких элементов по списку текстов
            check_text_is_visible(['Привет', 'Мир'])
        """
        if isinstance(text, str):
            text = [text]

        for t in text:
            with step(f'Найти элемент с "{t}"'):
                try:
                    browser.element(by.partial_text(t)).should(be.visible)
                except Exception as e:
                    raise Exception(f'"Элемент" c текстом "{t}" не найден\n{str(e)}')

    @staticmethod
    def check_text_is_not_visible(text):
        """
        Проверяет невидимость элементов с заданным текстом.

        Args:
            text (str or list): Текст элемента или список текстов элементов для проверки.
        Raises:
            AssertionError: Если элемент виден на странице.
        Examples:
            # Проверка невидимости элемента с текстом 'Привет'
            check_text_is_not_visible('Привет')

            # Проверка невидимости нескольких элементов по списку текстов
            check_text_is_not_visible(['Привет', 'Мир'])
        """
        if isinstance(text, str):
            text = [text]

        for t in text:
            with step(f'Проверить что элемент с текстом "{t}" не отображается"'):
                try:
                    browser.element(by.partial_text(t)).should(be.not_.visible)
                except Exception as e:
                    raise Exception(f'"Элемент" c текстом "{t}" присутствует\n{str(e)}')

    @staticmethod
    def check_element_contains_text(element, name: str, text: str):
        with step(f'Проверить что элемент "{name}" содержит текст "{text}"'):
            try:
                if isinstance(element, str):
                    element = browser.element(element)
                element.should(be.visible).should(have.text(text))
            except Exception as e:
                raise Exception(f'"Элемент" "{name}" не содержит текст "{text}"\n{str(e)}')

    @staticmethod
    def click_on_id(test_id, name=None):
        """
        Кликает на элемент с указанным идентификатором `id`.

        :param test_id: Идентификатор элемента для клика.
        :type test_id: str
        :param name: Название элемента для отображения в сообщениях об ошибках.
        :type name: str, optional

        :raises Exception: Если произошла ошибка при клике на элемент, метод вызывает исключение с информацией об ошибке.
        """
        with step(f'Кликнуть на элемент с индентификатором "{test_id}"'):
            try:
                if isinstance(test_id, str):
                    element = browser.element(f'[id="{test_id}"]')
                element.should(be.visible).hover().click()
            except Exception as e:
                msg = f'Произошла ошибка при клике на элемент с индентификатором "{test_id}"'
                if name is not None:
                    msg = f'Произошла ошибка при клике на "{name}"'
                raise Exception(f'{msg}: {str(e)}')

    @staticmethod
    def right_click(element, name: str):
        """
        Выполняет клик правой кнопкой мыши на указанном элементе.

        :param element: Элемент для выполнения правого клика. Может быть передан как строка (локатор) или объект PageObject.
        :type element: str or WebElement
        :param name: Название элемента для отображения в сообщениях об ошибках.
        :type name: str

        :raises Exception: Если произошла ошибка при выполнении правого клика, метод вызывает исключение с информацией об ошибке.
        """
        with step(f'Нажать правой кнопкой мыши на элемент "{name}"'):
            try:
                if isinstance(element, str):
                    element = browser.element(element)
                element.should(be.visible).hover().context_click()
            except Exception as e:
                raise Exception(f'Произошла ошибка при нажатии правой кнопки мыши на элемент "{name}"\n{str(e)}')

    @staticmethod
    def open_page(url: str = None):
        """
        Открывает страницу по указанной ссылке.

        :param url: URL-адрес страницы.
        :type url: str
        """
        if url is None:
            url = config.base_url
        with step(f'Открыть страницу "{url}"'):
            browser.open(url)

    @staticmethod
    def move_slider(element, name: str):
        from selenium import webdriver
        driver = webdriver.Chrome()
        """
        Передвинуть слайдер.

        :param element: Элемент слайдера.
        :param name: Наименование слайдера.
        """
        with step(f'Передвинуть слайдер "{name}"'):
            try:
                if isinstance(element, str):
                    element = driver.find_element(By.XPATH, element)
                action_chains = ActionChains(driver)
                action_chains.click_and_hold(element).move_by_offset(xoffset=200, yoffset=0).release().perform()
            except Exception as e:
                raise Exception(f'Произошла ошибка при передвижении слайдера "{name}"\n{str(e)}')
