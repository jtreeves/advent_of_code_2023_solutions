import time
from typing import List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


def determine_linear_equation_elements(data: str) -> List[List[int]]:
    lines = get_list_of_lines(data)
    linear_equation_elements: List[List[int]] = []
    for line in lines:
        trimmed = line.replace(" ", "")
        parts = trimmed.split("@")
        constants = parts[0].split(",")
        velocities = parts[1].split(",")
        xc = int(constants[0])
        yc = int(constants[1])
        xv = int(velocities[0])
        yv = int(velocities[1])
        linear_equation_elements.append([xc, yc, xv, yv])
    return linear_equation_elements


def calculate_2d_matrix_inverse(matrix: List[List[int]]) -> List[List[float]] | None:
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]
    d = matrix[1][1]
    determinant = a * d - b * c
    if determinant:
        reciprocal = 1 / determinant
        top = [d * reciprocal, -1 * b * reciprocal]
        bottom = [-1 * c * reciprocal, a * reciprocal]
        return [top, bottom]
    else:
        return None


def determine_2d_intersection_point(coefficients: List[List[int]], constants: List[int]) -> List[float] | None:
    inverse = calculate_2d_matrix_inverse(coefficients)
    if inverse:
        a = inverse[0][0]
        b = inverse[0][1]
        c = inverse[1][0]
        d = inverse[1][1]
        e = constants[0]
        f = constants[1]
        x = a * e + b * f
        y = c * e + d * f
        return [x, y]
    else:
        return None


def find_all_intersections_within_interval(equation_elements: List[List[int]]) -> int:
    total = 0
    min = 200000000000000
    max = 400000000000000
    for index in range(len(equation_elements) - 1):
        first_equation_elements = equation_elements[index]
        xc1 = first_equation_elements[0]
        yc1 = first_equation_elements[1]
        xv1 = first_equation_elements[2]
        yv1 = first_equation_elements[3]
        first_coefficients = [yv1, -1 * xv1]
        first_constant = yv1 * xc1 - xv1 * yc1
        for second_index in range(index + 1, len(equation_elements)):
            second_equation_elements = equation_elements[second_index]
            xc2 = second_equation_elements[0]
            yc2 = second_equation_elements[1]
            xv2 = second_equation_elements[2]
            yv2 = second_equation_elements[3]
            second_coefficients = [yv2, -1 * xv2]
            second_constant = yv2 * xc2 - xv2 * yc2
            coefficients = [first_coefficients, second_coefficients]
            constants = [first_constant, second_constant]
            intersection_point = determine_2d_intersection_point(coefficients, constants)
            if intersection_point:
                x = intersection_point[0]
                y = intersection_point[1]
                t1 = (x - xc1) / xv1
                t2 = (x - xc2) / xv2
                if min < x < max and min < y < max and t1 > 0 and t2 > 0:
                    total += 1
    return total


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(24, is_official)
    equation_elements = determine_linear_equation_elements(data)
    part_1 = find_all_intersections_within_interval(equation_elements)
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(24, part_1, part_2, execution_time)
    return results
