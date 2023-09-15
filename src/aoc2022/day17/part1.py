from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import pytest
from rich import print

from aoc2022.utils.point import Point

SAMPLE_INPUT = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""
EXPECTED = 24000

SHAPES = """\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##\
"""


"""
The tall, vertical chamber is exactly seven units wide.
Each rock appears so that its left edge is two units away from the left wall
and its bottom edge is three units above the highest rock in the room
(or the floor, if there isn't one).
"""

DIRECTIONS = {"<": Point(-1, 0), ">": Point(1, 0), "v": Point(0, -1)}


def create_shape_from_dots_hashtags(shape: str):
    positions = set()
    for j, line in enumerate(shape.splitlines()):
        for i, char in enumerate(line):
            if char == "#":
                positions.add(Point(i, j))

    return positions


ALL_SHAPES = tuple(
    create_shape_from_dots_hashtags(shape) for shape in SHAPES.split("\n\n")
)
print(ALL_SHAPES)


@dataclass
class Rock:
    locations: set[Point]
    fallen_rocks: "FallenRocks"

    def __iter__(self):
        yield from self.locations

    def set_start(self) -> None:
        self.locations = {
            Point(2, self.fallen_rocks.height + 3) + pt for pt in self.locations
        }

    def edges(self) -> tuple[int, int, int]:
        """Edges of the Rock

        Returns in the order (left,right,bottom)"""
        return (
            min(pt.x for pt in self.locations),
            max(pt.x for pt in self.locations),
            max(pt.y for pt in self.locations),
        )

    def move(self, dir: Literal["<"] | Literal[">"] | Literal["v"]) -> set[Point]:
        match dir:
            case ">":
                pts = {Point(1, 0) + pt for pt in self.locations}
                return pts
            case "<":
                pts = {Point(-1, 0) + pt for pt in self.locations}
                return pts
            case "v":
                pts = {Point(0, -1) + pt for pt in self.locations}
                return pts
            case _:
                raise ValueError("Invalid Choice for Movement")

    def check_can_move(
        self,
        dir: Literal["<"] | Literal[">"] | Literal["v"],
    ) -> bool:
        ...


@dataclass
class FallenRocks:
    fallen_rocks: set[tuple[int, int]]
    width: int = 7
    height: int = 0

    def __contains__(self, other: Rock) -> bool:
        points = tuple((pt.x, pt.y) for pt in other)
        if any(pt in self.fallen_rocks for pt in points):
            return True
        if any(pt.x < 0 or pt.x > self.width for pt in other):
            return True
        if any(pt.y < 0 for pt in other):
            return True
        return False

    def add_rock(self, other: Rock) -> None:
        self.fallen_rocks.update((pt.x, pt.y) for pt in other)
        max_height = max(pt.y for pt in other)
        self.height = max(self.height, max_height)


data = (Path(__file__).parent / "input.txt").read_text()


def parse_input(_input: str) -> str:
    return "str"


def compute_soln(_input: str) -> Any:
    parsed = parse_input(_input)
    return parsed


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    soln = compute_soln(_input)
    assert soln == expected


if __name__ == "__main__":
    soln = compute_soln(data)
    print(soln)
