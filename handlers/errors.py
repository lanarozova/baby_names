import os


def check_folder_exists(folder: str) -> bool:
    if not os.path.isdir(folder):
        return False
    return True

