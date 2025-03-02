import time
from selene.api import be, browser, by, config, have
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from assist.allure.custom_step import step


class BasePage:
    """
    Базовый класс для работы с элементами веб-страниц.

    Этот класс предоставляет методы для взаимодействия с элементами веб-страниц, такие как клики, ввод текста,
    проверка состояния элементов и другие.
    Все методы оформлены с использованием кастомных шагов `step`.
    """

    @staticmethod
    @step("Клик по элементу")
    def click_on(element):
        if isinstance(element, str):
            element = browser.element(element)
        element.should(be.visible).hover().click()

    @staticmethod
    @step("Двойной клик по элементу")
    def double_click_on(element):
        if isinstance(element, str):
            element = browser.element(element)
        element.should(be.visible).hover().double_click()

    @staticmethod
    @step("Клик по тексту элемента")
    def click_on_text(text: str):
        browser.element(f'//*[contains(text(),"{text}")]').hover().click()

    @staticmethod
    @step("Переключение на новое окно")
    def switch_to_new_window(time_to_wait=5):
        time.sleep(time_to_wait)
        browser.switch_to_tab(1)

    @staticmethod
    @step("Проверка заголовка страницы")
    def check_browser_title(title: str):
        if title is None:
            raise ValueError('Заголовок страницы не указан')

        current_title = browser.driver.title
        assert current_title == title, (
            f'Фактический заголовок страницы "{current_title}" '
            f'не соответствует ожидаемому "{title}"'
        )

    @staticmethod
    @step("Проверка текущего URL страницы")
    def check_url(url: str):
        current_url = browser.driver.current_url
        assert current_url == url, f'{current_url} не соответствует ожидаемому {url}'

    @staticmethod
    @step("Проверка, что элемент отображается")
    def check_element_is_visible(element):
        if isinstance(element, str):
            element = browser.element(element)
        element.should(be.visible)

    @staticmethod
    @step("Ввод текста в поле ввода")
    def type_text_into_input_field(element, text=None):
        if isinstance(element, str):
            element = browser.element(element)
        if text is None:
            text = 'random_text'
        element.should(be.visible).hover().clear().type(text)

    @staticmethod
    @step("Проверка, что элемент не отображается")
    def check_element_is_not_visible(element):
        if isinstance(element, str):
            element = browser.element(element)
        element.should(be.not_.visible)

    @staticmethod
    @step("Проверка, что текст отображается")
    def check_text_is_visible(text: str):
        browser.element(by.partial_text(text)).should(be.visible)

    @staticmethod
    @step("Проверка, что текст не отображается")
    def check_text_is_not_visible(text: str):
        browser.element(by.partial_text(text)).should(be.not_.visible)

    @staticmethod
    @step("Проверка, что элемент содержит текст")
    def check_element_contains_text(element, text: str):
        if isinstance(element, str):
            element = browser.element(element)
        element.should(be.visible).should(have.text(text))

    @staticmethod
    @step("Клик по элементу с id")
    def click_on_id(test_id: str):
        element = browser.element(f'[id="{test_id}"]')
        element.should(be.visible).hover().click()

    @staticmethod
    @step("Правый клик по элементу")
    def right_click(element):
        if isinstance(element, str):
            element = browser.element(element)
        element.should(be.visible).hover().context_click()

    @staticmethod
    @step("Открытие страницы")
    def open_page(url=None):
        browser.open(url or config.base_url)

    @staticmethod
    @step("Передвижение слайдера")
    def move_slider(element):
        driver = webdriver.Chrome()
        element = driver.find_element(By.XPATH, element) if isinstance(element, str) else element
        action_chains = ActionChains(driver)
        action_chains.click_and_hold(element).move_by_offset(xoffset=200, yoffset=0).release().perform()

    @staticmethod
    @step("Очистка поля ввода")
    def clear_input_field(element):
        if isinstance(element, str):
            element = browser.element(element)
        element.should(be.visible).hover().send_keys(Keys.CONTROL + 'a').send_keys(Keys.BACKSPACE)
