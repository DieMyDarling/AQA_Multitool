import json
import logging

import aiohttp
import allure
import requests

from environments import env


class APIClient:

    def __init__(self, api_url=env.api_portal_url, api_key=env.api_key, bearer=None):
        """
        Инициализация клиента API.

        Args:
            api_url (str): URL API.
            api_key (str): Ключ API.
            bearer (str): Токен для авторизации.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.bearer = bearer
        self.headers = {'Content-Type': 'application/json'}

        if self.api_key is not None:
            self.headers['x-app-key'] = self.api_key
        if self.bearer is not None:
            self.headers['Authorization'] = f'Bearer {self.bearer}'

        self.session = requests.Session()

    def get(self, endpoint='', params=None, headers=None):
        """
        Выполняет GET-запрос к API.

        Args:
            endpoint (str): Расширение URL для GET-запроса.
            params (dict): Параметры запроса.
            headers (dict): Заголовки запроса.

        Returns:
            requests.Response: Объект ответа от сервера или None в случае ошибки.
        """
        url = self.api_url + endpoint
        headers = self.headers

        with allure.step(f"Выполнение GET-запроса. URL: {url}"):
            try:
                response = self.session.get(url, params=params, headers=headers)
                response.raise_for_status()  # Вызывает исключение для статусных кодов 4xx и 5xx
                return response
            except requests.exceptions.RequestException as e:
                logging.error(f"Ошибка при выполнении GET-запроса: {e}")
                allure.attach(str(e), name="Ошибка GET-запроса", attachment_type=allure.attachment_type.TEXT)
                return None

    def post(self, endpoint='', data=None):
        """
        Выполняет POST-запрос к API.

        Args:
            endpoint (str): Расширение URL для POST-запроса.
            data (dict): Данные запроса.

        Returns:
            requests.Response: Объект ответа от сервера или None в случае ошибки.
        """
        url = self.api_url + endpoint
        headers = self.headers

        with allure.step(f"Выполнение POST-запроса. URL: {url}"):
            try:
                response = self.session.post(url, json=data, headers=headers)
                response.raise_for_status()  # Вызывает исключение для статусных кодов 4xx и 5xx
                return response
            except requests.exceptions.RequestException as e:
                logging.error(f"Ошибка при выполнении POST-запроса: {e}")
                allure.attach(str(e), name="Ошибка POST-запроса", attachment_type=allure.attachment_type.TEXT)
                return None

    def put(self, url=None, data=None, cookies=None):
        """
        Выполняет PUT-запрос к API.

        Args:
            url (str): URL для PUT-запроса.
            data (dict): Данные запроса.
            cookies (dict): Куки запроса.

        Returns:
            requests.Response: Объект ответа от сервера.
        """
        url = self.api_url + url
        headers = self.headers

        if url is None:
            url = self.api_url

        with allure.step(f"Выполнение PUT-запроса. URL: {url}"):
            response = self._send(url, data, headers, cookies, 'PUT')
            return response

    def patch(self, endpoint='', data=None):
        """
        Выполняет PATCH-запрос к API.

        Args:
            endpoint (str): Расширение URL для PATCH-запроса.
            data (dict): Данные запроса.

        Returns:
            requests.Response: Объект ответа от сервера или None в случае ошибки.
        """
        url = self.api_url + endpoint
        headers = self.headers

        with allure.step(f"Выполнение PATCH-запроса. URL: {url}"):
            try:
                response = self.session.patch(url, json=data, headers=headers)
                response.raise_for_status()  # Вызывает исключение для статусных кодов 4xx и 5xx
                return response
            except requests.exceptions.RequestException as e:
                logging.error(f"Ошибка при выполнении PATCH-запроса: {e}")
                allure.attach(str(e), name="Ошибка PATCH-запроса", attachment_type=allure.attachment_type.TEXT)
                return None

    def _send(self, url, data, headers, cookies, method, params=None):
        """
        Вспомогательный метод для отправки запроса к API.

        Args:
            url (str): URL для запроса.
            data (dict): Данные запроса.
            headers (dict): Заголовки запроса.
            cookies (dict): Куки запроса.
            method (str): Метод HTTP.
            params (dict): Параметры запроса.

        Returns:
            requests.Response: Объект ответа от сервера или None в случае ошибки.
        """
        if not headers:
            headers = {}

        if self.api_key is not None:
            self.headers['x-app-key'] = self.api_key
            self.headers['Content-Type'] = 'application/json'
        if self.bearer is not None:
            self.headers['Authorization'] = f'Bearer {self.bearer}'
            self.headers['Content-Type'] = 'application/json'

        if not cookies:
            cookies = {}

        with allure.step(f"Отправка {method}-запроса. URL: {url}"):
            try:
                if method == 'GET':
                    response = requests.get(url, params=params, headers=headers, cookies=cookies)
                elif method == 'POST':
                    response = requests.post(url, json=data, headers=headers, cookies=cookies)
                elif method == 'PUT':
                    response = requests.put(url, data=json.dumps(data), headers=headers, cookies=cookies)
                elif method == 'PATCH':
                    response = requests.patch(url, json=data, headers=headers, cookies=cookies)
                else:
                    raise Exception(f'Недопустимый метод HTTP: "{method}"')
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                logging.error(f"Ошибка при выполнении запроса: {e}")
                allure.attach(str(e), name=f"Ошибка {method}-запроса", attachment_type=allure.attachment_type.TEXT)
                return None

    def get_cookie(self, response, cookie_name):
        """
        Получает значение куки из ответа.

        Args:
            response (requests.Response): Объект ответа от сервера.
            cookie_name (str): Имя куки.

        Returns:
            str: Значение куки.

        Raises:
            AssertionError: Если указанная куки не найдена в ответе.
        """
        with allure.step(f"Получение значения куки: {cookie_name}"):
            assert cookie_name in response.cookies, f"Не удается найти куки с именем {cookie_name} в последнем ответе"
            return response.cookies[cookie_name]

    def get_header(self, response, header_name):
        """
        Получает значение заголовка из ответа.

        Args:
            response (requests.Response): Объект ответа от сервера.
            header_name (str): Имя заголовка.

        Returns:
            str: Значение заголовка.

        Raises:
            AssertionError: Если указанный заголовок не найден в ответе.
        """
        with allure.step(f"Получение значения заголовка: {header_name}"):
            assert header_name in response.headers, f"Не удается найти заголовок с именем {header_name} в последнем ответе"
            return response.headers[header_name]

    def get_json_value(self, response, key):
        """
        Получает значение из JSON-ответа по ключу.

        Args:
            response (requests.Response): Объект ответа от сервера.
            key (str): Ключ значения в JSON-ответе.

        Returns:
            Any: Значение из JSON-ответа по указанному ключу.

        Raises:
            AssertionError: Если ответ не является JSON или не содержит указанного ключа.
        """
        with allure.step(f"Получение значения из JSON-ответа по ключу: {key}"):
            try:
                response_dict = response.json()
            except json.decoder.JSONDecodeError:
                assert False, f"Ответ не в формате JSON. Текст ответа: '{response.text}'"

            assert key in response_dict, f"JSON ответа не содержит ключа '{key}'"

            return response_dict[key]


class APIClientAsync:

    def __init__(self, api_url=env.api_portal_url, api_key=env.api_key, bearer=None):
        """
        Инициализация асинхронного клиента API.

        Args:
            api_url (str): URL API.
            api_key (str): Ключ API.
            bearer (str): Токен для авторизации.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.bearer = bearer
        self.headers = {'Content-Type': 'application/json'}

        if self.api_key is not None:
            self.headers['x-app-key'] = self.api_key
        if self.bearer is not None:
            self.headers['Authorization'] = f'Bearer {self.bearer}'

    async def _request(self, method, endpoint, data=None):
        url = self.api_url + endpoint
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, json=data, headers=self.headers) as response:
                response_data = await response.json()
                return response, response_data

    async def get(self, endpoint=''):
        return await self._request('GET', endpoint)

    async def post(self, endpoint='', data=None):
        return await self._request('POST', endpoint, data)

    async def delete(self, endpoint=''):
        return await self._request('DELETE', endpoint)


"""
# Пример использования синхронного клиента:
api_url = 'https://api.example.com'
api_key = 'your-api-key'

# Создание экземпляра клиента
client = APIClient(api_url=api_url, api_key=api_key)

# Подготовка данных для POST-запроса
payload = {
    'name': 'John Doe',
    'email': 'johndoe@example.com',
    'message': 'Hello, world!'
}

# Отправка POST-запроса
response = client.post(endpoint='/messages', data=payload)

if response is not None:
    if response.status_code == 201:
        print('Сообщение успешно отправлено!')
    else:
        print(f'Ошибка при отправке сообщения. Код статуса: {response.status_code}')
else:
    print('Ошибка при выполнении POST-запроса.')


# Пример использования асинхронного клиента:
async def main():
    api_url = 'https://api.example.com'
    api_key = 'your-api-key'

    client = APIClientAsync(api_url=api_url, api_key=api_key)

    payload = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'message': 'Hello, world!'
    }

    response, response_data = await client.post(endpoint='/messages', data=payload)

    if response.status == 201:
        print('Сообщение успешно отправлено!')
    else:
        print(f'Ошибка при отправке сообщения. Код статуса: {response.status}')
"""
