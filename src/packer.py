import os
import tarfile

from constants import Constants
from rich import print as print

constants = Constants("xxfer", "notoriouslogank")

SEPARATOR = constants.SEPARATOR
ARCHIVE_NAME = constants.ARCHIVE_NAME
DESTINATION_DIR = constants.DATA_DIR
# try:
#    with open("config.yml", "r") as yml:
#        get_config = yaml.safe_load(yml)
#        settings = get_config["settings"]
# except (FileNotFoundError, NameError):
#    print("Cannot locate config.yml.\nPlease ensure file exists in this directtory.")
#    raise SystemExit
# else:
#    pass

# SEPARATOR = settings["separator"]
# ARCHIVE_NAME = settings["archive"]
# DESTINATION_DIR = settings["dest_dir"]


class Compressor:

    def compress(output_filename, source_directory):
        print(f"[+] Compressing {source_directory} to {output_filename}...")
        os.chdir(source_directory)
        archive_path = os.path.join(os.getcwd(), output_filename)
        with tarfile.open(archive_path, "w:gz") as tar:
            for file in os.listdir(os.getcwd()):
                tar.add(file)
            os.chdir(os.getcwd())

        return archive_path

    def unpack(archive):
        print(f"[+] Decompressing {archive}...")
        file = os.path.join(archive)
        with tarfile.open(file, "r:gz") as tar:
            tar.extractall()
        os.remove(file)

    def format_bytes(size):
        power = 2**10
        n = 0
        power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
        while size > power:
            size /= power
            n += 1
        power_string = f"{round(size)} {power_labels[n]}"
        return power_string


def main():

    Compressor.compress(ARCHIVE_NAME, input("Source directory: \n> "))


if __name__ == "__main__":
    main()
