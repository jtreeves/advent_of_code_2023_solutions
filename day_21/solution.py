import time
from typing import Tuple, Set, List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class FarmMap:
    def __init__(self, description: str) -> None:
        self.rows = get_list_of_lines(description)
        self.height = self.calculate_height()
        self.width = self.calculate_width()
        self.positions = self.create_positions()
        self.y_min = 0
        self.y_max = self.height - 1
        self.x_min = 0
        self.x_max = self.width - 1

    def calculate_height(self) -> int:
        return len(self.rows)

    def calculate_width(self) -> int:
        return len(self.rows[0])

    def create_positions(self) -> dict[Tuple[int, int], bool]:
        positions: dict[Tuple[int, int], bool] = {}
        for row in range(self.height):
            for column in range(self.width):
                representation = self.rows[row][column]
                value = True if representation == "." or representation == "S" else False
                coordinates = (column, row)
                positions[coordinates] = value
                if representation == "S":
                    self.start = coordinates
        return positions

    def find_possible_positions_after_step(self, start_position: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = start_position
        possible_positions: List[Tuple[int, int]] = []
        possible_coordinates = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for coordinates in possible_coordinates:
            new_x, new_y = coordinates
            if not self.x_min <= new_x <= self.x_max or not self.y_min <= new_y <= self.y_max:
                self.expand_positions()
            possible_plot = self.positions.get(coordinates)
            if possible_plot:
                possible_positions.append(coordinates)
        return possible_positions

    def find_all_possible_positions_after_step_with_multiple_starts(self, starting_positions: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        ending_positions: Set[Tuple[int, int]] = set()
        for position in starting_positions:
            possible_positions = self.find_possible_positions_after_step(position)
            ending_positions.update(possible_positions)
        return ending_positions

    def determine_reachable_plots_after_certain_steps(self, steps: int) -> int:
        current_step = 0
        current_positions: Set[Tuple[int, int]] = set([self.start])
        while current_step < steps:
            current_step += 1
            current_positions = self.find_all_possible_positions_after_step_with_multiple_starts(current_positions)
        return len(current_positions)

    def expand_positions(self) -> None:
        current_height = self.y_max - self.y_min + 1
        current_width = self.x_max - self.x_min + 1
        self.y_max += current_height
        self.y_min -= current_height
        self.x_max += current_width
        self.x_min -= current_width
        x_values = [-current_width, current_width, 0]
        y_values = [-current_height, current_height, 0]
        shifts = [(x, y) for x in x_values for y in y_values if (x, y) != (0, 0)]
        new_maps: List[dict[Tuple[int, int], bool]] = []
        for shift in shifts:
            shifted_map = {}
            for coordinates, value in self.positions.items():
                shifted_coordinates = tuple(x + dx for x, dx in zip(coordinates, shift))
                shifted_map[shifted_coordinates] = value
            new_maps.append(shifted_map)
        for new_map in new_maps:
            self.positions.update(new_map)


def check_if_perfect(value: int, power: int) -> bool:
    root = round(value ** (1 / power))
    original = root ** power
    deviation = abs(original - value)
    is_perfect = deviation < 1e-10
    return is_perfect


def check_if_perfect_square(value: int) -> bool:
    return check_if_perfect(value, 2)


def check_if_perfect_cube(value: int) -> bool:
    return check_if_perfect(value, 3)


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(21, is_official)
    farm = FarmMap(data)
    initial_steps = 64 if is_official else 6
    actual_steps = 26501365 if is_official else 100
    part_1 = farm.determine_reachable_plots_after_certain_steps(initial_steps)
    part_2 = farm.determine_reachable_plots_after_certain_steps(actual_steps)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(21, part_1, part_2, execution_time)
    return results
