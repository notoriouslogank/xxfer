import logging
import os
import socket

import tqdm
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style
from rich import print

from constants import Constants
from packer import Compressor

logger = logging.getLogger(__name__)
constants = Constants("xxfer", "notoriouslogank")

SEPARATOR = constants.SEPARATOR
BUFFER_SIZE = constants.BUFFER_SIZE
HOST = constants.HOST
PORT = constants.PORT
ARCHIVE_NAME = constants.ARCHIVE_NAME
CURRENT_DIR = os.getcwd()


class Client:
    known_hosts = ""
    style = Style.from_dict(
        {
            "completion-menu.completion": "bg:#008888 #ffffff",
            "completion-menu.completion.current": "bg:#00aaaa #000000",
            "scrollbar.background": "bg:#88aaaa",
            "scrollbar.button": "bg:#222222",
        }
    )
    autocompleter = WordCompleter([known_hosts])

    def get_known_hosts(self):

        host_list = []
        for _ in configs["known_hosts"]:
            host_list.append(_)
        length = len(self.known_hosts)
        counter = length
        while counter > 0:
            self.known_hosts.join(host_list.pop())
            counter -= 1
        return self.known_hosts

    def get_server_info(self):
        session = PromptSession(
            completer=self.autocompleter,
            style=self.style,
            color_depth=ColorDepth.TRUE_COLOR,
        )
        try:
            remote_ip = session.prompt("Remote Server IP\n>> ")
            remote_port = session.prompt("Remote Server Port\n>> ")
            if str(remote_ip) in self.known_hosts:
                remote_ip = configs["known_hosts"][remote_ip]["ip"]
                remote_port = configs["known_hosts"][remote_ip]["port"]
                self.host_ip = remote_ip
                self.host_port = remote_port
                return self.host_ip, self.host_port
            elif str(remote_ip) not in self.known_hosts:
                self.host_ip = remote_ip
                self.host_port = int(remote_port)
                return self.host_ip, self.host_port
        except KeyboardInterrupt:
            pass
        else:
            print(f"[+] Remote Host: {self.host_ip}:{self.host_port}")

    def send(self, host, port, filename=None):

        if filename == None:
            session = PromptSession(style=self.style, color_depth=ColorDepth.TRUE_COLOR)
            source_directory = os.path.join(
                session.prompt(
                    "File/directory to send\n[Absolute path unless in .]\n>> "
                )
            )
        else:
            source_directory = os.path.join(filename)
        compressed_file = Compressor.compress(ARCHIVE_NAME, source_directory)
        filesize = os.path.getsize(compressed_file)
        os.chdir(CURRENT_DIR)
        s = socket.socket()
        print(f"[+] Connecting to {host}:{port}...\n")
        s.connect((host, port))
        print(f"[+] Connected!\n")
        s.send(f"{ARCHIVE_NAME}{SEPARATOR}{filesize}".encode())

        progress = tqdm.tqdm(
            range(filesize),
            f"Sending {compressed_file}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

        with open(compressed_file, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))


def populate_known_hosts(known_hosts: list, length: int):
    counter = length
    host_list = []
    while counter > 0:
        host_list.append(known_hosts[counter])
        counter -= 1
    print(host_list)
