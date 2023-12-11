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

    def has_identical_x(self, other: object) -> bool:
        if isinstance(other, Tile):
            return self.x == other.x
        else:
            return False

    def has_identical_y(self, other: object) -> bool:
        if isinstance(other, Tile):
            return self.y == other.y
        else:
            return False

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

    def find_all_tiles_not_in_loop(self) -> List[Tile]:
        tiles_not_in_loop: List[Tile] = []
        for tile in self.tiles.values():
            if not tile.included_in_loop:
                tiles_not_in_loop.append(tile)
        return tiles_not_in_loop

    def determine_all_adjacent_tile_names_and_bind(self, initial_tile: Tile) -> List[dict[str, str]]:
        bound_adjacent_tile_names: List[dict[str, str]] = []
        adjacent_names = initial_tile.determine_all_adjacent_tile_names()
        for name in adjacent_names.values():
            bound_adjacent_tile_names.append({
                "name": name,
                "initial_tile_name": initial_tile.name
            })
        return bound_adjacent_tile_names

    def calculate_inside_count_for_chunk(self, initial_tile: Tile) -> int:
        inside_count = 1
        initial_tile.checked_inside = True
        is_open = False
        tile_names_to_check = self.determine_all_adjacent_tile_names_and_bind(initial_tile)
        while len(tile_names_to_check):
            next_tile_names_to_check: List[dict[str, str]] = []
            for tile_name in tile_names_to_check:
                potential_tile = self.tiles.get(tile_name["name"])
                comparison_tile = self.tiles.get(tile_name["initial_tile_name"])
                if potential_tile and not potential_tile.included_in_loop and not potential_tile.checked_inside:
                    inside_count += 1
                    potential_tile.checked_inside = True
                    next_tile_names_to_check.extend(self.determine_all_adjacent_tile_names_and_bind(potential_tile))
                    if potential_tile.x == 0 or potential_tile.y == 0 or potential_tile.x == self.width - 1 or potential_tile.y == self.height - 1:
                        is_open = True
                    if comparison_tile and self.check_if_disconnection_error(potential_tile, comparison_tile):
                        is_open = True
            tile_names_to_check = next_tile_names_to_check
        return inside_count if not is_open else 0

    def calculate_total_inside_count(self) -> int:
        total_inside_count = 0
        tiles_not_in_loop = self.find_all_tiles_not_in_loop()
        while len(tiles_not_in_loop):
            tile = tiles_not_in_loop.pop(0)
            if not tile.checked_inside:
                chunk_count = self.calculate_inside_count_for_chunk(tile)
                total_inside_count += chunk_count
        return total_inside_count

    def check_if_disconnection_error(self, first_tile: Tile, second_tile: Tile) -> bool:
        disconnection_error = False
        first_tile_adjacencies = first_tile.determine_all_adjacent_tile_names()
        second_tile_adjacencies = second_tile.determine_all_adjacent_tile_names()
        if first_tile.x == second_tile.x:
            first_pair = [first_tile_adjacencies["east"], second_tile_adjacencies["east"], "east"]
            second_pair = [first_tile_adjacencies["west"], second_tile_adjacencies["west"], "west"]
        else:
            first_pair = [first_tile_adjacencies["north"], second_tile_adjacencies["north"], "north"]
            second_pair = [first_tile_adjacencies["south"], second_tile_adjacencies["south"], "south"]
        pairs = [first_pair, second_pair]
        for pair in pairs:
            first_tile_in_pair = self.tiles.get(pair[0])
            second_tile_in_pair = self.tiles.get(pair[1])
            if first_tile_in_pair and second_tile_in_pair and first_tile_in_pair.included_in_loop and second_tile_in_pair.included_in_loop and first_tile_in_pair.name not in second_tile_in_pair.connecting_tile_names:
                direction = pair[2]
                disconnection_error = not self.check_if_disconnected_tiles_eventually_block_off(first_tile_in_pair, second_tile_in_pair, direction)
        return disconnection_error

    def check_if_disconnected_tiles_eventually_block_off(self, first_tile: Tile, second_tile: Tile, direction: str) -> bool:
        blocked_off = False
        none_left_to_check = False
        first_checked_tile = first_tile
        second_checked_tile = second_tile
        while not blocked_off and not none_left_to_check:
            first_name_adjacency = first_checked_tile.determine_all_adjacent_tile_names()[direction]
            second_name_adjacency = second_checked_tile.determine_all_adjacent_tile_names()[direction]
            first_tile_adjacency = self.tiles.get(first_name_adjacency)
            second_tile_adjacency = self.tiles.get(second_name_adjacency)
            if not first_tile_adjacency or not second_tile_adjacency:
                none_left_to_check = True
            else:
                if not first_tile_adjacency.included_in_loop or not second_tile_adjacency.included_in_loop:
                    none_left_to_check = True
                else:
                    if first_tile_adjacency.name in second_tile_adjacency.connecting_tile_names:
                        blocked_off = True
                    else:
                        first_checked_tile = first_tile_adjacency
                        second_checked_tile = second_tile_adjacency
        return blocked_off

    def traverse_maze_for_inside_count(self) -> int:
        inside_count = 0
        for row in range(self.height):
            end_loop_tiles_row = self.find_end_loop_tiles_for_row(row)
            crossed_loop_count = 0
            for column in range(self.width):
                end_loop_tiles_column = self.find_end_loop_tiles_for_column(column)
                name = f"x{column}y{row}"
                tile = self.tiles.get(name)
                if tile:
                    if tile.included_in_loop:
                        if tile.content == "|" or tile.content == "J" or tile.content == "L":
                            crossed_loop_count += 1
                    else:
                        if crossed_loop_count % 2 == 1 and tile.x > end_loop_tiles_row[0].x and tile.x < end_loop_tiles_row[-1].x and tile.y > end_loop_tiles_column[0].y and tile.y < end_loop_tiles_column[-1].y:
                            inside_count += 1
        return inside_count

    def find_end_loop_tiles_for_row(self, row: int) -> List[Tile]:
        row_tiles = sorted((value for value in self.tiles.values() if value.y == row and value.included_in_loop), key=lambda x: x.x)
        if row_tiles:
            return [row_tiles[0], row_tiles[-1]]
        else:
            return []

    def find_end_loop_tiles_for_column(self, column: int) -> List[Tile]:
        column_tiles = sorted((value for value in self.tiles.values() if value.x == column and value.included_in_loop), key=lambda y: y.y)
        if column_tiles:
            return [column_tiles[0], column_tiles[-1]]
        else:
            return []


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
