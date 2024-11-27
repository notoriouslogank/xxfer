import logging
import pathlib

import platformdirs
import yaml

from src.install.install import Installer

from .knownhosts import KnownHosts

logger = logging.getLogger(__name__)


class Constants:

    installer = Installer()
    hostsfile = KnownHosts()

    def __init__(self, APP_NAME, APP_AUTHOR):
        self.installer.make_files_and_dirs()
        self.APP_NAME = APP_NAME
        self.APP_AUTHOR = APP_AUTHOR
        self.CONFIGFILE = self.find_configfile()
        self.LOGFILE = self.find_logfile()
        self.HOSTSFILE = self.hostsfile.HOSTSFILE
        with open(self.CONFIGFILE, "r") as yml:
            configs = yaml.safe_load(yml)
            settings = configs["SETTINGS"]

        self.SEPARATOR = settings["SEPARATOR"]
        self.BUFFER_SIZE = settings["BUFFER_SIZE"]
        self.HOST = settings["HOST"]
        self.PORT = settings["PORT"]
        self.DOWNLOAD_DIR = self.find_download_dir()
        self.DATA_DIR = self.find_data_dir()
        self.ARCHIVE_NAME = settings["ARCHIVE_NAME"]

    def get_filepaths(self) -> pathlib.Path:
        """Get paths for default directories relative to platform

        Returns:
            pathlib.Path: user_download_dir, user_data_dir, user_config_dir, user_log_dir
        """
        user_config_dir = platformdirs.user_config_path(self.APP_NAME)
        user_log_dir = platformdirs.user_log_path(self.APP_NAME)
        user_data_dir = platformdirs.user_data_path(self.APP_NAME, self.APP_AUTHOR)
        user_download_dir = platformdirs.user_downloads_path()
        logger.info(
            f"Got directories: {user_data_dir, user_config_dir, user_download_dir, user_log_dir}"
        )
        return user_data_dir, user_config_dir, user_log_dir, user_download_dir

    def find_data_dir(self) -> pathlib.Path:
        """Get path for user data directory

        Returns:
            pathlib.Path: User data directory
        """
        user_data_dir, _, _, _ = self.get_filepaths()
        logger.info(f"DATA_DIR = {user_data_dir}")
        return user_data_dir

    def find_download_dir(self) -> pathlib.Path:
        """Get user download directory

        Returns:
            pathlib.Path: Get path for user download directory
        """
        _, _, _, user_download_dir = self.get_filepaths()
        logger.debug(f"DONLOAD_DIR = {user_download_dir}")
        return user_download_dir

    def find_configfile(self) -> pathlib.Path:
        """Get path to user configuration file

        Returns:
            pathlib.Path: User configuration file
        """
        _, user_config_path_stem, _, _ = self.get_filepaths()
        config_file_name = "config.yml"
        config_file = pathlib.Path.joinpath(user_config_path_stem, config_file_name)
        logger.info(f"CONFIGFILE = {config_file}")
        return config_file

    def find_logfile(self) -> pathlib.Path:
        """Get path to default system log file

        Returns:
            pathlib.Path: Logfile
        """
        _, _, user_log_dir, _ = self.get_filepaths()
        logfile_name = f"{self.APP_NAME}.log"
        logfile = pathlib.Path.joinpath(user_log_dir, logfile_name)
        logger.info(f"{logfile}")
        return logfile
