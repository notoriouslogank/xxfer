import logging
import os
from pathlib import Path

from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


class DecryptKeeper:
    def __init__(self, file: Path = "test.7z", keyfile: Path = "key.key", key=None):
        self.file = file
        self.keyfile = keyfile
        self.key = key

    def read_key_from_keyfile(self):
        logger.info(f"Read key from keyfile: {self.keyfile}")
        with open(self.keyfile, "rb") as f:
            key = f.read()
            return key

    def check_for_keyfile(self):
        keyfile_path = Path(self.keyfile)
        logger.debug(f"Checking for keyfile: {self.keyfile}")
        if keyfile_path.exists() == True:
            logger.debug(f"Found keyfile: {self.keyfile}")
            key = self.read_key_from_keyfile()
            fk = Fernet(key)
        else:
            if self.key == None:
                logger.critical(
                    f"No key OR keyfile provided.  Must provide keyfile or key to decrypt file."
                )
                raise Exception
            else:
                logger.critical(f"Using user-provided key: {self.key}")
                key = self.key
                fk = Fernet(key)
        return fk

    def decrypt_file(self, input_file: Path = "test.7z.encrypted"):
        base_filename, _ = os.path.splitext(input_file)
        fk = self.check_for_keyfile()
        logger.info(f"Beginning file decryption on file: {input_file}")
        with open(input_file, "rb") as f:
            file_content = f.read()
            decrypted_content = fk.decrypt(file_content)

        with open(base_filename, "wb") as f:
            f.write(decrypted_content)
        logger.info(f"Successfully decrypted file: {base_filename}")
