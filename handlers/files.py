import os

from handlers.normalizers import parse_names_from_lines


def get_list_of_files(folder: str) -> list[str]:
    files = os.listdir(folder)
    return files


def read_data_from_file(path: str) -> dict[str, int]:
    names = {}
    with open(path) as file_names:
        for line in file_names:
            line = parse_names_from_lines(line)
            if line is not None:
                name, qty = line
                names[name] = qty
    return names
