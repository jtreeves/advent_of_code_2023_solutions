import time
from typing import Tuple, Set, List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Map:
    def __init__(self, description: str) -> None:
        self.rows = get_list_of_lines(description)
        self.height = self.calculate_height()
        self.width = self.calculate_width()
        self.positions = self.create_positions()

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
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
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


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(21, is_official)
    map = Map(data)
    steps = 64 if is_official else 6
    part_1 = map.determine_reachable_plots_after_certain_steps(steps)
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(21, part_1, part_2, execution_time)
    return results
