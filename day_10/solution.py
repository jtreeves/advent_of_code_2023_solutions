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
        self.checked_inside = False
        self.distance_from_start = 0
        self.connecting_tile_names = self.determine_connecting_tile_names()

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}): {self.content}"

    def determine_adjacent_tile_name_in_direction(self, x_change: int, y_change: int) -> str:
        new_x = self.x + x_change
        new_y = self.y + y_change
        adjacent_tile = f"x{new_x}y{new_y}"
        return adjacent_tile

    def determine_all_adjacent_tile_names(self) -> dict[str, str]:
        north = self.determine_adjacent_tile_name_in_direction(0, -1)
        south = self.determine_adjacent_tile_name_in_direction(0, 1)
        east = self.determine_adjacent_tile_name_in_direction(1, 0)
        west = self.determine_adjacent_tile_name_in_direction(-1, 0)
        adjacent_tile_names = {
            "north": north,
            "south": south,
            "east": east,
            "west": west
        }
        return adjacent_tile_names

    def determine_connecting_tile_names(self) -> List[str]:
        adjacent_tile_names = self.determine_all_adjacent_tile_names()
        north = adjacent_tile_names["north"]
        south = adjacent_tile_names["south"]
        east = adjacent_tile_names["east"]
        west = adjacent_tile_names["west"]
        if self.content == "|":
            connecting_tile_names = [north, south]
        elif self.content == "-":
            connecting_tile_names = [east, west]
        elif self.content == "L":
            connecting_tile_names = [north, east]
        elif self.content == "J":
            connecting_tile_names = [north, west]
        elif self.content == "7":
            connecting_tile_names = [south, west]
        elif self.content == "F":
            connecting_tile_names = [south, east]
        else:
            connecting_tile_names = []
        return connecting_tile_names


class Maze:
    def __init__(self, description: str) -> None:
        self.rows = get_list_of_lines(description)
        self.height = self.calculate_height()
        self.width = self.calculate_width()
        self.tiles = self.create_tiles()
        self.maximum_distance_from_start = self.traverse_loop()
        self.total_inside_count = self.traverse_maze_for_inside_count()

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
        adjacent_names = self.start_tile.determine_all_adjacent_tile_names()
        directional_keys: List[str] = []
        for [k, v] in adjacent_names.items():
            potential_tile = self.tiles.get(v)
            if potential_tile and self.start_tile.name in potential_tile.connecting_tile_names:
                connected_tiles.append(potential_tile)
                directional_keys.append(k)
        if "north" in directional_keys and "south" in directional_keys:
            self.start_tile.content = "|"
        elif "east" in directional_keys and "west" in directional_keys:
            self.start_tile.content = "-"
        elif "north" in directional_keys and "east" in directional_keys:
            self.start_tile.content = "L"
        elif "north" in directional_keys and "west" in directional_keys:
            self.start_tile.content = "J"
        elif "south" in directional_keys and "west" in directional_keys:
            self.start_tile.content = "7"
        elif "south" in directional_keys and "east" in directional_keys:
            self.start_tile.content = "F"
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
                connected_names = tile.connecting_tile_names
                for name in connected_names:
                    potential_tile = self.tiles.get(name)
                    if potential_tile and not potential_tile.included_in_loop:
                        next_layer.append(potential_tile)
            tiles_at_layer = next_layer
        return layer

    def traverse_maze_for_inside_count(self) -> int:
        inside_count = 0
        for row in range(self.height):
            crossed_loop_count = 0
            for column in range(self.width):
                name = f"x{column}y{row}"
                tile = self.tiles.get(name)
                if tile:
                    if tile.included_in_loop:
                        if tile.content == "|" or tile.content == "J" or tile.content == "L":
                            crossed_loop_count += 1
                    else:
                        if crossed_loop_count % 2 == 1:
                            inside_count += 1
        return inside_count


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(10, is_official)
    maze = Maze(data)
    part_1 = maze.maximum_distance_from_start
    part_2 = maze.total_inside_count
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(10, part_1, part_2, execution_time)
    return results
