from pathlib import Path
from typing import Any

import pytest
from rich import print

SAMPLE_INPUT = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000\
"""
EXPECTED = 24000


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
