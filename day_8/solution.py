import time
from math import lcm
from typing import List
from utils.extract_data_from_file import extract_data_from_file
from utils.get_list_of_lines import get_list_of_lines
from utils.SolutionResults import SolutionResults


class DestinationPair:
    def __init__(self, description: str) -> None:
        parts = description.split(", ")
        self.left = parts[0].replace("(", "")
        self.right = parts[1].replace(")", "")


class Node:
    def __init__(self, description: str) -> None:
        elements = description.split(" = ")
        self.name = elements[0]
        self.destinations = DestinationPair(elements[1])

    def __repr__(self) -> str:
        return f"{self.name}: ({self.destinations.left}, {self.destinations.right})"

    def find_next_node(self, current_direction: str) -> str:
        if current_direction == "L":
            next_node_name = self.destinations.left
        else:
            next_node_name = self.destinations.right
        return next_node_name


class Network:
    def __init__(self, description: str) -> None:
        sections = description.split("\n\n")
        self.instructions = sections[0]
        self.nodes = self.determine_nodes(sections[1])

    def __repr__(self) -> str:
        representation = f"INSTRUCTIONS: {self.instructions}\n"
        for node in self.nodes.values():
            representation += f"{node.name}: ({node.destinations.left}, {node.destinations.right})\n"
        return representation

    def determine_nodes(self, description: str) -> dict[str, Node]:
        nodes: dict[str, Node] = {}
        lines = get_list_of_lines(description)
        for line in lines:
            node = Node(line)
            nodes[node.name] = node
        return nodes

    def find_all_start_nodes(self) -> List[Node]:
        start_nodes: List[Node] = []
        for node in self.nodes.values():
            if node.name[2] == "A":
                start_nodes.append(node)
        return start_nodes

    def count_steps_from_start_to_finish(self) -> int:
        current_node = self.nodes["AAA"]
        steps = 0
        while current_node.name != "ZZZ":
            current_direction = self.instructions[steps % len(self.instructions)]
            next_node_name = current_node.find_next_node(current_direction)
            current_node = self.nodes[next_node_name]
            steps += 1
        return steps

    def determine_steps_pattern_length_from_semi_start_to_semi_finish(self, start_node: Node) -> int:
        current_node = start_node
        steps = 0
        pattern: List[int] = []
        pattern_determined = False
        while not pattern_determined:
            current_direction = self.instructions[steps % len(self.instructions)]
            next_node_name = current_node.find_next_node(current_direction)
            current_node = self.nodes[next_node_name]
            if current_node.name[2] == "Z":
                starting_index = 0 if len(pattern) == 0 else pattern[-1]
                change_in_distance = steps - starting_index
                if len(pattern) > 1:
                    if change_in_distance != pattern[1] - pattern[0]:
                        pattern.append(steps)
                    else:
                        pattern_determined = True
                else:
                    pattern.append(steps)
            steps += 1
        length = pattern[1] - pattern[0]
        return length

    def determine_steps_pattern_lengths_for_all_semi_starts(self) -> List[int]:
        start_nodes = self.find_all_start_nodes()
        pattern_lengths: List[int] = []
        for node in start_nodes:
            length = self.determine_steps_pattern_length_from_semi_start_to_semi_finish(node)
            pattern_lengths.append(length)
        return pattern_lengths

    def find_first_overlap_in_patterns(self) -> int:
        lengths = self.determine_steps_pattern_lengths_for_all_semi_starts()
        first_overlap = lcm(*lengths)
        return first_overlap


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(8, is_official)
    network = Network(data)
    part_1 = network.count_steps_from_start_to_finish()
    part_2 = network.find_first_overlap_in_patterns()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(8, part_1, part_2, execution_time)
    return results
