import time
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


def apply_hash_algorithm(input: str) -> int:
    value = 0
    for character in input:
        value += ord(character)
        value *= 17
        value %= 256
    return value


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(15, is_official)
    steps = data.split(",")
    hash_value = 0
    for step in steps:
        hash_value += apply_hash_algorithm(step)
    part_1 = hash_value
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(15, part_1, part_2, execution_time)
    return results
