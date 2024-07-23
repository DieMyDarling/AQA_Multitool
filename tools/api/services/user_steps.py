import allure
from http import HTTPStatus
from tools.api.client import APIClientAsync


class UserSteps:

    def __init__(self, api_url, api_key, bearer=None):
        """
        Инициализация API-шагов.

        Args:
            api_url (str): URL API.
            api_key (str): Ключ API.
            bearer (str): Токен для авторизации.
        """
        self.client = APIClientAsync(api_url=api_url, api_key=api_key, bearer=bearer)

    @allure.step("Создание нового пользователя с данными: {user_data}")
    async def create_user(self, user_data):
        """
        Шаг для создания нового пользователя.

        Args:
            user_data (dict): Данные пользователя.

        Returns:
            dict: Данные созданного пользователя.
        """
        response, response_data = await self.client.post(endpoint='/users', data=user_data)
        assert response.status == HTTPStatus.CREATED, f'Не удалось создать пользователя. Код статуса: {response.status}'
        return response_data

    @allure.step("Получение списка пользователей")
    async def get_users(self):
        """
        Шаг для получения списка пользователей.

        Returns:
            list: Список пользователей.
        """
        response, response_data = await self.client.get(endpoint='/users')
        assert response.status == HTTPStatus.OK, f'Не удалось получить список пользователей. Код статуса: {response.status}'
        return response_data

    @allure.step("Получение пользователя по ID: {user_id}")
    async def get_user_by_id(self, user_id):
        """
        Шаг для получения пользователя по ID.

        Args:
            user_id (str): ID пользователя.

        Returns:
            dict: Данные пользователя.
        """
        response, response_data = await self.client.get(endpoint=f'/users/{user_id}')
        assert response.status == HTTPStatus.OK, f'Не удалось получить пользователя. Код статуса: {response.status}'
        return response_data

    @allure.step("Удаление пользователя с ID: {user_id}")
    async def delete_user(self, user_id):
        """
        Шаг для удаления пользователя по ID.

        Args:
            user_id (str): ID пользователя.

        Returns:
            None
        """
        response, _ = await self.client.delete(endpoint=f'/users/{user_id}')
        assert response.status == HTTPStatus.NO_CONTENT, f'Не удалось удалить пользователя. Код статуса: {response.status}'

    @allure.step("Попытка создания пользователя с данными: {user_data} и ожидание ошибки")
    async def create_user_expect_failure(self, user_data, expected_status):
        """
        Шаг для попытки создания пользователя и ожидания ошибки.

        Args:
            user_data (dict): Данные пользователя.
            expected_status (HTTPStatus): Ожидаемый HTTP статус ошибки.

        Returns:
            requests.Response: Ответ сервера на запрос создания пользователя.
        """
        response, _ = await self.client.post(endpoint='/users', data=user_data)
        assert response.status == expected_status, f'Ожидался статус {expected_status}, но получен {response.status}'
        return response

    @allure.step("Попытка получения списка пользователей с неверным API ключом и ожидание ошибки")
    async def get_users_expect_failure(self):
        """
        Шаг для попытки получения списка пользователей с неверным API ключом и ожидания ошибки.

        Returns:
            requests.Response: Ответ сервера на запрос списка пользователей.
        """
        response, _ = await self.client.get(endpoint='/users')
        assert response.status == HTTPStatus.FORBIDDEN, f'Ожидался статус {HTTPStatus.FORBIDDEN}, но получен {response.status}'
        return response


user_steps = UserSteps(api_url='https://api.example.com', api_key='your-api-key')
