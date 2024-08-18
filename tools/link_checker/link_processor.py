from allure import step
from bs4 import BeautifulSoup
from selene.api import browser
from selenium.webdriver.common.by import By


class LinkProcessor:
    """
    Класс для обработки списков ссылок.
    """

    @staticmethod
    @step('Получение всех ссылок на странице с использованием selene')
    def get_all_links_with_selene():
        """
        Получает все ссылки на текущей веб-странице с использованием selene.

        :returns: Список всех найденных ссылок на странице.
        :rtype: list
        """
        elements = browser.driver.find_elements(By.TAG_NAME, 'a')
        links = [element.get_attribute('href') for element in elements]
        return links

    @staticmethod
    @step('Получение всех ссылок на странице с использованием BeautifulSoup')
    def get_all_links_with_bs4(html_content):
        """
        Получает все ссылки из HTML-контента с использованием BeautifulSoup.

        :param html_content: HTML-контент страницы.
        :type html_content: str
        :returns: Список всех найденных ссылок в HTML.
        :rtype: list
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        return links

    @staticmethod
    @step('Логирование битых ссылок')
    def log_broken_link(url, status_code):
        """
        Записывает битую ссылку в файл broken_links.txt.

        :param url: Битая ссылка.
        :type url: str
        :param status_code: Код ответа HTTP.
        :type status_code: int
        """
        with open('broken_links.txt', 'a') as f:
            f.write(f'{url} - {status_code}\n')
