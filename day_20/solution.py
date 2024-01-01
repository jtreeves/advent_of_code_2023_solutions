import time
from typing import List, Tuple, Set, Sequence
from queue import Queue
from itertools import product
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
            self.inputs[input] = -1

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

    def find_flip_flop_modules(self) -> Set[str]:
        flip_flops: Set[str] = set()
        for module in self.modules.values():
            if isinstance(module, FlipFlop):
                flip_flops.add(module.name)
        return flip_flops

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

    def calculate_pulses_product_for_initial_pushes(self) -> int:
        for _ in range(1000):
            self.propagate_pulses_with_single_push()
        return abs(self.pulses[1] * self.pulses[-1])

    def set_starting_values(self, core_flip_flop_values: dict[str, int]) -> None:
        for module in self.modules.values():
            if isinstance(module, FlipFlop):
                if module.name in core_flip_flop_values.keys():
                    module.status = core_flip_flop_values[module.name]
                else:
                    module.status = -1
            elif isinstance(module, Conjunction):
                module.reset_all_inputs()
                if any(element in module.inputs.keys() for element in core_flip_flop_values.keys()):
                    for flip_flop in core_flip_flop_values.keys():
                        if flip_flop in module.inputs.keys():
                            module.inputs[flip_flop] = core_flip_flop_values[flip_flop]

    def check_output_at_starting_values(self, core_flip_flop_values: dict[str, int]) -> bool:
        self.set_starting_values(core_flip_flop_values)
        output_received_low = self.propagate_pulses_with_single_push()
        return output_received_low

    def find_permutations_sending_low_to_output(self) -> List[dict[str, int]]:
        low_permutations: List[dict[str, int]] = []
        stack: List[Tuple[str, int, dict[str, int], List[str]]] = [(self.output_module, -1, {}, [])]
        while len(stack):
            current_module_name, current_pulse_needed, current_flip_flops, current_path = stack.pop()
            if current_module_name == "broadcaster":
                if current_pulse_needed != 1:
                    low_permutations.append(current_flip_flops)
            elif len(find_pattern(current_path)[0]) == len(current_path) and len(current_path) < 100:
                current_path.append(current_module_name)
                for module in self.modules.values():
                    for destination in module.destinations:
                        if destination == current_module_name:
                            if isinstance(module, FlipFlop):
                                current_flip_flops_copy = current_flip_flops.copy()
                                current_flip_flops_copy[module.name] = -current_pulse_needed
                                current_pulse_needed = -1
                                stack.append((module.name, current_pulse_needed, current_flip_flops_copy, current_path.copy()))
                            elif isinstance(module, Conjunction):
                                if current_pulse_needed == -1:
                                    current_pulse_needed = 1
                                    stack.append((module.name, current_pulse_needed, current_flip_flops.copy(), current_path.copy()))
                                else:
                                    inputs = module.inputs
                                    options = [list(zip(inputs, p)) for p in product([1, -1], repeat=len(inputs)) if any(v == -1 for v in p)]
                                    for option in options:
                                        for sub_module in option:
                                            name, pulse = sub_module
                                            stack.append((name, pulse, current_flip_flops.copy(), current_path.copy()))
                            else:
                                stack.append((module.name, current_pulse_needed, current_flip_flops.copy(), current_path.copy()))
        return low_permutations

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

    def find_minimal_number_of_pushes_for_output(self) -> int:
        first_emissions: List[int] = []
        grandparents = self.find_output_grandparents()
        for grandparent in grandparents:
            first_high = self.find_first_high_emission(grandparent)
            first_emissions.append(first_high)
        return lcm(*first_emissions)

    def reset(self) -> None:
        for module in self.modules.values():
            if isinstance(module, FlipFlop):
                module.status = -1
            elif isinstance(module, Conjunction):
                module.reset_all_inputs()


def find_pattern(sequence: Sequence[int | str]) -> Tuple[Sequence[int | str], int]:
    minimum_size = 2
    sequence_length = len(sequence)
    if sequence_length >= minimum_size * 2:
        for window_size in range(minimum_size, sequence_length):
            start_index = sequence_length - window_size
            pattern_candidate = sequence[start_index:]
            first_pattern_index = find_sublist_index(sequence, pattern_candidate)
            if first_pattern_index != start_index and first_pattern_index + len(pattern_candidate) == start_index:
                return pattern_candidate, first_pattern_index
        return sequence, 0
    else:
        return sequence, 0


def find_sublist_index(main_list: Sequence[int | str], sublist: Sequence[int | str]) -> int:
    for i in range(len(main_list) - len(sublist) + 1):
        if main_list[i:i + len(sublist)] == sublist:
            return i
    return -1


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
