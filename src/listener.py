import logging
import os
import socket

import tqdm
from rich import print

logger = logging.getLogger(__name__)


class LocalClient:

    def __init__(self, separator, buffer_size, host, port, archive_name):
        self.host = host
        self.port = port
        self.filename = archive_name
        self.separator = separator
        self.buffer_size = buffer_size

    def write_data_to_file(self, filename, client_socket, progress):
        with open(filename, "wb") as f:
            while True:
                bytes_read = client_socket.recv(self.buffer_size)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

    def handle_data(self, client_socket):
        received_data = client_socket.recv(self.buffer_size).decode()
        filename, filesize = received_data.split(self.separator)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        progress = tqdm.tqdm(
            range(filesize),
            f"[+] Receiving {filename}...",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )
        self.write_data_to_file(
            filename=filename, client_socket=client_socket, progress=progress
        )

    def receive(self):
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen(5)
        print(f"\nListening on {self.host}:{self.port}\n")
        try:
            s.listen(5)
            client_socket, address = s.accept()
            self.handle_data(client_socket=client_socket)
            self.client_socket = client_socket
            s.close()
        except:
            s.close()
            client_socket.close()
