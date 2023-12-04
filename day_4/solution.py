import time
from typing import List
from utils.get_list_of_lines import get_list_of_lines
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Card:
    def __init__(self, description: str) -> None:
        initial_sections = description.split(":")
        number_sections = initial_sections[1].split("|")
        self.id = self.determine_id(initial_sections[0])
        self.winning_numbers = self.determine_numbers_list(number_sections[0])
        self.provided_numbers = self.determine_numbers_list(number_sections[1])
        self.matches = self.determine_matches()
        self.points = self.calculate_points()

    def __repr__(self) -> str:
        return f"Card {self.id}: {self.winning_numbers} | {self.provided_numbers} -> {self.matches} matches and {self.points} points"

    def determine_id(self, introduction: str) -> int:
        string_id = introduction.split()[1]
        id = int(string_id)
        return id

    def determine_numbers_list(self, raw_numbers: str) -> List[int]:
        string_numbers = raw_numbers.split(" ")
        numbers_list = list(map(int, filter(lambda x: x != "", string_numbers)))
        return numbers_list

    def determine_matches(self) -> int:
        matches = 0
        for provided_number in self.provided_numbers:
            if provided_number in self.winning_numbers:
                matches += 1
        return matches

    def calculate_points(self) -> int:
        if self.matches > 0:
            points = 2**(self.matches - 1)
        else:
            points = 0
        return points

    def determine_ids_of_copies(self) -> List[int]:
        ids: List[int] = []
        for value in range(self.matches):
            ids.append(self.id + value + 1)
        return ids


class Pile:
    def __init__(self, description: str) -> None:
        self.cards = self.create_cards(description)
        self.card_counts = self.initialize_counts_of_cards()
        self.total_points = self.calculate_total_points()

    def __repr__(self) -> str:
        representation = ""
        for card in self.cards:
            representation += card.__repr__() + "\n"
        representation += f"TOTAL POINTS: {self.total_points}"
        return f"{representation}"

    def create_cards(self, description: str) -> List[Card]:
        card_descriptions = get_list_of_lines(description)
        cards: List[Card] = []
        for card_description in card_descriptions:
            card = Card(card_description)
            cards.append(card)
        return cards

    def calculate_total_points(self) -> int:
        total_points = 0
        for card in self.cards:
            total_points += card.points
        return total_points

    def initialize_counts_of_cards(self) -> dict[int, int]:
        card_counts: dict[int, int] = {}
        for card in self.cards:
            card_counts[card.id] = 1
        return card_counts

    def increment_card_counts_iteratively(self) -> None:
        for card in self.cards:
            ids_of_copies = card.determine_ids_of_copies()
            for id in ids_of_copies:
                self.card_counts[id] += self.card_counts[card.id]

    def determine_total_card_count(self) -> int:
        total = 0
        for value in self.card_counts.values():
            total += value
        return total


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(4, is_official)
    pile = Pile(data)
    pile.increment_card_counts_iteratively()
    part_1 = pile.total_points
    part_2 = pile.determine_total_card_count()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(4, part_1, part_2, execution_time)
    return results
