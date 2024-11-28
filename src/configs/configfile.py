import logging
import os
import pathlib

import platformdirs
import yaml

logger = logging.getLogger(__name__)
APP_NAME = "xxfer"


class ConfigFile:

    settings = {
        "SEPARATOR": "<SEPARATOR>",
        "BUFFER_SIZE": 4096,
        "HOST": "0.0.0.0",
        "PORT": 5002,
        "DOWNLOAD_DIR": "xxfer_received",
        "ARCHIVE_NAME": "xxfer.zip",
    }
    data = {"SETTINGS": settings}
    dir = platformdirs.user_config_path(APP_NAME)
    name = "config.yml"

    def __init__(self):
        self.CONFIGFILE = pathlib.Path.joinpath(self.dir, self.name).resolve()

    def make_config_directory(self):
        if self.CONFIGFILE.exists() == False:
            logger.debug(f"Created config directory: {self.dir}")
            os.makedirs(self.dir, exist_ok=True)
        else:
            pass

    def write(self, configfile):
        with open(configfile, "w") as file:
            logger.debug(f"Wrote config file: {configfile}")
            yaml.dump(self.data, file, default_flow_style=False)
