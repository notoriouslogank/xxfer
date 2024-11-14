import os
import socket
import sys
import time
import tqdm
import yaml
from rich import print

from src.packer import Compressor

with open("config.yml", "r") as yml:
    configs = yaml.safe_load(yml)

server_configs = configs["server"]

SEPARATOR = server_configs["separator"]
BUFFER_SIZE = server_configs["buffer_size"]
SERVER_HOST = server_configs["server_host"]
SERVER_PORT = server_configs["server_port"]
ARCHIVE_NAME = configs["client"]["archive_name"]


class RemoteHost:

    def __init__(self):
        self.host = SERVER_HOST
        self.port = SERVER_PORT

    def receive(self):
        print(f"Now listening at {self.host}:{self.port}")
        print("receive loop")
        try:
            s = socket.socket()
            s.bind((self.host, self.port))
            s.listen(5)
            client_socket, address = s.accept()
            received_data = client_socket.recv(BUFFER_SIZE).decode()
            filename, filesize = received_data.split(SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)

            progress = tqdm.tqdm(
                range(filesize),
                f"[+] Receiving {filename}...",
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            )
            with open(filename, "wb") as f:
                while True:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    progress.update(len(bytes_read))
        except KeyboardInterrupt:
            client_socket.close()
            s.close()
            sys.exit()


if __name__ == "__main__":
    server = RemoteHost()
    while True:
        try:
            print("main loop")
            server.receive()
            Compressor.unpack(ARCHIVE_NAME)
        except KeyboardInterrupt:
            exit()
