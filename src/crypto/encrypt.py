from pathlib import Path

from cryptography.fernet import Fernet

encrypted_file_extension = "encrypted"


class EncryptKeeper:

    def __init__(self, file: Path = "test.7z", keyfile: Path = "key.key", key=None):
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
        if keyfile_path.exists() == True:
            fk = self.read_key_from_keyfile()
        else:
            self.generate_key()
            fk = self.read_key_from_keyfile()
        return fk

    def generate_key(self):
        new_key = Fernet.generate_key()
        with open(self.keyfile, "wb") as f:
            f.write(new_key)

    def encrypt_file(self, input_file: Path, key: str = None):
        if key == None:
            fk = self.check_for_keyfile()
        else:
            fernet_key = key.encode("utf-8")
            fk = Fernet(fernet_key)

        with open(input_file, "rb") as f:
            file_content = f.read()
        encrypted_content = fk.encrypt(file_content)
        with open(f"{input_file}.{encrypted_file_extension}", "wb") as f:
            f.write(encrypted_content)
        print(f"Your encryption key: {self.key}")


encryptor = EncryptKeeper()
encryptor.encrypt_file("test.7z")
