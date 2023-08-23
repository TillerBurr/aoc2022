from pathlib import Path

import pytest
from rich import print

SAMPLE_INPUT = """\
A Y
B X
C Z\
"""
EXPECTED = 12

data = (Path(__file__).parent / "input.txt").read_text()

lose_play = {"R": "S", "P": "R", "S": "P"}
win_play = {"R": "P", "P": "S", "S": "R"}
shape_score = {"R": 1, "P": 2, "S": 3}
decode_ = {"A": "R", "B": "P", "C": "S", "X": "L", "Y": "D", "Z": "W"}


def parse_input(_input: str) -> int:
    results = []
    for k, v in decode_.items():
        _input = _input.replace(k, v)
    all_plays = _input.splitlines()

    all_plays = [x.split(" ") for x in all_plays]
    for o, m in all_plays:
        if m == "L":
            results.append(shape_score[lose_play[o]])
        elif m == "W":
            results.append(6 + shape_score.get(win_play.get(o)))
        else:
            results.append(3 + shape_score.get(o))

    return sum(results)


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert parse_input(_input) == expected


if __name__ == "__main__":
    print(parse_input(data))
