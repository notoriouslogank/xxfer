import os
import socket
import subprocess
import tarfile

import tqdm
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style
from rich import print

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
CURRENT_DIR = os.getcwd()
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002

connection_completer = WordCompleter(
    ["192.168.0.13", "192.168.0.204", "127.0.0.1"], ignore_case=True
)

style = Style.from_dict(
    {
        "completion-menu.completion": "bg:#008888 #ffffff",
        "completion-menu.completion.current": "bg:#00aaaa #000000",
        "scrollbar.background": "bg:#88aaaa",
        "scrollbar.button": "bg:#222222",
    }
)


def bottom_toolbar():
    return os.path.join(os.getcwd())


def sender_info():
    session = PromptSession(
        completer=connection_completer, style=style, color_depth=ColorDepth.TRUE_COLOR
    )
    flow = 0
    while flow == 0:
        try:
            remote_ip = session.prompt("Remote IP\n> ")
            port = int(session.prompt("Port\n> ", default="5002"))
        except KeyboardInterrupt:
            continue
        else:
            print(f"IP: {remote_ip}\nPort: {port}")
            flow += 1
            return remote_ip, port


def compress(output_filename, source_directory):
    print(f"Compressing {source_directory} to {output_filename}")
    os.chdir(source_directory)
    with tarfile.open(os.path.join(CURRENT_DIR, output_filename), "w:gz") as tar:
        for file in os.listdir(os.getcwd()):
            tar.add(os.path.join(file))
    os.chdir(CURRENT_DIR)
    return output_filename


def sendfile(host, port):
    session = PromptSession(style=style, color_depth=ColorDepth.TRUE_COLOR)
    filename = os.path.join(session.prompt("File\n> "))
    compressed_file = compress(os.path.join("xfer.tar.gz"), filename)
    filesize = os.path.getsize(compressed_file)
    os.chdir(CURRENT_DIR)
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print(f"[+] Connected.")
    s.send(f"{compressed_file}{SEPARATOR}{filesize}".encode())

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
    s.close()


def receive():
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"[+] Listening as {SERVER_HOST}:{SERVER_PORT}")
    client_socket, address = s.accept()
    print(f"[+] {address} is connected.")

    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    progress = tqdm.tqdm(
        range(filesize),
        f"Receiving {filename}",
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
    client_socket.close()
    s.close()


def unpack():
    file = os.path.join("xfer.tar.gz")
    subprocess.call(["tar", "-xf", f"{file}"])
    os.remove(file)


def server():
    while True:
        try:
            receive()
            unpack()
        except KeyboardInterrupt:
            exit()


def main():
    session = PromptSession()

    flow = 0
    while flow == 0:
        try:
            choice = session.prompt("Send/receive\n> ")
        except KeyboardInterrupt:
            continue
        else:
            if choice == "send":
                host, port = sender_info()
                sendfile(
                    host,
                    port,
                )
                flow += 1
            elif choice == "receive":
                server()

    while flow == 1:
        try:
            sendfile(host, port)
        except KeyboardInterrupt:
            continue


if __name__ == "__main__":
    main()
