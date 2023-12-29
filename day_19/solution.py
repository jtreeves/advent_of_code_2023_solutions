import time
from typing import List, Callable
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Part:
    def __init__(self, ratings: str) -> None:
        categories = ratings[1:-1].split(",")
        self.x = int(categories[0][2:])
        self.m = int(categories[1][2:])
        self.a = int(categories[2][2:])
        self.s = int(categories[3][2:])

    def sum_ratings(self) -> int:
        return self.x + self.m + self.a + self.s


class Rule:
    def __init__(self, description: str) -> None:
        elements = description.split(":")
        expression = elements[0]
        self.category = expression[0]
        self.inequality = expression[1]
        self.breakpoint = int(expression[2:]) if expression != "True" else 0
        self.destination = elements[1]
        self.evaluation = self.create_evaluation(expression)

    def create_evaluation(self, expression: str) -> Callable[[int], bool]:
        if expression != "True":
            return lambda x: eval(expression, {"x": x, "m": x, "a": x, "s": x})
        else:
            return lambda x: True


class IntervalRange:
    def __init__(self, minimum: int, maximum: int) -> None:
        self.minimum = minimum
        self.maximum = maximum


class Path:
    def __init__(self, workflow: str, rule: int, categories: dict[str, IntervalRange]) -> None:
        self.workflow = workflow
        self.rule = rule
        self.x = categories["x"]
        self.m = categories["m"]
        self.a = categories["a"]
        self.s = categories["s"]
        self.accepted = False

    def count_rating_combinations(self) -> int:
        x_range = self.x.maximum - self.x.minimum + 1
        m_range = self.m.maximum - self.m.minimum + 1
        a_range = self.a.maximum - self.a.minimum + 1
        s_range = self.s.maximum - self.s.minimum + 1
        combinations = x_range * m_range * a_range * s_range
        return combinations


class Workflow:
    def __init__(self, description: str) -> None:
        elements = description.split("{")
        self.name = elements[0]
        self.rules = self.create_rules(elements[1][:-1])

    def create_rules(self, description: str) -> List[Rule]:
        stages = description.split(",")
        rules: List[Rule] = []
        for index in range(len(stages) - 1):
            rules.append(Rule(stages[index]))
        rules.append(Rule("True:" + stages[-1]))
        return rules


class Puzzle:
    def __init__(self, data: str) -> None:
        elements = data.split("\n\n")
        self.system = self.create_system(elements[0])
        self.pile = self.create_pile(elements[1])

    def create_system(self, description: str) -> dict[str, Workflow]:
        lines = get_list_of_lines(description)
        workflows: dict[str, Workflow] = {}
        for line in lines:
            workflow = Workflow(line)
            workflows[workflow.name] = workflow
        return workflows

    def create_pile(self, description: str) -> List[Part]:
        pile: List[Part] = []
        parts = get_list_of_lines(description)
        for part in parts:
            pile.append(Part(part))
        return pile

    def process_part(self, part: Part) -> bool:
        accepted = False
        processed = False
        current_workflow = self.system["in"]
        while not processed:
            workflow_evaluated = False
            rule_index = 0
            while not workflow_evaluated:
                rule = current_workflow.rules[rule_index]
                category = rule.category
                if category != "T":
                    value = getattr(part, category)
                else:
                    value = 0
                result = rule.evaluation(value)
                if result:
                    workflow_evaluated = True
                    next_step = self.system.get(rule.destination)
                    if next_step:
                        current_workflow = next_step
                    else:
                        processed = True
                        if rule.destination == "A":
                            accepted = True
                else:
                    rule_index += 1
        return accepted

    def find_all_accepted_parts(self) -> List[Part]:
        accepted_parts: List[Part] = []
        for part in self.pile:
            accepted = self.process_part(part)
            if accepted:
                accepted_parts.append(part)
        return accepted_parts

    def sum_all_accepted_ratings(self) -> int:
        total = 0
        accepted_parts = self.find_all_accepted_parts()
        for part in accepted_parts:
            total += part.sum_ratings()
        return total

    def traverse_all_paths(self) -> List[Path]:
        final_paths: List[Path] = []
        initial_paths: List[Path] = [Path("in", 0, {"x": IntervalRange(1, 4000), "m": IntervalRange(1, 4000), "a": IntervalRange(1, 4000), "s": IntervalRange(1, 4000)})]
        while len(initial_paths):
            current_path = initial_paths.pop()
            current_workflow = self.system.get(current_path.workflow)
            if current_workflow:
                current_rule = current_workflow.rules[current_path.rule]
                category = current_rule.category
                destination = current_rule.destination
                if category == "T":
                    current_path.workflow = destination
                    current_path.rule = 0
                    initial_paths.append(current_path)
                else:
                    core_interval: IntervalRange = getattr(current_path, category)
                    breakpoint = current_rule.breakpoint
                    inequality = current_rule.inequality
                    if inequality == "<":
                        first_minimum = core_interval.minimum
                        first_maximum = breakpoint - 1
                        second_minimum = breakpoint
                        second_maximum = core_interval.maximum
                    else:
                        first_minimum = breakpoint + 1
                        first_maximum = core_interval.maximum
                        second_minimum = core_interval.minimum
                        second_maximum = breakpoint
                    first_interval = IntervalRange(first_minimum, first_maximum)
                    second_interval = IntervalRange(second_minimum, second_maximum)
                    first_workflow_name = destination
                    first_rule_index = 0
                    second_workflow_name = current_path.workflow
                    second_rule_index = current_path.rule + 1
                    current_interval_collection = {
                        "x": current_path.x,
                        "m": current_path.m,
                        "a": current_path.a,
                        "s": current_path.s
                    }
                    initial_paths.append(Path(first_workflow_name, first_rule_index, {
                        **current_interval_collection,
                        category: first_interval
                    }))
                    initial_paths.append(Path(second_workflow_name, second_rule_index, {
                        **current_interval_collection,
                        category: second_interval
                    }))
            else:
                if current_path.workflow == "A":
                    current_path.accepted = True
                    final_paths.append(current_path)
                else:
                    final_paths.append(current_path)
        return final_paths

    def count_total_accepted_ratings_combinations(self) -> int:
        total = 0
        paths = self.traverse_all_paths()
        for path in paths:
            if path.accepted:
                total += path.count_rating_combinations()
        return total


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(19, is_official)
    puzzle = Puzzle(data)
    part_1 = puzzle.sum_all_accepted_ratings()
    part_2 = puzzle.count_total_accepted_ratings_combinations()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(19, part_1, part_2, execution_time)
    return results
