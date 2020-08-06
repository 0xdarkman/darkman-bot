import logging


class Logger:
    def __init__(self, name='default', level=logging.DEBUG, file_path=None):
        self.__set_logger(name, level)
        # self.__set_file_handler(file_path)
        self.__set_stream_handler()

    def __set_logger(self, name, level):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    @staticmethod
    def __get_formatter():
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def __set_file_handler(self, file_path):
        fh = logging.FileHandler(file_path, 'w+')
        fh.setFormatter(self.__get_formatter())
        self.logger.addHandler(fh)

    def __set_stream_handler(self):
        sh = logging.StreamHandler()
        sh.setFormatter(self.__get_formatter())
        self.logger.addHandler(sh)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)