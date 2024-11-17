import logging
import os
import socket
import sys

import tqdm
from rich import print

from constants import Constants

logger = logging.getLogger(__name__)
constants = Constants("xxfer", "notoriouslogank")

SEPARATOR = constants.SEPARATOR
BUFFER_SIZE = constants.BUFFER_SIZE
HOST = constants.HOST
PORT = constants.PORT
ARCHIVE_NAME = constants.ARCHIVE_NAME


class RemoteHost:

    def __init__(self):
        self.host = HOST
        self.port = PORT

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
