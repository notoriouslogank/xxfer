import logging
import pathlib

import platformdirs
import yaml

logger = logging.getLogger(__name__)
APP_NAME = "xxfer"


class KnownHosts:

    host_data = {"HOST": "0.0.0.0", "PORT": 5002}
    known_hostnames = {"localhost": host_data}
    data = {"KNOWN_HOSTS": known_hostnames}
    dir = platformdirs.user_config_path(APP_NAME)
    name = "hosts.yml"

    def __init__(self):
        self.HOSTSFILE = pathlib.Path.joinpath(self.dir, self.name)

    def write(self, hostsfile: pathlib.Path) -> None:
        """Write known hosts file

        Args:
            hostsfile (pathlib.Path): Path to known hosts file
        """
        if hostsfile:
            logger.info(f"Hostsfile already exists: {hostsfile}")
            pass
        else:
            with open(hostsfile, "w") as file:
                logger.debug(f"Writing hostsfile: {hostsfile}")
                yaml.dump(self.data, file, default_flow_style=False)
