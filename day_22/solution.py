import time
from typing import Tuple, List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Brick:
    def __init__(self, snapshot: str) -> None:
        ends = snapshot.split("~")
        self.start = self.create_coordinates(ends[0])
        self.end = self.create_coordinates(ends[1])
        self.orientation = self.determine_orientation()
        self.length = self.determine_length()

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
        return length

    def get_all_cubes(self) -> List[Tuple[int, ...]]:
        cubes: List[Tuple[int, ...]] = []
        orientation = self.orientation
        length = self.length
        for index in range(length):
            if orientation == 0:
                cubes.append((self.start[0] + index, self.start[1], self.start[2]))
            if orientation == 1:
                cubes.append((self.start[0], self.start[1] + index, self.start[2]))
            if orientation == 2:
                cubes.append((self.start[0], self.start[1], self.start[2] + index))
        return cubes


class Stack:
    def __init__(self, description: str) -> None:
        snapshots = get_list_of_lines(description)
        self.bricks = self.create_bricks(snapshots)
        self.dimensions = self.determine_dimensions()
        self.points = self.create_points()
        self.time = 0

    def create_bricks(self, snapshots: List[str]) -> List[Brick]:
        initial_bricks: List[Brick] = []
        for snapshot in snapshots:
            brick = Brick(snapshot)
            initial_bricks.append(brick)
        sorted_bricks = sorted(initial_bricks, key=lambda x: x.start[2])
        return sorted_bricks

    def determine_dimensions(self) -> Tuple[int, ...]:
        x_max = 0
        y_max = 0
        z_max = 0
        for brick in self.bricks:
            x, y, z = brick.start
            orientation = brick.orientation
            length = brick.length
            if orientation == 0:
                x += length
            if orientation == 1:
                y += length
            if orientation == 2:
                z += length
            if x > x_max:
                x_max = x
            if y > y_max:
                y_max = y
            if z > z_max:
                z_max = z
        return x_max + 1, y_max + 1, z_max + 1

    def create_points(self) -> dict[Tuple[int, ...], bool]:
        points: dict[Tuple[int, ...], bool] = {}
        x_max, y_max, z_max = self.dimensions
        for x in range(x_max):
            for y in range(y_max):
                for z in range(z_max):
                    points[x, y, z] = False
        for brick in self.bricks:
            cubes = brick.get_all_cubes()
            for cube in cubes:
                points[cube] = True
        return points

    def move_bricks_down_once(self) -> int:
        total_bricks_moved = 0
        for brick in self.bricks:
            can_move_down = self.check_if_brick_can_move_down(brick)
            if can_move_down:
                total_bricks_moved += 1
                cubes = brick.get_all_cubes()
                for cube in cubes:
                    self.points[cube] = False
                for cube in cubes:
                    self.points[cube[0], cube[1], cube[2] - (1 + self.time)] = True
        return total_bricks_moved

    def move_all_bricks_down_to_ground(self) -> None:
        can_any_bricks_move = True
        while can_any_bricks_move:
            self.time += 1
            total_bricks_moved = self.move_bricks_down_once()
            can_any_bricks_move = True if total_bricks_moved != 0 else False

    def check_if_brick_can_move_down(self, brick: Brick) -> bool:
        can_move_down = True
        if brick.orientation == 2:
            x, y, z = brick.start
            if z - (1 + self.time) == 1:
                can_move_down = False
            else:
                can_move_down = not self.points[x, y, z - (1 + self.time)]
        else:
            cubes = brick.get_all_cubes()
            for cube in cubes:
                x, y, z = cube
                if z - (1 + self.time) == 1 or self.points[x, y, z - (1 + self.time)]:
                    can_move_down = False
        return can_move_down


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(22, is_official)
    stack = Stack(data)
    print(stack.points)
    print(stack.dimensions)
    print(len(stack.points.keys()))
    stack.move_all_bricks_down_to_ground()
    print(stack.points)
    part_1 = 1 if data else 0
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(22, part_1, part_2, execution_time)
    return results
