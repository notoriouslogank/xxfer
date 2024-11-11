import os
import socket

import tqdm
from rich import print as pprint

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

host = "24.254.180.168"
port = 5002
filename = input("path/to/file: ")
filesize = os.path.getsize(filename)

s = socket.socket()
pprint(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
pprint("[+] Connected.")

s.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(
    range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024
)
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))
s.close()
