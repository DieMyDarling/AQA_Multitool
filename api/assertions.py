import json
import json.decoder

from requests import Response


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        """
        Проверить, что значение ключа JSON в ответе соответствует ожидаемому значению.

        Аргументы:
            response (Response): Объект ответа, содержащий JSON.
            name (str): Имя ключа JSON для проверки значения.
            expected_value (Any): Ожидаемое значение ключа JSON.
            error_message (str): Сообщение об ошибке, которое будет выдано в случае несоответствия.

        Исключения:
            AssertionError: Если ответ не в формате JSON.
            AssertionError: Если JSON не содержит указанный ключ.
            AssertionError: Если значение ключа JSON не соответствует ожидаемому значению.
        """

        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в формате JSON. Текст ответа: '{response.text}'"

        assert name in response_as_dict, f"JSON ответа не содержит ключа '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        """
        Проверить, что ключ JSON присутствует в ответе.

        Аргументы:
            response (Response): Объект ответа, содержащий JSON.
            name (str): Имя ключа JSON для проверки наличия.

        Исключения:
            AssertionError: Если ответ не в формате JSON.
            AssertionError: Если JSON не содержит указанный ключ.
        """

        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в формате JSON. Текст ответа: '{response.text}'"

        assert name in response_as_dict, f"JSON ответа не содержит ключа '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        """
        Проверить, что все указанные ключи JSON присутствуют в ответе.

        Аргументы:
            response (Response): Объект ответа, содержащий JSON.
            names (list): Список имен ключей JSON для проверки наличия.

        Исключения:
            AssertionError: Если ответ не в формате JSON.
            AssertionError: Если JSON не содержит хотя бы один из указанных ключей.
        """

        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в формате JSON. Текст ответа: '{response.text}'"

        for name in names:
            assert name in response_as_dict, f"JSON ответа не содержит ключа '{name}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        """
        Проверить, что ключ JSON отсутствует в ответе.

        Аргументы:
            response (Response): Объект ответа, содержащий JSON.
            name (str): Имя ключа JSON для проверки отсутствия.

        Исключения:
            AssertionError: Если ответ не в формате JSON.
            AssertionError: Если JSON содержит указанный ключ.
        """

        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в формате JSON. Текст ответа: '{response.text}'"

        assert name not in response_as_dict, f"JSON ответа не должен содержать ключ '{name}'. Однако он присутствует"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        """
        Проверить, что код статуса ответа соответствует ожидаемому значению.

        Аргументы:
            response (Response): Объект ответа.
            expected_status_code (int): Ожидаемый код статуса.

        Исключения:
            AssertionError: Если код статуса не соответствует ожидаемому значению.
        """

        assert response.status_code == expected_status_code, \
            f"Неожиданный код статуса! Ожидается: {expected_status_code}. Фактический: {response.status_code}"

    @staticmethod
    def assert_content(response: Response, expected_content):
        """
        Проверить, что содержимое ответа соответствует ожидаемому значению.

        Аргументы:
            response (Response): Объект ответа.
            expected_content (str): Ожидаемое содержимое ответа.

        Исключения:
            AssertionError: Если содержимое ответа не соответствует ожидаемому значению.
        """

        assert response.content.decode(
            "utf-8") == expected_content, f"Неожиданное содержимое ответа {response.content}."
