import re
from pathlib import Path

import pytest
from rich import print

SAMPLE_INPUT = """\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2\
"""
EXPECTED = "CMZ"

data = Path("./input.txt").read_text()


def parse_input(_input: str) -> str:
    crates, instructions = _input.split("\n\n")
    number_of_crates = max([int(x) for x in crates.splitlines()[-1].split()])
    stacks = [[] for _ in range(number_of_crates)]
    print(stacks)
    crates = crates.splitlines()[:-1]
    print(crates)
    crates.reverse()
    for crate_line in crates:
        for i, x in enumerate(crate_line[1::4]):
            stacks[i].append(x)
    stacks = [list("".join(x).strip()) for x in stacks]
    print(stacks)
    instructions = instructions.splitlines()
    instructions = [re.findall(r"\d+", y) for y in instructions]
    instructions = [[int(y) for y in x] for x in instructions]
    print(instructions)
    for instr in instructions:
        n, f, t = instr
        for i in range(n):
            moved = stacks[f - 1].pop()
            stacks[t - 1].append(moved)

    result = "".join([x[-1] for x in stacks])
    return result


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert parse_input(_input) == expected


if __name__ == "__main__":
    print(f"Input:{parse_input(data)}")
