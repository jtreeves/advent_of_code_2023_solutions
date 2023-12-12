import time
from typing import List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class ConditionsRecord:
    def __init__(self, record_description: str) -> None:
        versions = record_description.split(" ")
        self.original_conditions = versions[0]
        self.contiguous_groups = self.determine_contiguous_groups(versions[1])

    def determine_contiguous_groups(self, notes: str) -> List[int]:
        groups = notes.split(",")
        contiguous_groups: List[int] = []
        for group in groups:
            contiguous_groups.append(int(group))
        return contiguous_groups

    def count_acceptable_arrangements(self) -> int:
        acceptable_arrangements = 1
        possible_beginnings: List[str] = []
        next_unknown_index = self.find_next_unknown_condition(0)
        if next_unknown_index != -1:
            set_subsection = self.original_conditions[0:next_unknown_index]
            first_possibility = set_subsection + "#"
            second_possibility = set_subsection + "."
            possible_beginnings.extend([first_possibility, second_possibility])
        while len(possible_beginnings) != 0:
            possible_beginning = possible_beginnings.pop()
            current_index = len(possible_beginning)
            next_unknown_index = self.find_next_unknown_condition(current_index)
            if next_unknown_index != -1:
                set_subsection = possible_beginning + self.original_conditions[current_index:next_unknown_index]
                first_possibility = set_subsection + "#"
                second_possibility = set_subsection + "."
                possible_beginnings.extend([first_possibility, second_possibility])
            else:
                acceptable_arrangements += 1
        return acceptable_arrangements

    def find_next_unknown_condition(self, start_index: int) -> int:
        next_index = self.original_conditions.find("?", start_index)
        return next_index

    def find_next_damaged_group(self, start_index: int) -> dict[str, int]:
        next_damaged_index = self.original_conditions.find("#", start_index)
        later_operational_index = self.original_conditions.find(".", next_damaged_index)
        damaged_group_length = later_operational_index - next_damaged_index
        damaged_group = {
            "start_index": next_damaged_index,
            "length": damaged_group_length
        }
        return damaged_group

    def check_if_meets_criteria(self, description: str) -> bool:
        meets_criteria = True
        start_index = 0
        while meets_criteria:
            for group_length in self.contiguous_groups:
                next_damaged_group = self.find_next_damaged_group(start_index)
                if next_damaged_group["length"] != group_length:
                    meets_criteria = False
        return meets_criteria


class RecordsCollection:
    def __init__(self, record_descriptions: List[str]) -> None:
        self.records = self.create_records(record_descriptions)

    def create_records(self, descriptions: List[str]) -> List[ConditionsRecord]:
        records: List[ConditionsRecord] = []
        for description in descriptions:
            records.append(ConditionsRecord(description))
        return records


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(12, is_official)
    record_descriptions = get_list_of_lines(data)
    records = RecordsCollection(record_descriptions)
    part_1 = 1 if data else 0
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(12, part_1, part_2, execution_time)
    return results
