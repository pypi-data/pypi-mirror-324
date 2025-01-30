import logging

STEP = "STEP"
INFO = "INFO"
ERROR = "ERROR"
DEBUG = "DEBUG"


def step(self, message, *args, **kwargs):
    self._log(15, message, args, **kwargs)


def success(self, message, *args, **kwargs):
    self._log(16, message, args, **kwargs)


logging.Logger.step = step
logging.Logger.success = success


class CustomFormatter(logging.Formatter):
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    RESET = "\033[0m"
    formatting = (
        "%(asctime)s - %(module)s:%(name)s - "
        "%(filename)s:%(lineno)s - "
        "%(funcName)s() - %(levelname)s - %(message)s"
    )

    logging.addLevelName(15, "STEP")
    logging.addLevelName(16, "SUCCESS")
    logging.STEP = 15
    logging.SUCCESS = 16

    FORMATS = {
        logging.DEBUG: MAGENTA + formatting + RESET,
        logging.INFO: YELLOW + formatting + RESET,
        logging.STEP: BLUE + formatting + RESET,
        logging.SUCCESS: GREEN + formatting + RESET,
        logging.ERROR: RED + formatting + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)


def logger_instance():
    return Logger.logger
