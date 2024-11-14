from rich import print_json
import json

hosts = []
known_hosts = []


class Host:

    def __init__(self, name: str, ip: str, port: int | str):
        self.name = name
        self.ip = ip
        self.port = port

    def show_host(self):
        print(f"Hostname: {self.name}, IP: {self.ip}, PORT: {self.port}")

    def new_host(self):
        host = {"name": self.name, "ip": self.ip, "port": self.port}
        return host

    def make_json(self, data):
        json_data = json.dumps(data, indent=3)
        return json_data


names = ["logank", "mimir", "localhost"]
ips = ["192.168.0.204", "192.168.0.13", "0.0.0.0"]
ports = ["5001", "5002", "5002"]


def make_hostnames():

    for i in range(len(names)):
        data = [names[i], ips[i], ports[i]]
        host = Host(data[0], data[1], data[2])
        host_data = host.new_host()
        host.make_json(host_data)
        print_json(host.make_json(host_data))


#        print(len(known_hosts
make_hostnames()
# print_json(known_hosts)
# print_json(make_hostnames())

# host1.new_host()
# host2.new_host()
# host1.make_json()
# host2.make_json()
# for i in known_hosts:
#    print_json(i)
