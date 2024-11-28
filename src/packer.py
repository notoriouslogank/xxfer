import logging
import os
import secrets
from pathlib import Path

import pyzipper
from rich import print as print

from src.configs.constants import Constants

constants = Constants("xxfer", "notoriouslogank")

SEPARATOR = constants.SEPARATOR
ARCHIVE_NAME = constants.ARCHIVE_NAME
DESTINATION_DIR = constants.DATA_DIR

logger = logging.getLogger(__name__)
random_bytes = secrets.token_bytes(32)
random_string = random_bytes.hex()


class Compressor:
    """Class to represent a Compressor, allowing for compressing and decompressing archives"""

    def compress(input_folder: Path, output_file: Path) -> Path:
        """Compress and encrypt folder to zipped archive

        Args:
            input_folder (Path): Folder too compress and send
            output_file (Path): Output file path

        Returns:
            Path: Path to encrypted, zipped archive
        """
        with pyzipper.AESZipFile(
            f"{output_file}.enc", "w", compression=pyzipper.ZIP_LZMA
        ) as encrypted:
            encrypted.setpassword(random_string.encode("utf-8"))
            encrypted.setencryption(pyzipper.WZ_AES, nbits=256)

            for foldername, subfolders, filenames in os.walk(input_folder):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, input_folder)
                    encrypted.write(file_path, arcname=arcname)
        print(f"Key: {random_string}")
        encrypted_file = os.path.join(f"{output_file}.enc")
        return encrypted_file

    def format_bytes(size: int) -> str:
        """Format the bytesize to be human readable

        Args:
            size (int): Unit size to use ("K, M, G, T")

        Returns:
            str: The printable bytesize
        """
        logger.debug(f"Formatting bytesize")
        power = 2**10
        n = 0
        power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
        while size > power:
            size /= power
            n += 1
        power_string = f"{round(size)} {power_labels[n]}"
        return power_string

    def decompress(input_file: Path, output_folder: Path, password: str) -> None:
        """Decrypt and decompress zipped archive

        Args:
            input_file (Path): Zipped archive to decrypt and decompress
            output_folder (Path): Destination folder after unzipping/decrypting
            password (str): Decryption key
        """
        with pyzipper.AESZipFile(input_file) as f:
            f.setpassword(password.encode("utf-8"))
            f.extractall(path=output_folder)
