import os

from handlers.errors import check_folder_exists
from handlers.files import get_list_of_files, read_data_from_file
from handlers.normalizers import filter_files_names, sort_names
from handlers.normalizers import check_year
from prettytable import PrettyTable


def get_names_for_specific_year(folder: str, file: str, year: str) -> dict[str, list[tuple]]:
    result_names = {}
    path = os.path.join(folder, file)
    names = sort_names(read_data_from_file(path))
    result_names[year] = names
    return result_names


def get_pop_unpop_names(
        names_for_specific_year: dict[str, list[tuple]],
        popular: bool = True
) -> list[str]:

    result = []
    pop = 0 if popular else -1
    for year in names_for_specific_year:
        name = names_for_specific_year[year][pop][0]
        number = names_for_specific_year[year][pop][1]
        result.extend([year, name, number])
    return result


def print_statistics(table_data: list[list[str]], pop):
    table = PrettyTable()
    table.field_names = ["Year", pop, "Number"]
    for line in table_data:
        table.add_row(line)
    print(table)


def main(folder: str, years: str, sex: str = "Both", popular=True) -> None:
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "sex",
    #     metavar="sex",
    #     type=str,
    #     help="Enter sex preferred for names statistics: 'girls' | 'boys' | blank line for both"
    # )
    # args = parser.parse_args()
    # sex = args.sex
    if not check_folder_exists(folder):
        print(f'Incorrect folder: {folder}')
        return None

    files = get_list_of_files(folder)
    files_filtered = filter_files_names(files)

    sex = sex.lower()
    last_year_in_files = max(files_filtered[sex].keys())
    possible_years = [year for year in years.split() if check_year(year) and year <= last_year_in_files]

    pop_names_for_chosen_years = []

    for year in possible_years:
        file = files_filtered[sex][year]
        names_for_current_year = get_names_for_specific_year(folder, file, year)
        pop_names_for_chosen_years.append(get_pop_unpop_names(names_for_current_year))

    pop = "Most Popular Name" if popular else "Most Unpopular Name"
    print(f"The {pop}s for {sex} in {', '.join(possible_years)} were: \n")
    print_statistics(pop_names_for_chosen_years, pop)


if __name__ == '__main__':
    folder1 = 'data'
    main(folder1, '1900 1950 2000 2024', 'girls', True)
