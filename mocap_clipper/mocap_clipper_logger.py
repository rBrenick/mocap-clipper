import logging

LOGGER_CLS = logging.getLogger("mocap_clipper")
LOGGER_CLS.setLevel(logging.DEBUG)


def get_logger():
    return LOGGER_CLS
