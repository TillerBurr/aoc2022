from pathlib import Path

import pytest
from rich import print

SAMPLE_INPUT = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""
EXPECTED = """\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""


data = (Path(__file__).parent / "input.txt").read_text()


def parse_input(_input: str) -> str:
    lines = _input.splitlines()
    data = []
    for line in lines:
        try:
            x, y = line.split()
            data.append((x, int(y)))
        except ValueError:
            data.append((line, None))
    return data


def process(_input: list[tuple[str, int | None]]) -> str:
    cycles = [["." for _ in range(40)] for _ in range(6)]
    X = 1
    current_cycle = 1
    for op, val in _input:
        row, col = get_row_and_column(current_cycle)
        cycles, current_cycle = update_screen(cycles, row, col, current_cycle, X)

        if op == "addx":
            row, col = get_row_and_column(current_cycle)
            cycles, current_cycle = update_screen(cycles, row, col, current_cycle, X)
            X += val

    out = "\n".join(["".join(x) for x in cycles])
    return out


def update_screen(
    cycles: list[list[str]], row: int, col: int, current_cycle: int, X: int
) -> tuple[list[list[str]], int]:
    if X - 1 <= (current_cycle - 1) % 40 <= X + 1:
        cycles[row][col] = "#"
    current_cycle += 1
    return cycles, current_cycle


def get_row_and_column(cycle: int) -> tuple[int, int]:
    return (cycle - 1) // 40, (cycle - 1) % 40


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    data = parse_input(SAMPLE_INPUT)
    assert process(data) == expected


if __name__ == "__main__":
    data = parse_input(data)
    print(f"Input:\n{process(data)}")
