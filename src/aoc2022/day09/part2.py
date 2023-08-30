from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Self, TypeAlias

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
EXPECTED = 1

SAMPLE_2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
EXPECTED_2 = 36
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


Direction: TypeAlias = Literal["U"] | Literal["D"] | Literal["L"] | Literal["R"]


@dataclass
class Movement:
    direction: Direction
    amount: int


DIRECTIONS = {"U": Point(0, 1), "D": Point(0, -1), "L": Point(-1, 0), "R": Point(1, 0)}


def parse_input(_input: str) -> list[Movement]:
    instr = _input.splitlines()
    instructions = [Movement(x.split()[0], int(x.split()[1])) for x in instr]
    return instructions


def simulate(data: list[Movement]) -> int:
    knots = [Point(0, 0) for _ in range(10)]
    visited = set()
    visited.add(knots[-1].coords)
    for movement in data:
        direction = DIRECTIONS[movement.direction]
        for _ in range(movement.amount):
            knots[0] = knots[0] + direction
            for n in range(9):
                knots[n], knots[n + 1] = move_knot(knots[n], knots[n + 1])

            visited.add(knots[-1].coords)

    return len(visited)


def move_knot(head: Point, tail: Point) -> tuple[Point, Point]:
    dist = head.adjacent_dist(tail)

    if dist > 1:
        dx = head.dx(tail)
        dy = head.dy(tail)
        # print(f"{dx=}|{dy=}")

        move_x = dx // abs(dx) if dx != 0 else 0
        move_y = dy // abs(dy) if dy != 0 else 0
        move = Point(move_x, move_y)

        tail = tail + move

    return head, tail


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED), (SAMPLE_2, EXPECTED_2)),
)
def test(_input: str, expected: int) -> None:
    inp = parse_input(_input)
    # print(inp)
    soln = simulate(inp)
    print(soln)
    assert soln == expected


if __name__ == "__main__":
    data = parse_input(data)
    print(f"Input:{simulate(data)}")
