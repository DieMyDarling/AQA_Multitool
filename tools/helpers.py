import random
import string


class Tool:
    @staticmethod
    def random_string(prefix=None, max_len=None):
        """
        Генерирует случайную строку заданной длины.

        :param prefix: Префикс, который будет добавлен в начало сгенерированной строки.
        :type prefix: str

        :param max_len: Максимальная длина сгенерированной строки.
        :type max_len: int

        :return: Случайно сгенерированная строка с добавленным префиксом.
        :rtype: str
        """
        symbols = string.ascii_letters + string.digits
        if prefix is None:
            prefix = 'test-'
        if max_len is None:
            max_len = 16
        return prefix + ''.join([random.choice(symbols) for i in range(max_len)]).lower()


tool = Tool()
