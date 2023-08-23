from pathlib import Path

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


def parse_input(_input: str) -> list[list[int]]:
    all_elves = _input.split("\n\n")
    calorie_lists = [list(map(int, elf.split("\n"))) for elf in all_elves]
    return calorie_lists


def sum_calories(_input: str) -> list[int]:
    summed = list(map(sum, parse_input(_input)))
    total_calories = sorted(summed, reverse=True)
    return total_calories


def get_top_n_sum(_input: str, n: int = 1) -> int:
    all_elves = sum_calories(_input)
    top_n_elves = all_elves[:n]
    return sum(top_n_elves)


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert get_top_n_sum(_input) == expected


if __name__ == "__main__":
    print(f"Most Calories:{get_top_n_sum(data)}")
    print(f"The sum is {get_top_n_sum(data, 3)}")
