import time
from typing import List, Set, Tuple, Callable
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

    def break_components_into_partitions(self) -> Tuple[Set[str], Set[str]]:
        initial_components = set(self.components.keys())
        count_external_edges: Callable[[str], int] = lambda component_name: len(set(self.components[component_name].connections) - initial_components)
        while initial_components and sum(map(count_external_edges, initial_components)) != 3:
            component_to_remove = max(initial_components, key=count_external_edges)
            initial_components.remove(component_to_remove)
        first_partition = initial_components
        second_partition = set(self.components.keys()) - initial_components
        return first_partition, second_partition

    def calculate_product_of_partition_sizes(self) -> int:
        first_partition, second_partition = self.break_components_into_partitions()
        product = len(first_partition) * len(second_partition)
        return product


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(25, is_official)
    diagram = WiringDiagram(data)
    part_1 = diagram.calculate_product_of_partition_sizes()
    part_2 = 50
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(25, part_1, part_2, execution_time)
    return results

# CREDIT: https://www.reddit.com/r/adventofcode/comments/18qbsxs/comment/ketzp94/
