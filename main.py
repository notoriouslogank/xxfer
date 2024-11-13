import sys
from time import sleep

from prompt_toolkit import PromptSession

from client import Client
from server import RemoteHost


def main():
    flow = 0
    session = PromptSession()
    while flow == 0:
        try:
            choice = session.prompt("Send or Receive?\n[S/r]\n>> ")
            flow += 1
        except KeyboardInterrupt:
            sys.exit()
        else:
            if str(choice).lower() == "s":
                client = Client()
                host, port = client.get_server_info()
                client.send(host, port)
            elif str(choice).lower() == "r":
                server = RemoteHost()
                while True:
                    try:
                        server.receive()
                    except KeyboardInterrupt:
                        sys.exit()
            if str(choice).lower() == "q":
                print(f"Closing application\n")
                sleep(0.1)
                sys.exit()


if __name__ == "__main__":
    main()
