import logging
import sys
from colorlog import ColoredFormatter

LOG_FORMAT = "%(log_color)s%(asctime)s [%(levelname)s]%(reset)s %(white)s%(message)s"

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(ColoredFormatter(LOG_FORMAT))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)

