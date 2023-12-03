from typing import List
import time


class Scenario:
    def __init__(self, red_value: int, green_value: int, blue_value: int) -> None:
        self.red = red_value
        self.green = green_value
        self.blue = blue_value


class GameInfo:
    def __init__(self, id: int, scenarios: List[Scenario]) -> None:
        self.id = id
        self.scenarios = scenarios

    def calculate_power_of_game(self) -> int:
        power = 1
        color_counts = self.determine_minimum_blocks_required_across_all_scenarios()
        for value in color_counts.__dict__.values():
            power *= value
        return power

    def determine_minimum_blocks_required_across_all_scenarios(self) -> Scenario:
        max_red = 0
        max_green = 0
        max_blue = 0
        for scenario in self.scenarios:
            if scenario.red > max_red:
                max_red = scenario.red
            if scenario.green > max_green:
                max_green = scenario.green
            if scenario.blue > max_blue:
                max_blue = scenario.blue
        minimum_blocks_required = Scenario(max_red, max_green, max_blue)
        return minimum_blocks_required

    def get_game_id_if_all_scenarios_possible(self, color_count_rules: Scenario) -> int:
        game_id = self.id
        if self.check_if_any_maximum_exceeded_in_scenarios(color_count_rules):
            game_id = 0
        return game_id

    def check_if_any_maximum_exceeded_in_scenarios(self, color_count_rules: Scenario) -> bool:
        exceeded = False
        for scenario in self.scenarios:
            for attr, value in color_count_rules.__dict__.items():
                if self.check_if_maximum_exceeded_in_scenario(scenario, attr, value):
                    exceeded = True
        return exceeded

    def check_if_maximum_exceeded_in_scenario(self, scenario: Scenario, color: str, max: int) -> bool:
        color_count_in_scenario = getattr(scenario, color)
        exceeded = color_count_in_scenario > max
        return exceeded


class SolutionResults:
    def __init__(self, part_1: int, part_2: int, execution_time: float) -> None:
        self.part_1 = part_1
        self.part_2 = part_2
        self.execution_time = execution_time

    def __repr__(self):
        return f"SOLUTIONS\nPart 1: {self.part_1}\nPart 2: {self.part_2}\nTotal execution time: {self.execution_time} seconds"


def solution(is_official: bool = True) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(2, is_official)
    games = list_games(data)
    info_for_all_games = compile_info_for_all_games(games)
    id_sum = sum_all_ids_possible_with_rules(info_for_all_games)
    power_sum = sum_powers_of_all_games(info_for_all_games)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(id_sum, power_sum, execution_time)
    return results


def sum_powers_of_all_games(all_game_infos: List[GameInfo]) -> int:
    power_sum = 0
    for game_info in all_game_infos:
        game_power = game_info.calculate_power_of_game()
        power_sum += game_power
    return power_sum


def sum_all_ids_possible_with_rules(all_game_infos: List[GameInfo]) -> int:
    id_sum = 0
    rules = Scenario(12, 13, 14)
    for game_info in all_game_infos:
        game_id = game_info.get_game_id_if_all_scenarios_possible(rules)
        id_sum += game_id
    return id_sum


def compile_info_for_all_games(games: List[str]) -> List[GameInfo]:
    all_info: List[GameInfo] = []
    for game in games:
        game_info = compile_game_info(game)
        all_info.append(game_info)
    return all_info


def compile_game_info(game: str) -> GameInfo:
    main_sections = separate_description_from_sets(game)
    game_id = determine_game_id(main_sections[0])
    game_scenarios = determine_block_scenarios_for_game(main_sections[1])
    game_info = GameInfo(game_id, game_scenarios)
    return game_info


def determine_block_scenarios_for_game(collected_sets: str) -> List[Scenario]:
    sets = collected_sets.split("; ")
    block_scenarios: List[Scenario] = []
    for single_set in sets:
        block_details = determine_block_details_for_scenario(single_set)
        block_scenarios.append(block_details)
    return block_scenarios


def determine_block_details_for_scenario(single_set: str) -> Scenario:
    cubes = single_set.split(", ")
    red_count = 0
    green_count = 0
    blue_count = 0
    for cube_description in cubes:
        cube_pieces = cube_description.split(" ")
        color = cube_pieces[1]
        count = int(cube_pieces[0])
        if color == "red":
            red_count = count
        elif color == "green":
            green_count = count
        elif color == "blue":
            blue_count = count
    block_details = Scenario(red_count, green_count, blue_count)
    return block_details


def determine_game_id(description: str) -> int:
    description_sections = description.split(" ")
    game_id = int(description_sections[1])
    return game_id


def separate_description_from_sets(game: str) -> List[str]:
    main_sections = game.split(": ")
    return main_sections


def list_games(data: str) -> List[str]:
    games = data.split("\n")
    return games


def extract_data_from_file(day_number: int, is_official: bool) -> str:
    name = "data" if is_official else "practice"
    file = open(f"day_{day_number}/{name}.txt", "r")
    data = file.read()
    file.close()
    return data


result = solution()
print(result)
