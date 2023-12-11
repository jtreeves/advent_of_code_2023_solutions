import time
from typing import List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Galaxy:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def calculate_distance(self, other: object) -> int:
        if isinstance(other, Galaxy):
            distance = abs(self.x - other.x) + abs(self.y - other.y)
        else:
            distance = 0
        return distance


class Image:
    def __init__(self, description: str) -> None:
        self.initial_rows = get_list_of_lines(description)
        self.initial_height = self.calculate_initial_height()
        self.initial_width = self.calculate_initial_width()
        self.initial_columns = self.create_initial_columns()
        self.expand_universe()

    def calculate_initial_height(self) -> int:
        return len(self.initial_rows)

    def calculate_initial_width(self) -> int:
        return len(self.initial_rows[0])

    def create_initial_columns(self) -> List[str]:
        columns: List[str] = []
        for column in range(self.initial_width):
            column_values = ""
            for row in self.initial_rows:
                column_values += row[column]
            columns.append(column_values)
        return columns

    def expand_universe(self) -> None:
        new_rows = self.create_new_rows()
        galaxies: List[Galaxy] = []
        for row in range(len(new_rows)):
            for column in range(len(new_rows[0])):
                character = new_rows[row][column]
                if character == "#":
                    new_galaxy = Galaxy(column, row)
                    galaxies.append(new_galaxy)
        self.galaxies = galaxies

    def determine_rows_without_galaxies(self) -> List[int]:
        return self.determine_elements_without_galaxies(self.initial_rows)

    def determine_columns_without_galaxies(self) -> List[int]:
        return self.determine_elements_without_galaxies(self.initial_columns)

    def determine_elements_without_galaxies(self, elements: List[str]) -> List[int]:
        elements_without_galaxies: List[int] = []
        for element_index in range(len(elements)):
            if "#" not in elements[element_index]:
                elements_without_galaxies.append(element_index + 1 + len(elements_without_galaxies))
        return elements_without_galaxies

    def create_new_rows(self) -> List[str]:
        rows_without_galaxies = self.determine_rows_without_galaxies()
        columns_without_galaxies = self.determine_columns_without_galaxies()
        new_width = self.initial_width + len(columns_without_galaxies)
        new_rows: List[str] = []
        for old_row_index in range(self.initial_height):
            new_row = ""
            new_column_index = 0
            empty_columns_tracked = 0
            while new_column_index < new_width:
                if new_column_index in columns_without_galaxies:
                    new_row += "."
                    empty_columns_tracked += 1
                else:
                    new_row += self.initial_rows[old_row_index][new_column_index - empty_columns_tracked]
                new_column_index += 1
            new_rows.append(new_row)
        full_empty_row = ""
        empty_row_index = 0
        while empty_row_index < new_width:
            full_empty_row += "."
            empty_row_index += 1
        for empty_row in rows_without_galaxies:
            new_rows.insert(empty_row, full_empty_row)
        return new_rows

    def find_minimal_distances_between_all_galaxy_pairs(self) -> List[int]:
        minimal_distances: List[int] = []
        for index in range(len(self.galaxies)):
            matching_index = index + 1
            while matching_index < len(self.galaxies):
                distance = self.galaxies[index].calculate_distance(self.galaxies[matching_index])
                minimal_distances.append(distance)
                matching_index += 1
        return minimal_distances

    def calculate_total_minimal_distances(self) -> int:
        total_minimal_distances = 0
        minimal_distances = self.find_minimal_distances_between_all_galaxy_pairs()
        for distance in minimal_distances:
            total_minimal_distances += distance
        return total_minimal_distances


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(11, is_official)
    image = Image(data)
    part_1 = image.calculate_total_minimal_distances()
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(11, part_1, part_2, execution_time)
    return results
