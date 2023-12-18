import time
from typing import List
from copy import deepcopy
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Block:
    def __init__(self, x: int, y: int, heat_loss: int) -> None:
        self.x = x
        self.y = y
        self.heat_loss = heat_loss
        self.name = f"x{x}y{y}"


class Path:
    def __init__(self, direction: str, current_steps_in_direction: int, heat_loss: int, latest_total_step: int, highest_x: int, highest_y: int, end: Block, tracked_blocks: dict[str, dict[str, int]]) -> None:
        self.direction = direction
        self.current_steps_in_direction = current_steps_in_direction
        self.heat_loss = heat_loss
        self.latest_total_step = latest_total_step
        self.highest_x = highest_x
        self.highest_y = highest_y
        self.end = end
        self.tracked_blocks = tracked_blocks

    def __repr__(self) -> str:
        representation = f"TOTAL HEAT LOSS: {self.heat_loss}\n"
        extracted_tracking: List[dict[str, int | str]] = []
        for [name, value] in self.tracked_blocks.items():
            for [direction, step] in value.items():
                if step != 0:
                    extracted_tracking.append({
                        "step": step,
                        "name": name,
                        "direction": direction
                    })
        for info in sorted(extracted_tracking, key=lambda x: int(x["step"])):
            representation += f"{info['step']}.\t{info['name']}:\t{info['direction']}\n"
        return representation


class City:
    def __init__(self, description: str) -> None:
        self.rows = get_list_of_lines(description)
        self.height = self.calculate_height()
        self.width = self.calculate_width()
        self.blocks = self.create_blocks()
        self.start = self.blocks["x0y0"]
        self.end = self.blocks[f"x{self.width - 1}y{self.height - 1}"]

    def calculate_height(self) -> int:
        return len(self.rows)

    def calculate_width(self) -> int:
        return len(self.rows[0])

    def create_blocks(self) -> dict[str, Block]:
        blocks: dict[str, Block] = {}
        for row in range(self.height):
            for column in range(self.width):
                heat_loss = int(self.rows[row][column])
                name = f"x{column}y{row}"
                new_block = Block(column, row, heat_loss)
                blocks[name] = new_block
        return blocks

    def create_tracked_blocks(self) -> dict[str, dict[str, int]]:
        blocks: dict[str, dict[str, int]] = {}
        for row in range(self.height):
            for column in range(self.width):
                name = f"x{column}y{row}"
                tracked_directions = {
                    ">": 0,
                    "<": 0,
                    "^": 0,
                    "v": 0
                }
                blocks[name] = tracked_directions
        return blocks

    def minimize_heat_loss(self) -> int:
        total_heat_loss = 0
        paths: List[Path] = [Path("", 0, 0, 0, 0, 0, self.start, self.create_tracked_blocks())]
        while len(paths) != 0:
            path = paths.pop()
            if path.end == self.end:
                total_heat_loss = path.heat_loss
                print(path)
            else:
                print('*** MINIMAL HEAT LOSS SO FAR:', total_heat_loss)
                print('PATHS STILL IN QUEUE:', len(paths))
                max_in_direction = 3
                current_steps_in_direction = path.current_steps_in_direction
                first_heat_loss = path.heat_loss
                second_heat_loss = path.heat_loss
                straight_heat_loss = path.heat_loss
                first_step = path.latest_total_step
                second_step = path.latest_total_step
                straight_step = path.latest_total_step
                first_end_block = deepcopy(path.end)
                second_end_block = deepcopy(path.end)
                straight_end_block = deepcopy(path.end)
                first_tracked_blocks = deepcopy(path.tracked_blocks)
                second_tracked_blocks = deepcopy(path.tracked_blocks)
                straight_tracked_blocks = deepcopy(path.tracked_blocks)
                if path.direction == ">" or path.direction == "<":
                    first_direction = "^"
                    second_direction = "v"
                    first_x_increment = 0
                    first_y_increment = -1
                    second_x_increment = 0
                    second_y_increment = 1
                    if path.direction == ">":
                        straight_x_increment = 1
                        straight_y_increment = 0
                    else:
                        straight_x_increment = -1
                        straight_y_increment = 0
                elif path.direction == "^" or path.direction == "v":
                    first_direction = ">"
                    second_direction = "<"
                    first_x_increment = 1
                    first_y_increment = 0
                    second_x_increment = -1
                    second_y_increment = 0
                    if path.direction == "v":
                        straight_x_increment = 0
                        straight_y_increment = 1
                    else:
                        straight_x_increment = 0
                        straight_y_increment = -1
                else:
                    first_direction = ">"
                    second_direction = "v"
                    first_x_increment = 1
                    first_y_increment = 0
                    second_x_increment = 0
                    second_y_increment = 1
                    straight_x_increment = 0
                    straight_y_increment = 0
                first_x = path.end.x + first_x_increment
                first_y = path.end.y + first_y_increment
                second_x = path.end.x + second_x_increment
                second_y = path.end.y + second_y_increment
                straight_x = path.end.x + straight_x_increment
                straight_y = path.end.y + straight_y_increment
                first_name = f"x{first_x}y{first_y}"
                second_name = f"x{second_x}y{second_y}"
                straight_name = f"x{straight_x}y{straight_y}"
                first_block = self.blocks.get(first_name)
                second_block = self.blocks.get(second_name)
                straight_block = self.blocks.get(straight_name)
                if first_block and first_tracked_blocks[first_block.name][first_direction] == 0 and first_block.x >= path.highest_x - 1 and first_block.y >= path.highest_y - 1:
                    first_heat_loss += first_block.heat_loss
                    first_end_block = first_block
                    first_tracked_blocks[first_block.name][first_direction] = first_step + 1
                    if first_end_block.name != path.end.name and (total_heat_loss == 0 or (total_heat_loss != 0 and first_heat_loss + self.end.x - first_end_block.x + self.end.y - first_end_block.y < total_heat_loss)):
                        print('NEW BLOCK:', first_end_block.name)
                        print('NEW HEAT LOSS:', first_heat_loss)
                        paths.append(Path(first_direction, 0, first_heat_loss, first_step + 1, first_block.x if first_block.x > path.highest_x else path.highest_x, first_block.y if first_block.y > path.highest_y else path.highest_y, first_end_block, first_tracked_blocks))
                if second_block and second_tracked_blocks[second_block.name][second_direction] == 0 and second_block.x >= path.highest_x - 1 and second_block.y >= path.highest_y - 1:
                    second_heat_loss += second_block.heat_loss
                    second_end_block = second_block
                    second_tracked_blocks[second_block.name][second_direction] = second_step + 1
                    if second_end_block.name != path.end.name and (total_heat_loss == 0 or (total_heat_loss != 0 and second_heat_loss + self.end.x - second_end_block.x + self.end.y - second_end_block.y < total_heat_loss)):
                        print('NEW BLOCK:', second_end_block.name)
                        print('NEW HEAT LOSS:', second_heat_loss)
                        paths.append(Path(second_direction, 0, second_heat_loss, second_step + 1, second_block.x if second_block.x > path.highest_x else path.highest_x, second_block.y if second_block.y > path.highest_y else path.highest_y, second_end_block, second_tracked_blocks))
                if straight_block and path.direction and straight_tracked_blocks[straight_block.name][path.direction] == 0 and current_steps_in_direction + 1 < max_in_direction and straight_block.x >= path.highest_x - 1 and straight_block.y >= path.highest_y - 1:
                    straight_heat_loss += straight_block.heat_loss
                    straight_end_block = straight_block
                    straight_tracked_blocks[straight_block.name][path.direction] = straight_step + 1
                    if straight_end_block.name != path.end.name and (total_heat_loss == 0 or (total_heat_loss != 0 and straight_heat_loss + self.end.x - straight_end_block.x + self.end.y - straight_end_block.y < total_heat_loss)):
                        print('NEW BLOCK:', straight_end_block.name)
                        print('NEW HEAT LOSS:', straight_heat_loss)
                        paths.append(Path(path.direction, current_steps_in_direction + 1, straight_heat_loss, straight_step + 1, straight_block.x if straight_block.x > path.highest_x else path.highest_x, straight_block.y if straight_block.y > path.highest_y else path.highest_y, straight_end_block, straight_tracked_blocks))
        return total_heat_loss


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(17, is_official)
    city = City(data)
    part_1 = city.minimize_heat_loss()
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(17, part_1, part_2, execution_time)
    return results

# DFS with minimal guardrails: just under 10 hours to execute on practice data (4 hours to find, 6 to verify)
# DFS with more guardrails, including eliminating paths with heat losses currently below the minimum but far enough away from the end that they would be above the minimum once they reached there: just under 4 hours to execute on practice data (2 hours to find, 2 to verify)
