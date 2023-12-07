import time
from typing import List
from utils.extract_data_from_file import extract_data_from_file
from utils.get_list_of_lines import get_list_of_lines
from utils.SolutionResults import SolutionResults

card_orders = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


class Hand:
    def __init__(self, description: str) -> None:
        elements = description.split(" ")
        self.cards = elements[0]
        self.bid = int(elements[1])
        self.value = self.calculate_value()

    def __repr__(self) -> str:
        return f"{self.cards}: {self.bid} -> {self.value}"

    def calculate_value(self) -> int:
        value = 0
        sorted_cards = sorted(self.cards)
        matches: dict[str, int] = {}
        for index in range(len(sorted_cards) - 1):
            if sorted_cards[index] == sorted_cards[index + 1]:
                card = sorted_cards[index]
                if matches.get(card):
                    matches[card] += 1
                else:
                    matches[card] = 2
        if len(matches.items()) == 0:
            value = 1
        else:
            for inner_value in matches.values():
                value += inner_value ** inner_value
        return value


class CardSet:
    def __init__(self, description: str) -> None:
        self.hands = self.determine_hands(description)

    def __repr__(self) -> str:
        description = ""
        for hand in self.hands:
            description += f"{hand.cards}: {hand.bid} -> {hand.value}\n"
        return description

    def determine_hands(self, description: str) -> List[Hand]:
        hands: List[Hand] = []
        inputs = get_list_of_lines(description)
        for input in inputs:
            hand = Hand(input)
            hands.append(hand)
        return hands

    def order_hands(self) -> List[Hand]:
        return sorted(self.hands, key=lambda x: (x.value, card_orders.index(x.cards[0]), card_orders.index(x.cards[1]), card_orders.index(x.cards[2]), card_orders.index(x.cards[3]), card_orders.index(x.cards[4])))

    def calculate_winnings(self) -> int:
        winnings = 0
        ordered_hands = self.order_hands()
        for index in range(len(ordered_hands)):
            winnings += (index + 1) * ordered_hands[index].bid
        return winnings


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(7, is_official)
    cards = CardSet(data)
    part_1 = cards.calculate_winnings()
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(7, part_1, part_2, execution_time)
    return results
