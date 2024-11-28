import logging
import os
from pathlib import Path

from cryptography.fernet import Fernet

from src.configs.constants import Constants

encrypted_file_extension = "encrypted"
logger = logging.getLogger(__name__)
APP_NAME = "xxfer"
APP_AUTHOR = "notoriouslogank"
constants = Constants(APP_NAME, APP_AUTHOR)
KEYFILE = constants.KEYFILE_PATH


class EncryptKeeper:

    def __init__(self, file: Path = "ellie.7z", keyfile: Path = KEYFILE, key=None):
        self.file = file
        self.keyfile = keyfile
        self.key = key

    def read_key_from_keyfile(self):
        with open(self.keyfile, "rb") as f:
            self.key = f.read()
            fk = Fernet(self.key)
            return fk

    def check_for_keyfile(self):
        keyfile_path = Path(self.keyfile)
        logger.debug(f"Checking for keyfile: {keyfile_path}")
        if keyfile_path.exists() == True:
            logger.info(f"Reading key from keyfile: {keyfile_path}")
            fk = self.read_key_from_keyfile()
        else:
            logger.info(f"Could not find keyfile.  Generating new key...")
            self.generate_key()
            fk = self.read_key_from_keyfile()
        return fk

    def generate_key(self):
        new_key = Fernet.generate_key()
        with open(self.keyfile, "wb") as f:
            f.write(new_key)
        logger.debug(f"Generated new keyfile: {self.keyfile}")

    def encrypt_file(self, input_file: Path, key: str = None):
        if key == None:
            logger.debug("No key provided; checking for keyfile.")
            fk = self.check_for_keyfile()
        else:
            logger.debug("Key provided!")
            fernet_key = key.encode("utf-8")
            fk = Fernet(fernet_key)

        with open(input_file, "rb") as f:
            file_content = f.read()
        encrypted_content = fk.encrypt(file_content)
        encrypted_file_name = f"{input_file}.{encrypted_file_extension}"
        encrypted_file = os.path.join(encrypted_file_name)
        with open(f"{encrypted_file}", "wb") as f:
            f.write(encrypted_content)
        logger.info(f"Successfully encrypted file: {encrypted_file}")
        print(f"Successfully encrypted file: {encrypted_file}")
        return encrypted_file
