import string
from pathlib import Path
import click
ALL_COLLUMNS = list(string.ascii_uppercase)


def to_num(letter: str) -> int:
    """Convert an uppercase letter to its corresponding numeric position."""
    return ord(letter) - 65


def to_letter(number: int) -> str:
    """Convert a number to its corresponding uppercase letter."""
    return chr(number + 65)


def parse_file(source: Path, column: str, delimiter: str) -> dict:
    """
    Parses a CSV file and returns a dictionary, where each key is a value in the
    specified column of the file, and each value is a list containing the fields
    in the corresponding row of the file.

    Args:
        source (Path): The path to the CSV file.
        column (str): The name of the column whose values will be used as keys in the
                        resulting dictionary.
        delimiter (str): The delimiter used in the CSV file.

    Returns:
        dict: A dictionary containing the contents of the CSV file, where each key
              is a value in the specified column of the file, and each value is a list
              containing the fields in the corresponding row of the file.
    """
    csv = {}
    for line in source.open():
        split_line = line.strip().split(delimiter)
        csv[split_line[to_num(column)]] = split_line
    return csv


def is_approx_equal(cell1: str, cell2: str, epsilon: float) -> bool:
    """
    Check if two cells are approximately equal.

    Args:
        cell1 (str): The first cell to compare.
        cell2 (str): The second cell to compare.
        epsilon (float): The maximum difference between the two cells
                         that is considered approximately equal. If `epsilon` is `None`,
                         then the cells must be exactly equal.

    Returns:
        bool: `True` if the cells are approximately equal, `False` otherwise.
    """
    if epsilon is None:
        return cell1 == cell2
    try:
        val1 = float(cell1)
        val2 = float(cell2)
        return abs(val1 - val2) <= epsilon
    except ValueError:
        return cell1 == cell2


def compare_files(first: dict, second: dict, columns: str, epsilon: float) -> None:
    """
    Compares two CSV files represented as dictionaries.

    Args:
        first (dict): A dictionary representing the first CSV file. Keys should be the identifiers for each line,
                        and values should be lists representing the values in each column.
        second (dict): A dictionary representing the second CSV file. Keys should be the identifiers for each line,
                       and values should be lists representing the values in each column.
        columns (str): A string containing the column letters to be compared, e.g. "AB". If a column letter
                       is not included in this string, the values in that column will not be compared.
        epsilon (float): A value representing the maximum difference between two numeric values that should be
                         considered equal. If set to None, numeric values will be compared exactly.

    Returns:
        None

    Prints out any differences between the two CSV files.
    First, prints any items that are in the first file but not in the second file, and vice versa.
    Then, prints any lines in the two files that differ, based on the specified columns and epsilon value.
    If a column is not included in the `columns` parameter, the values in that column will not be compared.
    """
    # In first but not in second file
    missing = [key for key in first if key not in second]
    if missing:
        print("Following objects are in first file but not in second:")
        print('\n    '.join(missing))

    # In second but not in first file
    missing = [key for key in second if key not in first]
    if missing:
        print("Following objects are in second file but not in first:")
        print('\n    '.join(missing))

    print("<<<<<<<<<<<< DIFFERENCES: >>>>>>>>>>>>")
    different_lines = 0
    for key, line1 in first.items():
        if key in second:
            line2 = second[key]
            differs = False
            # This should not happen... but just in case
            if len(line1) != len(line2):
                print(f"The item '{key}' does not have same number of columns!")
                continue
            for i, cell1 in enumerate(line1):
                # Interesting and not same column
                if to_letter(i) in columns and not is_approx_equal(cell1, line2[i], epsilon):
                    if not differs:
                        differs = True
                        different_lines += 1
                        print(f"There are following differences in item '{key}':")
                    print(f"    Column {to_letter(i)} does not match: '{line1[i]}' != '{line2[i]}'")
    print(f"  >> There are {different_lines} lines that differ (with given criteria). <<")


@click.command()
@click.option('--source1', '-s1', type=Path, help='Path to first CSV file')
@click.option('--source2', '-s2', type=Path, help='Path to second CSV file')
@click.option('--identifier', '-id', default="B", type=click.Choice(ALL_COLLUMNS),
              help='Name of column which identifies item')
@click.option('--compare', '-c', default=["all"], type=click.Choice(ALL_COLLUMNS + ["all"]), multiple=True,
              help='Name of compared column(s) ("all" if any difference counts)')
@click.option('--delimiter', '-d', type=str, default=",", help='Delimiter in the .csv files.')
@click.option('--epsilon', '-e', type=float, default=None,
              help='Maximum difference in float cells. If None is set, only string difference is compared.')
def main(source1: Path, source2: Path, identifier: str, compare: str, delimiter: str, epsilon: float):
    """
    Runs the main script to compare two CSV files.

    Args:
        source1 (Path): Path to the first source CSV file.
        source2 (Path): Path to the second source CSV file.
        identifier (str): Column name in CSV files to identify lines.
        compare (str): Column name in CSV files to compare or "all" to compare all columns.
        delimiter (str): Delimiter used in CSV files.
        epsilon (float): Maximum epsilon difference allowed between compared values.

    Raises:
        ValueError: If source1 or source2 parameter is not an existing file.

    Returns:
        None.
    """
    click.echo(f"First source .csv: {source1}")
    click.echo(f"Second source .csv: {source2}")
    click.echo(f"Identifier column: {identifier}")
    click.echo(f"Compared column: {compare}")
    click.echo(f"Delimiter: {delimiter}")
    click.echo(f"Maximum epsilon difference: {epsilon}")
    if not source1 or not source1.is_file():
        raise ValueError(f"Parameter source1 is not an existing file '{source1}'")

    if not source2 or not source2.is_file():
        raise ValueError(f"Parameter source2 is not an existing file '{source2}'")

    # Convert .csv files to dictionaries
    dict_one = parse_file(source1, identifier, delimiter)
    dict_two = parse_file(source2, identifier, delimiter)

    # Actual compare of the "files"
    if "all" in compare:
        compare = ALL_COLLUMNS
    compare_files(dict_one, dict_two, compare, epsilon)


if __name__ == '__main__':
    main()
