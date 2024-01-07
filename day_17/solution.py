import time
import heapq
from typing import List, Tuple, Set
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class City:
    def __init__(self, description: str) -> None:
        self.rows = get_list_of_lines(description)
        self.height = self.calculate_height()
        self.width = self.calculate_width()
        self.blocks = self.create_blocks()
        self.start = 0, 0
        self.end = self.width - 1, self.height - 1

    def calculate_height(self) -> int:
        return len(self.rows)

    def calculate_width(self) -> int:
        return len(self.rows[0])

    def create_blocks(self) -> dict[Tuple[int, int], int]:
        blocks: dict[Tuple[int, int], int] = {}
        for row in range(self.height):
            for column in range(self.width):
                heat_loss = int(self.rows[row][column])
                coordinates = column, row
                blocks[coordinates] = heat_loss
        return blocks

    def minimize_heat_loss(self, least_steps: int, most_steps: int) -> int:
        queue: List[Tuple[int, int, int, int, int]] = [(0, *self.start, 0, 0)]
        visited: Set[Tuple[int, int, int, int]] = set()
        directions: Set[Tuple[int, int]] = {(1, 0), (0, 1), (-1, 0), (0, -1)}
        while queue:
            heat, x, y, px, py = heapq.heappop(queue)
            if (x, y) == self.end:
                return heat
            if (x, y, px, py) in visited:
                continue
            visited.add((x, y, px, py))
            previous_changes: Set[Tuple[int, int]] = {(px, py), (-px, -py)}
            for dx, dy in directions - previous_changes:
                nx, ny, nh = x, y, heat
                for i in range(1, most_steps + 1):
                    nx, ny = nx + dx, ny + dy
                    if (nx, ny) in self.blocks:
                        nh += self.blocks[(nx, ny)]
                        if i >= least_steps:
                            heapq.heappush(queue, (nh, nx, ny, dx, dy))
        return 0


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(17, is_official)
    city = City(data)
    part_1 = city.minimize_heat_loss(1, 3)
    part_2 = city.minimize_heat_loss(4, 10)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(17, part_1, part_2, execution_time)
    return results

# CREDIT: https://www.reddit.com/r/adventofcode/comments/18k9ne5/comment/kdq86mr/
# Used to find efficient search algorithm via priority queue and keeping track of only turns (similar to one of my earlier attempts)
