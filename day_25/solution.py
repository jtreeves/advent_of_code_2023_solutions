import time
from typing import List, Set
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Component:
    def __init__(self, name: str, connections: List[str]) -> None:
        self.name = name
        self.connections = set(connections)


class WiringDiagram:
    def __init__(self, description: str) -> None:
        component_descriptions = get_list_of_lines(description)
        self.components = self.create_components(component_descriptions)

    def __repr__(self) -> str:
        representation = ""
        for key in sorted(self.components.keys()):
            component = self.components[key]
            representation += f"{component.name}: {component.connections}\n"
        return representation

    def create_components(self, descriptions: List[str]) -> dict[str, Component]:
        components: dict[str, Component] = {}
        for description in descriptions:
            parts = description.split(": ")
            name = parts[0]
            connections = parts[1].split(" ")
            existing_component = components.get(name)
            if existing_component:
                existing_component.connections |= set(connections)
            else:
                new_component = Component(name, connections)
                components[name] = new_component
            for connection in connections:
                existing_connection = components.get(connection)
                if existing_connection:
                    existing_connection.connections.add(name)
                else:
                    new_connection = Component(connection, [name])
                    components[connection] = new_connection
        return components

    def find_partitions_with_stoer_wagner(self) -> List[Set[str]]:
        initial_partition: Set[str] = set(self.components.keys())
        new_partition: Set[str] = set()
        while len(new_partition) < len(initial_partition) - 3:
            min_cut_size = float("inf")
            min_cut_node = ""
            for component in initial_partition:
                cut_size = sum(1 for neighbor in self.components[component].connections if neighbor in new_partition)
                if cut_size < min_cut_size:
                    min_cut_size = cut_size
                    min_cut_node = component
            initial_partition.remove(min_cut_node)
            new_partition.add(min_cut_node)
        return [initial_partition, new_partition]

    def calculate_product_of_partition_sizes(self) -> int:
        partitions = self.find_partitions_with_stoer_wagner()
        first_partition = partitions[0]
        second_partition = partitions[1]
        product = len(first_partition) * len(second_partition)
        return product


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(25, is_official)
    diagram = WiringDiagram(data)
    part_1 = diagram.calculate_product_of_partition_sizes()
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(25, part_1, part_2, execution_time)
    return results
