import time
from typing import Tuple, Set, List
from queue import Queue
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Brick:
    def __init__(self, name: str, snapshot: str) -> None:
        ends = snapshot.split("~")
        self.name = name
        self.start = self.create_coordinates(ends[0])
        self.end = self.create_coordinates(ends[1])
        self.orientation = self.determine_orientation()
        self.length = self.determine_length()
        self.beneath_bricks: Set[str] = set()
        self.above_bricks: Set[str] = set()

    def __repr__(self) -> str:
        return f"{self.name}: {self.start} -> {self.length}"

    def create_coordinates(self, description: str) -> Tuple[int, ...]:
        parts = description.split(",")
        coordinates = tuple([int(part) for part in parts])
        return coordinates

    def determine_orientation(self) -> int:
        orientation = 0
        for index in range(len(self.start)):
            if self.end[index] > self.start[index]:
                orientation = index
        return orientation

    def determine_length(self) -> int:
        length = self.end[self.orientation] - self.start[self.orientation]
        return length + 1

    def create_all_cubes(self) -> List[Tuple[int, int, int, str]]:
        cubes: List[Tuple[int, int, int, str]] = []
        orientation = self.orientation
        length = self.length
        for index in range(length):
            if orientation == 0:
                cubes.append((self.start[0] + index, self.start[1], self.start[2], self.name))
            if orientation == 1:
                cubes.append((self.start[0], self.start[1] + index, self.start[2], self.name))
            if orientation == 2:
                cubes.append((self.start[0], self.start[1], self.start[2] + index, self.name))
        return cubes


class Stack:
    def __init__(self, description: str) -> None:
        snapshots = get_list_of_lines(description)
        self.bricks = self.create_bricks(snapshots)
        self.bricks_queue = self.create_bricks_queue()
        self.dimensions = self.determine_base_dimensions()
        self.base = self.create_base()

    def create_bricks(self, snapshots: List[str]) -> dict[str, Brick]:
        bricks: dict[str, Brick] = {}
        for index in range(len(snapshots)):
            snapshot = snapshots[index]
            name = f"B{index}"
            brick = Brick(name, snapshot)
            bricks[name] = brick
        return bricks

    def create_bricks_queue(self) -> Queue[List[Tuple[int, int, int, str]]]:
        bricks_to_drop: List[List[Tuple[int, int, int, str]]] = []
        for brick in self.bricks.values():
            cubes = brick.create_all_cubes()
            bricks_to_drop.append(cubes)
        sorted_bricks = sorted(bricks_to_drop, key=lambda x: x[0][2])
        bricks_queue: Queue[List[Tuple[int, int, int, str]]] = Queue()
        for brick in sorted_bricks:
            bricks_queue.put(brick)
        return bricks_queue

    def determine_base_dimensions(self) -> Tuple[int, ...]:
        x_max = 0
        y_max = 0
        for brick in self.bricks.values():
            x, y, _ = brick.start
            orientation = brick.orientation
            length = brick.length
            if orientation == 0:
                x += length
            if orientation == 1:
                y += length
            if x > x_max:
                x_max = x
            if y > y_max:
                y_max = y
        return x_max + 1, y_max + 1

    def create_base(self) -> dict[Tuple[int, ...], str]:
        points: dict[Tuple[int, ...], str] = {}
        x_max, y_max = self.dimensions
        for x in range(x_max):
            for y in range(y_max):
                points[(x, y, 0)] = ""
        return points

    def move_bricks_down_once(self) -> None:
        updated_queue: Queue[List[Tuple[int, int, int, str]]] = Queue()
        while not self.bricks_queue.empty():
            brick = self.bricks_queue.get()
            can_move_down = self.check_if_brick_can_move_down(brick)
            if can_move_down:
                new_brick: List[Tuple[int, int, int, str]] = []
                for cube in brick:
                    x0, y0, z0, name = cube
                    x1, y1, z1 = x0, y0, z0 - 1
                    new_brick.append((x1, y1, z1, name))
                updated_queue.put(new_brick)
            else:
                full_brick = self.bricks[brick[0][3]]
                for cube in brick:
                    x, y, z, name = cube
                    self.base[(x, y, z)] = name
                    potential_below = self.base.get((x, y, z - 1))
                    if potential_below:
                        if full_brick.name != potential_below:
                            full_brick.above_bricks.add(potential_below)
                        full_below_brick = self.bricks[potential_below]
                        if full_below_brick.name != full_brick.name:
                            full_below_brick.beneath_bricks.add(full_brick.name)
        self.bricks_queue = updated_queue

    def move_all_bricks_down_to_ground(self) -> None:
        while not self.bricks_queue.empty():
            self.move_bricks_down_once()

    def check_if_brick_can_move_down(self, brick: List[Tuple[int, int, int, str]]) -> bool:
        can_move_down = True
        for cube in brick:
            if not self.check_if_cube_can_move_down(cube):
                can_move_down = False
        return can_move_down

    def check_if_cube_can_move_down(self, cube: Tuple[int, int, int, str]) -> bool:
        can_move_down = True
        x0, y0, z0, _ = cube
        x1, y1, z1 = x0, y0, z0 - 1
        if z1 == 0:
            can_move_down = False
        else:
            if self.base.get((x1, y1, z1)):
                can_move_down = False
        return can_move_down

    def check_if_brick_can_be_removed(self, brick: Brick) -> bool:
        can_be_removed = False
        brick_count_above = len(brick.beneath_bricks)
        if brick_count_above == 0:
            can_be_removed = True
        else:
            above_bricks_covered_elsewhere = 0
            for above_brick in brick.beneath_bricks:
                full_brick = self.bricks[above_brick]
                if len(full_brick.above_bricks) >= 2:
                    above_bricks_covered_elsewhere += 1
            if above_bricks_covered_elsewhere == brick_count_above:
                can_be_removed = True
        return can_be_removed

    def find_bricks_could_remove(self) -> Set[str]:
        self.move_all_bricks_down_to_ground()
        removable_bricks: Set[str] = set()
        for brick in self.bricks.values():
            can_be_removed = self.check_if_brick_can_be_removed(brick)
            if can_be_removed:
                removable_bricks.add(brick.name)
        return removable_bricks

    def find_bricks_cannot_remove(self) -> Set[str]:
        total_bricks = set(self.bricks.keys())
        removable_bricks = self.find_bricks_could_remove()
        non_removable_bricks: Set[str] = total_bricks - removable_bricks
        return non_removable_bricks

    def count_total_bricks_could_remove(self) -> int:
        removable_bricks = self.find_bricks_could_remove()
        return len(removable_bricks)

    def find_bricks_destroyed_in_chain_reaction(self, brick_name: str) -> Set[str]:
        affected_bricks: Set[str] = set()
        bricks_to_search: List[str] = [brick_name]
        while len(bricks_to_search):
            current_name = bricks_to_search.pop()
            current_brick = self.bricks[current_name]
            bricks_above = current_brick.beneath_bricks
            affected_bricks |= bricks_above
            bricks_to_search += bricks_above
        return affected_bricks

    def count_all_bricks_destroyed_in_chain_reaction(self) -> int:
        total = 0
        non_removable_bricks = self.find_bricks_cannot_remove()
        for brick in non_removable_bricks:
            bricks_destroyed = self.find_bricks_destroyed_in_chain_reaction(brick)
            total += len(bricks_destroyed)
        return total


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(22, is_official)
    stack = Stack(data)
    part_1 = stack.count_total_bricks_could_remove()
    part_2 = stack.count_all_bricks_destroyed_in_chain_reaction()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(22, part_1, part_2, execution_time)
    return results
