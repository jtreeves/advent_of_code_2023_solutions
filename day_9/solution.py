import time
from typing import List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class History:
    def __init__(self, summary: str) -> None:
        self.values = self.determine_values(summary)
        self.layers = self.generate_all_layers()
        self.predicted_next = self.predict_next_value()
        self.predicted_previous = self.predict_previous_value()

    def determine_values(self, summary: str) -> List[int]:
        extractions = summary.split(" ")
        values: List[int] = []
        for extraction in extractions:
            values.append(int(extraction))
        return values

    def calculate_differences_at_layer(self, layer: List[int]) -> List[int]:
        differences: List[int] = []
        for index in range(len(layer) - 1):
            differences.append(layer[index + 1] - layer[index])
        return differences

    def check_if_final_layer(self, layer: List[int]) -> bool:
        zeroes = 0
        for value in layer:
            if value == 0:
                zeroes += 1
        is_final = True if zeroes == len(layer) else False
        return is_final

    def generate_all_layers(self) -> List[List[int]]:
        layers: List[List[int]] = [self.values]
        is_final = False
        while not is_final:
            layers.append(self.calculate_differences_at_layer(layers[-1]))
            is_final = self.check_if_final_layer(layers[-1])
        return layers

    def predict_next_value(self) -> int:
        prediction = 0
        for layer in self.layers:
            prediction += layer[-1]
        return prediction

    def predict_previous_value(self) -> int:
        prediction = 0
        for index in range(len(self.layers)):
            prediction += self.layers[index][0] * ((-1) ** index)
        return prediction


class Report:
    def __init__(self, description: str) -> None:
        self.histories = self.determine_histories(description)

    def determine_histories(self, description: str) -> List[History]:
        lines = get_list_of_lines(description)
        histories: List[History] = []
        for line in lines:
            histories.append(History(line))
        return histories

    def sum_extrapolated_next_values(self) -> int:
        total = 0
        for history in self.histories:
            total += history.predicted_next
        return total

    def sum_extrapolated_previous_values(self) -> int:
        total = 0
        for history in self.histories:
            total += history.predicted_previous
        return total


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(9, is_official)
    report = Report(data)
    part_1 = report.sum_extrapolated_next_values()
    part_2 = report.sum_extrapolated_previous_values()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(9, part_1, part_2, execution_time)
    return results
