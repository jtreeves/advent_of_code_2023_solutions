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
        current_vertex = determine_next_vertex(current_vertex, direction, length)
        plan[current_vertex] = color
    return plan


def extract_vertices_from_plan(plan: dict[Tuple[int, int], str]) -> Sequence[Tuple[int, int]]:
    vertices: Sequence[Tuple[int, int]] = []
    for vertex in plan.keys():
        vertices.append(vertex)
    return vertices


def convert_colors_to_vertices(plan: dict[Tuple[int, int], str]) -> Sequence[Tuple[int, int]]:
    vertices: Sequence[Tuple[int, int]] = []
    current_vertex = (0, 0)
    for color in plan.values():
        direction_code = int(color[-1])
        direction = "R" if direction_code == 0 else "D" if direction_code == 1 else "L" if direction_code == 2 else "U"
        length = int(color[1:-1], 16)
        current_vertex = determine_next_vertex(current_vertex, direction, length)
        vertices.append(current_vertex)
    return vertices


def determine_next_vertex(current_vertex: Tuple[int, int], direction: str, length: int) -> Tuple[int, int]:
    x1, y1 = current_vertex
    if direction == "R":
        x2, y2 = x1 + length, y1
    elif direction == "D":
        x2, y2 = x1, y1 + length
    elif direction == "L":
        x2, y2 = x1 - length, y1
    else:
        x2, y2 = x1, y1 - length
    next_vertex = (x2, y2)
    return next_vertex


def calculate_area_with_shoelace(vertices: Sequence[Tuple[int, int]]) -> int:
    area = 0
    size = len(vertices)
    for index in range(size):
        x1, y1 = vertices[index]
        x2, y2 = vertices[(index + 1) % size]
        area += x1 * y2 - x2 * y1 + abs(x2 - x1) + abs(y2 - y1)
    return 1 + abs(area) // 2


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(18, is_official)
    steps = get_list_of_lines(data)
    plan = create_dig_plan(steps)
    original_vertices = extract_vertices_from_plan(plan)
    color_vertices = convert_colors_to_vertices(plan)
    part_1 = calculate_area_with_shoelace(original_vertices)
    part_2 = calculate_area_with_shoelace(color_vertices)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(18, part_1, part_2, execution_time)
    return results
