import logging
import os
import pathlib

import platformdirs

logger = logging.getLogger(__name__)
APP_NAME = "xxfer"


class LogFile:

    logname = f"{APP_NAME}.log"
    dir = platformdirs.user_log_path(APP_NAME)

    def __init__(self):
        self.LOGFILE = pathlib.Path.joinpath(self.dir, self.logname).resolve()

    def make_log_directory(self):
        """Create logfile directory if it does not exist"""
        if self.LOGFILE.exists() == False:
            logger.debug(f"Making Log directory: {self.dir}")
            os.makedirs(self.dir, exist_ok=True)
        else:
            pass
