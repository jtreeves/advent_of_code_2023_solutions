import time
from typing import List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Beam:
    def __init__(self, start_x: int, start_y: int, start_horizontally: bool = True, start_increasing: bool = True) -> None:
        self.x = start_x
        self.y = start_y
        self.moving_horizontally = start_horizontally
        self.increment = 1 if start_increasing else -1
        self.active = True


class Tile:
    def __init__(self, x: int, y: int, content: str) -> None:
        self.x = x
        self.y = y
        self.content = content
        self.energized = False
        self.beams_tracker = {
            ">": 0,
            "<": 0,
            "^": 0,
            "v": 0
        }


class Contraption:
    def __init__(self, description: str) -> None:
        self.rows = get_list_of_lines(description)
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
        return tiles

    def fire_beam(self, x: int, y: int, horizontal: bool, increasing: bool) -> None:
        beam = Beam(x, y, horizontal, increasing)
        while beam.active:
            current_name = f"x{beam.x}y{beam.y}"
            current_tile = self.tiles.get(current_name)
            if current_tile:
                if beam.moving_horizontally and beam.increment == 1:
                    current_direction = ">"
                elif beam.moving_horizontally and beam.increment == -1:
                    current_direction = "<"
                elif not beam.moving_horizontally and beam.increment == -1:
                    current_direction = "^"
                else:
                    current_direction = "v"
                if current_tile.beams_tracker[current_direction] == 0:
                    current_tile.beams_tracker[current_direction] = 1
                    current_tile.energized = True
                    if current_tile.content == "." or (current_tile.content == "|" and not beam.moving_horizontally) or (current_tile.content == "-" and beam.moving_horizontally):
                        pass
                    elif current_tile.content == "|":
                        self.fire_beam(beam.x, beam.y + 1, False, True)
                        self.fire_beam(beam.x, beam.y - 1, False, False)
                        beam.active = False
                    elif current_tile.content == "-":
                        self.fire_beam(beam.x + 1, beam.y, True, True)
                        self.fire_beam(beam.x - 1, beam.y, True, False)
                        beam.active = False
                    else:
                        beam.moving_horizontally = not beam.moving_horizontally
                        if current_tile.content == "/":
                            beam.increment *= -1
                    beam.x = beam.x if not beam.moving_horizontally else beam.x + beam.increment
                    beam.y = beam.y if beam.moving_horizontally else beam.y + beam.increment
                else:
                    beam.active = False
            else:
                beam.active = False

    def count_energized_tiles_for_configuration(self, x: int, y: int, horizontal: bool, increasing: bool) -> int:
        self.fire_beam(x, y, horizontal, increasing)
        count = 0
        for tile in self.tiles.values():
            if tile.energized:
                count += 1
        self.reset_energized_values()
        return count

    def reset_energized_values(self) -> None:
        for tile in self.tiles.values():
            tile.energized = False
            tile.beams_tracker = {
                ">": 0,
                "<": 0,
                "^": 0,
                "v": 0
            }

    def maximize_energized_tiles(self) -> int:
        configuration_counts: List[int] = []
        for column in range(self.width):
            configuration_counts.append(self.count_energized_tiles_for_configuration(column, 0, False, True))
            configuration_counts.append(self.count_energized_tiles_for_configuration(column, self.height - 1, False, False))
        for row in range(self.height):
            configuration_counts.append(self.count_energized_tiles_for_configuration(0, row, True, True))
            configuration_counts.append(self.count_energized_tiles_for_configuration(self.width - 1, row, True, False))
        return sorted(configuration_counts)[-1]


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(16, is_official)
    grid = Contraption(data)
    part_1 = grid.count_energized_tiles_for_configuration(0, 0, True, True)
    part_2 = grid.maximize_energized_tiles()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(16, part_1, part_2, execution_time)
    return results
