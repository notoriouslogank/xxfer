import os
from pathlib import Path

from cryptography.fernet import Fernet


class DecryptKeeper:
    def __init__(self, file: Path = "test.7z", keyfile: Path = "key.key", key=None):
        self.file = file
        self.keyfile = keyfile
        self.key = key

    def read_key_from_keyfile(self):
        with open(self.keyfile, "rb") as f:
            key = f.read()
            return key

    def check_for_keyfile(self):
        keyfile_path = Path(self.keyfile)
        if keyfile_path.exists() == True:
            key = self.read_key_from_keyfile()
            fk = Fernet(key)
        else:
            if self.key == None:
                raise Exception
            else:
                key = self.key
                fk = Fernet(key)
        return fk

    def decrypt_file(self, input_file: Path = "test.7z.encrypted"):
        base_filename, _ = os.path.splitext(input_file)
        fk = self.check_for_keyfile()

        with open(input_file, "rb") as f:
            file_content = f.read()
            decrypted_content = fk.decrypt(file_content)

        with open(base_filename, "wb") as f:
            f.write(decrypted_content)


decryptor = DecryptKeeper()
decryptor.decrypt_file()
