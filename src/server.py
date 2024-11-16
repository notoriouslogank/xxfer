import logging
import os
import socket
import sys

import tqdm
import yaml
from rich import print

from packer import Compressor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s::%(levelname)s:%(message)s")
file_handler = logging.FileHandler("xxfer.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

try:
    with open("config.yml", "r") as yml:
        configs = yaml.safe_load(yml)
except FileNotFoundError:
    logger.error("No config.yml found")
    pass
else:
    logger.info("Loaded config.yml")

settings = configs["settings"]
known_hosts = configs["known-hosts"]

SEPARATOR = settings["separator"]
BUFFER_SIZE = settings["buffer_size"]
SERVER_HOST = settings["host"]
SERVER_PORT = settings["port"]
ARCHIVE_NAME = settings["archive"]


class RemoteHost:

    def __init__(self):
        self.host = SERVER_HOST
        self.port = SERVER_PORT

    def receive(self):
        print(f"Now listening at {self.host}:{self.port}")
        try:
            s = socket.socket()
            s.bind((self.host, self.port))
            s.listen(5)
            client_socket, address = s.accept()
            received_data = client_socket.recv(BUFFER_SIZE).decode()
            filename, filesize = received_data.split(SEPARATOR)
            logging.debug(f"Received file {filename}{SEPARATOR}{int(filesize)/1024}")
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
        #                client_socket.close()
        #                s.close()
        except (KeyboardInterrupt, UnboundLocalError):
            client_socket.close()
            s.close()
        try:
            client_socket.close()
            s.close()
        except UnboundLocalError:
            sys.exit()
