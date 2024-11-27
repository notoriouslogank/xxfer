import logging

from src.configs.constants import Constants

constants = Constants("xxfer", "notoriouslogank")
LOGFILE = constants.LOGFILE
APP_NAME = constants.APP_NAME
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:Line %(lineno)s\n%(message)s")
file_handler = logging.FileHandler(f"{LOGFILE}", "a")
