import os
import datetime


CURRENT_YEAR = datetime.date.today().year


def check_folder_exists(folder: str) -> bool:
    if not os.path.isdir(folder):
        return False
    return True


def check_year(year: str) -> bool:
    if '1900' >= year >= str(CURRENT_YEAR):
        raise ValueError(f"Year should be within 1900 and {CURRENT_YEAR}")
    return True
