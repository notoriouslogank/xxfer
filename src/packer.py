import os
import secrets
import pyzipper
import logging
import tarfile
from pathlib import Path

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

    def compress(input_folder, output_file):
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
        return output_file

    # def compress(output_filename: str, source_directory: Path) -> Path:
    #    """Compress a dir to an archive

    #        Args:
    #            output_filename (str): Relative filename, including extension
    #            source_directory (Path): Directory to be archived

    #        Returns:
    #            Path: An archive representing the input dir
    #        """

    # logger.debug(
    #    f"Compressing {source_directory} to {source_directory}/#{output_filename}."
    # )
    # print(f"[+] Compressing {source_directory} to {output_filename}...")
    # os.chdir(source_directory)
    # archive_path = os.path.join(os.getcwd(), output_filename)
    # with tarfile.open(archive_path, "w:gz") as tar:
    #    for file in os.listdir(os.getcwd()):
    #        tar.add(file)
    #    os.chdir(os.getcwd())
    # logger.debug(f"Archive path: {archive_path}")
    # return archive_path

    def unpack(archive: Path) -> None:
        """Unpack an archive into a dir of files

        Args:
            archive (Path): Archive to unpack
        """
        print(f"[+] Decompressing {archive}...")
        logger.debug(f"Unpacking archive: {archive}")
        file = os.path.join(archive)
        with tarfile.open(file, "r:gz") as tar:
            tar.extractall()
        os.remove(file)

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
