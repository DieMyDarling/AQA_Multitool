import allure
import pytest

import web


@pytest.mark.regression
@allure.severity(allure.severity_level.NORMAL)
@allure.title('Basic scenario')
@allure.description('Basic scenario')
@allure.testcase('', '')
@allure.link('', '')
@allure.issue('', '')
def test_basic():

    web.login_page.authorization()
