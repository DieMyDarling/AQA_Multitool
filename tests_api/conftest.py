import subprocess
import time
import pytest

@pytest.fixture(scope="session", autouse=True)
def start_server():
    """
    Фикстура, которая запускает Flask-сервер перед началом тестирования,
    а после завершения тестов гарантированно завершает процесс сервера.
    Предполагается, что сервер запускается из файла app.py.
    """

    server_process = subprocess.Popen(
        ["python", "./server/server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Ждём, чтобы сервер точно запустился
    time.sleep(1)
    try:
        yield
    finally:
        server_process.terminate()
        server_process.wait()
