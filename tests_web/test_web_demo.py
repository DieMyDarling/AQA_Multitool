import pytest

from tools.web import web


@pytest.mark.regression
def test_web_demo():
    web.login_page.open()
    web.login_page.fill_auth_form()
    web.login_page.press_login_button()


@pytest.mark.regression
def test_web_demo_fail():
    web.login_page.open()
    web.login_page.fill_auth_form(password='wrong_password')
    web.login_page.press_login_button()
