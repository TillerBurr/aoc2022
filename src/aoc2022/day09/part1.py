from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Self

import pytest
from rich import print

SAMPLE_INPUT = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
EXPECTED = 13


data = (Path(__file__).parent / "input.txt").read_text()


@dataclass()
class Point:
    x: int
    y: int

    def move(self, other_x: int, other_y: int) -> Self:
        return Point(self.x + other_x, self.y + other_y)

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)

    def adjacent_dist(self, other: Self) -> int:
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def dx(self, other: Self) -> int:
        return self.x - other.x

    def dy(self, other: Self) -> int:
        return self.y - other.y

    @property
    def coords(self) -> tuple[int, int]:
        return (self.x, self.y)


@dataclass
class Movement:
    direction: Literal["U"] | Literal["D"] | Literal["L"] | Literal["R"]
    amount: int


DIRECTIONS = {"U": Point(0, 1), "D": Point(0, -1), "L": Point(-1, 0), "R": Point(1, 0)}


def parse_input(_input: str) -> int:
    instr = _input.splitlines()
    instructions = [Movement(x.split()[0], int(x.split()[1])) for x in instr]
    head = tail = Point(0, 0)
    visited = set()
    visited.add(tail.coords)

    for m in instructions:
        direction = DIRECTIONS[m.direction]
        for _ in range(m.amount):
            head = head + direction
            dist = head.adjacent_dist(tail)

            if dist > 1:
                dx = head.dx(tail)
                dy = head.dy(tail)
                # print(f"{dx=}|{dy=}")

                move_x = dx // abs(dx) if dx != 0 else 0
                move_y = dy // abs(dy) if dy != 0 else 0
                move = Point(move_x, move_y)

                tail = tail + move
                visited.add(tail.coords)

    return len(visited)


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert parse_input(_input) == expected


if __name__ == "__main__":
    print(f"Input:{parse_input(data)}")
