from collections import deque
from pathlib import Path

import pytest
from rich import print

from aoc2022.utils.point import Point

SAMPLE_INPUT = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
EXPECTED = 31
# start=Point(0,0)
# end = Point(2,5)

data = (Path(__file__).parent / "input.txt").read_text()


def calc_height(char: str) -> int:
    return ord(char) - ord("a") + 1


def parse_input(_input: str) -> tuple[dict[Point, int], Point, Point]:
    heights = {}
    for i, line in enumerate(_input.splitlines()):
        for j, char in enumerate(list(line)):
            match char:
                case "S":
                    height = 1
                    starting = Point(i, j)
                case "E":
                    height = 26
                    end = Point(i, j)
                case _:
                    height = calc_height(char)
            heights[Point(i, j)] = height
    return heights, starting, end


def make_trail(heights: dict[Point, int], starting_point: Point, ending_point: Point):
    visited = set()
    path = deque([(starting_point, 0)])
    visited.add(starting_point)
    while path:
        current_point, count, trail = path.popleft()
        if current_point == ending_point:
            print(path)
            print(visited)
            print(trail)
            return count

        for tentative in current_point.get_adjacent():
            if tentative in heights.keys() and tentative not in visited:
                if heights[tentative] - heights[current_point] <= 1:
                    visited.add(tentative)
                    path.append((tentative, count + 1))


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    heights, starting, ending = parse_input(_input)
    soln = make_trail(heights, starting, ending)
    assert soln == expected


if __name__ == "__main__":
    heights, starting, ending = parse_input(SAMPLE_INPUT)
    # print(f"Input:{}")
    print(make_trail(heights, starting, ending))
