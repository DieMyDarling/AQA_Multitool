import json


class User:
    """
    Класс для представления пользователя.

    :param str username: Имя пользователя.
    :param str password: Пароль пользователя.
    """

    def __init__(self, username, password):
        self.username: str = username
        self.password: str = password

    @classmethod
    def from_json(cls, file_name: str = 'user_for_main'):
        """
        Создает экземпляр класса из JSON-файла.

        :param file_name: Имя JSON-файла без расширения.
        :return: Экземпляр класса User.
        """
        file_path = f'config/{file_name}.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        return cls(**data)


user_for_main = User.from_json(file_name='user_for_main')
