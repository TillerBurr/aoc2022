import operator
from functools import reduce
from pathlib import Path

import pytest
from rich import print

SAMPLE_INPUT = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 8

data = (Path(__file__).parent / "input.txt").read_text()


def parse_input(_input: str) -> str:
    lines = _input.splitlines()
    items = [[int(y) for y in x] for x in lines]
    best_score = 0
    x_max = len(lines)
    y_max = len(lines[0])
    for y in range(1, y_max - 1):
        for x in range(1, x_max - 1):
            # print((x, y))
            scores = score(x, y, items, x_max, y_max)
            current_score = reduce(operator.mul, scores.values())
            if current_score >= best_score:
                best_score = current_score
            # print(scores)
            # print(current_score)

    print(best_score)

    return best_score


def score(x: int, y: int, items: list[list[int]], x_max: int, y_max: int) -> int:
    scores = {"top": 0, "bottom": 0, "right": 0, "left": 0}
    for i in range(x + 1, x_max):
        scores["bottom"] += 1
        if items[x][y] <= items[i][y]:
            break
    for i in range(y + 1, y_max):
        scores["right"] += 1
        if items[x][y] <= items[x][i]:
            break
    for i in range(x - 1, -1, -1):
        scores["top"] += 1

        if items[x][y] <= items[i][y]:
            break
    for i in range(y - 1, -1, -1):
        scores["left"] += 1
        if items[x][y] <= items[x][i]:
            break
    return scores


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert parse_input(_input) == expected


if __name__ == "__main__":
    print(f"Input:{parse_input(data)}")
