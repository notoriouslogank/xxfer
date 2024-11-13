import os
import socket
import subprocess
import tarfile

import tqdm
import yaml
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


with open("config.yml", "r") as yml:
    get_yaml = yaml.safe_load(yml)


SEPARATOR = get_yaml["server"]["separator"]
BUFFER_SIZE = get_yaml["server"]["buffer_size"]
SERVER_HOST = get_yaml["server"]["server_host"]
SERVER_PORT = get_yaml["server"]["server_port"]
CURRENT_DIR = os.getcwd()


def get_known_hosts():
    known_hosts = []
    for _ in get_yaml["client"]["known_hosts"]:
        known_hosts.append(_)
    return known_hosts


known_hosts = get_known_hosts()

connection_completer = WordCompleter([known_hosts[0], known_hosts[1], known_hosts[2]])

style = Style.from_dict(
    {
        "completion-menu.completion": "bg:#008888 #ffffff",
        "completion-menu.completion.current": "bg:#00aaaa #000000",
        "scrollbar.background": "bg:#88aaaa",
        "scrollbar.button": "bg:#222222",
    }
)


def sender_info():
    session = PromptSession(
        completer=connection_completer, style=style, color_depth=ColorDepth.TRUE_COLOR
    )
    flow = 0
    while flow == 0:
        try:
            print(
                Panel.fit(
                    "Remote Host IP?",
                    title="xfer",
                    subtitle="<TAB> to see Known Hosts",
                    highlight=True,
                )
            )
            console.rule("[bold red]Remote IP")
            remote_ip = session.prompt("Remote IP\n> ")
            # port = session.prompt("Port\n> ")
            if remote_ip in known_hosts:
                server_ip = get_yaml["client"]["known_hosts"][remote_ip]["ip"]
                server_port = get_yaml["client"]["known_hosts"][remote_ip]["port"]
                print(f"[+] Connecting to: {server_ip}:{str(server_port)}")
                return server_ip, server_port
            elif remote_ip not in known_hosts:
                port = session.prompt("Port:\n> ", default="5002")
                print(f"[+] Connecting to {remote_ip}:{str(port)}")
                return remote_ip, port
        except KeyboardInterrupt:
            continue
        else:
            print(f"IP: {remote_ip}\nPort: {port}")
            flow += 1
            return remote_ip, port


def compress(output_filename, source_directory):
    print(f"Compressing {source_directory} to {output_filename}")
    os.chdir(source_directory)
    table = Table(
        title="Received Files",
        caption="./xfer.tar.gz",
        show_lines=False,
        show_edge=True,
        expand=False,
        collapse_padding=True,
    )
    table.add_column(
        "File", justify="right", style="#2200f8", no_wrap=True, overflow="ellipsis"
    )
    table.add_column("Filesize", style="magenta", no_wrap=True, justify="left")
    with tarfile.open(os.path.join(CURRENT_DIR, output_filename), "w:gz") as tar:
        for file in os.listdir(os.getcwd()):
            table.add_row(file, str(format_bytes(os.path.getsize(file))))
            tar.add(file)
        os.chdir(CURRENT_DIR)
        table.add_row(
            "Total",
            f"{str(format_bytes(os.path.getsize(output_filename)))}",
            style="#887191 bold",
            end_section=True,
        )

    console = Console()
    console.print(table)
    return output_filename


def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    power_string = f"{round(size)} {power_labels[n]}B"
    return power_string


def sendfile(host, port):
    print(Panel.fit("File or directory to send?", title="xfer"))
    session = PromptSession(style=style, color_depth=ColorDepth.TRUE_COLOR)
    filename = os.path.join(session.prompt("\n> "))
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
    print(
        Panel.fit("Would you like to send or receive?", title="xfer", subtitle="[S\\r]")
    )
    session = PromptSession()

    flow = 0
    while flow == 0:
        try:
            choice = session.prompt("> ", default="s")
        except KeyboardInterrupt:
            continue
        else:
            if choice == "s":
                host, port = sender_info()
                sendfile(
                    host,
                    port,
                )
                flow += 1
            elif choice == "r":
                server()

    while flow == 1:
        try:
            sendfile(host, port)
        except KeyboardInterrupt:
            continue


if __name__ == "__main__":
    main()
