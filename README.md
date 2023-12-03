# Advent of Code: 2023 - Solutions

_My solutions to the annual challenge problems_

This repo contains my solutions to the **Advent of Code** challenge problems from [2023](https://adventofcode.com/2023). The code is written in **Python**.

## Setup

-   Clone this repository: `git clone https://github.com/jtreeves/advent_of_code_2023_solutions.git`
-   Ensure Python3 installed (v3.11.4 ideally): `python3 --version`

## Viewing the Solutions

-   From the root of the repo, run the `main.py` file, with a positional argument for the day to run: `python3 main.py 1` (substituting the specific day for `1`)
-   Optionally, provide an additional boolean positional argument to select between viewing solutions from the practice data or the final data, where `True` is for the final data and `False` is for the practice data: `python3 main.py 1 False` (if not provided, it defaults to `True`)
-   Each solution printed will indicate its day and provide the values for both parts 1 and 2, along with a cumulative execution time

Example solution summary:

```
DAY 1 SOLUTIONS
Part 1: 55712
Part 2: 55413
Total execution time: 0.009216785430908203 seconds
```

To view solutions for all days up to and including today, omit the day positional argument: `python3 main.py`

## Code Analysis

Unlike most coding challenge approaches, this repo is written more like a library, with type annotations for documentation, and it uses a more OOP approach overall.

### General Patterns

-   snake_case used for file names unless the file is for a class, in which case PascalCase is used
-   each day has its own folder for its solution
-   strong type annotation is used throughout
-   OOP approach utilized over a more direct functional programming approach
-   verbose variables used instead of single-character alternatives
-   abstraction orients itself around the problem statement as opposed to the attempting to reduce functionality to bitwise operations

### Key Folders and Files

-   files at the root
    -   `main.py`: module entry point for repo, exposing the `print_solution_for_day` function
    -   `setup.cfg`: indicates any deviations from PEP 8 default styling rules
    -   `pyrightconfig.json`: indicates any deviations from Pyright default type-checking rules
-   `day_` folders for each day's files (e.g., `day_1`)
    -   `solution.py`: code for solving that day's problem
    -   `data.txt`: puzzle input, individuated by AOC for each user
    -   `practice.txt`: general test input, provided by AOC in the initial question
-   `utils` folder for reusable code
    -   classes for common objects, indicated by PascalCase names (e.g., `SolutionResults.py`)
    -   granular functions for common tasks, indicated by snake_case names (e.g., `extract_data_from_file.py`)

### Code Examples

**Reusable class for working with coordinate pairs containing some sort of content in `utils/Cell.py`**

```py
class Cell:
    def __init__(self, x: int, y: int, content: str) -> None:
        self.x = x
        self.y = y
        self.content = content

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}): {self.content}"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cell):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        else:
            return False

    def has_identical_x(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self.x == other.x
        else:
            return False

    def has_identical_y(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self.y == other.y
        else:
            return False
```

**Finds a sequence of cells containing digits from a grid in `day_3/solution.py`**

```py
def find_part_number(self, core_cell: Cell) -> PartNumber:
    cells: List[Cell] = [core_cell]
    left_cell = self.grid.get_left_cell(core_cell)
    right_cell = self.grid.get_right_cell(core_cell)
    while left_cell is not None and left_cell.content.isdigit():
        cells.insert(0, left_cell)
        left_cell = self.grid.get_left_cell(left_cell)
    while right_cell is not None and right_cell.content.isdigit():
        cells.append(right_cell)
        right_cell = self.grid.get_right_cell(right_cell)
    part_number = PartNumber(cells)
    return part_number
```
