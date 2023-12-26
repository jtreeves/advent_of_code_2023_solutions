import time
from typing import Tuple, Sequence
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


def create_hiking_map(description: str) -> dict[Tuple[int, int], str]:
    hiking_map: dict[Tuple[int, int], str] = {}
    rows = get_list_of_lines(description)
    for row in range(len(rows)):
        for column in range(len(rows[0])):
            hiking_map[(column, row)] = rows[row][column]
    return hiking_map


def find_start_and_end(hiking_map: dict[Tuple[int, int], str]) -> dict[str, Tuple[int, int]]:
    start_and_end: dict[str, Tuple[int, int]] = {}
    max_y = 0
    for [k, v] in hiking_map.items():
        y = k[1]
        if y > max_y:
            max_y = y
        if y == 0 and v == ".":
            start_and_end["start"] = k
        if y == max_y and v == ".":
            start_and_end["end"] = k
    return start_and_end


def find_traversable_neighbors(position: Tuple[int, int], hiking_map: dict[Tuple[int, int], str], minding_slopes: bool) -> Sequence[Tuple[int, int]]:
    traversable_neighbors: Sequence[Tuple[int, int]] = []
    x, y = position
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        next_position = hiking_map.get((nx, ny))
        if next_position and next_position != "#":
            if not minding_slopes:
                traversable_neighbors.append((nx, ny))
            else:
                if (nx < x and next_position != ">") or (nx > x and next_position != "<") or (ny < y and next_position != "v") or (ny > y and next_position != "^"):
                    traversable_neighbors.append((nx, ny))
    return traversable_neighbors


def determine_longest_path_length(hiking_map: dict[Tuple[int, int], str], minding_slopes: bool) -> int:
    longest_path_length = 0
    start_and_end = find_start_and_end(hiking_map)
    start = start_and_end["start"]
    end = start_and_end["end"]
    stack: Sequence[Sequence[Tuple[int, int]]] = [[start]]
    while len(stack):
        print('STACK LENGTH:', len(stack))
        print('CURRENT MAX LENGTH:', longest_path_length)
        path = stack.pop()
        current_location = path[-1]
        if current_location == end and len(path) - 1 > longest_path_length:
            longest_path_length = len(path) - 1
        else:
            neighbors = find_traversable_neighbors(current_location, hiking_map, minding_slopes)
            for neighbor in neighbors:
                if neighbor not in path:
                    stack.append([*path, neighbor])
    return longest_path_length


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(23, is_official)
    hiking_map = create_hiking_map(data)
    part_1 = determine_longest_path_length(hiking_map, True)
    # EXCEPTION: Brute-force technique requires more than 2 days to execute with full data, and even then it doesn't finish, it merely has found the longest path (not verified it)
    part_2 = determine_longest_path_length(hiking_map, False)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(23, part_1, part_2, execution_time)
    return results
