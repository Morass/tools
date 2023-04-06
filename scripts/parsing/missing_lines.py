import click
from typing import Tuple, Set, List
from pathlib import Path


def get_file_lines(path: Path) -> Tuple[set, list]:
    """
    Reads the file at the given path and returns two sets:
        - The first set contains all lines in the file
        - The second set contains tuples (line number, line) for all lines in the file

    Args:
        path: The path to the file to read

    Returns:
        A tuple of set and list, the first containing all lines and the second containing tuples of (line number, line)
    """
    lines = set()
    numbered_lines = []
    with path.open("r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            lines.add(line)
            numbered_lines.append((i+1, line))
    return lines, numbered_lines


def find_missing_lines(line_tuples1: List[Tuple[int, str]], lines2: Set[str]) -> None:
    """
    Finds the lines from `line_tuples1` that are not present in `lines2`
    and prints them along with their line number.

    Args:
        line_tuples1: A list of tuples (line number, line) to compare against `lines2`.
        lines2: A set of lines to compare against `line_tuples1`.

    Returns:
        None.
    """
    for line_number, line in line_tuples1:
        if line not in lines2:
            print(f"Line {line_number}: {line}")


@click.command()
@click.option('--file1', type=Path, help='Path to first file', required=True)
@click.option('--file2', type=Path, help='Path to second file', required=True)
def main(file1: Path, file2: Path):
    """
    Finds lines which are not present in the other file.

    Args:
        file1 (Path): Path to the first file file.
        file2 (Path): Path to the second file file.

    Raises:
        ValueError: If file1 or file2 parameter is not an existing file.

    Returns:
        None.
    """
    if not file1 or not file1.is_file():
        raise ValueError(f"Parameter file1 is not an existing file '{file1}'")

    if not file2 or not file2.is_file():
        raise ValueError(f"Parameter file2 is not an existing file '{file2}'")

    lines1, numbered_lines1 = get_file_lines(file1)
    lines2, numbered_lines2 = get_file_lines(file2)

    print("    Lines missing from first file:")
    find_missing_lines(numbered_lines2, lines1)
    print("    Lines missing from second file:")
    find_missing_lines(numbered_lines1, lines2)


if __name__ == '__main__':
    main()
