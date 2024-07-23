import allure

from tools.api.client import APIClient


@allure.feature('API Tests')
@allure.story('Create and Retrieve User')
def test_create_and_retrieve_user():
    api_url = 'https://api.example.com'
    api_key = 'your-api-key'

    client = APIClient(api_url=api_url, api_key=api_key)

    new_user = {
        'name': 'John Doe',
        'email': 'johndoe@example.com'
    }

    with allure.step("Создание нового пользователя"):
        create_response = client.post(endpoint='/users', data=new_user)
        assert create_response is not None, 'Ответ на POST-запрос пустой'
        assert create_response.status_code == 201, f'Не удалось создать пользователя. Код статуса: {create_response.status_code}'
        user_id = create_response.json().get('id')

    with allure.step("Получение списка пользователей"):
        get_response = client.get(endpoint='/users')
        assert get_response is not None, 'Ответ на GET-запрос пустой'
        assert get_response.status_code == 200, f'Не удалось получить список пользователей. Код статуса: {get_response.status_code}'

    with allure.step("Проверка, что новый пользователь в списке пользователей"):
        users = get_response.json()
        user_emails = [user['email'] for user in users]
        assert new_user['email'] in user_emails, 'Новый пользователь не найден в списке пользователей'


@allure.feature('API Tests')
@allure.story('Negative Tests')
def test_create_user_without_required_fields():
    api_url = 'https://api.example.com'
    api_key = 'your-api-key'

    client = APIClient(api_url=api_url, api_key=api_key)

    incomplete_user = {
        'name': 'John Doe'
    }

    with allure.step("Попытка создать пользователя без обязательного поля email"):
        create_response = client.post(endpoint='/users', data=incomplete_user)
        assert create_response is not None, 'Ответ на POST-запрос пустой'
        assert create_response.status_code == 400, f'Ожидался статус 400, но получен {create_response.status_code}'


@allure.feature('API Tests')
@allure.story('Negative Tests')
def test_create_user_with_existing_email():
    api_url = 'https://api.example.com'
    api_key = 'your-api-key'

    client = APIClient(api_url=api_url, api_key=api_key)

    existing_user = {
        'name': 'Jane Doe',
        'email': 'johndoe@example.com'  # Используем email, который уже существует
    }

    with allure.step("Попытка создать пользователя с уже существующим email"):
        create_response = client.post(endpoint='/users', data=existing_user)
        assert create_response is not None, 'Ответ на POST-запрос пустой'
        assert create_response.status_code == 409, f'Ожидался статус 409, но получен {create_response.status_code}'


@allure.feature('API Tests')
@allure.story('Negative Tests')
def test_get_users_with_invalid_api_key():
    api_url = 'https://api.example.com'
    invalid_api_key = 'invalid-api-key'

    client = APIClient(api_url=api_url, api_key=invalid_api_key)

    with allure.step("Попытка получить список пользователей с неверным API ключом"):
        get_response = client.get(endpoint='/users')
        assert get_response is not None, 'Ответ на GET-запрос пустой'
        assert get_response.status_code == 403, f'Ожидался статус 403, но получен {get_response.status_code}'
