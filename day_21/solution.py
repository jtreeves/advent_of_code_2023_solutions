import time
from typing import Tuple, Set, List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class FarmMap:
    def __init__(self, description: str) -> None:
        self.rows = get_list_of_lines(description)
        self.height = self.calculate_height()
        self.width = self.calculate_width()
        self.positions = self.create_positions()
        self.y_min = 0
        self.y_max = self.height - 1
        self.x_min = 0
        self.x_max = self.width - 1

    def calculate_height(self) -> int:
        return len(self.rows)

    def calculate_width(self) -> int:
        return len(self.rows[0])

    def create_positions(self) -> dict[Tuple[int, int], bool]:
        positions: dict[Tuple[int, int], bool] = {}
        for row in range(self.height):
            for column in range(self.width):
                representation = self.rows[row][column]
                value = True if representation == "." or representation == "S" else False
                coordinates = (column, row)
                positions[coordinates] = value
                if representation == "S":
                    self.start = coordinates
        return positions

    def find_possible_positions_after_step(self, start_position: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = start_position
        possible_positions: List[Tuple[int, int]] = []
        possible_coordinates = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for coordinates in possible_coordinates:
            new_x, new_y = coordinates
            if not self.x_min <= new_x <= self.x_max or not self.y_min <= new_y <= self.y_max:
                self.expand_positions()
            possible_plot = self.positions.get(coordinates)
            if possible_plot:
                possible_positions.append(coordinates)
        return possible_positions

    def find_all_possible_positions_after_step_with_multiple_starts(self, starting_positions: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        ending_positions: Set[Tuple[int, int]] = set()
        for position in starting_positions:
            possible_positions = self.find_possible_positions_after_step(position)
            ending_positions.update(possible_positions)
        return ending_positions

    def determine_reachable_plots_after_certain_steps_by_traversal(self, steps: int) -> int:
        current_step = 0
        # all_visited_positions: Set[Tuple[int, int]] = set([self.start])
        current_positions: Set[Tuple[int, int]] = set([self.start])
        while current_step < steps:
            current_step += 1
            # previous_farm_size = len(self.positions)
            # previous_total_positions = len(all_visited_positions)
            # previous_positions_length = len(current_positions)
            current_positions = self.find_all_possible_positions_after_step_with_multiple_starts(current_positions)
            # all_visited_positions.update(current_positions)
            # updated_total_positions = len(all_visited_positions)
            # change_in_totals = updated_total_positions - previous_total_positions
            # updated_farm_size = len(self.positions)
            # change_in_farm_size = updated_farm_size - previous_farm_size
            # if change_in_farm_size:
            #     print('CHANGE IN FARM SIZE:', change_in_farm_size)
            # print(f"{current_step} -> {change_in_totals}")
            # current_positions_length = len(current_positions)
            # print(f"{current_step} -> {current_positions_length}")
            # change_in_positions = current_positions_length - previous_positions_length
            # print(f"{current_step} -> {change_in_positions}")
            # step_square = check_if_perfect_square(current_step)
            # step_cube = check_if_perfect_cube(current_step)
            # farm_size = len(self.positions)
            # print(f"{current_step} -> {current_positions_length}\nCHANGE: {change_in_positions}\nPERFECTS? square - {step_square}; cube - {step_cube}\nFARM SIZE:{farm_size}\n*****")
        return len(current_positions)

    def determine_reachable_plots_after_certain_steps_by_equation(self, steps: int) -> int:
        equation = self.determine_quadratic_equation_for_positions()
        a, b, c = equation
        reachable_plots = a * steps**2 + b * steps + c
        return int(reachable_plots)

    def expand_positions(self) -> None:
        current_height = self.y_max - self.y_min + 1
        current_width = self.x_max - self.x_min + 1
        self.y_max += current_height
        self.y_min -= current_height
        self.x_max += current_width
        self.x_min -= current_width
        x_values = [-current_width, current_width, 0]
        y_values = [-current_height, current_height, 0]
        shifts = [(x, y) for x in x_values for y in y_values if (x, y) != (0, 0)]
        new_maps: List[dict[Tuple[int, int], bool]] = []
        for shift in shifts:
            shifted_map = {}
            for coordinates, value in self.positions.items():
                shifted_coordinates = tuple(x + dx for x, dx in zip(coordinates, shift))
                shifted_map[shifted_coordinates] = value
            new_maps.append(shifted_map)
        for new_map in new_maps:
            self.positions.update(new_map)

    def determine_quadratic_equation_for_positions(self) -> List[int]:
        core_farm_size = self.height
        # print(core_farm_size)
        # start_value = 5
        half_way_point = core_farm_size // 2
        steps = [half_way_point, half_way_point + 2 * core_farm_size, half_way_point + 4 * core_farm_size]
        # steps = [10, 20, 30]
        # steps = [start_value, start_value + core_farm_size, start_value + 2 * core_farm_size]
        print(steps)
        coordinate_pairs: List[Tuple[int, int]] = []
        for count in steps:
            positions = self.determine_reachable_plots_after_certain_steps_by_traversal(count)
            coordinate_pairs.append((count, positions))
        coefficients, constants = create_matrices_for_system(coordinate_pairs)
        result = solve_3x3_system_with_cramers_rule(coefficients, constants)
        print('QUADRATIC EQUATION FOR SYSTEM:', result)
        return result


def check_if_perfect(value: int, power: int) -> bool:
    root = round(value ** (1 / power))
    original = root ** power
    deviation = abs(original - value)
    is_perfect = deviation < 1e-10
    return is_perfect


def check_if_perfect_square(value: int) -> bool:
    return check_if_perfect(value, 2)


def check_if_perfect_cube(value: int) -> bool:
    return check_if_perfect(value, 3)


def create_quadratic_vector(coordinates: Tuple[int, int]) -> List[int]:
    x, y = coordinates
    vector = [x**2, x, 1, y]
    return vector


def create_matrices_for_system(coordinate_pairs: List[Tuple[int, int]]) -> Tuple[List[List[int]], List[int]]:
    coefficients: List[List[int]] = []
    constants: List[int] = []
    for pair in coordinate_pairs:
        vector = create_quadratic_vector(pair)
        # print('VECTOR:', vector)
        coefficients.append(vector[:-1])
        constants.append(vector[-1])
    return coefficients, constants


def calculate_determinant_for_2x2_matrix(matrix: List[List[int]]) -> int:
    T, B = matrix
    a, b = T
    c, d = B
    determinant = a * d - b * c
    return determinant


def calculate_determinant_for_3x3_matrix(matrix: List[List[int]]) -> int:
    T, M, B = matrix
    # print('T:', T)
    # print('M:', M)
    # print('B:', B)
    a, b, c = T
    d, e, f = M
    g, h, i = B
    minor_a = calculate_determinant_for_2x2_matrix([[e, f], [h, i]])
    minor_b = calculate_determinant_for_2x2_matrix([[d, f], [g, i]])
    minor_c = calculate_determinant_for_2x2_matrix([[d, e], [g, h]])
    determinant = a * minor_a - b * minor_b + c * minor_c
    return determinant


def formulate_minors_matrix(matrix: List[List[int]]) -> List[List[int]]:
    minors_matrix: List[List[int]] = []
    for i in range(3):
        row: List[int] = []
        for j in range(3):
            minor_matrix = [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]
            minor_determinant = calculate_determinant_for_2x2_matrix(minor_matrix)
            row.append(minor_determinant)
        minors_matrix.append(row)
    return minors_matrix


def formulate_cofactors_matrix(matrix: List[List[int]]) -> List[List[int]]:
    minors_matrix = formulate_minors_matrix(matrix)
    cofactors_matrix: List[List[int]] = []
    for i in range(3):
        row: List[int] = []
        for j in range(3):
            sign = (-1) ** (i + j)
            cofactor_value = sign * minors_matrix[i][j]
            row.append(cofactor_value)
        cofactors_matrix.append(row)
    return cofactors_matrix


def formulate_adjugate_matrix(matrix: List[List[int]]) -> List[List[int]]:
    cofactors_matrix = formulate_cofactors_matrix(matrix)
    adjugate_matrix = [[cofactors_matrix[j][i] for j in range(3)] for i in range(3)]
    return adjugate_matrix


def formulate_inverse_matrix(matrix: List[List[int]]) -> List[List[float]]:
    determinant = calculate_determinant_for_3x3_matrix(matrix)
    # print('DETERMINANT:', determinant)
    adjugate_matrix = formulate_adjugate_matrix(matrix)
    inverse_matrix = [[adjugate_matrix[i][j] / determinant for j in range(3)] for i in range(3)]
    return inverse_matrix


def multiply_matrix_by_vector(matrix: List[List[float]], vector: List[int]) -> List[float]:
    product: List[float] = [0.0, 0.0, 0.0]
    for i in range(3):
        for j in range(3):
            product[i] += matrix[i][j] * vector[j]
    return product


def create_matrix_with_column_replaced(matrix: List[List[int]], replacement_column: List[int], column_index: int) -> List[List[int]]:
    result_matrix: List[List[int]] = [row.copy() for row in matrix]
    for index in range(len(result_matrix)):
        result_matrix[index][column_index] = replacement_column[index]
    return result_matrix


def solve_3x3_system_with_matrix_inverse(coefficients: List[List[int]], constants: List[int]) -> List[float]:
    # print('COEFFICIENTS:', coefficients)
    # print('CONSTANTS:', constants)
    inverse_coefficients = formulate_inverse_matrix(coefficients)
    # print('INVERSE MATRIX:', inverse_coefficients)
    solution = multiply_matrix_by_vector(inverse_coefficients, constants)
    # coefficients_determinant = calculate_determinant_for_3x3_matrix(coefficients)
    # print('COEFFICIENTS DET:', coefficients_determinant)
    # for index in range(3):
    #     variable_matrix = create_matrix_with_column_replaced(coefficients, constants, index)
    #     print('MATRIX WITH COLUMN REPLACED:', variable_matrix)
    #     variable_determinant = calculate_determinant_for_3x3_matrix(variable_matrix)
    #     print('VARIABLE DET:', variable_determinant)
    #     variable_value = variable_determinant / coefficients_determinant
    #     solution.append(variable_value)
    return solution


def solve_3x3_system_with_cramers_rule(coefficients: List[List[int]], constants: List[int]) -> List[int]:
    # print('COEFFICIENTS:', coefficients)
    # print('CONSTANTS:', constants)
    # inverse_coefficients = formulate_inverse_matrix(coefficients)
    # print('INVERSE MATRIX:', inverse_coefficients)
    # solution = multiply_matrix_by_vector(inverse_coefficients, constants)
    solution: List[int] = []
    coefficients_determinant = calculate_determinant_for_3x3_matrix(coefficients)
    # print('COEFFICIENTS DET:', coefficients_determinant)
    for index in range(3):
        variable_matrix = create_matrix_with_column_replaced(coefficients, constants, index)
        # print('MATRIX WITH COLUMN REPLACED:', variable_matrix)
        variable_determinant = calculate_determinant_for_3x3_matrix(variable_matrix)
        # print('VARIABLE DET:', variable_determinant)
        variable_value = variable_determinant // coefficients_determinant
        solution.append(variable_value)
    return solution


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(21, is_official)
    farm = FarmMap(data)
    initial_steps = 64 if is_official else 6
    actual_steps = 26501365 if is_official else 100
    part_1 = farm.determine_reachable_plots_after_certain_steps_by_traversal(initial_steps)
    part_2 = farm.determine_reachable_plots_after_certain_steps_by_equation(actual_steps)
    # coefficients, constants = create_matrices_for_system([(3, 14), (4, 25), (7, 82)])
    # result = solve_3x3_system_with_cramers_rule(coefficients, constants)
    # result = solve_3x3_system_with_matrix_inverse([[1, 1, 1], [0, 2, 5], [2, 5, -1]], [6, -4, 27])
    # print('TEST RESULT:', result)
    # det = calculate_determinant_for_3x3_matrix([[6, 1, 1], [4, -2, 5], [2, 8, 7]])
    # print('DETERMINANT:', det)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(21, part_1, part_2, execution_time)
    return results
