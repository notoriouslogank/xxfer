import json

from rich import print_json

hosts = []  # TODO: Change the names for these functions
known_hosts = []  # TODO: Change the names for these functions


class Host:
    """Class for identifying and saving user-submitted known-hosts"""

    def __init__(self, name: str, ip: str, port: int | str):
        self.name = name
        self.ip = ip
        self.port = port

    def show_host(self):
        """Pretty prints the entered information in a human-readable way way." """
        print(f"Hostname: {self.name}, IP: {self.ip}, PORT: {self.port}")

    def new_host(self):
        """Create a dict for the provided host information.

        Returns:
            host (dict): Name, IP, and Port for the remote host.
        """
        host = {"name": self.name, "ip": self.ip, "port": self.port}
        return host

    def make_json(self, data):
        """Return a json object containing the host information

        Args:
            data (_type_): Input data (host information) to transform into JSON

        Returns:
            json_data (str): JSON formatted input data containing host information
        """
        json_data = json.dumps(data, indent=3)
        return json_data


names = ["logank", "mimir", "localhost"]
ips = ["192.168.0.204", "192.168.0.13", "0.0.0.0"]
ports = ["5001", "5002", "5002"]


def make_hostnames():
    """Print JSON-encoded known hosts to terminal (eventually to JSON file as well)"""
    i = len(names) - 1
    while i >= 0:
        data = [names[i], ips[i], ports[i]]
        host = Host(data[0], data[1], data[2])
        host_data = host.new_host()
        json_hostnames = host.make_json(host_data)
        print_json(json_hostnames)
        i -= 1
        # TODO: Write this to JSON file


make_hostnames()
