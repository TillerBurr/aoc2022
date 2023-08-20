from pathlib import Path

import pytest
from rich import print

SAMPLE_INPUT = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8\
"""
EXPECTED = 2

data = Path("./input.txt").read_text()


def parse_input(_input: str) -> int:
    result = 0
    lines = [x.split(",") for x in _input.splitlines()]
    for a, b in lines:
        e1_start, e1_end = [int(x) for x in a.split("-")]
        e2_start, e2_end = [int(x) for x in b.split("-")]
        if (e1_start <= e2_start and e1_end >= e2_end) or (
            e1_start >= e2_start and e1_end <= e2_end
        ):
            result += 1

    return result


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert parse_input(_input) == expected


if __name__ == "__main__":
    print(parse_input(data))
