from dataclasses import dataclass
from itertools import cycle
from pathlib import Path
from typing import Any, Literal, Self

import pytest
from rich import print

from aoc2022.utils.point import Point

SAMPLE_INPUT = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
EXPECTED = 3068

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


def create_shape_from_dots_hashtags(shape: str) -> set[Point]:
    positions = set()
    lines = shape.splitlines()
    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char == "#":
                positions.add(Point(i, len(lines) - j - 1))

    return positions


ALL_SHAPES = tuple(
    create_shape_from_dots_hashtags(shape) for shape in SHAPES.split("\n\n")
)
ROCKS = cycle(ALL_SHAPES)
print(ALL_SHAPES)


def plot_shapes_as_dots(shape: set[Point]) -> str:
    row = []
    for y in range(3, -1, -1):
        line = ["|"]
        for x in range(4):
            if Point(x, y) in shape:
                line.append("#")
            else:
                line.append(".")
        line += ["|\n"]
        row.append("".join(line))
    row.append(f"+{'-' * 4}+")
    print("".join(row))


# for shape in ALL_SHAPES:
#     print(plot_shapes_as_dots(shape))


@dataclass
class Rock:
    locations: set[Point]
    fallen_rocks: "FallenRocks"

    def __iter__(self):
        yield self.locations

    def set_start(self) -> None:
        self.locations = {
            Point(2, self.fallen_rocks.height + 3) + pt for pt in self.locations
        }

    def left(self) -> set[Point]:
        return {pt + Point(-1, 0) for pt in self.locations}

    def right(self) -> set[Point]:
        return {pt + Point(1, 0) for pt in self.locations}

    def down(self) -> set[Point]:
        return {pt + Point(0, -1) for pt in self.locations}

    def _test_move(self, dir: Literal["<"] | Literal[">"] | Literal["v"]) -> Self:
        # print(dir)
        match dir:
            case ">":
                offset = Point(1, 0)
            case "<":
                offset = Point(-1, 0)
            case "v":
                offset = Point(0, -1)
            case _:
                raise ValueError(f"Invalid Choice for Movement:{dir}")

        new_ = {offset + pt for pt in self.locations}
        tentative = Rock(
            new_,
            fallen_rocks=self.fallen_rocks,
        )
        return tentative

    def check_can_move(
        self,
        dir: Literal["<"] | Literal[">"] | Literal["v"],
    ) -> bool | None:
        # print(f"{dir=}")
        tentative_move = self._test_move(dir)

        if any(pt in self.fallen_rocks for pt in tentative_move):
            if dir == "v":
                self.fallen_rocks.add_rock(self)
                return False
            return None
        self.locations = tentative_move.locations
        return True

    def print_current_state(self) -> None:
        row = []
        for y in range(self.fallen_rocks.height + 8, -1, -1):
            line = ["|"]
            for x in range(self.fallen_rocks.width):
                if (
                    Point(x, y) in self.locations
                    or (x, y) in self.fallen_rocks.fallen_rocks
                ):
                    line.append("#")
                else:
                    line.append(".")
            line += ["|\n"]
            row.append("".join(line))
        print("".join(row))


@dataclass
class FallenRocks:
    fallen_rocks: set[tuple[int, int]]
    width: int = 7
    height: int = 0

    def __contains__(self, other: Rock) -> bool:
        """
        Check if the given rock is contained within the instance of the class.

        Args:
            other (Rock): The rock to check.

        Returns:
            bool: True if the rock piece would collide, False otherwise.
        """
        # Convert the rock points to a tuple of (x, y) coordinates

        points = tuple((pt.x, pt.y) for pt in other)

        # Check if any of the points are in the fallen rocks
        if any(pt in self.fallen_rocks for pt in points):
            return True

        # Check if any of the points are outside the width of the instance
        if any(pt.x < 0 or pt.x >= self.width for pt in other):
            return True

        # Check if any of the points are below 0 in the y-axis
        if any(pt.y < 0 for pt in other):
            return True

        return False

    def add_rock(self, other: Rock) -> None:
        self.fallen_rocks.update((pt.x, pt.y) for pt in other.locations)
        max_height = max(pt.y for pt in other.locations) + 1
        self.height = max(self.height, max_height)

    def string(self) -> None:
        row = []
        for y in range(self.height + 1, -1, -1):
            line = ["|"]
            for x in range(self.width):
                if (x, y) in self.fallen_rocks:
                    line.append("#")
                else:
                    line.append(".")
            line += ["|\n"]
            row.append("".join(line))
        row.append(f"+{'-' * self.width}+")
        return "".join(row)


data = (Path(__file__).parent / "input.txt").read_text()


def parse_input(_input: str) -> str:
    pattern = list(_input.strip())
    return cycle(pattern)


def compute_soln(_input: str, n_iter: str) -> Any:
    parsed = parse_input(_input)
    fallen = FallenRocks(set())
    for _ in range(n_iter):
        rock = Rock(next(ROCKS), fallen)
        rock.set_start()
        moved = True
        while moved:
            # rock.print_current_state()
            movement = next(parsed)
            # print(f"{movement=}")
            rock.check_can_move(movement)
            moved = rock.check_can_move("v")
    return fallen


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    soln = compute_soln(_input, 2022)
    assert soln.height == expected


if __name__ == "__main__":
    soln = compute_soln(data, 2022)
    # print(soln.string())
    print(soln.height)
