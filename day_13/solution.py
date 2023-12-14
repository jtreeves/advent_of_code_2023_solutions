import time
from typing import List
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Pattern:
    def __init__(self, notes: str) -> None:
        self.notes = notes
        self.rows = self.determine_rows()
        self.columns = self.determine_columns()

    def determine_rows(self) -> List[str]:
        rows = self.notes.split("\n")
        return rows

    def determine_columns(self) -> List[str]:
        raw_columns = [list(x) for x in zip(*self.rows)]
        columns = [''.join(column) for column in raw_columns]
        return columns

    def calculate_value_of_symmetry(self) -> int:
        horizontal = self.find_horizontal_line_of_symmetry()
        vertical = self.find_vertical_line_of_symmetry()
        if horizontal != 0:
            value_of_symmetry = 100 * (horizontal + 1)
        else:
            value_of_symmetry = vertical + 1
        return value_of_symmetry

    def find_horizontal_line_of_symmetry(self) -> int:
        return self.find_line_of_symmetry(self.rows)

    def find_vertical_line_of_symmetry(self) -> int:
        return self.find_line_of_symmetry(self.columns)

    def find_line_of_symmetry(self, dimension: List[str]) -> int:
        line_index = 0
        potential_indices_of_symmetry = self.find_potential_indices_of_symmetry(dimension)
        for index in potential_indices_of_symmetry:
            fully_symmetric = self.check_if_fully_symmetric(index, dimension)
            if fully_symmetric:
                line_index = index
        return line_index

    def find_potential_indices_of_symmetry(self, dimension: List[str]) -> List[int]:
        potential_indices_of_symmetry: List[int] = []
        for index in range(len(dimension) - 1):
            if dimension[index] == dimension[index + 1]:
                potential_indices_of_symmetry.append(index)
        return potential_indices_of_symmetry

    def check_if_fully_symmetric(self, potential_index: int, dimension: List[str]) -> bool:
        fully_symmetric = True
        preceding_index = potential_index - 1
        succeeding_index = potential_index + 2
        while fully_symmetric and preceding_index >= 0 and succeeding_index < len(dimension):
            if dimension[preceding_index] != dimension[succeeding_index]:
                fully_symmetric = False
            else:
                preceding_index -= 1
                succeeding_index += 1
        return fully_symmetric


class Collection:
    def __init__(self, description: str) -> None:
        self.description = description
        self.patterns = self.determine_patterns()

    def determine_patterns(self) -> List[Pattern]:
        patterns: List[Pattern] = []
        descriptions = self.description.split("\n\n")
        for notes in descriptions:
            pattern = Pattern(notes)
            patterns.append(pattern)
        return patterns

    def calculate_total_values_of_symmetry(self) -> int:
        total = 0
        for pattern in self.patterns:
            total += pattern.calculate_value_of_symmetry()
        return total


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(13, is_official)
    collection = Collection(data)
    part_1 = collection.calculate_total_values_of_symmetry()
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(13, part_1, part_2, execution_time)
    return results
