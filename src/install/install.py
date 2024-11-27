import logging

from src.configs import configfile, knownhosts, logfile

logger = logging.getLogger(__name__)
APP_NAME = "xxfer"  # Can't get this from constants??

logger.info("Starting installer...")


class Installer:

    def __init__(self):
        self.app_name = APP_NAME
        self.configfile = configfile.ConfigFile()
        self.hostsfile = knownhosts.KnownHosts()
        self.logfile = logfile.LogFile()

    def make_files_and_dirs(self) -> None:
        """Create necessary files and dirs for log file, config file, and known hosts file"""
        self.configfile.make_config_directory()
        self.configfile.write(self.configfile.CONFIGFILE)
        self.hostsfile.write(self.hostsfile.HOSTSFILE)
        self.logfile.make_log_directory()


installer = Installer()
installer.make_files_and_dirs()
