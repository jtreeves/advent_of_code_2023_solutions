from typing import List

numeral_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
word_digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


class NumberInLine:
    def __init__(self, value: int | str, index: int) -> None:
        self.value = value
        self.index = index

    def __repr__(self):
        return f"Value {self.value} at index {self.index}"


class SolutionResults:
    def __init__(self, part_1: int, part_2: int) -> None:
        self.part_1 = part_1
        self.part_2 = part_2

    def __repr__(self):
        return f"SOLUTIONS\nPart 1: {self.part_1}\nPart 2: {self.part_2}"


def solution(is_official: bool = True) -> SolutionResults:
    words_not_possible_calibration_sum = get_calibration_sum_based_on_word_possibility(False, is_official)
    words_possible_calibration_sum = get_calibration_sum_based_on_word_possibility(True, is_official)
    results = SolutionResults(words_not_possible_calibration_sum, words_possible_calibration_sum)
    return results


def get_calibration_sum_based_on_word_possibility(words_possible: bool, is_official: bool) -> int:
    total = 0
    part_number = 2 if words_possible else 1
    chunks = extract_data_from_file(1, part_number, is_official)
    lines = break_chunk_into_lines(chunks)
    for line in lines:
        numbers_in_line = find_all_numbers_in_line(line, words_possible)
        final_digit = combine_first_and_last_numbers_from_line_into_new_number(
            numbers_in_line)
        total += final_digit
    return total


def combine_first_and_last_numbers_from_line_into_new_number(numbers_array: List[NumberInLine]) -> int:
    first_and_last_numbers = determine_first_and_last_numbers_for_line(
        numbers_array)
    first_number = first_and_last_numbers[0]
    last_number = first_and_last_numbers[1]
    composite_string = str(first_number) + str(last_number)
    composite_number = int(composite_string)
    return composite_number


def determine_first_and_last_numbers_for_line(numbers_array: List[NumberInLine]) -> List[int]:
    sorted_substrings = sorted(numbers_array, key=lambda x: x.index)
    first_number_obj = sorted_substrings[0]
    last_number_obj = sorted_substrings[-1]
    first_number = int(first_number_obj.value if str(first_number_obj.value).isdigit(
    ) else convert_string_to_number(str(first_number_obj.value)))
    last_number = int(last_number_obj.value if str(last_number_obj.value).isdigit(
    ) else convert_string_to_number(str(last_number_obj.value)))
    return [first_number, last_number]


def convert_string_to_number(digit: str) -> int:
    index = word_digits.index(digit)
    value = index + 1
    return value


def find_all_numbers_in_line(line: str, words_possible: bool) -> List[NumberInLine]:
    numbers_in_line: List[NumberInLine] = []
    digits = numeral_digits + word_digits if words_possible else numeral_digits
    for digit in digits:
        index = line.find(str(digit))
        while index != -1:
            number_in_line = NumberInLine(digit, index)
            numbers_in_line.append(number_in_line)
            index = line.find(str(digit), index + 1)
    return numbers_in_line


def break_chunk_into_lines(chunk: str) -> List[str]:
    lines = chunk.split("\n")
    return lines


def extract_data_from_file(day_number: int, part_number: int, is_official: bool) -> str:
    name = "data" if is_official else f"practice_{part_number}"
    file = open(f"day_{day_number}/{name}.txt", "r")
    data = file.read()
    file.close()
    return data


result = solution()
print(result)
