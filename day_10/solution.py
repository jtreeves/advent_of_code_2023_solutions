import time
from typing import List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Tile:
    def __init__(self, x: int, y: int, content: str) -> None:
        self.x = x
        self.y = y
        self.content = content
        self.name = f"x{self.x}y{self.y}"
        self.included_in_loop = False
        self.distance_from_start = 0
        self.connecting_tiles = self.determine_connecting_tiles()

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}): {self.content}"

    def determine_adjacent_tile_in_direction(self, x_change: int, y_change: int) -> str:
        new_x = self.x + x_change
        new_y = self.y + y_change
        adjacent_tile = f"x{new_x}y{new_y}"
        return adjacent_tile

    def determine_connecting_tiles(self) -> List[str]:
        north = self.determine_adjacent_tile_in_direction(0, -1)
        south = self.determine_adjacent_tile_in_direction(0, 1)
        east = self.determine_adjacent_tile_in_direction(1, 0)
        west = self.determine_adjacent_tile_in_direction(-1, 0)
        if self.content == "|":
            connecting_tiles = [north, south]
        elif self.content == "-":
            connecting_tiles = [east, west]
        elif self.content == "L":
            connecting_tiles = [north, east]
        elif self.content == "J":
            connecting_tiles = [north, west]
        elif self.content == "7":
            connecting_tiles = [south, west]
        elif self.content == "F":
            connecting_tiles = [south, east]
        else:
            connecting_tiles = []
        return connecting_tiles


class Grid:
    def __init__(self, rows: List[str]) -> None:
        self.rows = rows
        self.height = self.calculate_height()
        self.width = self.calculate_width()
        self.tiles = self.create_tiles()

    def calculate_height(self) -> int:
        return len(self.rows)

    def calculate_width(self) -> int:
        return len(self.rows[0])

    def create_tiles(self) -> dict[str, Tile]:
        tiles: dict[str, Tile] = {}
        for row in range(self.height):
            for column in range(self.width):
                character = self.rows[row][column]
                name = f"x{column}y{row}"
                new_tile = Tile(column, row, character)
                tiles[name] = new_tile
                if character == "S":
                    self.start_tile = new_tile
                    self.start_tile.included_in_loop = True
        return tiles

    def find_tiles_connected_to_start(self) -> List[Tile]:
        connected_tiles: List[Tile] = []
        north_name = self.start_tile.determine_adjacent_tile_in_direction(0, -1)
        south_name = self.start_tile.determine_adjacent_tile_in_direction(0, 1)
        east_name = self.start_tile.determine_adjacent_tile_in_direction(1, 0)
        west_name = self.start_tile.determine_adjacent_tile_in_direction(-1, 0)
        initial_names = [north_name, south_name, east_name, west_name]
        for name in initial_names:
            potential_tile = self.tiles.get(name)
            if potential_tile and self.start_tile.name in potential_tile.connecting_tiles:
                connected_tiles.append(potential_tile)
        return connected_tiles

    def traverse_loop(self) -> int:
        layer = 0
        tiles_at_layer = self.find_tiles_connected_to_start()
        while len(tiles_at_layer):
            layer += 1
            next_layer: List[Tile] = []
            for tile in tiles_at_layer:
                tile.distance_from_start = layer
                tile.included_in_loop = True
                connected_names = tile.connecting_tiles
                for name in connected_names:
                    potential_tile = self.tiles.get(name)
                    if potential_tile and not potential_tile.included_in_loop:
                        next_layer.append(potential_tile)
            tiles_at_layer = next_layer
        return layer


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(10, is_official)
    lines = get_list_of_lines(data)
    grid = Grid(lines)
    part_1 = grid.traverse_loop()
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(10, part_1, part_2, execution_time)
    return results
