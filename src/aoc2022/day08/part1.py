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
EXPECTED = 21

data = (Path(__file__).parent / "input.txt").read_text()


def parse_input(_input: str) -> str:
    lines = _input.splitlines()
    items = [[int(y) for y in x] for x in lines]
    visible = set()
    x_max = len(lines)
    y_max = len(lines[0])
    for y in range(y_max):
        # top

        for x in range(x_max):
            visible_top = all(items[x][y] > items[i][y] for i in range(x))
            visible_bottom = all(items[x][y] > items[i][y] for i in range(x + 1, x_max))
            visible_left = all(items[x][y] > items[x][i] for i in range(y))
            visible_right = all(items[x][y] > items[x][i] for i in range(y + 1, y_max))
            is_visible = visible_top or visible_bottom or visible_left or visible_right
            if is_visible:
                visible.add((x, y))
    visible = list(visible)
    visible.sort()

    return len(visible)


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert parse_input(_input) == expected


if __name__ == "__main__":
    print(f"Input:{parse_input(data)}")
