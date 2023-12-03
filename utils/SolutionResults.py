class SolutionResults:
    def __init__(self, day: int, part_1: int, part_2: int, execution_time: float) -> None:
        self.day = day
        self.part_1 = part_1
        self.part_2 = part_2
        self.execution_time = execution_time

    def __repr__(self) -> str:
        return f"DAY {self.day} SOLUTIONS\nPart 1: {self.part_1}\nPart 2: {self.part_2}\nTotal execution time: {self.execution_time} seconds"
