import time
from typing import List
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class Conversion:
    def __init__(self, description: str) -> None:
        elements = description.split(" ")
        self.minimum = int(elements[1])
        self.maximum = self.minimum + int(elements[2]) - 1
        self.increment = (self.minimum - int(elements[0])) * -1

    def __repr__(self) -> str:
        return f"({self.minimum}, {self.maximum}): {self.increment}"


class TypeConversions:
    def __init__(self, description: str) -> None:
        elements = description.split(":\n")
        transformation_parts = elements[0].split(" ")[0].split("-to-")
        self.source = transformation_parts[0]
        self.destination = transformation_parts[1]
        self.conversions = self.determine_conversions(elements[1])

    def __repr__(self) -> str:
        return f"{self.source} -> {self.destination}\n{self.conversions}"

    def determine_conversions(self, description: str) -> List[Conversion]:
        conversion_descriptions = description.split("\n")
        conversions: List[Conversion] = []
        for conversion_description in conversion_descriptions:
            conversion = Conversion(conversion_description)
            conversions.append(conversion)
        sorted_conversions = sorted(conversions, key=lambda conversion: conversion.minimum)
        return sorted_conversions

    def convert_value(self, input: int) -> int:
        result = 0
        searched_conversions = 0
        while searched_conversions < len(self.conversions):
            for conversion in self.conversions:
                if input >= conversion.minimum and input <= conversion.maximum:
                    result = input + conversion.increment
                searched_conversions += 1
        if result == 0:
            result = input
        return result


class Almanac:
    def __init__(self, description: str) -> None:
        elements = description.split("\n\n")
        self.seeds = self.determine_seeds(elements[0])
        self.type_conversions = self.determine_type_conversions(elements[1:])

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

    def determine_locations_for_all_seeds(self) -> List[int]:
        locations: List[int] = []
        for seed in self.seeds:
            location = self.determine_location_for_seed(seed)
            locations.append(location)
        return locations

    def determine_lowest_location(self) -> int:
        locations = self.determine_locations_for_all_seeds()
        sorted_locations = sorted(locations)
        return sorted_locations[0]


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(5, is_official)
    almanac = Almanac(data)
    part_1 = almanac.determine_lowest_location()
    part_2 = 2 if data else 0
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(5, part_1, part_2, execution_time)
    return results
