import logging


class Logs:
    def __init__(self):
        self.logger = logging.getLogger(name="test")
        self.logger.setLevel(logging.DEBUG)

        self.fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.Formater = logging.Formatter(self.fmt)
        self.file_handler = logging.FileHandler("log_information.log")
        self.file_handler.setFormatter(self.Formater)
        self.logger.addHandler(self.file_handler)

        # self.logException()

    def logException(self, exception):
        self.logger.exception(str(exception))


if __name__ == "__main__":
    Logs().logException("error")
