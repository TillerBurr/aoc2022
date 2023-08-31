from pathlib import Path
from typing import Any, TypeAlias

import pytest
from rich import print

SAMPLE_INPUT = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
EXPECTED = 13


data = (Path(__file__).parent / "input.txt").read_text()

List_ish: TypeAlias = int | list["List_ish"]


def parse_input(_input: str) -> List_ish:
    packet_pairs = _input.split("\n\n")
    packets = [[eval(i) for i in x.splitlines()] for x in packet_pairs]
    return packets


def compute_soln(_input: str) -> Any:
    parsed = parse_input(_input)
    solns = []
    for left, right in parsed:
        soln = correct_order(left, right)
        solns.append(soln)
    total = 0
    for i, val in enumerate(solns):
        if val:
            total += i + 1
    return total


def correct_order(left: List_ish, right: List_ish) -> bool:
    left_t = type(left)
    right_t = type(right)
    # print(f"{left=}")
    # print(f"{right=}")

    if left_t != right_t:
        if left_t == int:
            return correct_order([left], right)
        if right_t == int:
            return correct_order(left, [right])
    if left_t == right_t == int:
        if left < right:
            return True
        elif left == right:
            return None
        else:
            return False

    if left_t == right_t == list:
        for left_sublist, right_sublist in zip(left, right):
            is_correct = correct_order(left_sublist, right_sublist)
            if is_correct is not None:
                return is_correct

        if len(left) < len(right):
            return True
        if len(right) < len(left):
            return False


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
