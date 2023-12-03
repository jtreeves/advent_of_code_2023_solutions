from typing import List
from utils.Cell import Cell


class Grid:
    def __init__(self, rows: List[str]) -> None:
        self.rows = rows
        self.height = self.calculate_height()
        self.width = self.calculate_width()
        self.cells = self.create_cells()

    def calculate_height(self) -> int:
        return len(self.rows)

    def calculate_width(self) -> int:
        return len(self.rows[0])

    def create_cells(self) -> dict[str, Cell]:
        cells: dict[str, Cell] = {}
        for row in range(self.height):
            for column in range(self.width):
                character = self.rows[row][column]
                name = f"x{column}y{row}"
                new_cell = Cell(column, row, character)
                cells[name] = new_cell
        return cells

    def get_adjacent_cell_in_direction(self, single_cell: Cell, x_change: int, y_change: int) -> Cell | None:
        new_x = single_cell.x + x_change
        new_y = single_cell.y + y_change
        adjacent_cell = self.cells.get(f"x{new_x}y{new_y}")
        return adjacent_cell

    def get_left_cell(self, single_cell: Cell) -> Cell | None:
        left_cell = self.get_adjacent_cell_in_direction(single_cell, -1, 0)
        return left_cell

    def get_right_cell(self, single_cell: Cell) -> Cell | None:
        right_cell = self.get_adjacent_cell_in_direction(single_cell, 1, 0)
        return right_cell

    def get_top_cell(self, single_cell: Cell) -> Cell | None:
        top_cell = self.get_adjacent_cell_in_direction(single_cell, 0, -1)
        return top_cell

    def get_bottom_cell(self, single_cell: Cell) -> Cell | None:
        bottom_cell = self.get_adjacent_cell_in_direction(single_cell, 0, 1)
        return bottom_cell

    def get_tl_cell(self, single_cell: Cell) -> Cell | None:
        tl_cell = self.get_adjacent_cell_in_direction(single_cell, -1, -1)
        return tl_cell

    def get_tr_cell(self, single_cell: Cell) -> Cell | None:
        tr_cell = self.get_adjacent_cell_in_direction(single_cell, 1, -1)
        return tr_cell

    def get_bl_cell(self, single_cell: Cell) -> Cell | None:
        bl_cell = self.get_adjacent_cell_in_direction(single_cell, -1, 1)
        return bl_cell

    def get_br_cell(self, single_cell: Cell) -> Cell | None:
        br_cell = self.get_adjacent_cell_in_direction(single_cell, 1, 1)
        return br_cell

    def get_adjacent_cells(self, single_cell: Cell) -> List[Cell]:
        cells: List[Cell] = []
        top_cell = self.get_top_cell(single_cell)
        bottom_cell = self.get_bottom_cell(single_cell)
        left_cell = self.get_left_cell(single_cell)
        right_cell = self.get_right_cell(single_cell)
        tl_cell = self.get_tl_cell(single_cell)
        tr_cell = self.get_tr_cell(single_cell)
        bl_cell = self.get_bl_cell(single_cell)
        br_cell = self.get_br_cell(single_cell)
        if top_cell is not None:
            cells.append(top_cell)
        if bottom_cell is not None:
            cells.append(bottom_cell)
        if left_cell is not None:
            cells.append(left_cell)
        if right_cell is not None:
            cells.append(right_cell)
        if tl_cell is not None:
            cells.append(tl_cell)
        if tr_cell is not None:
            cells.append(tr_cell)
        if bl_cell is not None:
            cells.append(bl_cell)
        if br_cell is not None:
            cells.append(br_cell)
        return cells
