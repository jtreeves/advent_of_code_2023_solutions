import time
from typing import List
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


class ReverseConversion:
    def __init__(self, description: str) -> None:
        elements = description.split(" ")
        self.minimum = int(elements[0])
        self.maximum = self.minimum + int(elements[2]) - 1
        self.increment = int(elements[0]) - self.minimum


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

    def convert_value(self, input: int) -> int:
        result = 0
        searched_conversions = 0
        while searched_conversions < len(self.conversions):
            for conversion in self.conversions:
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

    def get_reversal_for_conversion(self, conversion: Conversion) -> Conversion:
        reversed_minimum = conversion.minimum + conversion.increment
        reversed_maximum = conversion.maximum + conversion.increment
        reversed_increment = conversion.increment * -1
        reversal = Conversion('', reversed_minimum, reversed_maximum, reversed_increment)
        return reversal


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

    def determine_seeds_by_pairs(self) -> List[int]:
        seeds: List[int] = []
        for index in range(len(self.seeds) - 1):
            if index % 2 == 0:
                for sub_index in range(self.seeds[index + 1]):
                    seeds.append(self.seeds[index] + sub_index)
        return seeds

    def find_all_seed_ranges(self) -> List[List[int]]:
        seed_ranges: List[List[int]] = []
        for index in range(len(self.seeds) - 1):
            if index % 2 == 0:
                seed_ranges.append([self.seeds[index], self.seeds[index] + self.seeds[index + 1] - 1])
        sorted_ranges = sorted(seed_ranges, key=lambda range: range[0])
        return sorted_ranges

    def find_seed_ranges_matching_location_range(self, location_range: Conversion) -> List[Conversion]:
        initial_humidity_range = self.type_conversions["humidity"].get_reversal_for_conversion(location_range)
        final_humidity_ranges: List[Conversion] = []
        for conversion in self.type_conversions["temperature"].conversions:
            if (initial_humidity_range.minimum >= conversion.minimum and initial_humidity_range.minimum <= conversion.maximum) or (initial_humidity_range.maximum <= conversion.maximum and initial_humidity_range.maximum >= conversion.minimum):
                final_humidity_ranges.append(Conversion('', max(conversion.minimum, initial_humidity_range.minimum), min(conversion.maximum, initial_humidity_range.maximum), conversion.increment))
        initial_temperature_ranges: List[Conversion] = []
        for humidity_range in final_humidity_ranges:
            initial_temperature_range = self.type_conversions["temperature"].get_reversal_for_conversion(humidity_range)
            initial_temperature_ranges.append(initial_temperature_range)
        final_temperature_ranges: List[Conversion] = []
        for temperature_range in initial_temperature_ranges:
            for conversion in self.type_conversions["light"].conversions:
                if (temperature_range.minimum >= conversion.minimum and temperature_range.minimum <= conversion.maximum) or (temperature_range.maximum <= conversion.maximum and temperature_range.maximum >= conversion.minimum):
                    final_temperature_ranges.append(Conversion('', max(conversion.minimum, temperature_range.minimum), min(conversion.maximum, temperature_range.maximum), conversion.increment))
        initial_light_ranges: List[Conversion] = []
        for temperature_range in final_temperature_ranges:
            initial_light_range = self.type_conversions["light"].get_reversal_for_conversion(temperature_range)
            initial_light_ranges.append(initial_light_range)
        final_light_ranges: List[Conversion] = []
        for light_range in initial_light_ranges:
            for conversion in self.type_conversions["water"].conversions:
                if (light_range.minimum >= conversion.minimum and light_range.minimum <= conversion.maximum) or (light_range.maximum <= conversion.maximum and light_range.maximum >= conversion.minimum):
                    final_light_ranges.append(Conversion('', max(conversion.minimum, light_range.minimum), min(conversion.maximum, light_range.maximum), conversion.increment))
        initial_water_ranges: List[Conversion] = []
        for light_range in final_light_ranges:
            initial_water_range = self.type_conversions["water"].get_reversal_for_conversion(light_range)
            initial_water_ranges.append(initial_water_range)
        final_water_ranges: List[Conversion] = []
        for water_range in initial_water_ranges:
            for conversion in self.type_conversions["fertilizer"].conversions:
                if (water_range.minimum >= conversion.minimum and water_range.minimum <= conversion.maximum) or (water_range.maximum <= conversion.maximum and water_range.maximum >= conversion.minimum):
                    final_water_ranges.append(Conversion('', max(conversion.minimum, water_range.minimum), min(conversion.maximum, water_range.maximum), conversion.increment))
        initial_fertilizer_ranges: List[Conversion] = []
        for water_range in final_water_ranges:
            initial_fertilizer_range = self.type_conversions["fertilizer"].get_reversal_for_conversion(water_range)
            initial_fertilizer_ranges.append(initial_fertilizer_range)
        final_fertilizer_ranges: List[Conversion] = []
        for fertilizer_range in initial_fertilizer_ranges:
            for conversion in self.type_conversions["soil"].conversions:
                if (fertilizer_range.minimum >= conversion.minimum and fertilizer_range.minimum <= conversion.maximum) or (fertilizer_range.maximum <= conversion.maximum and fertilizer_range.maximum >= conversion.minimum):
                    final_fertilizer_ranges.append(Conversion('', max(conversion.minimum, fertilizer_range.minimum), min(conversion.maximum, fertilizer_range.maximum), conversion.increment))
        initial_soil_ranges: List[Conversion] = []
        for fertilizer_range in final_fertilizer_ranges:
            initial_soil_range = self.type_conversions["soil"].get_reversal_for_conversion(fertilizer_range)
            initial_soil_ranges.append(initial_soil_range)
        final_soil_ranges: List[Conversion] = []
        for soil_range in initial_soil_ranges:
            for conversion in self.type_conversions["seed"].conversions:
                if (soil_range.minimum >= conversion.minimum and soil_range.minimum <= conversion.maximum) or (soil_range.maximum <= conversion.maximum and soil_range.maximum >= conversion.minimum):
                    final_soil_ranges.append(Conversion('', max(conversion.minimum, soil_range.minimum), min(conversion.maximum, soil_range.maximum), conversion.increment))
        seed_ranges: List[Conversion] = []
        for soil_range in final_soil_ranges:
            seed_range = self.type_conversions["seed"].get_reversal_for_conversion(soil_range)
            seed_ranges.append(seed_range)
        unique_seed_ranges = list(set(seed_ranges))
        sorted_seed_ranges = sorted(unique_seed_ranges, key=lambda conversion: conversion.minimum)
        return sorted_seed_ranges

    def determine_minimum_location_for_seed_range(self, seed_min: int, seed_max: int) -> int:
        possible_minima: List[int] = []
        if seed_min == seed_max:
            possible_minimum = self.determine_location_for_seed(seed_min)
            possible_minima.append(possible_minimum)
        for seed_index in range(seed_min, seed_max):
            possible_minimum = self.determine_location_for_seed(seed_index)
            possible_minima.append(possible_minimum)
        sorted_minima = sorted(possible_minima)
        return sorted_minima[0]

    def determine_minimum_location_based_on_location_ranges(self, location_ranges: List[Conversion]) -> int:
        possible_minima: List[int] = []
        searched_ranges = 0
        all_seed_ranges = self.find_all_seed_ranges()
        while searched_ranges < len(location_ranges):
            for location_range in location_ranges:
                searched_ranges += 1
                seed_ranges = self.find_seed_ranges_matching_location_range(location_range)
                for seed_range in seed_ranges:
                    for possible_seed_range in all_seed_ranges:
                        if (possible_seed_range[0] >= seed_range.minimum and possible_seed_range[0] <= seed_range.maximum) or (possible_seed_range[1] >= seed_range.minimum and possible_seed_range[1] <= seed_range.maximum):
                            potential_range = [max(int(seed_range.minimum) if seed_range.minimum != float('-inf') else 0, possible_seed_range[0]), min(int(seed_range.maximum) if seed_range.maximum != float('inf') else possible_seed_range[1], possible_seed_range[1])]
                            hash_range = f"a{potential_range[0]}b{potential_range[1]}"
                            find_existing = self.seed_ranges_checked.get(hash_range, None)
                            if find_existing:
                                possible_minimum = find_existing
                            else:
                                possible_minimum = self.determine_minimum_location_for_seed_range(potential_range[0], potential_range[1])
                                self.seed_ranges_checked[hash_range] = possible_minimum
                            possible_minima.append(possible_minimum)
        sorted_minima = sorted(possible_minima)
        return sorted_minima[0]

    # def get_seed_from_location(self, location: int) -> int:
    #     humidity = self.type_conversions["humidity"].conversions


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(5, is_official)
    almanac = Almanac(data)
    part_1 = almanac.determine_lowest_location(almanac.seeds)
    part_2 = almanac.determine_minimum_location_based_on_location_ranges(almanac.type_conversions["humidity"].conversions)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(5, part_1, part_2, execution_time)
    return results
