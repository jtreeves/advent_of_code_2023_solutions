import time
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(14, is_official)
    rows = get_list_of_lines(data)
    columns = [''.join(column) + "#" for column in [list(reversed(x)) for x in zip(*rows)]]
    total = 0
    for column in columns:
        last_cube = 0
        cube = column.find("#")
        while cube > -1:
            sub_column = column[last_cube:cube]
            spheres = sub_column.count("O")
            for sphere in range(spheres):
                total += cube - sphere
            last_cube = cube
            cube = column.find("#", cube + 1)
    part_1 = total
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(14, part_1, part_2, execution_time)
    return results
