import logging
import config

logger_level = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'error': logging.ERROR
}

logger = logging.getLogger()
logger.setLevel(logger_level.get(config.PYTHON_LOG_LEVEL, 'warning'))
