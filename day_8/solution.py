import time
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


def solution(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(8, is_official)
    part_1 = 1 if data else 0
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(8, part_1, part_2, execution_time)
    return results
