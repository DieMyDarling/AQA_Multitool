import allure
import pytest

from tools.web import web


@pytest.mark.regression
@allure.severity(allure.severity_level.NORMAL)
@allure.title('Basic scenario')
@allure.description('Basic scenario')
@allure.testcase('', '')
@allure.link('', '')
@allure.issue('', '')
def test_web_demo():
    web.login_page.open()
    web.login_page.fill_auth_form()
    web.login_page.press_login_button()
