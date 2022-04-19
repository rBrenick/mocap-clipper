import logging

LOGGER_CLS = logging.getLogger("mocap_clipper")
LOGGER_CLS.setLevel(logging.INFO)


def get_logger():
    return LOGGER_CLS


def get_log_level_options():
    return {
        logging.getLevelName(logging.DEBUG): logging.DEBUG,
        logging.getLevelName(logging.INFO): logging.INFO,
        logging.getLevelName(logging.WARNING): logging.WARNING,
    }

