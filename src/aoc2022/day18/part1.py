from pathlib import Path
from typing import Any

import pytest
from rich import print

SAMPLE_INPUT = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5\
"""
EXPECTED = 64


data = (Path(__file__).parent / "input.txt").read_text()


def adjacent_cubes(x: int, y: int, z: int) -> set[tuple[int, int, int]]:
    return {
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    }


def parse_input(_input: str) -> str:
    lines = _input.splitlines()
    cubes = tuple(tuple(map(int, line.split(","))) for line in lines)
    return cubes


def compute_soln(_input: str) -> Any:
    parsed = parse_input(_input)
    total_faces = 0
    all_cubes = set()
    for cube in parsed:
        total_faces += 6
        for adjacent in adjacent_cubes(*cube):
            if adjacent in all_cubes:
                total_faces -= 2

        all_cubes.add(cube)

    return total_faces


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
