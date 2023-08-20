from pathlib import Path

import pytest
from rich import print

SAMPLE_INPUT = """\
A Y
B X
C Z\
"""
EXPECTED = 15

data = Path("./input.txt").read_text()

winning_play = {"R": "S", "P": "R", "S": "P"}
shape_score = {"R": 1, "P": 2, "S": 3}
decode_ = {"A": "R", "B": "P", "C": "S", "X": "R", "Y": "P", "Z": "S"}


def parse_input(_input: str) -> list[list[int]]:
    results = []
    for k, v in decode_.items():
        _input = _input.replace(k, v)
    all_plays = _input.splitlines()

    all_plays = [x.split(" ") for x in all_plays]
    for o, m in all_plays:
        if o == m:
            results.append(3 + shape_score.get(m))
        elif winning_play[m] == o:
            results.append(6 + shape_score.get(m))
        else:
            results.append(shape_score.get(m))
    return sum(results)


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert parse_input(_input) == expected


if __name__ == "__main__":
    print(parse_input(data))
