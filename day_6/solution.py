import math
import time
from typing import List
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Race:
    def __init__(self, time: int, distance: int) -> None:
        self.time = time
        self.distance = distance

    def calculate_min_and_max_holds(self) -> List[int]:
        discriminant = self.time**2 - 4 * self.distance
        upper = (self.time + discriminant**(1 / 2)) / 2
        lower = (self.time - discriminant**(1 / 2)) / 2
        if upper == int(upper):
            upper -= 1
        if lower == int(lower):
            lower += 1
        holds = [math.ceil(lower), math.floor(upper)]
        return holds

    def calculate_total_scenarios(self) -> int:
        holds = self.calculate_min_and_max_holds()
        total_scenarios = len(range(holds[0], holds[1] + 1))
        return total_scenarios


class Summary:
    def __init__(self, description: str) -> None:
        self.races = self.determine_race_conditions(description)

    def determine_race_conditions(self, description: str) -> List[Race]:
        sections = description.split("\n")
        times = list(filter(None, sections[0].split(":")[1].split(" ")))
        distances = list(filter(None, sections[1].split(":")[1].split(" ")))
        race_conditions: List[Race] = []
        for i in range(len(times)):
            race_conditions.append(Race(int(times[i]), int(distances[i])))
        return race_conditions

    def calculate_margin_of_error(self) -> int:
        margin = 1
        for race in self.races:
            margin *= race.calculate_total_scenarios()
        return margin


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(6, is_official)
    summary = Summary(data)
    part_1 = summary.calculate_margin_of_error()
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(6, part_1, part_2, execution_time)
    return results
