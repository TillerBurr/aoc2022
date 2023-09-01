from pathlib import Path
from typing import Any

import pytest
from rich import print

from aoc2022.utils.point import Point

SAMPLE_INPUT = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
EXPECTED = 93


data = (Path(__file__).parent / "input.txt").read_text()


def get_point_from_csv(val: str) -> Point:
    x, y = map(int, val.split(","))
    return Point(x, y)


def get_list_of_points_from_line(line: list[str]) -> list[Point]:
    return [get_point_from_csv(x) for x in line.split(" -> ")]


def parse_input(_input: str) -> list[list[Point]]:
    lines = _input.splitlines()
    pts = [get_list_of_points_from_line(line) for line in lines]
    return pts


def fill_in_rocks(parsed_data: list[list[Point]], filled_in: set[Point]) -> set[Point]:
    for line in parsed_data:
        for i in range(len(line) - 1):
            pt1, pt2 = line[i], line[i + 1]
            if pt1.x == pt2.x:
                min_y = min(pt1.y, pt2.y)
                max_y = max(pt1.y, pt2.y)
                for j in range(min_y, max_y + 1):
                    filled_in.add(Point(pt1.x, j))
            if pt1.y == pt2.y:
                max_x = max(pt1.x, pt2.x)
                min_x = min(pt1.x, pt2.x)
                for j in range(min_x, max_x + 1):
                    filled_in.add(Point(j, pt1.y))
    return filled_in


def drop_sand_grain(
    filled_in: set[Point], time: int, floor: int
) -> tuple[set[Point], int, bool]:
    sand = Point(500, 0)
    while True:
        if sand.coords[1] == floor - 1:
            filled_in.add(sand)
            break
        time += 1
        # print(f"{tentative_pt=}")
        tentative_pt = sand + Point(0, 1)
        if tentative_pt not in filled_in:
            sand = tentative_pt
        elif tentative_pt in filled_in:
            # Fell as far as it's going to
            # Check
            if (left := sand + Point(-1, 1)) not in filled_in:
                sand = left
            elif (right := sand + Point(1, 1)) not in filled_in:
                sand = right
            else:
                filled_in.add(sand)
                break
    return filled_in, time


def find_floor(filled_in: set[Point]) -> int:
    y_vals = [pt.coords[1] for pt in filled_in]
    return max(y_vals) + 2


def compute_soln(_input: str) -> Any:
    parsed = parse_input(_input)
    # filled_in = set()
    filled_in = fill_in_rocks(parsed, set())
    floor = find_floor(filled_in)

    sand = 0
    time = 0
    while True:
        if Point(500, 0) in filled_in:
            return sand
        filled_in, time = drop_sand_grain(filled_in=filled_in, time=time, floor=floor)

        sand += 1
        # print(sand)


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
