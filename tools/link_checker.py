import requests
from allure import step
from selene.api import browser
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class LinkChecker:
    """
    Класс для проверки всех ссылок на странице и логирования битых ссылок.
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
    @step('Проверка доступности ссылки')
    def check_link(url):
        """
        Проверяет доступность ссылки с помощью HTTP-запроса.

        :param url: Ссылка для проверки.
        :type url: str
        :returns: HTTP-ответ на запрос.
        :rtype: requests.Response
        """
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            return e.response

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

    @step('Проверка всех ссылок на странице')
    def check_all_links(self, links, base_url):
        """
        Проверяет все ссылки на текущей веб-странице и логирует битые ссылки.

        :param links: Список ссылок для проверки.
        :type links: list
        :param base_url: Базовый URL для построения полных ссылок.
        :type base_url: str
        :returns: Список битых ссылок с кодами ответа.
        :rtype: list of tuples
        """
        broken_links = []
        for link in links:
            if link:
                full_url = urljoin(base_url, link)
                response = self.check_link(full_url)
                if response is None or response.status_code != 200:
                    status_code = response.status_code if response else 'No Response'
                    broken_links.append((full_url, status_code))
                    self.log_broken_link(full_url, status_code)
        return broken_links

    def check_links_on_page_with_selene(self, page_url):
        """
        Проверяет все ссылки на указанной странице с использованием selene и логирует битые ссылки.

        :param page_url: URL страницы для проверки.
        :type page_url: str
        :returns: Список битых ссылок с кодами ответа.
        :rtype: list of tuples
        """
        with step(f'Открытие страницы {page_url} для проверки ссылок с использованием selene'):
            browser.open(page_url)
        links = self.get_all_links_with_selene()
        return self.check_all_links(links, page_url)

    def check_links_on_page_with_bs4(self, page_url):
        """
        Проверяет все ссылки на указанной странице с использованием BeautifulSoup и логирует битые ссылки.

        :param page_url: URL страницы для проверки.
        :type page_url: str
        :returns: Список битых ссылок с кодами ответа.
        :rtype: list of tuples
        """
        with step(f'Открытие страницы {page_url} для проверки ссылок с использованием BeautifulSoup'):
            response = requests.get(page_url)
        assert response.status_code == 200, f'Не удалось открыть страницу: {page_url}'
        html_content = response.text
        links = self.get_all_links_with_bs4(html_content)
        return self.check_all_links(links, page_url)

    @step('Проверка отсутствия битых ссылок')
    def assert_no_broken_links(self, broken_links):
        """
        Проверяет отсутствие битых ссылок.

        :param broken_links: Список битых ссылок с кодами ответа.
        :type broken_links: list of tuples
        """
        assert not broken_links, f'Найдены битые ссылки: {broken_links}'


link_checker = LinkChecker()
