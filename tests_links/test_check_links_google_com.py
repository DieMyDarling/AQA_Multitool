import pytest
import allure

from tools.link_checker.cheker import LinkCheckerFactory

link_checker = LinkCheckerFactory.create_checker('async')


@allure.epic('Проверка всех ссылок на странице с использованием selene')
@pytest.mark.asyncio
@pytest.mark.parametrize("page_url", [
    "https://www.google.com",
    "https://example.com"
])
async def test_check_all_links_with_selene(page_url):
    """
    Тест для проверки всех ссылок на странице с использованием selene.
    """
    broken_links = await link_checker.check_links_on_page_with_selene(page_url)
    link_checker.assert_no_broken_links(broken_links)


@allure.epic('Проверка всех ссылок на странице с использованием BeautifulSoup')
@pytest.mark.asyncio
@pytest.mark.parametrize("page_url", [
    "https://www.google.com",
    "https://example.com"
])
async def test_check_all_links_with_bs4(page_url):
    """
    Тест для проверки всех ссылок на странице с использованием BeautifulSoup.
    """
    broken_links = await link_checker.check_links_on_page_with_bs4(page_url)
    link_checker.assert_no_broken_links(broken_links)
