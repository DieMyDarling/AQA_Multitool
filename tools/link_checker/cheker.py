from tools.link_checker.link_checker_async import LinkCheckerAsync
from tools.link_checker.link_checker_old import LinkCheckerOld
from tools.link_checker.link_checker_sync import LinkCheckerSync


class LinkCheckerFactory:
    """
    Фабрика для создания экземпляров LinkChecker в зависимости от переданного флага.
    """

    @staticmethod
    def create_checker(checker_type):
        """
        Создает экземпляр LinkChecker в зависимости от переданного флага.

        :param checker_type: Тип чекера ('old', 'sync' или 'async').
        :type checker_type: str
        :returns: Экземпляр LinkChecker.
        :rtype: LinkCheckerOld or LinkCheckerSync or LinkCheckerAsync
        """
        if checker_type == 'old':
            return LinkCheckerOld()
        elif checker_type == 'sync':
            return LinkCheckerSync()
        elif checker_type == 'async':
            return LinkCheckerAsync()
        else:
            raise ValueError(f'Неизвестный тип чекера: {checker_type}')


checker = LinkCheckerFactory.create_checker('async')
