import logging


class BotLogger:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger()
        self.logger

    def info(self, msg: str):
        self.logger.info(msg)

    def warn(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)
