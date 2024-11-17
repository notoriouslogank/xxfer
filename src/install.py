import yaml
import logging
import platformdirs

# from constants import Constants
import pathlib
import os

APP_NAME = "xxfer"


class ConfigFile:

    settings = {
        "SEPARATOR": "<SEPARATOR>",
        "BUFFER_SIZE": 4096,
        "HOST": "0.0.0.0",
        "PORT": 5002,
        "DOWNLOAD_DIR": "xxfer_received",
        "ARCHIVE_NAME": "xxfer.tar.gz",
    }
    data = {"SETTINGS": settings}
    dir = platformdirs.user_config_path(APP_NAME)
    name = "config.yml"

    def __init__(self):
        self.CONFIGFILE = pathlib.Path.joinpath(self.dir, self.name).resolve()

    def make_config_directory(self):
        if self.CONFIGFILE.exists() == False:
            os.makedirs(self.dir, exist_ok=True)
        else:
            pass

    def write(self, configfile):
        with open(configfile, "w") as file:
            yaml.dump(self.data, file, default_flow_style=False)


class LogFile:

    logname = "xxfer.log"
    dir = platformdirs.user_log_path(APP_NAME)

    def __init__(self):
        self.LOGFILE = pathlib.Path.joinpath(self.dir, self.logname).resolve()

    def make_log_directory(self):
        if self.LOGFILE.exists() == False:
            os.makedirs(self.dir, exist_ok=True)
        else:
            pass


class KnownHosts:

    host_data = {"HOST": "0.0.0.0", "PORT": 5002}
    known_hostnames = {"localhost": host_data}
    data = {"KNOWN_HOSTS": known_hostnames}
    dir = platformdirs.user_config_path(APP_NAME)
    name = "hosts.yml"

    def __init__(self):
        self.HOSTSFILE = pathlib.Path.joinpath(self.dir, self.name)

    def write(self, hostsfile):
        with open(hostsfile, "w") as file:
            yaml.dump(self.data, file, default_flow_style=False)


class Installer:

    def __init__(self):
        self.app_name = APP_NAME
        self.configfile = ConfigFile()
        self.hostsfile = KnownHosts()
        self.logfile = LogFile()

    def make_files_and_dirs(self):
        self.configfile.make_config_directory()
        self.configfile.write(self.configfile.CONFIGFILE)
        self.hostsfile.write(self.hostsfile.HOSTSFILE)
        self.logfile.make_log_directory()


installer = Installer()
installer.make_files_and_dirs()
