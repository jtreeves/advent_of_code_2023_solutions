import time
from typing import List
from utils.extract_data_from_file import extract_data_from_file
from utils.get_list_of_lines import get_list_of_lines
from utils.SolutionResults import SolutionResults

plain_card_orders = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
joker_card_orders = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


class Hand:
    def __init__(self, description: str) -> None:
        elements = description.split(" ")
        self.cards = elements[0]
        self.bid = int(elements[1])
        self.value = self.calculate_value()
        self.joker_value = self.calculate_value_with_jokers()

    def __repr__(self) -> str:
        return f"{self.cards}: {self.bid} -> {self.value}"

    def calculate_value(self) -> int:
        matches = self.determine_matches()
        value = self.calculate_final_value(matches)
        return value

    def calculate_value_with_jokers(self) -> int:
        matches = self.determine_matches()
        if "J" in self.cards:
            if len(matches.items()) == 0:
                matches["J"] = 2
            else:
                if not matches.get("J"):
                    temp_key = ""
                    temp_value = 0
                    for [k, v] in matches.items():
                        if v > temp_value:
                            temp_value = v
                            temp_key = k
                    highest_match = temp_value + 1
                    matches[temp_key] = highest_match
                else:
                    if len(matches.items()) == 1:
                        if matches["J"] != 5:
                            matches["J"] += 1
                    else:
                        temp_key = ""
                        temp_value = 0
                        for [k, v] in matches.items():
                            if v > temp_value and k != "J":
                                temp_value = v
                                temp_key = k
                        highest_match = temp_value + matches["J"]
                        matches[temp_key] = highest_match
                        del matches["J"]
        value = self.calculate_final_value(matches)
        return value

    def determine_matches(self) -> dict[str, int]:
        sorted_cards = sorted(self.cards)
        matches: dict[str, int] = {}
        for index in range(len(sorted_cards) - 1):
            if sorted_cards[index] == sorted_cards[index + 1]:
                card = sorted_cards[index]
                if matches.get(card):
                    matches[card] += 1
                else:
                    matches[card] = 2
        return matches

    def calculate_final_value(self, matches: dict[str, int]) -> int:
        value = 0
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

    def order_hands(self, with_jokers: bool) -> List[Hand]:
        card_orders = plain_card_orders if not with_jokers else joker_card_orders
        ordered_hands = sorted(self.hands, key=lambda x: (x.value if not with_jokers else x.joker_value, card_orders.index(x.cards[0]), card_orders.index(x.cards[1]), card_orders.index(x.cards[2]), card_orders.index(x.cards[3]), card_orders.index(x.cards[4])))
        return ordered_hands

    def calculate_winnings(self, with_jokers: bool) -> int:
        winnings = 0
        ordered_hands = self.order_hands_without_jokers() if not with_jokers else self.order_hands_with_jokers()
        for index in range(len(ordered_hands)):
            winnings += (index + 1) * ordered_hands[index].bid
        return winnings

    def order_hands_without_jokers(self) -> List[Hand]:
        return self.order_hands(False)

    def order_hands_with_jokers(self) -> List[Hand]:
        return self.order_hands(True)

    def calculate_winnings_without_jokers(self) -> int:
        return self.calculate_winnings(False)

    def calculate_winnings_with_jokers(self) -> int:
        return self.calculate_winnings(True)


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(7, is_official)
    cards = CardSet(data)
    part_1 = cards.calculate_winnings_without_jokers()
    part_2 = cards.calculate_winnings_with_jokers()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(7, part_1, part_2, execution_time)
    return results
