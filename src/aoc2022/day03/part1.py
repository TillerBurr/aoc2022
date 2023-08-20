from pathlib import Path

import pytest
from rich import print

SAMPLE_INPUT = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw\
"""
EXPECTED = 157

data = Path("./input.txt").read_text()


def parse_input(_input: str) -> int:
    result = []
    items = _input.splitlines()
    items = [(x[: len(x) // 2], x[len(x) // 2 :]) for x in items]
    for a, b in items:
        result.append(list(set(a) & set(b))[0])

    results = [points(x) for x in result]

    return sum(results)


def points(val: str) -> int:
    if val.islower():
        return ord(val) - ord("a") + 1
    else:
        return ord(val) - ord("A") + 27


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert parse_input(_input) == expected


if __name__ == "__main__":
    print(parse_input(data))
    # print([(len(x[0]), len(x[1])) for x in parse_input(data)])
