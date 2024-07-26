from urllib.parse import urljoin

import requests
from allure import step
from selene.api import browser

from tools.api.client import APIClientAsync
from tools.link_checker.link_processor import LinkProcessor


class LinkCheckerAsync(LinkProcessor):
    """
    Класс для проверки всех ссылок на странице и логирования битых ссылок с использованием асинхронного API клиента.
    """

    def __init__(self):
        self.client = APIClientAsync()

    @step('Проверка всех ссылок на странице')
    async def check_all_links(self, links, base_url):
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
                response, _ = await self.client.get(full_url)
                if response.status != 200:
                    broken_links.append((full_url, response.status))
                    self.log_broken_link(full_url, response.status)
        return broken_links

    async def check_links_on_page_with_selene(self, page_url):
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
        return await self.check_all_links(links, page_url)

    async def check_links_on_page_with_bs4(self, page_url):
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
        return await self.check_all_links(links, page_url)

    @step('Проверка отсутствия битых ссылок')
    def assert_no_broken_links(self, broken_links):
        """
        Проверяет отсутствие битых ссылок.

        :param broken_links: Список битых ссылок с кодами ответа.
        :type broken_links: list of tuples
        """
        assert not broken_links, f'Найдены битые ссылки: {broken_links}'
