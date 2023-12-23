import time
from typing import List, Tuple, Sequence
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


def create_dig_plan(steps: List[str]) -> dict[Tuple[int, int], str]:
    plan: dict[Tuple[int, int], str] = {}
    current_vertex = (0, 0)
    for step in steps:
        elements = step.split(" ")
        direction = elements[0]
        length = int(elements[1])
        color = elements[2][1:-1]
        x1, y1 = current_vertex
        if direction == "R":
            x2, y2 = x1 + length, y1
        elif direction == "D":
            x2, y2 = x1, y1 + length
        elif direction == "L":
            x2, y2 = x1 - length, y1
        else:
            x2, y2 = x1, y1 - length
        current_vertex = (x2, y2)
        plan[current_vertex] = color
    return plan


def extract_vertices_from_plan(plan: dict[Tuple[int, int], str]) -> Sequence[Tuple[int, int]]:
    vertices: Sequence[Tuple[int, int]] = []
    for vertex in plan.keys():
        vertices.append(vertex)
    return vertices


def calculate_area_with_shoelace(vertices: Sequence[Tuple[int, int]]) -> int:
    area = 0
    size = len(vertices)
    for index in range(size):
        x1, y1 = vertices[index]
        x2, y2 = vertices[(index + 1) % size]
        area += x1 * y2 - x2 * y1
    return int(abs(area) / 2)


def calculate_perimeter(vertices: Sequence[Tuple[int, int]]) -> int:
    perimeter = 0
    for index in range(len(vertices)):
        x2, y2 = vertices[index]
        x1, y1 = vertices[index - 1]
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        perimeter += dx + dy
    return perimeter


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(18, is_official)
    steps = get_list_of_lines(data)
    plan = create_dig_plan(steps)
    vertices = extract_vertices_from_plan(plan)
    print('VERTICES:', vertices)
    area = calculate_area_with_shoelace(vertices)
    perimeter = calculate_perimeter(vertices)
    print('AREA:', area)
    print('PERIMETER:', perimeter)
    part_1 = area
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(18, part_1, part_2, execution_time)
    return results
