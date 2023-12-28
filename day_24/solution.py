import time
from math import log10, ceil
from typing import List, Set
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
        zc = int(constants[2])
        xv = int(velocities[0])
        yv = int(velocities[1])
        zv = int(velocities[2])
        linear_equation_elements.append([xc, yc, zc, xv, yv, zv])
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


def find_all_2d_intersections_within_interval(equation_elements: List[List[int]], minimum: int, maximum: int) -> int:
    total = 0
    for index in range(len(equation_elements) - 1):
        first_equation_elements = equation_elements[index]
        xc1 = first_equation_elements[0]
        yc1 = first_equation_elements[1]
        xv1 = first_equation_elements[3]
        yv1 = first_equation_elements[4]
        first_coefficients = [yv1, -1 * xv1]
        first_constant = yv1 * xc1 - xv1 * yc1
        for second_index in range(index + 1, len(equation_elements)):
            second_equation_elements = equation_elements[second_index]
            xc2 = second_equation_elements[0]
            yc2 = second_equation_elements[1]
            xv2 = second_equation_elements[3]
            yv2 = second_equation_elements[4]
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
                if minimum < x < maximum and minimum < y < maximum and t1 > 0 and t2 > 0:
                    total += 1
    return total


def get_velocity_magnitude_for_dimension(equation_elements: List[List[int]], velocity_index: int) -> int:
    magnitude = 0
    for equation in equation_elements:
        velocity = equation[velocity_index]
        current_magnitude = ceil(log10(abs(velocity)))
        if current_magnitude > magnitude:
            magnitude = current_magnitude
    return magnitude


def find_velocity_for_dimension_with_parallels(equation_elements: List[List[int]], velocity_index: int) -> int:
    velocities: Set[int] = set()
    index = 0
    velocity_magnitude = get_velocity_magnitude_for_dimension(equation_elements, velocity_index)
    while len(velocities) != 1 and index < len(equation_elements) - 1:
        first_equation_elements = equation_elements[index]
        v1 = first_equation_elements[velocity_index]
        for second_index in range(index + 1, len(equation_elements)):
            second_equation_elements = equation_elements[second_index]
            v2 = second_equation_elements[velocity_index]
            if v1 == v2:
                sub_velocities: Set[int] = set()
                constant_index = velocity_index - 3
                c1 = first_equation_elements[constant_index]
                c2 = second_equation_elements[constant_index]
                distance = abs(c2 - c1)
                factors = [i for i in range(-10**velocity_magnitude, 10**velocity_magnitude) if i != 0 and distance % i == 0]
                for factor in factors:
                    potential_velocity = v1 - factor
                    if potential_velocity:
                        sub_velocities.add(potential_velocity)
                if len(velocities):
                    velocities &= sub_velocities
                else:
                    velocities = sub_velocities
        index += 1
    return velocities.pop()


def calculate_initial_positions_with_cramers_rule(equation_elements: List[List[int]]) -> List[int]:
    x_velocity = find_velocity_for_dimension_with_parallels(equation_elements, 3)
    y_velocity = find_velocity_for_dimension_with_parallels(equation_elements, 4)
    z_velocity = find_velocity_for_dimension_with_parallels(equation_elements, 5)
    index = 0
    coefficients: List[List[int]] = []
    constants: List[int] = []
    while index < 3:
        xc, yc, zc, xv, yv, zv = equation_elements[index]
        total_xv = xv - x_velocity
        total_yv = yv - y_velocity
        total_zv = zv - z_velocity
        x_coefficient = total_yv * total_zv
        y_coefficient = total_xv * total_zv
        z_coefficient = -2 * total_xv * total_yv
        coefficients.append([x_coefficient, y_coefficient, z_coefficient])
        constants.append(xc * x_coefficient + yc * y_coefficient + zc * z_coefficient)
        index += 1
    x_coefficients: List[List[int]] = [[], [], []]
    y_coefficients: List[List[int]] = [[], [], []]
    z_coefficients: List[List[int]] = [[], [], []]
    for column in range(3):
        if column == 0:
            x_coefficients[0].append(constants[0])
            x_coefficients[1].append(constants[1])
            x_coefficients[2].append(constants[2])
            x_coefficients[0].append(coefficients[0][1])
            x_coefficients[1].append(coefficients[1][1])
            x_coefficients[2].append(coefficients[2][1])
            x_coefficients[0].append(coefficients[0][2])
            x_coefficients[1].append(coefficients[1][2])
            x_coefficients[2].append(coefficients[2][2])
        elif column == 1:
            y_coefficients[0].append(coefficients[0][0])
            y_coefficients[1].append(coefficients[1][0])
            y_coefficients[2].append(coefficients[2][0])
            y_coefficients[0].append(constants[0])
            y_coefficients[1].append(constants[1])
            y_coefficients[2].append(constants[2])
            y_coefficients[0].append(coefficients[0][2])
            y_coefficients[1].append(coefficients[1][2])
            y_coefficients[2].append(coefficients[2][2])
        else:
            z_coefficients[0].append(coefficients[0][0])
            z_coefficients[1].append(coefficients[1][0])
            z_coefficients[2].append(coefficients[2][0])
            z_coefficients[0].append(coefficients[0][1])
            z_coefficients[1].append(coefficients[1][1])
            z_coefficients[2].append(coefficients[2][1])
            z_coefficients[0].append(constants[0])
            z_coefficients[1].append(constants[1])
            z_coefficients[2].append(constants[2])
    coefficients_determinant = coefficients[0][0] * (coefficients[1][1] * coefficients[2][2] - coefficients[1][2] * coefficients[2][1]) - coefficients[0][1] * (coefficients[1][0] * coefficients[2][2] - coefficients[1][2] * coefficients[2][0]) + coefficients[0][2] * (coefficients[1][0] * coefficients[2][1] - coefficients[1][1] * coefficients[2][0])
    x_determinant = x_coefficients[0][0] * (x_coefficients[1][1] * x_coefficients[2][2] - x_coefficients[1][2] * x_coefficients[2][1]) - x_coefficients[0][1] * (x_coefficients[1][0] * x_coefficients[2][2] - x_coefficients[1][2] * x_coefficients[2][0]) + x_coefficients[0][2] * (x_coefficients[1][0] * x_coefficients[2][1] - x_coefficients[1][1] * x_coefficients[2][0])
    y_determinant = y_coefficients[0][0] * (y_coefficients[1][1] * y_coefficients[2][2] - y_coefficients[1][2] * y_coefficients[2][1]) - y_coefficients[0][1] * (y_coefficients[1][0] * y_coefficients[2][2] - y_coefficients[1][2] * y_coefficients[2][0]) + y_coefficients[0][2] * (y_coefficients[1][0] * y_coefficients[2][1] - y_coefficients[1][1] * y_coefficients[2][0])
    z_determinant = z_coefficients[0][0] * (z_coefficients[1][1] * z_coefficients[2][2] - z_coefficients[1][2] * z_coefficients[2][1]) - z_coefficients[0][1] * (z_coefficients[1][0] * z_coefficients[2][2] - z_coefficients[1][2] * z_coefficients[2][0]) + z_coefficients[0][2] * (z_coefficients[1][0] * z_coefficients[2][1] - z_coefficients[1][1] * z_coefficients[2][0])
    x = x_determinant // coefficients_determinant
    y = y_determinant // coefficients_determinant
    z = z_determinant // coefficients_determinant
    return [x, y, z]


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(24, is_official)
    equation_elements = determine_linear_equation_elements(data)
    minimum = 200000000000000 if is_official else 7
    maximum = 400000000000000 if is_official else 27
    part_1 = find_all_2d_intersections_within_interval(equation_elements, minimum, maximum)
    part_2 = sum(calculate_initial_positions_with_cramers_rule(equation_elements))
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(24, part_1, part_2, execution_time)
    return results
