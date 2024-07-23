from http import HTTPStatus

import allure
import pytest

from tools.api.services.user_steps import user_steps, UserSteps


@allure.feature('API Tests')
@allure.story('Create and Retrieve User')
@pytest.mark.asyncio
async def test_create_and_retrieve_user():
    """
    Тест-кейс: Создание и получение пользователя

    Шаги:
    1. Создать нового пользователя с именем 'John Doe' и email 'johndoe@example.com'.
    2. Получить список пользователей.
    3. Проверить, что созданный пользователь присутствует в списке пользователей.

    Ожидаемый результат:
    - Новый пользователь должен быть успешно создан.
    - Новый пользователь должен быть найден в списке пользователей.
    """
    new_user = {
        'name': 'John Doe',
        'email': 'johndoe@example.com'
    }

    created_user = await user_steps.create_user(new_user)
    user_id = created_user.get('id')

    users = await user_steps.get_users()
    user_emails = [user['email'] for user in users]
    assert new_user['email'] in user_emails, 'Новый пользователь не найден в списке пользователей'


@allure.feature('API Tests')
@allure.story('Create and Delete User')
@pytest.mark.asyncio
async def test_create_and_delete_user():
    """
    Тест-кейс: Создание и удаление пользователя

    Шаги:
    1. Создать нового пользователя с именем 'Jane Smith' и email 'janesmith@example.com'.
    2. Удалить созданного пользователя.
    3. Проверить, что пользователь был успешно удален.

    Ожидаемый результат:
    - Новый пользователь должен быть успешно создан.
    - Новый пользователь должен быть успешно удален.
    - Попытка получения удаленного пользователя должна вернуть ответ о том, что пользователь не найден.
    """
    new_user = {
        'name': 'Jane Smith',
        'email': 'janesmith@example.com'
    }

    created_user = await user_steps.create_user(new_user)
    user_id = created_user.get('id')

    await user_steps.delete_user(user_id)

    response = await user_steps.get_user_by_id(user_id)
    assert response is None, 'Пользователь не был удален'


@allure.feature('API Tests')
@allure.story('Negative Tests')
@pytest.mark.asyncio
async def test_create_user_without_required_fields():
    """
    Тест-кейс: Попытка создания пользователя без обязательного поля email

    Шаги:
    1. Попытаться создать пользователя с именем 'John Doe' без указания email.

    Ожидаемый результат:
    - Запрос на создание пользователя должен завершиться ошибкой с кодом 400 (Bad Request).
    """
    incomplete_user = {
        'name': 'John Doe'
    }

    await user_steps.create_user_expect_failure(incomplete_user, HTTPStatus.BAD_REQUEST)


@allure.feature('API Tests')
@allure.story('Negative Tests')
@pytest.mark.asyncio
async def test_create_user_with_existing_email():
    """
    Тест-кейс: Попытка создания пользователя с уже существующим email

    Шаги:
    1. Попытаться создать пользователя с именем 'Jane Doe' и email 'johndoe@example.com', который уже существует.

    Ожидаемый результат:
    - Запрос на создание пользователя должен завершиться ошибкой с кодом 409 (Conflict).
    """
    existing_user = {
        'name': 'Jane Doe',
        'email': 'johndoe@example.com'  # Используем email, который уже существует
    }

    await user_steps.create_user_expect_failure(existing_user, HTTPStatus.CONFLICT)


@allure.feature('API Tests')
@allure.story('Negative Tests')
@pytest.mark.asyncio
async def test_get_users_with_invalid_api_key():
    """
    Тест-кейс: Попытка получения списка пользователей с неверным API ключом

    Шаги:
    1. Использовать неверный API ключ для получения списка пользователей.

    Ожидаемый результат:
    - Запрос на получение списка пользователей должен завершиться ошибкой с кодом 403 (Forbidden).
    """
    invalid_user_steps = UserSteps(api_url='https://api.example.com', api_key='invalid-api-key')

    await invalid_user_steps.get_users_expect_failure()
