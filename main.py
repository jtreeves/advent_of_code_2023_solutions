import argparse
from datetime import date
from day_1.solution import solve_problem as solve_1
from day_2.solution import solve_problem as solve_2
from day_3.solution import solve_problem as solve_3
from day_4.solution import solve_problem as solve_4
from day_5.solution import solve_problem as solve_5
from day_6.solution import solve_problem as solve_6
from day_7.solution import solve_problem as solve_7
from day_8.solution import solve_problem as solve_8
from day_9.solution import solve_problem as solve_9
from day_10.solution import solve_problem as solve_10
from day_11.solution import solve_problem as solve_11
from day_12.solution import solve_problem as solve_12
from day_13.solution import solve_problem as solve_13
from day_14.solution import solve_problem as solve_14
from day_15.solution import solve_problem as solve_15
from day_16.solution import solve_problem as solve_16
from day_17.solution import solve_problem as solve_17
from day_18.solution import solve_problem as solve_18
from day_19.solution import solve_problem as solve_19
from day_20.solution import solve_problem as solve_20
from day_21.solution import solve_problem as solve_21
from day_22.solution import solve_problem as solve_22
from day_23.solution import solve_problem as solve_23
from day_24.solution import solve_problem as solve_24
from day_25.solution import solve_problem as solve_25

solve_functions_mapper = {
    1: solve_1,
    2: solve_2,
    3: solve_3,
    4: solve_4,
    5: solve_5,
    6: solve_6,
    7: solve_7,
    8: solve_8,
    9: solve_9,
    10: solve_10,
    11: solve_11,
    12: solve_12,
    13: solve_13,
    14: solve_14,
    15: solve_15,
    16: solve_16,
    17: solve_17,
    18: solve_18,
    19: solve_19,
    20: solve_20,
    21: solve_21,
    22: solve_22,
    23: solve_23,
    24: solve_24,
    25: solve_25,
}


def print_solution_for_day(day: int, is_official: bool) -> None:
    selected_solve_function = solve_functions_mapper.get(day, solve_1)
    solution = selected_solve_function(is_official)
    print(solution)


def print_solutions_for_all_active_days(is_official: bool) -> None:
    current_date = date.today()
    current_day = current_date.day
    all_days = sorted(solve_functions_mapper.keys())
    active_days = all_days[:current_day]
    for day in active_days:
        print_solution_for_day(day, is_official)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print solution for day")
    parser.add_argument("day", type=int, choices=range(1, 25 + 1), nargs="?", default=0, help="Select which day's solutions to display")
    parser.add_argument("is_official", choices=["True", "False"], nargs="?", default="True", help="Select True to work with the final data or False to work with the practice data")
    args = parser.parse_args()
    is_official = True if args.is_official == "True" else False
    day = args.day
    if day:
        print_solution_for_day(day, is_official)
    else:
        print_solutions_for_all_active_days(is_official)
