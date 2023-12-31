import time
from typing import List, Tuple, Set
from queue import Queue
from itertools import product
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

    def set_all_inputs(self, pulse: int) -> None:
        for input in self.inputs.keys():
            self.set_input(input, pulse)

    def reset_all_inputs(self) -> None:
        self.set_all_inputs(-1)

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
        self.output_module = self.find_output_module()
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

    def propagate_pulses_with_single_push(self) -> bool:
        # print("*** NEW BUTTON CLICK")
        # for flip_flop in self.flip_flops.values():
        #     if flip_flop.name == "cx":
        #         print(f"{flip_flop.name}: {flip_flop.status}")
        # interactions: List[str] = []
        output_received_low = False
        processing_modules: Queue[Tuple[Module, int, str]] = Queue()
        processing_modules.put((self.modules['button'], 0, ''))
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
                        # interactions.append(f"{next_source} -> {next_module.name}")
                else:
                    self.update_pulses_tracker(next_pulse)
                    if destination == self.output_module and next_pulse == -1:
                        output_received_low = True
                    # interactions.append(f"{next_source} -> output")
        return output_received_low

    def count_pushes_in_cycle(self) -> int:
        pushes = 0
        all_off = self.check_if_all_flip_flops_off()
        while not all_off or not pushes:
            self.propagate_pulses_with_single_push()
            all_off = self.check_if_all_flip_flops_off()
            pushes += 1
        return pushes

    def calculate_pulses_product_for_initial_pushes(self) -> int:
        # all_steps: List[List[str]] = []
        for _ in range(4):
            self.propagate_pulses_with_single_push()
            # all_steps.append(steps)
        # options: Set[str] = set()
        # indices: List[Tuple[int, List[str], int]] = []
        # for index in range(len(all_steps)):
        #     # print("*** BUTTON PUSH")
        #     steps = all_steps[index]
        #     potential_option = '|'.join(steps)
        #     if potential_option not in options:
        #         indices.append((index, steps, len(steps)))
        #     options.add(potential_option)
        #     # for step in steps:
        #     #     print(step)
        # sorted_indices = sorted(indices, key=lambda x: x[2])
        # for element in sorted_indices:
        #     i, steps, length = element
        #     print('*** NEW OPTION')
        #     print('INDEX:', i)
        #     # print('STEPS:', steps)
        #     print('LENGTH:', length)
        # print(options)
        # print('LENGTH OF OPTIONS:', len(options))
        # print('LENGTH OF INDICES:', len(indices))
        return abs(self.pulses[1] * self.pulses[-1])

    def find_output_module(self) -> str:
        input_modules: Set[str] = set()
        destination_modules: Set[str] = set()
        for module in self.modules.values():
            input_modules.add(module.name)
            for destination in module.destinations:
                destination_modules.add(destination)
        output_modules = destination_modules - input_modules
        return output_modules.pop()

    def find_paths_to_output_module(self, current_module_name: str = "button", visited: Set[str] = set(), path: List[str] = []) -> List[List[str]]:
        visited.add(current_module_name)
        path.append(current_module_name)
        if current_module_name == self.output_module:
            return [path]
        else:
            paths: List[List[str]] = []
            current_module = self.modules.get(current_module_name)
            if current_module:
                for destination in current_module.destinations:
                    if destination not in visited:
                        new_paths = self.find_paths_to_output_module(destination, visited.copy(), path.copy())
                        paths.extend(new_paths)
            return paths

    def find_flip_flop_dependencies_for_output_module(self) -> List[str]:
        checked_modules: Set[str] = set()
        flip_flops: Set[str] = set()
        stack: List[str] = [self.output_module]
        while len(stack):
            current_module_name = stack.pop()
            if current_module_name != "broadcaster":
                for module in self.modules.values():
                    for destination in module.destinations:
                        if destination == current_module_name and module.name not in checked_modules:
                            stack.append(module.name)
                            checked_modules.add(module.name)
                            potential_flip_flop = self.modules.get(destination)
                            if potential_flip_flop and isinstance(potential_flip_flop, FlipFlop):
                                flip_flops.add(destination)
        print(checked_modules)
        return list(flip_flops)

    def find_flip_flop_permutations_for_output_module(self) -> List[dict[str, int]]:
        values = [-1, 1]
        dependencies = self.find_flip_flop_dependencies_for_output_module()
        permutations = [dict(zip(dependencies, permutation)) for permutation in product(values, repeat=len(dependencies))]
        return permutations

    def find_minimal_number_of_pushes_for_rx(self) -> int:
        pushes = 0
        return pushes

    def check_if_all_flip_flops_off(self) -> bool:
        statuses = 0
        for module in self.flip_flops.values():
            statuses += module.status
        all_off = statuses == -len(self.flip_flops)
        return all_off

    def set_starting_values(self, core_flip_flop_values: dict[str, int]) -> None:
        for module in self.modules.values():
            if isinstance(module, FlipFlop):
                if module.name in core_flip_flop_values.keys():
                    module.status = core_flip_flop_values[module.name]
                else:
                    module.status = -1
            elif isinstance(module, Conjunction):
                module.set_all_inputs(1)
                if any(element in module.inputs.keys() for element in core_flip_flop_values.keys()):
                    for flip_flop in core_flip_flop_values.keys():
                        if flip_flop in module.inputs.keys():
                            module.inputs[flip_flop] = core_flip_flop_values[flip_flop]

    def check_output_at_starting_values(self, core_flip_flop_values: dict[str, int]) -> bool:
        self.set_starting_values(core_flip_flop_values)
        output_received_low = self.propagate_pulses_with_single_push()
        return output_received_low

    def find_all_permutations_sending_low_to_output(self) -> List[dict[str, int]]:
        low_permutations: List[dict[str, int]] = []
        all_permutations = self.find_flip_flop_permutations_for_output_module()
        print(len(all_permutations))
        for permutation in all_permutations:
            output_received_low = self.check_output_at_starting_values(permutation)
            if output_received_low:
                low_permutations.append(permutation)
        print(len(low_permutations))
        return low_permutations

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
    # paths = first_configuration.find_paths_to_output_module()
    # print(paths)
    flip_flops = first_configuration.find_flip_flop_dependencies_for_output_module()
    print(flip_flops)
    # permutations = first_configuration.find_flip_flop_permutations_for_output_module()
    # print(permutations)
    # check_output = first_configuration.check_output_at_starting_values(permutations[2])
    # print(check_output)
    all_low = first_configuration.find_all_permutations_sending_low_to_output()
    print(all_low)
    # part_1 = first_configuration.calculate_pulses_product_for_initial_pushes()
    part_1 = 1
    part_2 = second_configuration.find_minimal_number_of_pushes_for_rx()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(20, part_1, part_2, execution_time)
    return results
