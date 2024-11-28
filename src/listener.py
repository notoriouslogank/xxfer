import logging
import os
import socket
from pathlib import Path

import tqdm
from rich import print
from src.crypto.decrypt import DecryptKeeper
from src.configs.constants import Constants

logger = logging.getLogger(__name__)
constants = Constants("xxfer", "notoriouslogank")
KEYFILE = constants.KEYFILE_PATH


class LocalClient:

    def __init__(self, separator, buffer_size, host, port, archive_name):
        self.host = host
        self.port = port
        self.filename = archive_name
        self.separator = separator
        self.buffer_size = buffer_size

    def write_data_to_file(
        self, filename: Path, client_socket: socket, progress: tqdm.tqdm
    ) -> None:
        """Write received data to output file

        Args:
            filename (Path): Path to output file
            client_socket (socket): Socket object representing connection to remote
            progress (tqdm[int]): Data stream to display progress bar(s)
        """
        with open(filename, "wb") as f:
            logger.debug(f"Writing data to file: {filename}")
            while True:
                bytes_read = client_socket.recv(self.buffer_size)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

    def handle_data(self, client_socket: socket) -> None:
        """Handle incoming data stream and display progress information

        Args:
            client_socket (socket): Remote connection from which to receive data
        """
        received_data = client_socket.recv(self.buffer_size).decode()
        logger.info(f"Received data from: {client_socket}")
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
        decrypt = DecryptKeeper(filename, keyfile=KEYFILE)
        decrypted_file = decrypt.decrypt_file()
        self.write_data_to_file(decrypted_file, client_socket)

    def receive(self) -> None:
        """Open a socket and listen for incoming connection"""
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen(5)
        print(f"\nListening on {self.host}:{self.port}\n")
        logger.info(f"Listening for connection(s) on: {self.host}:{self.port}")
        try:
            s.listen(5)
            client_socket, address = s.accept()
            self.handle_data(client_socket=client_socket)
            self.client_socket = client_socket
            s.close()
            client_socket.close()
        except:
            logger.debug("Encountered exception in receive method.")
            s.close()
            client_socket.close()
