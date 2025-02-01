"""


Author:
    Inspyre Softworks

Project:
    inSPy-Logger

File:
    inspy_logger/constants.py


Description:


"""


import logging
from rich.logging import RichHandler
from inspy_logger.utils import check_if_interactive


DEFAULT_LOGGING_LEVEL = logging.DEBUG

HANDLER_TYPES = {
        'console': RichHandler,
        'file': logging.FileHandler
        }

LEVEL_MAP = {
    'internal': 5,
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
    'fatal': logging.FATAL,
}
"""A mapping of level names to their corresponding logging levels."""


LEVELS = [level.upper() for level in LEVEL_MAP]

INTERNAL = LEVEL_MAP['debug'] - 5


INTERACTIVE_SESSION = check_if_interactive()
"""A flag to indicate whether the session is interactive."""
