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
        self.destination = elements[1]
        self.evaluation = self.create_evaluation(expression)

    def create_evaluation(self, expression: str) -> Callable[[int], bool]:
        if expression != "True":
            return lambda x: eval(expression, {"x": x, "m": x, "a": x, "s": x})
        else:
            return lambda x: True


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


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(19, is_official)
    puzzle = Puzzle(data)
    part_1 = puzzle.sum_all_accepted_ratings()
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(19, part_1, part_2, execution_time)
    return results
