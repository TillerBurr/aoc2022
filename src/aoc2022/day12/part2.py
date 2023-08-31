from collections import deque
from pathlib import Path
from typing import Any

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
EXPECTED = 29
# start=Point(0,0)
# end = Point(2,5)

data = (Path(__file__).parent / "input.txt").read_text()


def calc_height(char: str) -> int:
    return ord(char) - ord("a") + 1


def parse_input(_input: str) -> tuple[dict[Point, int], list[Point], Point]:
    heights = {}
    starting = []
    for i, line in enumerate(_input.splitlines()):
        for j, char in enumerate(list(line)):
            match char:
                case "S" | "a":
                    height = 1
                    starting.append(Point(i, j))
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
        # print(path)

        # print("=" * 40)
        current_point, count = path.popleft()
        if current_point == ending_point:
            return count
        else:
            # visited.add(current_point)
            for tentative in current_point.get_adjacent():
                if tentative in heights.keys() and tentative not in visited:
                    if heights[tentative] - heights[current_point] <= 1:
                        visited.add(tentative)
                        path.append((tentative, count + 1))


def compute_soln(_input: str) -> Any:
    heights, starting, ending = parse_input(_input)
    steps = []
    for starting_point in starting:
        num_steps = make_trail(heights, starting_point, ending)
        if num_steps is not None:
            steps.append(num_steps)
    return min(steps)


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
