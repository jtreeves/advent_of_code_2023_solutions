import time
from typing import List
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


def apply_hash_algorithm(input: str) -> int:
    value = 0
    for character in input:
        value += ord(character)
        value *= 17
        value %= 256
    return value


def move_lenses(steps: List[str]) -> dict[int, dict[str, dict[str, int]]]:
    boxes: dict[int, dict[str, dict[str, int]]] = {}
    for box_number in range(256):
        boxes[box_number] = {}
    for step in steps:
        if step.find("=") != -1:
            parts = step.split("=")
            label = parts[0]
            correct_box = apply_hash_algorithm(label)
            focal_length = int(parts[1])
            if boxes[correct_box].get(label):
                boxes[correct_box][label] = {
                    "focal_length": focal_length,
                    "index": boxes[correct_box][label]["index"]
                }
            else:
                boxes[correct_box][label] = {
                    "focal_length": focal_length,
                    "index": len(boxes[correct_box].values())
                }
        else:
            label = step[:-1]
            correct_box = apply_hash_algorithm(label)
            if boxes[correct_box].get(label):
                current_index = boxes[correct_box][label]["index"]
                for other_label in boxes[correct_box].keys():
                    if boxes[correct_box][other_label]["index"] > current_index:
                        boxes[correct_box][other_label]["index"] -= 1
                del boxes[correct_box][label]
    return boxes


def calculate_total_focusing_power(boxes: dict[int, dict[str, dict[str, int]]]) -> int:
    total_focusing_power = 0
    for [box_number, lenses] in boxes.items():
        box_focusing_power = 0
        for lense in lenses.values():
            box_focusing_power += (box_number + 1) * (lense["index"] + 1) * lense["focal_length"]
        total_focusing_power += box_focusing_power
    return total_focusing_power


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(15, is_official)
    steps = data.split(",")
    sum_hash_values = 0
    for step in steps:
        sum_hash_values += apply_hash_algorithm(step)
    final_boxes = move_lenses(steps)
    total_focusing_power = calculate_total_focusing_power(final_boxes)
    part_1 = sum_hash_values
    part_2 = total_focusing_power
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(15, part_1, part_2, execution_time)
    return results
