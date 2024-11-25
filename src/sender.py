import logging
import os
import socket

import tqdm
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style
from rich import print

from packer import Compressor

logger = logging.getLogger(__name__)

CURRENT_DIR = os.getcwd()


class RemoteClient:
    known_hosts = []
    style = Style.from_dict(
        {
            "completion-menu.completion": "bg:#008888 #ffffff",
            "completion-menu.completion.current": "bg:#00aaaa #000000",
            "scrollbar.background": "bg:#88aaaa",
            "scrollbar.button": "bg:#222222",
        }
    )
    autocompleter = WordCompleter([known_hosts])

    def __init__(self, hostsfile, buffer_size, separator, host, port, archive_name):
        self.hostsfile = hostsfile
        self.buffer_size = buffer_size
        self.separator = separator
        self.host = host
        self.port = port
        self.archive_name = archive_name
        self.current_dir = os.getcwd()

    def prepare_payload(self, source_directory):
        compressed_file = Compressor.compress(self.archive_name, source_directory)
        return compressed_file

    def get_remote_ip(self):
        session = PromptSession(style=self.style, color_depth=ColorDepth.TRUE_COLOR)
        try:
            remote_ip = session.prompt("\nEnter remote IP: \n>>")
        except KeyboardInterrupt:
            pass
        else:
            print(f"[+] Remote IP: {remote_ip}")
            return remote_ip

    def get_remote_port(self):
        session = PromptSession(style=self.style, color_depth=ColorDepth.TRUE_COLOR)
        try:
            remote_port = session.prompt("\nEnter remote Port: \n>>")
        except KeyboardInterrupt:
            pass
        else:
            print(f"[+] Remote Port: {remote_port}")
            return int(remote_port)

    def get_target_files(self):
        session = PromptSession(style=self.style, color_depth=ColorDepth.TRUE_COLOR)
        try:
            target_files = session.prompt("\nEnter target file(s) to send: \n>>")
        except KeyboardInterrupt:
            pass
        else:
            print(f"[+] File(s) to send: {target_files}")
            return os.path.join(target_files)

    def send(self, host, port, filename=None):
        if filename == None:
            session = PromptSession(style=self.style, color_depth=ColorDepth.TRUE_COLOR)
            source_directory = os.path.join(
                session.prompt(
                    "File/directory to send\n[Absolute path unless in .]\n>> "
                )
            )
        else:
            source_directory = os.getcwd()
            compressed_file = self.prepare_payload(source_directory)
            filesize = os.path.getsize(compressed_file)
        os.chdir(CURRENT_DIR)
        s = socket.socket()
        print(f"[+] Connecting to {host}:{port}...\n")
        s.connect((host, port))
        print(f"[+] Connected!\n")
        s.send(f"{self.archive_name}{self.separator}{filesize}".encode())

        progress = tqdm.tqdm(
            range(filesize),
            f"Sending {compressed_file}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

        with open(compressed_file, "rb") as f:
            while True:
                bytes_read = f.read(self.buffer_size)
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
