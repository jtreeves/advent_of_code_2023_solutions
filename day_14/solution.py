import time
from typing import List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


def tilt_north(rows: List[str]) -> List[str]:
    return tilt_vertically(rows, True)


def tilt_south(rows: List[str]) -> List[str]:
    return tilt_vertically(rows, False)


def tilt_west(rows: List[str]) -> List[str]:
    return tilt_horizontally(rows, False)


def tilt_east(rows: List[str]) -> List[str]:
    return tilt_horizontally(rows, True)


def tilt_vertically(rows: List[str], increasing: bool) -> List[str]:
    columns = [''.join(column) + "#" for column in [list(reversed(x)) for x in zip(*rows)]]
    final_columns = tilt_in_direction(columns, increasing)
    final_rows = list(reversed([''.join(row) for row in [list(x) for x in zip(*final_columns)]]))
    return final_rows


def tilt_horizontally(rows: List[str], increasing: bool) -> List[str]:
    reversed_rows = [row + "#" for row in rows[::-1]]
    final_rows = tilt_in_direction(reversed_rows, increasing)
    return final_rows[::-1]


def tilt_in_direction(vectors: List[str], increasing: bool) -> List[str]:
    final_vectors: List[str] = []
    for vector in vectors:
        last_cube = 0
        cube = vector.find("#")
        final_vector = ""
        while cube > -1:
            sub_column = vector[last_cube:cube]
            spheres = sub_column.count("O")
            empties = sub_column.count(".")
            if increasing:
                for _ in range(empties):
                    final_vector += "."
                for _ in range(spheres):
                    final_vector += "O"
            else:
                for _ in range(spheres):
                    final_vector += "O"
                for _ in range(empties):
                    final_vector += "."
            last_cube = cube
            cube = vector.find("#", cube + 1)
            if len(final_vector) < len(vector) - 1:
                final_vector += "#"
        final_vectors.append(final_vector)
    return final_vectors


def spin_cycle(rows: List[str]) -> List[str]:
    rows_after_north = tilt_north(rows)
    rows_after_west = tilt_west(rows_after_north)
    rows_after_south = tilt_south(rows_after_west)
    rows_after_east = tilt_east(rows_after_south)
    return rows_after_east


def calculate_north_load(rows: List[str]) -> int:
    reversed_rows = list(reversed(rows))
    total = 0
    for index in range(len(reversed_rows)):
        total += reversed_rows[index].count("O") * (index + 1)
    return total


def calculate_north_load_after_multiple_spin_cycles(rows: List[str], cycles: int) -> int:
    final_rows: List[str] = rows
    loads: List[int] = []
    current_cycle = 0
    pattern_length = -1
    start_index = -1
    minimum_pattern_length = 3
    while current_cycle < cycles and pattern_length < minimum_pattern_length:
        final_rows = spin_cycle(final_rows)
        loads.append(calculate_north_load(final_rows))
        pattern = find_pattern(loads)
        if pattern["pattern_length"] > minimum_pattern_length:
            pattern_length = pattern["pattern_length"]
            start_index = pattern["start_index"]
        else:
            current_cycle += 1
    if pattern_length > minimum_pattern_length:
        index_in_main = (cycles - start_index) % pattern_length + start_index - 1
        load = loads[index_in_main]
    else:
        load = loads[-1]
    return load


def find_pattern(integers: List[int]) -> dict[str, int]:
    original_length = len(integers)
    current_index = 1
    start_index = -1
    pattern_length = -1
    minimum_pattern_length = 3
    while current_index < original_length and pattern_length < minimum_pattern_length:
        start = 0
        while start < current_index and pattern_length < minimum_pattern_length:
            end = start
            while end < start + current_index and pattern_length < minimum_pattern_length:
                if original_length % current_index == 0:
                    pattern = integers[start:end]
                    repeated_pattern = pattern * 2
                    repeated_length = len(repeated_pattern)
                    repeated_is_subset = False
                    for i in range(original_length - repeated_length + 1):
                        if integers[i:i + repeated_length] == repeated_pattern:
                            repeated_is_subset = True
                    if repeated_is_subset:
                        start_index = start
                        pattern_length = len(pattern)
                end += 1
            start += 1
        current_index += 1
    return {
        "start_index": start_index,
        "pattern_length": pattern_length
    }


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(14, is_official)
    rows = get_list_of_lines(data)
    part_1 = calculate_north_load(tilt_north(rows))
    part_2 = calculate_north_load_after_multiple_spin_cycles(rows, 1000000000)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(14, part_1, part_2, execution_time)
    return results
