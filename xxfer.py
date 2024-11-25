import argparse
import logging
import sys
from pathlib import Path
from time import sleep

from prompt_toolkit import PromptSession

from src.constants import Constants
from src.listener import LocalClient
from src.sender import RemoteClient

constants = Constants("xxfer", "notoriouslogank")

APP_AUTHOR = constants.APP_AUTHOR
APP_NAME = constants.APP_NAME
ARCHIVE_NAME = constants.ARCHIVE_NAME
BUFFER_SIZE = constants.BUFFER_SIZE
CONFIGFILE = constants.CONFIGFILE
SEPARATOR = constants.SEPARATOR
HOST = constants.HOST
PORT = constants.PORT
LOGFILE = constants.LOGFILE
DOWNLOAD_DIR = constants.DOWNLOAD_DIR
HOSTSFILE = constants.HOSTSFILE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s::%(levelname)s::Line %(lineno)s\n%(message)s"
)
file_handler = logging.FileHandler(f"{LOGFILE}", "w")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("Program start")


parser = argparse.ArgumentParser(
    prog="xfer",
    description="Application to send/receive files to/from remote machine.",
    epilog="Thanks for playing",
)

parser.add_argument(
    "-r",
    "--receive",
    required=False,
    help="Listen for incoming connections.",
    action="store_true",
    default=argparse.SUPPRESS,
)

parser.add_argument(
    "-s",
    "--send",
    nargs="?",
    help="Send file(s) to IP.",
    type=str,
    required=False,
    default=argparse.SUPPRESS,
)

parser.add_argument(
    "-p",
    "--port",
    help="Remote host port",
    nargs="?",
    type=int,
    required=False,
    default=argparse.SUPPRESS,
)

parser.add_argument(
    "-f",
    "--file",
    help="Absolute or relative path to file or directory to send",
    nargs="?",
    type=Path,
    required=False,
    default=argparse.SUPPRESS,
)


args = parser.parse_args()
logger.debug(f"Parsed the following args: {args}")


class CommandLineInterface:
    """Class for taking command line arguments"""

    def __init__(self, host=RemoteClient, port=PORT, file=Path.cwd()):
        self.host = host
        self.port = port
        self.file = file

    def print_me(self):
        """Pretty print CLI client information"""
        print(self.host, self.port, self.file)

    def cli_receive(self):
        """Listen for incoming connections; recieve incoming files"""
        try:
            client = LocalClient(SEPARATOR, BUFFER_SIZE, HOST, PORT, ARCHIVE_NAME)
            client.receive()
        except KeyboardInterrupt:
            logger.debug("Receive stopped by user.")
            raise SystemExit

    def cli_send(self):
        """Send file via command line options"""
        logging.debug("Attempting to send:")
        client = RemoteClient(
            HOSTSFILE, BUFFER_SIZE, SEPARATOR, HOST, PORT, ARCHIVE_NAME
        )
        client.send(self.host, self.port, self.file)
        logging.info("Files sent successfully!")


class InteractivePrompt:

    def __init__(
        self,
        client=RemoteClient(
            HOSTSFILE, BUFFER_SIZE, SEPARATOR, HOST, PORT, ARCHIVE_NAME
        ),
        server=LocalClient(SEPARATOR, BUFFER_SIZE, HOST, PORT, ARCHIVE_NAME),
    ):
        self.client = client
        self.server = server

    def send(self):
        logger.debug("Sending file tui.send()")
        host = self.client.get_remote_ip()
        port = self.client.get_remote_port()
        file = self.client.get_target_files()
        self.client.send(host, port, file)

    def receive(self):
        logger.debug("Listening for conection")
        while True:
            try:
                self.server.receive()
            except KeyboardInterrupt:
                logger.exception(KeyboardInterrupt)
                raise SystemExit

    def quit(self):
        logging.debug("User closed application.")
        sleep(0.5)
        logging.debug(SystemExit)
        raise SystemExit


def launch_interactive():
    logging.debug("Launching interactive.")
    flow = 0
    session = PromptSession()
    while flow == 0:
        try:
            logging.debug("Entered try block.")
            choice = session.prompt(
                "Press [S] to Send Files\nPress [R] to Receive Files\nPress [Q] to Quit\n>> "
            )
            choice = str(choice).lower()
            flow += 1
        except KeyboardInterrupt:
            logger.exception(SystemExit)
            raise SystemExit
        else:
            logging.debug("Exited try/except.")
            interactive_prompt = InteractivePrompt()
            if choice == "s":
                interactive_prompt.send()
            elif choice == "r":
                interactive_prompt = InteractivePrompt(
                    RemoteClient,
                    LocalClient(SEPARATOR, BUFFER_SIZE, HOST, PORT, ARCHIVE_NAME),
                )
                interactive_prompt.receive()
            elif choice == "q":
                interactive_prompt.quit()


def main():
    """Main Loop

    Raises:
        AttributeError: Missing given attribute, typically from bad command line args
        SystemExit: Exits the system due to fatal error
    """
    if len(sys.argv) == 1:
        launch_interactive()
    if len(sys.argv) == 2:
        try:
            if "receive" in args:
                client = LocalClient(SEPARATOR, BUFFER_SIZE, HOST, PORT, ARCHIVE_NAME)
                if args.receive == True:
                    client.receive()
        except AttributeError:
            pass
    elif len(sys.argv) > 2:
        try:
            if "send" not in args:
                pass
            if "send" in args and args.send != None:
                logger.debug(f"Send arg: {args.send}")
                host = args.send
            elif "send" in args and args.send == None:
                logger.critical(f"Missing IP argument")
                raise AttributeError
        except AttributeError:
            logger.critical(
                "Missing IP information.\nSee python main.py --help for more information."
            )
            raise SystemExit(
                "Missing IP information.\nSee python main.py --help for more information."
            )
        else:
            try:
                if "port" in args and args.port != None:
                    logger.debug(f"Port: {args.port}")
                    port = args.port
                elif "port" in args and args.port == None:
                    logger.warning(
                        f"Missing Port information.  Using default port: 5002"
                    )
                    port = 5002
                elif "port" not in args:
                    logger.info("No Port flag provided. Using default Port 5002.")
                    port = 5002
            except AttributeError:
                logger.critical(
                    "Missing Port information.\nSince [-p --port] was given but not None, using default Port 5002."
                )
                port = 5002
            else:
                logger.debug(f"IP: {host}\nPort: {port}")
            try:
                if "file" in args and args.file != None:
                    logger.info(f"Source file: {args.file}")
                    file = args.file
                elif "file" not in args:
                    logger.info("No filename provided.  Using default [.]")
                    file = Path(".")
            except Exception:
                logger.critical("No arguments received.")
                sys.exit()
            else:
                try:
                    cli = CommandLineInterface(host, port, file)
                    cli.print_me()
                    logger.info(f"Creating CLI: {cli.host}:{cli.port} {cli.file}")
                    cli.cli_send()
                except NameError:
                    logging.error(f"Missing information: {NameError()}")


if __name__ == "__main__":
    main()
