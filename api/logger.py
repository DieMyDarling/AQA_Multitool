import datetime
import os
import logging
from allure import step
from requests import Response


class Logger:
    instance = None
    logger = None
    path = "logger.log"
    data = ""

    def __init__(self):
        """
        Инициализация объекта логгера.

        Создает и настраивает логгер, который записывает логи в файл.
        Если файл лога уже существует, он будет удален перед созданием нового логгера.
        """

        if os.path.exists(self.path):
            os.remove(self.path)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        handler = logging.FileHandler(self.path)
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    @classmethod
    def get_instance(cls):
        """
        Получить экземпляр логгера.

        Если экземпляр логгера уже существует, возвращает его. Если нет, создает новый экземпляр и возвращает его.

        Возвращает:
            Logger: Экземпляр логгера.
        """

        if cls.instance is None:
            cls.instance = cls()

        return cls.instance

    @step("{method} request to {url}")
    def add_request(self, url: str, data: dict, headers: dict, cookies: dict, method: str):
        """
        Добавить информацию о запросе в лог.

        Аргументы:
            url (str): URL запроса.
            data (dict): Данные запроса.
            headers (dict): Заголовки запроса.
            cookies (dict): Куки запроса.
            method (str): Метод запроса.
        """

        data_to_add = f"\n-----\n"
        data_to_add += f"[{str(datetime.datetime.now())}] Метод запроса: {method}\n"
        data_to_add += f"[{str(datetime.datetime.now())}] URL запроса: {url}\n"
        data_to_add += f"[{str(datetime.datetime.now())}] Данные запроса: {data}\n"
        data_to_add += f"[{str(datetime.datetime.now())}] Заголовки запроса: {headers}\n"
        data_to_add += f"[{str(datetime.datetime.now())}] Куки запроса: {cookies}"
        data_to_add += "\n"

        self.data += data_to_add
        self.logger.info(data_to_add)

    def add_response(self, response: Response):
        """
        Добавить информацию о ответе в лог.

        Аргументы:
            response (Response): Объект ответа.
        """

        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"\n"
        data_to_add += f"[{str(datetime.datetime.now())}] Код ответа: {response.status_code}\n"
        data_to_add += f"[{str(datetime.datetime.now())}] Текст ответа: {response.text}\n"
        data_to_add += f"[{str(datetime.datetime.now())}] Заголовки ответа: {headers_as_dict}\n"
        data_to_add += f"[{str(datetime.datetime.now())}] Куки ответа: {cookies_as_dict}"
        data_to_add += "\n-----\n"

        self.data += data_to_add
        self.logger.info(data_to_add)

    def clear_data(self):
        """
        Очистить данные лога.

        Удаляет все сохраненные данные лога.
        """

        self.data = ""

    def show_all_data(self):
        """
        Показать все данные лога.

        Если в логе есть данные, выводит их на экран.
        """

        if len(self.data) > 0:
            print("\n\nSTART OF LOG")
            print(self.data)
            print("END OF LOG\n\n")

    def write_log_to_file(self):
        """
        Записать лог в файл.

        Записывает сохраненные данные лога в файл лога.
        """

        with open(self.path, 'a', encoding='utf-8') as logger_file:
            test_name = os.environ.get('PYTEST_CURRENT_TEST')
            logger_file.write(f"START TEST {test_name}\n")
            logger_file.write(self.data)
            logger_file.write(f"\nEND TEST {test_name}\n\n")
            self.clear_data()
