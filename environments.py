import json
import sys

from pydantic import BaseModel


class Environments(BaseModel):
    web_url: str
    api_key: str
    api_url: str


def open_config():
    # Инициировать переменную command_line_env значением None.
    command_line_env = None

    # Проверить наличие опции командной строки --env в списке sys.argv.
    if "--env" in sys.argv:
        # Найти индекс опции --env в списке sys.argv.
        env_index = sys.argv.index("--env")
        if env_index + 1 < len(sys.argv):
            # Если следующий элемент после --env существует, назначить его значение переменной command_line_env.
            command_line_env = sys.argv[env_index + 1]

    # Если command_line_env остается None (не быть установленной), установить значение на 'master' по умолчанию.
    if command_line_env is None:
        command_line_env = 'env_main'

    # Сформировать путь к файлу конфигурации, используя значение command_line_env.
    config_path = f'./config/{command_line_env}.json'

    # Открыть и загрузить JSON-файл конфигурации.
    with open(config_path) as json_file:
        config = json.load(json_file)

    # Вернуть загруженную конфигурацию.
    return config


data = open_config()

environment = Environments(**data)


class ENV:
    web_url = environment.web_url
    api_key = environment.api_key
    api_url = environment.api_portal_url


env = ENV()
