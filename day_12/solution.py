import time
from typing import List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class PotentialScenario:
    def __init__(self, start: str, unknown_damaged: int = 0, unknown_operational: int = 0) -> None:
        self.scenario = start
        self.unknown_damaged = unknown_damaged
        self.unknown_operational = unknown_operational


class ConditionsRecord:
    def __init__(self, record_description: str) -> None:
        versions = record_description.split(" ")
        self.original_conditions = versions[0]
        self.contiguous_groups = self.determine_contiguous_groups(versions[1])
        self.length = len(self.original_conditions)
        self.total_damaged = self.determine_total_damaged()
        self.total_operational = self.length - self.total_damaged
        self.unknown_damaged = self.total_damaged - self.original_conditions.count("#")
        self.unknown_operational = self.total_operational - self.original_conditions.count(".")

    def determine_contiguous_groups(self, notes: str) -> List[int]:
        groups = notes.split(",")
        contiguous_groups: List[int] = []
        for group in groups:
            contiguous_groups.append(int(group))
        return contiguous_groups

    def determine_total_damaged(self) -> int:
        damaged = 0
        for group in self.contiguous_groups:
            damaged += group
        return damaged

    def count_acceptable_arrangements(self) -> int:
        acceptable_arrangements = 0
        possible_scenarios: List[PotentialScenario] = [PotentialScenario("")]
        while len(possible_scenarios) != 0:
            possibility = possible_scenarios.pop()
            current_index = len(possibility.scenario)
            next_unknown_index = self.find_next_unknown_condition(current_index)
            if next_unknown_index != -1:
                set_subsection = possibility.scenario + self.original_conditions[current_index:next_unknown_index]
                damaged_possibility = PotentialScenario(set_subsection + "#", possibility.unknown_damaged + 1, possibility.unknown_operational)
                operational_possibility = PotentialScenario(set_subsection + ".", possibility.unknown_damaged, possibility.unknown_operational + 1)
                new_possibilities = [damaged_possibility, operational_possibility]
                for new_possibility in new_possibilities:
                    if new_possibility.unknown_damaged <= self.unknown_damaged and new_possibility.unknown_operational <= self.unknown_operational and not self.check_if_scenario_violates_pattern(new_possibility.scenario):
                        possible_scenarios.append(new_possibility)
            else:
                full_scenario = possibility.scenario + self.original_conditions[current_index:]
                if not self.check_if_scenario_violates_pattern(full_scenario):
                    acceptable_arrangements += 1
        return acceptable_arrangements

    def find_next_unknown_condition(self, start_index: int) -> int:
        next_index = self.original_conditions.find("?", start_index)
        return next_index

    def find_next_damaged_group_in_scenario(self, start_index: int, scenario: str) -> dict[str, int]:
        next_damaged_index = scenario.find("#", start_index)
        if next_damaged_index != -1:
            operational_index_after = scenario.find(".", next_damaged_index)
            if operational_index_after != -1:
                damaged_group_length = operational_index_after - next_damaged_index
            else:
                damaged_group_length = len(scenario) - next_damaged_index
        else:
            damaged_group_length = 0
        return {
            "length": damaged_group_length,
            "index": next_damaged_index
        }

    def check_if_scenario_violates_pattern(self, scenario: str) -> bool:
        pattern_index = 0
        searching_index = 0
        violates_pattern = False
        while not violates_pattern and pattern_index < len(self.contiguous_groups) and searching_index < len(scenario):
            next_damaged_group = self.find_next_damaged_group_in_scenario(searching_index, scenario)
            if next_damaged_group["length"] == self.contiguous_groups[pattern_index]:
                pattern_index += 1
                searching_index = next_damaged_group["index"] + next_damaged_group["length"]
            elif next_damaged_group["length"] > self.contiguous_groups[pattern_index] or (next_damaged_group["length"] < self.contiguous_groups[pattern_index] and next_damaged_group["index"] != -1 and (scenario[-1] == "." or len(scenario) == len(self.original_conditions))):
                violates_pattern = True
            else:
                break
        return violates_pattern


class RecordsCollection:
    def __init__(self, record_descriptions: List[str]) -> None:
        self.records = self.create_records(record_descriptions)

    def create_records(self, descriptions: List[str]) -> List[ConditionsRecord]:
        records: List[ConditionsRecord] = []
        for description in descriptions:
            records.append(ConditionsRecord(description))
        return records

    def calculate_total_arrangements(self) -> int:
        total = 0
        for record in self.records:
            total += record.count_acceptable_arrangements()
        return total


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(12, is_official)
    record_descriptions = get_list_of_lines(data)
    collection = RecordsCollection(record_descriptions)
    part_1 = collection.calculate_total_arrangements()
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(12, part_1, part_2, execution_time)
    return results
