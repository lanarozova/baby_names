import os

from handlers.errors import check_folder_exists, check_year
from handlers.files import get_list_of_files, read_data_from_file
from handlers.normalizers import filter_files_names, sort_names
from prettytable import PrettyTable
import argparse


def get_possible_years(years: str, first_year_in_files, last_year_in_files) -> list[str]:
    """
    Depending on last_year_in_files and years in diapason from 1900 till the current year function looks up for
    :param years: string with year, separate years or years range in the format:
                                                                    '1990', '1990, 1995, 1993' or '1990-2000'
    :param first_year_in_files: first year found in files with of available names statistics
    :param last_year_in_files: last year found in files with of available names statistics
    :return: list of years for which stats can be provided
    """
    years = years.strip()

    if years == 'all':
        return [str(year) for year in range(int(first_year_in_files), int(last_year_in_files) + 1)]

    separator = years[4]
    years_r = years.split(separator)

    if separator == '-':
        first_year = years_r[0]
        last_year = years_r[1]

        if all(
                [check_year(first_year),
                 check_year(last_year),
                 first_year < last_year,
                 first_year < last_year_in_files]
        ):
            last_year = int(last_year) if last_year <= last_year_in_files else int(last_year_in_files)
            return [str(year) for year in range(int(first_year), last_year + 1)]

    return [
        year for year
        in years_r
        if check_year(year) and first_year_in_files <= year <= last_year_in_files
    ]


def switcher(input_p: int) -> list[int]:
    """
    Helps program logic to work with optional parameters and turn them to iterable objects:
    sex and popular which have 10 as default value meaning both
    :param input_p: parameter received by a program: 10 - both, 1 - 'boys'/True, 0 - 'girls'/False
    :return: list with chosen options: [1, 0], [1] or [0]
    """
    both = [1, 0]
    if input_p == 10:
        return both
    if input_p in both:
        return [input_p]


def get_names_from_specific_file(folder: str, file: str) -> dict[str, list[tuple]]:
    """
    Retrieves names from the specific file
    :param folder: folder name where the files with names are located
    :param file: file name
    :return: dict with year and associated sorted names with this year: {'year': [list_of_names]}
    """
    result_names = {}
    path = os.path.join(folder, file)
    names = sort_names(read_data_from_file(path))
    year = file[:4]
    result_names[year] = names
    return result_names


def get_pop_or_unpop_names(
        names_for_specific_year: dict[str, list[tuple]],
        popular: int,
) -> list[str]:
    """
    Depending on popular flag, finds most popular or unpopular name in names_for_specific_year
    :param names_for_specific_year: all names found for a specific year
    :param popular: True for most popular names, False for most unpopular names
    :return: list of required parameters for printing the table:
         Year, Most popular/unpopular name, Number of people named with this name within a year
    """
    pop = 0 if popular else -1
    for year in names_for_specific_year:
        name = names_for_specific_year[year][pop][0]
        number = names_for_specific_year[year][pop][1]
        return [year, name, number]


def join_pop_and_unpop_names(pop_names: list[str], unpop_names: list[str]) -> list[str]:
    pop_and_unpop = []
    pop_and_unpop.extend(pop_names)
    pop_and_unpop.extend(unpop_names[1:])
    return pop_and_unpop


def create_table(table_fields: list[str], table_values: list[list[str]]) -> PrettyTable:
    """
    Creates table depending on the incoming parameters
    :param table_values: list of lists with table column data (rows)
    :param table_fields: list of str names for table columns
    :return: table object
    """
    table = PrettyTable()
    table.field_names = table_fields
    for row in table_values:
        table.add_row(row)
    return table


def main(folder: str, years: str = "all", sex: int = 10, popular: int = 10) -> None:

    # main logic
    if not check_folder_exists(folder):
        print(f'Incorrect folder: {folder}')
        return None

    files = get_list_of_files(folder)
    files_filtered = filter_files_names(files)

    sex = switcher(sex)
    popular = switcher(popular)

    # gathering table data depending on the inserted parameters: sex, popular, years
    for s in sex:
        first_year_in_files = min(files_filtered[s])
        last_year_in_files = max(files_filtered[s])
        possible_years = get_possible_years(years, first_year_in_files, last_year_in_files)

        table_values = []
        table_fields = []

        sex_str = 'boys' if s else 'girls'

        for year in possible_years:
            file = files_filtered[s][year]
            names_for_current_year = get_names_from_specific_file(folder, file)

            if len(popular) == 2:
                pop_names = get_pop_or_unpop_names(names_for_current_year, popular[0])
                unpop_names = get_pop_or_unpop_names(names_for_current_year, popular[1])
                table_values.append(join_pop_and_unpop_names(pop_names, unpop_names))
                table_fields = ["Year", "Most popular", "Count_popular", "Most unpopular", "Count_unpopular"]

            else:
                table_values.append(get_pop_or_unpop_names(names_for_current_year, popular[0]))
                pop = "most popular" if popular[0] else "most unpopular"
                table_fields = ["Year", pop.capitalize(), "Count"]
        # printing table
        if len(table_fields) < 5:
            print(f"\nThe {table_fields[1].lower()} names for {sex_str} in {years} years were: \n")
        else:
            print(f"\nThe most popular and most unpopular names for {sex_str} in {years} years were: \n")
        print(create_table(table_fields, table_values))


def baby_names_args_parser():
    # adding command line parser
    parser = argparse.ArgumentParser(
        prog="baby_names",
        description="Looks up for the popular/unpopular girls/boys names "
                    "for the specified years in the given files and returns data in a table",
    )
    parser.add_argument(
        "folder",
        metavar="folder",
        type=str,
        action="store",
        help="Enter folder name where the required files are located. "
             "File name format(year_SexNames.txt): '1990_BoysNames.txt' | '2004_GirlsNames.txt'"
    )
    parser.add_argument(
        "-y", "--years",
        metavar="years",
        default="all",
        action="store",
        type=str,
        help="Enter year, several years or range of years in the following format: "
             "'2000' - for a single year | '1990,1992,2000' - for separate several years | '1990-1992' for years range"
             "If nothing is stated, stats for all years found in files will be printed"
    )
    parser.add_argument(
        "-s", "--sex",
        metavar="sex",
        action="store",
        type=int,
        default=10,
        help="Enter sex preferred for names statistics: "
             "1 for boys | 0 for girls"
             "If nothing is stated, stats for both will be found and printed"
    )
    parser.add_argument(
        "-p", "--popular",
        action="store",
        metavar="popular",
        default=10,
        type=int,
        help="Enter which names stats you prefer: "
             "1 for popular | 0 for unpopular"
             "If nothing is stated, stats for both will be found and printed"
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    cli_run = False

    folder = 'data'
    years = '1990-2001'
    sex = 1
    pop = 10

    if cli_run:
        args = baby_names_args_parser()
        folder = args.folder
        years = args.years
        sex = args.sex
        pop = args.popular

    main(folder, years, sex, pop)
