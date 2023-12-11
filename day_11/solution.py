import time
from typing import List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Galaxy:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class GalaxyPair:
    def __init__(self, first_galaxy: Galaxy, second_galaxy: Galaxy, horizontal_gaps: List[int], vertical_gaps: List[int], expansion_factor: int) -> None:
        self.first_galaxy = first_galaxy
        self.second_galaxy = second_galaxy
        self.horizontal_gaps = horizontal_gaps
        self.vertical_gaps = vertical_gaps
        self.expansion_factor = expansion_factor
        self.distance = self.calculate_expanded_distance()

    def calculate_initial_distance(self) -> int:
        horizontal_change = abs(self.first_galaxy.x - self.second_galaxy.x)
        vertical_change = abs(self.first_galaxy.y - self.second_galaxy.y)
        distance = horizontal_change + vertical_change
        return distance

    def determine_gaps_along_dimension(self, is_vertical: bool) -> int:
        known_gaps = self.vertical_gaps if is_vertical else self.horizontal_gaps
        endpoints = sorted([self.first_galaxy.y, self.second_galaxy.y]) if is_vertical else sorted([self.first_galaxy.x, self.second_galaxy.x])
        gaps_between_endpoints = 0
        for gap in known_gaps:
            if gap in range(*endpoints):
                gaps_between_endpoints += 1
        return gaps_between_endpoints

    def determine_vertical_gaps(self) -> int:
        return self.determine_gaps_along_dimension(True)

    def determine_horizontal_gaps(self) -> int:
        return self.determine_gaps_along_dimension(False)

    def determine_total_gaps(self) -> int:
        return self.determine_vertical_gaps() + self.determine_horizontal_gaps()

    def calculate_expanded_distance(self) -> int:
        initial_distance = self.calculate_initial_distance()
        total_gaps = self.determine_total_gaps()
        distance = initial_distance + total_gaps * (self.expansion_factor - 1)
        return distance


class Image:
    def __init__(self, description: str) -> None:
        self.rows = get_list_of_lines(description)
        self.height = self.calculate_initial_height()
        self.width = self.calculate_initial_width()
        self.columns = self.create_initial_columns()
        self.empty_rows = self.determine_rows_without_galaxies()
        self.empty_columns = self.determine_columns_without_galaxies()
        self.galaxies = self.create_galaxies()

    def calculate_initial_height(self) -> int:
        return len(self.rows)

    def calculate_initial_width(self) -> int:
        return len(self.rows[0])

    def create_initial_columns(self) -> List[str]:
        columns: List[str] = []
        for column in range(self.width):
            column_values = ""
            for row in self.rows:
                column_values += row[column]
            columns.append(column_values)
        return columns

    def create_galaxies(self) -> List[Galaxy]:
        galaxies: List[Galaxy] = []
        for row in range(self.height):
            for column in range(self.width):
                character = self.rows[row][column]
                if character == "#":
                    galaxies.append(Galaxy(column, row))
        return galaxies

    def determine_rows_without_galaxies(self) -> List[int]:
        return self.determine_elements_without_galaxies(self.rows)

    def determine_columns_without_galaxies(self) -> List[int]:
        return self.determine_elements_without_galaxies(self.columns)

    def determine_elements_without_galaxies(self, elements: List[str]) -> List[int]:
        elements_without_galaxies: List[int] = []
        for element_index in range(len(elements)):
            if "#" not in elements[element_index]:
                elements_without_galaxies.append(element_index)
        return elements_without_galaxies

    def find_distances_between_galaxy_pairs_with_expansion(self, expansion_factor: int) -> List[int]:
        minimal_distances: List[int] = []
        for index in range(len(self.galaxies)):
            matching_index = index + 1
            while matching_index < len(self.galaxies):
                distance = GalaxyPair(self.galaxies[index], self.galaxies[matching_index], self.empty_columns, self.empty_rows, expansion_factor).distance
                minimal_distances.append(distance)
                matching_index += 1
        return minimal_distances

    def calculate_total_distances_with_expansion(self, expansion_factor: int) -> int:
        total_minimal_distances = 0
        minimal_distances = self.find_distances_between_galaxy_pairs_with_expansion(expansion_factor)
        for distance in minimal_distances:
            total_minimal_distances += distance
        return total_minimal_distances


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(11, is_official)
    image = Image(data)
    part_1 = image.calculate_total_distances_with_expansion(2)
    part_2 = image.calculate_total_distances_with_expansion(1000000)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(11, part_1, part_2, execution_time)
    return results
