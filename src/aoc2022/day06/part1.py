from collections import deque
from pathlib import Path

import pytest
from rich import print

SAMPLE_INPUT = """\
mjqjpqmgbljsphdztnvjfqwrcgsmlb\
"""
EXPECTED = 7

data = Path("./input.txt").read_text()


def parse_input(_input: str) -> str:
    _input = _input.strip()
    four_deque = deque(maxlen=4)
    for i, char in enumerate(_input):
        four_deque.append(char)
        if len(four_deque) == 4 and len(set(four_deque)) == 4:
            return i + 1


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert parse_input(_input) == expected


if __name__ == "__main__":
    print(f"Input:{parse_input(data)}")
