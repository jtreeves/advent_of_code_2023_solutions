from typing import List


class BlockDetail:
    def __init__(self, color: str, count: int) -> None:
        self.color = color
        self.count = count


class GameInfo:
    def __init__(self, id: int, scenarios: List[List[BlockDetail]]) -> None:
        self.id = id
        self.scenarios = scenarios

    def calculate_power_of_game(self) -> int:
        power = 1
        color_counts = self.determine_minimum_blocks_required_across_all_scenarios()
        for color_count in color_counts:
            power *= color_count.count
        return power

    def determine_minimum_blocks_required_across_all_scenarios(self) -> List[BlockDetail]:
        max_red = 0
        max_green = 0
        max_blue = 0
        for scenario in self.scenarios:
            for block_details in scenario:
                if block_details.color == "red" and block_details.count > max_red:
                    max_red = block_details.count
                if block_details.color == "green" and block_details.count > max_green:
                    max_green = block_details.count
                if block_details.color == "blue" and block_details.count > max_blue:
                    max_blue = block_details.count
        minimum_blocks_required = [
            BlockDetail("red", max_red),
            BlockDetail("green", max_green),
            BlockDetail("blue", max_blue),
        ]
        return minimum_blocks_required

    def get_game_id_if_all_scenarios_possible(self, color_count_rules: List[BlockDetail]) -> int:
        game_id = self.id
        if self.check_if_any_maximum_exceeded_in_scenarios(color_count_rules):
            game_id = 0
        return game_id

    def check_if_any_maximum_exceeded_in_scenarios(self, color_count_rules: List[BlockDetail]) -> bool:
        exceeded = False
        for scenario in self.scenarios:
            for color_count_pair in color_count_rules:
                if self.check_if_maximum_exceeded_in_scenario(scenario, color_count_pair.color, color_count_pair.count):
                    exceeded = True
        return exceeded

    def check_if_maximum_exceeded_in_scenario(self, scenario: List[BlockDetail], color: str, max: int) -> bool:
        exceeded = False
        for block_detail in scenario:
            if block_detail.color == color:
                if block_detail.count > max:
                    exceeded = True
        return exceeded


class SolutionResults:
    def __init__(self, part_1: int, part_2: int) -> None:
        self.part_1 = part_1
        self.part_2 = part_2

    def __repr__(self):
        return f"SOLUTIONS\nPart 1: {self.part_1}\nPart 2: {self.part_2}"


def solution() -> SolutionResults:
    data = extract_data_from_file()
    games = list_games(data)
    info_for_all_games = compile_info_for_all_games(games)
    id_sum = sum_all_ids_possible_with_rules(info_for_all_games)
    power_sum = sum_powers_of_all_games(info_for_all_games)
    results = SolutionResults(id_sum, power_sum)
    return results


def sum_powers_of_all_games(all_game_infos: List[GameInfo]) -> int:
    power_sum = 0
    for game_info in all_game_infos:
        game_power = game_info.calculate_power_of_game()
        power_sum += game_power
    return power_sum


def sum_all_ids_possible_with_rules(all_game_infos: List[GameInfo]) -> int:
    id_sum = 0
    rules = [BlockDetail("red", 12), BlockDetail("green", 13), BlockDetail("blue", 14)]
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


def determine_block_scenarios_for_game(collected_sets: str) -> List[List[BlockDetail]]:
    sets = collected_sets.split("; ")
    block_scenarios: List[List[BlockDetail]] = []
    for single_set in sets:
        block_details = determine_block_details_for_scenario(single_set)
        block_scenarios.append(block_details)
    return block_scenarios


def determine_block_details_for_scenario(single_set: str) -> List[BlockDetail]:
    cubes = single_set.split(", ")
    block_details: List[BlockDetail] = []
    for cube_description in cubes:
        cube_pieces = cube_description.split(" ")
        color = cube_pieces[1]
        count = int(cube_pieces[0])
        block_detail = BlockDetail(color, count)
        block_details.append(block_detail)
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


def extract_data_from_file() -> str:
    file = open("data.txt", "r")
    data = file.read()
    file.close()
    return data


result = solution()
print(result)
