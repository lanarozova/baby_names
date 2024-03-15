import re
from typing import Optional
import datetime
from collections import defaultdict


CURRENT_YEAR = datetime.date.today().year


def check_year(year: str) -> bool:
    if '1900' <= year <= str(CURRENT_YEAR):
        return True
    return False


def filter_files_names(files: list[str]):
    filtered_names = {
        "boys": {},
        "girls": {}
    }

    for file in files:

        match = re.match(r'^(19[0-9]{2}|20[0-9]{2})_(BoysNames|GirlsNames)\.txt$', file)
        if match:
            sex = 'boys' if 'Boys' in match.group() else 'girls'
            year = match.group()[:4]
            if check_year(year):
                filtered_names[sex][year] = file

    return filtered_names


def sort_names(names: dict[str, int]) -> list[tuple]:
    sorted_names = sorted(names.items(), key=lambda item: item[1], reverse=True)
    return sorted_names


def parse_names_from_lines(line: str) -> Optional[tuple[str, int]]:
    line = line.strip()
    match = re.match(r'^[A-Z][a-z]+\s[0-9]+$', line)
    if match:
        name, qty = match.group(0).split()
        return name, int(qty)
    return None

