import argparse
from day_1.solution import solution as solution_1
from day_2.solution import solution as solution_2
from day_3.solution import solution as solution_3
from day_4.solution import solution as solution_4
from day_5.solution import solution as solution_5
from day_6.solution import solution as solution_6
from day_7.solution import solution as solution_7
from day_8.solution import solution as solution_8
from day_9.solution import solution as solution_9
from day_10.solution import solution as solution_10
from day_11.solution import solution as solution_11
from day_12.solution import solution as solution_12
from day_13.solution import solution as solution_13
from day_14.solution import solution as solution_14
from day_15.solution import solution as solution_15
from day_16.solution import solution as solution_16
from day_17.solution import solution as solution_17
from day_18.solution import solution as solution_18
from day_19.solution import solution as solution_19
from day_20.solution import solution as solution_20
from day_21.solution import solution as solution_21
from day_22.solution import solution as solution_22
from day_23.solution import solution as solution_23
from day_24.solution import solution as solution_24
from day_25.solution import solution as solution_25


def print_solution_for_day(day: int, is_official: bool) -> None:
    solutions_mapper = {
        1: solution_1,
        2: solution_2,
        3: solution_3,
        4: solution_4,
        5: solution_5,
        6: solution_6,
        7: solution_7,
        8: solution_8,
        9: solution_9,
        10: solution_10,
        11: solution_11,
        12: solution_12,
        13: solution_13,
        14: solution_14,
        15: solution_15,
        16: solution_16,
        17: solution_17,
        18: solution_18,
        19: solution_19,
        20: solution_20,
        21: solution_21,
        22: solution_22,
        23: solution_23,
        24: solution_24,
        25: solution_25,
    }
    selected_solution = solutions_mapper.get(day, solution_1)
    result = selected_solution(is_official)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print solution for day")
    parser.add_argument("day", type=int, choices=range(1, 25 + 1), help="Select which day's solutions to display")
    parser.add_argument("is_official", choices=["True", "False"], help="Select True to work with the final data or False to work with the practice data")
    args = parser.parse_args()
    is_official = True if args.is_official == "True" else False
    print_solution_for_day(args.day, is_official)
