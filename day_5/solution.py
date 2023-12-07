import time
from typing import List
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class ReverseConversion:
    def __init__(self, description: str, minimum: int | float = 0, maximum: int | float = 0, increment: int = 0) -> None:
        if description:
            elements = description.split(" ")
            self.minimum = int(elements[0])
            self.maximum = self.minimum + int(elements[2]) - 1
            self.increment = int(elements[1]) - self.minimum
        else:
            self.minimum = minimum
            self.maximum = maximum
            self.increment = increment


class Conversion:
    def __init__(self, description: str, minimum: int | float = 0, maximum: int | float = 0, increment: int = 0) -> None:
        if description:
            elements = description.split(" ")
            self.minimum = int(elements[1])
            self.maximum = self.minimum + int(elements[2]) - 1
            self.increment = (self.minimum - int(elements[0])) * -1
        else:
            self.minimum = minimum
            self.maximum = maximum
            self.increment = increment

    def __repr__(self) -> str:
        return f"({self.minimum}, {self.maximum}): {self.increment}"

    def __hash__(self) -> int:
        return hash((self.minimum, self.maximum, self.increment))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Conversion):
            if (self.minimum == other.minimum or self.maximum == other.maximum) and self.increment == other.increment:
                return True
            else:
                return False
        else:
            return False


class TypeConversions:
    def __init__(self, description: str) -> None:
        elements = description.split(":\n")
        transformation_parts = elements[0].split(" ")[0].split("-to-")
        self.source = transformation_parts[0]
        self.destination = transformation_parts[1]
        self.conversions = self.determine_conversions(elements[1])
        self.reverse_conversions = self.determine_reverse_conversions(elements[1])

    def __repr__(self) -> str:
        return f"{self.source} -> {self.destination}\n{self.conversions}"

    def determine_conversions(self, description: str) -> List[Conversion]:
        conversion_descriptions = description.split("\n")
        conversions: List[Conversion] = []
        for conversion_description in conversion_descriptions:
            conversion = Conversion(conversion_description)
            conversions.append(conversion)
        sorted_conversions = sorted(conversions, key=lambda conversion: conversion.minimum)
        conversions_with_gaps_filled = self.fill_gaps(sorted_conversions)
        return conversions_with_gaps_filled

    def determine_reverse_conversions(self, description: str) -> List[ReverseConversion]:
        conversion_descriptions = description.split("\n")
        conversions: List[ReverseConversion] = []
        for conversion_description in conversion_descriptions:
            conversion = ReverseConversion(conversion_description)
            conversions.append(conversion)
        sorted_conversions = sorted(conversions, key=lambda conversion: conversion.minimum)
        conversions_with_gaps_filled = self.reverse_fill_gaps(sorted_conversions)
        return conversions_with_gaps_filled

    def convert_value(self, input: int) -> int:
        result = 0
        searched_conversions = 0
        while searched_conversions < len(self.conversions):
            for conversion in self.conversions:
                if input >= conversion.minimum and input <= conversion.maximum:
                    result = input + conversion.increment
                searched_conversions += 1
        return result

    def reverse_convert_value(self, input: int) -> int:
        result = 0
        searched_conversions = 0
        while searched_conversions < len(self.reverse_conversions):
            for conversion in self.reverse_conversions:
                if input >= conversion.minimum and input <= conversion.maximum:
                    result = input + conversion.increment
                searched_conversions += 1
        return result

    def fill_gaps(self, initial_conversions: List[Conversion]) -> List[Conversion]:
        final_conversions: List[Conversion] = [Conversion('', float('-inf'), initial_conversions[0].minimum - 1, 0)]
        for i in range(len(initial_conversions) - 1):
            current_conversion = initial_conversions[i]
            next_conversion = initial_conversions[i + 1]
            final_conversions.append(current_conversion)
            if current_conversion.maximum < next_conversion.minimum - 1:
                final_conversions.append(Conversion('', current_conversion.maximum + 1, next_conversion.minimum - 1))
        final_conversions.append(initial_conversions[-1])
        final_conversions.append(Conversion('', initial_conversions[-1].maximum + 1, float('inf')))
        return final_conversions

    def reverse_fill_gaps(self, initial_conversions: List[ReverseConversion]) -> List[ReverseConversion]:
        final_conversions: List[ReverseConversion] = [ReverseConversion('', float('-inf'), initial_conversions[0].minimum - 1, 0)]
        for i in range(len(initial_conversions) - 1):
            current_conversion = initial_conversions[i]
            next_conversion = initial_conversions[i + 1]
            final_conversions.append(current_conversion)
            if current_conversion.maximum < next_conversion.minimum - 1:
                final_conversions.append(ReverseConversion('', current_conversion.maximum + 1, next_conversion.minimum - 1))
        final_conversions.append(initial_conversions[-1])
        final_conversions.append(ReverseConversion('', initial_conversions[-1].maximum + 1, float('inf')))
        return final_conversions


class Almanac:
    def __init__(self, description: str) -> None:
        elements = description.split("\n\n")
        self.seeds = self.determine_seeds(elements[0])
        self.type_conversions = self.determine_type_conversions(elements[1:])
        self.seed_ranges_checked: dict[str, int] = {}

    def __repr__(self) -> str:
        description = f"{self.seeds}\n\n"
        for conversion in self.type_conversions.values():
            description += f"{conversion}\n\n"
        return description

    def determine_seeds(self, description: str) -> List[int]:
        sections = description.split(": ")
        seeds: List[int] = []
        for part in sections[1].split(" "):
            seed = int(part)
            seeds.append(seed)
        return seeds

    def determine_type_conversions(self, elements: List[str]) -> dict[str, TypeConversions]:
        type_conversions: dict[str, TypeConversions] = {}
        for element in elements:
            conversion = TypeConversions(element)
            type_conversions[conversion.source] = conversion
        return type_conversions

    def determine_location_for_seed(self, seed: int) -> int:
        soil = self.type_conversions["seed"].convert_value(seed)
        fertilizer = self.type_conversions["soil"].convert_value(soil)
        water = self.type_conversions["fertilizer"].convert_value(fertilizer)
        light = self.type_conversions["water"].convert_value(water)
        temperature = self.type_conversions["light"].convert_value(light)
        humidity = self.type_conversions["temperature"].convert_value(temperature)
        location = self.type_conversions["humidity"].convert_value(humidity)
        return location

    def determine_locations_for_all_seeds(self, seeds: List[int]) -> List[int]:
        locations: List[int] = []
        for seed in seeds:
            location = self.determine_location_for_seed(seed)
            locations.append(location)
        return locations

    def determine_lowest_location(self, seeds: List[int]) -> int:
        locations = self.determine_locations_for_all_seeds(seeds)
        sorted_locations = sorted(locations)
        return sorted_locations[0]

    def find_all_seed_ranges(self) -> List[List[int]]:
        seed_ranges: List[List[int]] = []
        for index in range(len(self.seeds) - 1):
            if index % 2 == 0:
                seed_ranges.append([self.seeds[index], self.seeds[index] + self.seeds[index + 1] - 1])
        sorted_ranges = sorted(seed_ranges, key=lambda range: range[0])
        return sorted_ranges

    def get_seed_from_location(self, location: int) -> int:
        humidity = self.type_conversions["humidity"].reverse_convert_value(location)
        temperature = self.type_conversions["temperature"].reverse_convert_value(humidity)
        light = self.type_conversions["light"].reverse_convert_value(temperature)
        water = self.type_conversions["water"].reverse_convert_value(light)
        fertilizer = self.type_conversions["fertilizer"].reverse_convert_value(water)
        soil = self.type_conversions["soil"].reverse_convert_value(fertilizer)
        seed = self.type_conversions["seed"].reverse_convert_value(soil)
        return seed

    def find_lowest_location_for_existing_seeds(self) -> int:
        seed_ranges = self.find_all_seed_ranges()
        location = 0
        found_seed = False
        while not found_seed:
            location += 1
            matching_seed = self.get_seed_from_location(location)
            for seed_range in seed_ranges:
                if matching_seed in range(seed_range[0], seed_range[1]):
                    found_seed = True
        return location


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(5, is_official)
    almanac = Almanac(data)
    part_1 = almanac.determine_lowest_location(almanac.seeds)
    part_2 = almanac.find_lowest_location_for_existing_seeds()
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(5, part_1, part_2, execution_time)
    return results
