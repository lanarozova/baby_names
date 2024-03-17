import re
from typing import Optional
from handlers.errors import check_year


def filter_files_names(files: list[str]):
    filtered_names = {
        1: {},
        0: {}
    }

    for file in files:

        match = re.match(r'^(19[0-9]{2}|20[0-9]{2})_(BoysNames|GirlsNames)\.txt$', file)
        if match:
            sex = 1 if 'Boys' in match.group() or 'boys' in match.group() else 0
            year = match.group()[:4]
            if check_year(year):
                filtered_names[sex][year] = file

    return filtered_names


def parse_names_from_lines(line: str) -> Optional[tuple[str, int]]:
    line = line.strip()
    match = re.match(r'^[A-Z][a-z]+\s[0-9]+$', line)
    if match:
        name, qty = match.group(0).split()
        return name, int(qty)
    return None


def sort_names(names: dict[str, int]) -> list[tuple]:
    sorted_names = sorted(names.items(), key=lambda item: item[1], reverse=True)
    return sorted_names
