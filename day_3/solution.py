import time
from typing import List
from utils.extract_data_from_file import extract_data_from_file
from utils.get_list_of_lines import get_list_of_lines
from utils.Cell import Cell
from utils.Grid import Grid
from utils.SolutionResults import SolutionResults

special_character_values = ["@", "#", "$", "%", "&", "*", "-", "+", "=", "/"]


class PartNumber:
    def __init__(self, cells: List[Cell]) -> None:
        self.cells = cells
        self.value = self.get_value_of_chain()

    def __repr__(self) -> str:
        return f"{self.cells[0]}"

    def __hash__(self) -> int:
        return hash((self.cells[0], self.value))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PartNumber):
            if self.cells[0] == other.cells[0]:
                return True
            else:
                return False
        else:
            return False

    def get_value_of_chain(self) -> int:
        digits = ''
        for cell in self.cells:
            digits += cell.content
        value = int(digits)
        return value


class Gear:
    def __init__(self, cell: Cell, part_numbers: List[PartNumber]) -> None:
        self.cell = cell
        self.part_numbers = part_numbers
        self.ratio = self.get_ratio()

    def __repr__(self) -> str:
        return f"{self.cell}: {self.ratio}"

    def __hash__(self) -> int:
        return hash((self.cell, self.ratio))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Gear):
            if self.cell == other.cell:
                return True
            else:
                return False
        else:
            return False

    def get_ratio(self) -> int:
        ratio = 1
        for part_number in self.part_numbers:
            ratio *= part_number.value
        return ratio


class Schematic:
    def __init__(self, rows: List[str]) -> None:
        self.grid = Grid(rows)
        self.special_characters = self.find_all_special_characters()
        self.part_numbers = self.find_all_part_numbers()
        self.gears = self.find_all_gears()

    def find_all_gears(self) -> List[Gear]:
        gears: List[Gear] = []
        for cell in self.special_characters:
            if cell.content == "*":
                adjacent_numerals = self.find_all_adjacent_numeral_cells(cell)
                if len(adjacent_numerals) >= 2:
                    adjacent_parts: List[PartNumber] = []
                    for adjacency in adjacent_numerals:
                        for part_number in self.part_numbers:
                            for part_cell in part_number.cells:
                                if adjacency == part_cell:
                                    adjacent_parts.append(part_number)
                    unique_parts = set(adjacent_parts)
                    listed_parts = list(unique_parts)
                    if len(listed_parts) == 2:
                        gear = Gear(cell, listed_parts)
                        gears.append(gear)
        return gears

    def find_all_special_characters(self) -> List[Cell]:
        special_characters: List[Cell] = []
        for cell in self.grid.cells.values():
            if cell.content in special_character_values:
                special_characters.append(cell)
        return special_characters

    def find_all_part_numbers(self) -> List[PartNumber]:
        part_numbers: List[PartNumber] = []
        for cell in self.find_all_numeral_cells_adjacent_to_special_character():
            part_number = self.find_part_number(cell)
            part_numbers.append(part_number)
        return list(set(part_numbers))

    def find_all_numeral_cells_adjacent_to_special_character(self) -> List[Cell]:
        adjacent_numerals: List[Cell] = []
        for cell in self.special_characters:
            adjacent_cells = self.find_all_adjacent_numeral_cells(cell)
            adjacent_numerals.extend(adjacent_cells)
        return list(set(adjacent_numerals))

    def find_all_adjacent_numeral_cells(self, core_cell: Cell) -> List[Cell]:
        adjacent_numerals: List[Cell] = []
        adjacent_cells = self.grid.get_adjacent_cells(core_cell)
        for adjacent_cell in adjacent_cells:
            if adjacent_cell.content.isdigit():
                adjacent_numerals.append(adjacent_cell)
        return list(set(adjacent_numerals))

    def find_part_number(self, core_cell: Cell) -> PartNumber:
        cells: List[Cell] = [core_cell]
        left_cell = self.grid.get_left_cell(core_cell)
        right_cell = self.grid.get_right_cell(core_cell)
        while left_cell is not None and left_cell.content.isdigit():
            cells.insert(0, left_cell)
            left_cell = self.grid.get_left_cell(left_cell)
        while right_cell is not None and right_cell.content.isdigit():
            cells.append(right_cell)
            right_cell = self.grid.get_right_cell(right_cell)
        part_number = PartNumber(cells)
        return part_number

    def calculate_part_numbers_sum(self) -> int:
        total = 0
        for part_number in self.part_numbers:
            total += part_number.value
        return total

    def calculate_gear_ratios_sum(self) -> int:
        total = 0
        for gear in self.gears:
            total += gear.ratio
        return total


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(3, is_official)
    rows = get_list_of_lines(data)
    schematic = Schematic(rows)
    part_1 = schematic.calculate_part_numbers_sum()
    part_2 = schematic.calculate_gear_ratios_sum()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(3, part_1, part_2, execution_time)
    return results
