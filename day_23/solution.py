import time
from typing import List, Tuple, Sequence
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


def find_traversable_neighbors(position: Tuple[int, int], hiking_map: dict[Tuple[int, int], str]) -> Sequence[Tuple[int, int]]:
    traversable_neighbors: Sequence[Tuple[int, int]] = []
    x, y = position
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        next_position = hiking_map.get((nx, ny))
        if next_position and next_position != "#":
            if (nx < x and next_position != ">") or (nx > x and next_position != "<") or (ny < y and next_position != "v") or (ny > y and next_position != "^"):
                traversable_neighbors.append((nx, ny))
    return traversable_neighbors


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


def determine_longest_path_length(hiking_map: dict[Tuple[int, int], str]) -> int:
    path_lengths: List[int] = []
    start_and_end = find_start_and_end(hiking_map)
    start = start_and_end["start"]
    end = start_and_end["end"]
    stack: Sequence[Sequence[Tuple[int, int]]] = [[start]]
    while len(stack):
        path = stack.pop()
        current_location = path[-1]
        if current_location == end:
            path_lengths.append(len(path) - 1)
        else:
            neighbors = find_traversable_neighbors(current_location, hiking_map)
            for neighbor in neighbors:
                if neighbor not in path:
                    stack.append([*path, neighbor])
    return sorted(path_lengths)[-1]


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(23, is_official)
    hiking_map = create_hiking_map(data)
    part_1 = determine_longest_path_length(hiking_map)
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(23, part_1, part_2, execution_time)
    return results
