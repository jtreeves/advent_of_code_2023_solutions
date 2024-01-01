import time
from typing import List, Tuple, Set
from queue import Queue
from math import lcm
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Module:
    def __init__(self, name: str, destinations: List[str]) -> None:
        self.name = name
        self.destinations = destinations


class Button(Module):
    def __init__(self) -> None:
        super().__init__("button", ["broadcaster"])


class Broadcaster(Module):
    def __init__(self, destinations: List[str]) -> None:
        super().__init__("broadcaster", destinations)


class FlipFlop(Module):
    def __init__(self, name: str, destinations: List[str]) -> None:
        super().__init__(name, destinations)
        self.status = -1


class Conjunction(Module):
    def __init__(self, name: str, destinations: List[str]) -> None:
        super().__init__(name, destinations)
        self.inputs: dict[str, int] = {}

    def add_input(self, input: str) -> None:
        self.inputs[input] = -1

    def set_input(self, input: str, pulse: int) -> None:
        self.inputs[input] = pulse

    def reset_all_inputs(self) -> None:
        for input in self.inputs.keys():
            self.set_input(input, -1)

    def check_if_all_inputs_high(self) -> bool:
        pulses = 0
        for pulse in self.inputs.values():
            pulses += pulse
        all_high = pulses == len(self.inputs.keys())
        return all_high


class Configuration:
    def __init__(self, description: str) -> None:
        module_descriptions = get_list_of_lines(description)
        self.modules = self.create_modules(module_descriptions)
        self.output_module = self.find_output_module()
        self.pulses = self.create_pulses_tracker()
        self.populate_all_inputs_memos()

    def create_modules(self, descriptions: List[str]) -> dict[str, Module]:
        all_modules: dict[str, Module] = {}
        for description in descriptions:
            elements = description.split(" -> ")
            name = elements[0]
            destinations = elements[1].split(", ")
            if name == "broadcaster":
                new_module = Broadcaster(destinations)
            elif name[0] == "%":
                name = name[1:]
                new_module = FlipFlop(name, destinations)
            elif name[0] == "&":
                name = name[1:]
                new_module = Conjunction(name, destinations)
            else:
                new_module = Module(name, destinations)
            all_modules[new_module.name] = new_module
        all_modules["button"] = Button()
        return all_modules

    def find_output_module(self) -> str:
        input_modules: Set[str] = set()
        destination_modules: Set[str] = set()
        for module in self.modules.values():
            input_modules.add(module.name)
            for destination in module.destinations:
                destination_modules.add(destination)
        output_modules = destination_modules - input_modules
        return output_modules.pop()

    def create_pulses_tracker(self) -> dict[int, int]:
        pulses_tracker = {
            1: 0,
            0: 0,
            -1: 0
        }
        return pulses_tracker

    def update_pulses_tracker(self, pulse: int) -> None:
        self.pulses[pulse] += pulse

    def populate_all_inputs_memos(self) -> None:
        for module in self.modules.values():
            destinations = module.destinations
            for destination in destinations:
                potential_conjunction = self.modules.get(destination)
                if potential_conjunction and isinstance(potential_conjunction, Conjunction):
                    potential_conjunction.add_input(module.name)

    def reset(self) -> None:
        for module in self.modules.values():
            if isinstance(module, FlipFlop):
                module.status = -1
            elif isinstance(module, Conjunction):
                module.reset_all_inputs()

    def propagate_pulses_with_single_push(self, tracking_module: str = "") -> bool:
        high_emitted = False
        processing_modules: Queue[Tuple[Module, int, str]] = Queue()
        processing_modules.put((self.modules["button"], 0, ""))
        while not processing_modules.empty():
            current_module, current_pulse, current_source = processing_modules.get()
            self.update_pulses_tracker(current_pulse)
            next_source = current_module.name
            if isinstance(current_module, (Button, Broadcaster)):
                next_pulse = -1
            elif isinstance(current_module, FlipFlop):
                current_module.status *= current_pulse
                next_pulse = current_module.status
            elif isinstance(current_module, Conjunction):
                current_module.set_input(current_source, current_pulse)
                all_high = current_module.check_if_all_inputs_high()
                if all_high:
                    next_pulse = -1
                else:
                    next_pulse = 1
            else:
                next_pulse = 0
            destinations = current_module.destinations
            for destination in destinations:
                next_module = self.modules.get(destination)
                if next_module:
                    if not isinstance(current_module, FlipFlop) or current_pulse == -1:
                        processing_modules.put((next_module, next_pulse, next_source))
                        if next_source == tracking_module and next_pulse == 1:
                            high_emitted = True
                else:
                    self.update_pulses_tracker(next_pulse)
        return high_emitted

    def find_output_grandparents(self) -> List[str]:
        grandparents: List[str] = []
        for module in self.modules.values():
            for destination in module.destinations:
                if destination == self.output_module and isinstance(module, Conjunction):
                    for input in module.inputs.keys():
                        grandparents.append(input)
        return grandparents

    def find_first_high_emission(self, name: str) -> int:
        self.reset()
        pushes = 0
        high_emitted = False
        while not high_emitted:
            pushes += 1
            high_emitted = self.propagate_pulses_with_single_push(name)
        return pushes

    def calculate_pulses_product_for_initial_pushes(self) -> int:
        for _ in range(1000):
            self.propagate_pulses_with_single_push()
        return abs(self.pulses[1] * self.pulses[-1])

    def find_minimal_number_of_pushes_for_output(self) -> int:
        first_emissions: List[int] = []
        grandparents = self.find_output_grandparents()
        for grandparent in grandparents:
            first_high = self.find_first_high_emission(grandparent)
            first_emissions.append(first_high)
        minimal_pushes = lcm(*first_emissions)
        return minimal_pushes


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(20, is_official)
    configuration = Configuration(data)
    part_1 = configuration.calculate_pulses_product_for_initial_pushes()
    part_2 = configuration.find_minimal_number_of_pushes_for_output()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(20, part_1, part_2, execution_time)
    return results
