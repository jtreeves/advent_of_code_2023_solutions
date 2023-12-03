class Cell:
    def __init__(self, x: int, y: int, content: str) -> None:
        self.x = x
        self.y = y
        self.content = content

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}): {self.content}"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cell):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        else:
            return False

    def has_identical_x(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self.x == other.x
        else:
            return False

    def has_identical_y(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self.y == other.y
        else:
            return False
