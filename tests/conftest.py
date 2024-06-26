import os
import allure
import pytest
from selene.api import browser, config
from selenium import webdriver
import environments


@pytest.fixture(scope='function', autouse=True)
def browser_chrome(request):
    """
    Фикстура для настройки Chrome браузера.
    Настраивает окно браузера с заданными размерами и опциями.

    :param request: Запрос фикстуры от pytest
    """
    # Настройка параметров браузера
    config.window_width = 1920
    config.window_height = 1080
    config.reports_folder = './.reports'
    config.base_url = environments.env.web_url
    config.timeout = 30

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')  # Отключаем "песочницу"
    options.add_argument('--disable-dev-shm-usage')  # Отключаем использование разделяемой памяти
    options.add_argument('--disable-gpu')  # Отключаем использование GPU
    options.add_argument('--ignore-ssl-errors=yes')  # Игнорируем ошибки SSL
    options.add_argument('--ignore-certificate-errors')  # Игнорируем ошибки сертификатов
    options.add_argument('--blink-settings=imagesEnabled=false')  # Блокировка загрузки изображений
    options.add_argument('--start-maximized')  # Открыть браузер на весь экран
    options.add_argument('--disable-infobars')  # Отключить инфо-панели

    yield browser

    # Устанавливаем finalizer для прикрепления скриншота, если он существует
    request.addfinalizer(attach_screenshot_if_exists)

    # Закрываем браузер и добавляем шаг в отчет
    with allure.step('Закрыть браузер'):
        browser.quit()


def attach_screenshot_if_exists():
    """
    Проверяет наличие скриншотов в папке отчетов и прикрепляет их к отчету.
    """
    if os.path.exists(config.reports_folder):
        try:
            files = os.listdir(config.reports_folder)
            png_files = [file for file in files if file.endswith('.png')]
            if png_files:
                newest_png = max(png_files, key=lambda x: os.path.getctime(os.path.join(config.reports_folder, x)))
                screenshot_path = os.path.join(config.reports_folder, newest_png)
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(image_file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            error_message = f'Произошла ошибка при прикреплении скриншота\n{str(e)}'
            with allure.step(error_message):
                print(error_message)


def pytest_addoption(parser):
    """
    Добавляем параметры командной строки для pytest.

    :param parser: Объект парсера аргументов командной строки
    """
    parser.addoption('--env', action='store', help='Описание окружения')


@pytest.fixture(scope='session', autouse=True)
def set_env(request):
    """
    Считываем параметр командной строки --env и устанавливаем окружение.

    :param request: Запрос фикстуры от pytest
    """
    environments.command_line_env = request.config.getoption("--env")
