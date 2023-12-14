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
            possibilities = [first_possibility, second_possibility]
            print('INITIAL POSSIBILITIES:', possibilities)
            for possibility in possibilities:
                meets_criteria = self.check_if_meets_criteria(possibility)
                if meets_criteria:
                    possible_beginnings.append(possibility)
        while len(possible_beginnings) != 0:
            possible_beginning = possible_beginnings.pop()
            print('POSSIBLE BEGINNING:', possible_beginning)
            current_index = len(possible_beginning)
            next_unknown_index = self.find_next_unknown_condition(current_index)
            if next_unknown_index != -1:
                set_subsection = possible_beginning + self.original_conditions[current_index:next_unknown_index]
                first_possibility = set_subsection + "#"
                second_possibility = set_subsection + "."
                possibilities = [first_possibility, second_possibility]
                for possibility in possibilities:
                    meets_criteria = self.check_if_meets_criteria(possibility)
                    if meets_criteria:
                        possible_beginnings.append(possibility)
            else:
                acceptable_arrangements += 1
        return acceptable_arrangements

    def find_next_unknown_condition(self, start_index: int) -> int:
        next_index = self.original_conditions.find("?", start_index)
        return next_index

    def find_next_damaged_group(self, possible_description: str, start_index: int) -> dict[str, int]:
        print('INSIDE FIND NEXT DAMAGED GROUP')
        print('START INDEX:', start_index)
        next_damaged_index = possible_description.find("#", start_index)
        next_unknown_index = possible_description.find("?", start_index)
        least_starting_index = next_damaged_index if next_damaged_index < next_unknown_index else next_unknown_index
        later_operational_index = possible_description.find(".", least_starting_index)
        later_unknown_index = possible_description.find("?", least_starting_index)
        least_ending_index = later_operational_index if later_operational_index < later_unknown_index else later_unknown_index
        damaged_group_length = least_ending_index - least_starting_index if least_ending_index != least_starting_index else 1
        damaged_group = {
            "length": damaged_group_length,
            "end_index": least_ending_index
        }
        return damaged_group

    def check_if_meets_criteria(self, possible_beginning: str) -> bool:
        print('*** BEGIN NEW CHECK')
        meets_criteria = True
        possible_description = possible_beginning + self.original_conditions[len(possible_beginning):]
        print('DESCRIPTION TO CHECK:', possible_description)
        description_index_to_check = 0
        group_index_to_check = 0
        while meets_criteria and description_index_to_check < len(self.original_conditions) and group_index_to_check < len(self.contiguous_groups):
            next_damaged_group = self.find_next_damaged_group(possible_description, description_index_to_check)
            print('NEXT DAMAGED GROUP:', next_damaged_group)
            print('GROUP INDEX TO CHECK:', group_index_to_check)
            if self.contiguous_groups[group_index_to_check] < next_damaged_group["length"]:
                meets_criteria = False
            else:
                description_index_to_check = next_damaged_group["end_index"]
                group_index_to_check += 1
        if group_index_to_check != len(self.contiguous_groups):
            meets_criteria = False
        print('MEETS CRITERIA?', meets_criteria)
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
    collection = RecordsCollection(record_descriptions)
    print('FIRST POSSIBILITIES:', collection.records[1].count_acceptable_arrangements())
    part_1 = 1 if data else 0
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(12, part_1, part_2, execution_time)
    return results
