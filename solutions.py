import argparse
from day_1.solution import solution as solution_1
from day_2.solution import solution as solution_2


def print_solution_for_day(day: int, is_official: bool) -> None:
    solutions = {
        1: solution_1,
        2: solution_2
    }
    selected_solution = solutions.get(day, solution_1)
    result = selected_solution(is_official)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print solution for day")
    parser.add_argument("day", type=int, choices=range(1, 26), help="Select which day's solutions to display")
    parser.add_argument("is_official", choices=["True", "False"], help="Select True to work with the final data or False to work with the practice data")
    args = parser.parse_args()
    is_official = True if args.is_official == "True" else False
    print_solution_for_day(args.day, is_official)
