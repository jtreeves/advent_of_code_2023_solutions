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

    def calculate_value_of_symmetry(self, required_differences: int) -> int:
        horizontal = self.find_horizontal_line_of_symmetry(required_differences)
        vertical = self.find_vertical_line_of_symmetry(required_differences)
        if horizontal != 0:
            value_of_symmetry = 100 * horizontal
        else:
            value_of_symmetry = vertical
        return value_of_symmetry

    def find_horizontal_line_of_symmetry(self, required_differences: int) -> int:
        return self.find_line_of_symmetry_with_differences(self.rows, required_differences)

    def find_vertical_line_of_symmetry(self, required_differences: int) -> int:
        return self.find_line_of_symmetry_with_differences(self.columns, required_differences)

    def find_line_of_symmetry_with_differences(self, dimension: List[str], required_differences: int) -> int:
        line_index = 0
        current_index = 0
        symmetry_found = False
        while current_index < len(dimension) - 1 and not symmetry_found:
            differences = 0
            preceding_index = current_index
            succeeding_index = current_index + 1
            while preceding_index >= 0 and succeeding_index < len(dimension) and differences <= required_differences:
                inner_index = 0
                while inner_index < len(dimension[preceding_index]) and differences <= required_differences:
                    if dimension[preceding_index][inner_index] != dimension[succeeding_index][inner_index]:
                        differences += 1
                    inner_index += 1
                preceding_index -= 1
                succeeding_index += 1
            current_index += 1
            if differences == required_differences:
                line_index = current_index
                symmetry_found = True
        return line_index


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

    def calculate_total_values_of_symmetry(self, required_differences: int) -> int:
        total = 0
        for pattern in self.patterns:
            total += pattern.calculate_value_of_symmetry(required_differences)
        return total


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(13, is_official)
    collection = Collection(data)
    part_1 = collection.calculate_total_values_of_symmetry(0)
    part_2 = collection.calculate_total_values_of_symmetry(1)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(13, part_1, part_2, execution_time)
    return results
