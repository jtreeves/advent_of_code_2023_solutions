import time
from typing import List, Tuple
from queue import Queue
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Module:
    def __init__(self, name: str, destinations: List[str]) -> None:
        self.name = name
        self.destinations = destinations


class Button(Module):
    def __init__(self) -> None:
        super().__init__('button', ['broadcaster'])


class Broadcaster(Module):
    def __init__(self, destinations: List[str]) -> None:
        super().__init__('broadcaster', destinations)


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
        self.pulses = self.create_pulses_tracker()
        self.populate_all_inputs_memos()

    def create_modules(self, descriptions: List[str]) -> dict[str, Module]:
        all_modules: dict[str, Module] = {}
        flip_flops: dict[str, FlipFlop] = {}
        conjunctions: dict[str, Conjunction] = {}
        for description in descriptions:
            elements = description.split(" -> ")
            name = elements[0]
            destinations = elements[1].split(", ")
            if name == "broadcaster":
                new_module = Broadcaster(destinations)
            elif name[0] == "%":
                name = name[1:]
                new_module = FlipFlop(name, destinations)
                flip_flops[name] = new_module
            elif name[0] == "&":
                name = name[1:]
                new_module = Conjunction(name, destinations)
                conjunctions[name] = new_module
            else:
                new_module = Module(name, destinations)
            all_modules[new_module.name] = new_module
        all_modules["button"] = Button()
        self.flip_flops = flip_flops
        self.conjunctions = conjunctions
        return all_modules

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
                potential_conjunction = self.conjunctions.get(destination)
                if potential_conjunction:
                    potential_conjunction.add_input(module.name)

    def propagate_pulses_with_single_push(self) -> None:
        processing_modules: Queue[Tuple[Module, int, str]] = Queue()
        processing_modules.put((self.modules['button'], 0, ''))
        while not processing_modules.empty():
            current_module, current_pulse, current_source = processing_modules.get()
            self.update_pulses_tracker(current_pulse)
            next_name = current_module.name
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
                        processing_modules.put((next_module, next_pulse, next_name))
                else:
                    self.update_pulses_tracker(next_pulse)

    def count_pushes_in_cycle(self) -> int:
        pushes = 0
        all_off = self.check_if_all_flip_flops_off()
        while not all_off or not pushes:
            self.propagate_pulses_with_single_push()
            all_off = self.check_if_all_flip_flops_off()
            pushes += 1
        return pushes

    def calculate_pulses_product_for_pushes(self, pushes: int) -> int:
        pushes_in_cycle = self.count_pushes_in_cycle()
        low_pulses_in_cycle = self.pulses[-1]
        high_pulses_in_cycle = self.pulses[1]
        cycles_needed = pushes // pushes_in_cycle
        total_low_pulses = low_pulses_in_cycle * cycles_needed
        total_high_pulses = high_pulses_in_cycle * cycles_needed
        pulses_product = abs(total_low_pulses * total_high_pulses)
        return pulses_product

    def find_minimal_number_of_pushes_for_rx(self) -> int:
        pushes = 0
        return pushes

    def check_if_all_flip_flops_off(self) -> bool:
        statuses = 0
        for module in self.flip_flops.values():
            statuses += module.status
        all_off = statuses == -len(self.flip_flops)
        return all_off

    def reset(self) -> None:
        for module in self.flip_flops.values():
            module.status = -1
        for module in self.conjunctions.values():
            module.reset_all_inputs()


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(20, is_official)
    first_configuration = Configuration(data)
    second_configuration = Configuration(data)
    part_1 = first_configuration.calculate_pulses_product_for_pushes(1000)
    part_2 = second_configuration.find_minimal_number_of_pushes_for_rx()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(20, part_1, part_2, execution_time)
    return results
