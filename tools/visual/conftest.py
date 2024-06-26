import logging

import pytest
from selene.support.shared import browser
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

driver = browser.driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    rep = outcome.get_result()
    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    extra = getattr(rep, 'extra', [])

    setattr(item, "rep_" + rep.when, rep)
    if rep.when == "call" and rep.failed:
        _gather_screenshot(item, driver, extra)
        rep.extra = extra
    return rep


@pytest.fixture(scope="function", autouse=True)
def browser_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    logger.info("browser version: %s" % browser.driver.capabilities['browserVersion'])

    yield browser_driver
    driver.delete_all_cookies()
    driver.quit()
    logger.info('close driver now')


@pytest.fixture(scope='function')
def screenshots_cache(request):
    request.config.screenshots_cache = {"production": None, "staging": None, "diff": None}
    return request.config.screenshots_cache


def _gather_screenshot(item, browser_driver, extra):
    request = getattr(item, '_request', None)
    pytest_html = item.config.pluginmanager.getplugin('html')
    diff = item.config.screenshots_cache['diff'].decode()
    prod = item.config.screenshots_cache['production'].decode()
    staging = item.config.screenshots_cache['staging'].decode()

    if pytest_html is not None:
        extra.append(pytest_html.extras.image(prod, 'Screenshot of production'))
        extra.append(pytest_html.extras.image(staging, 'Screenshot of staging'))
        extra.append(pytest_html.extras.image(diff, 'Difference'))
