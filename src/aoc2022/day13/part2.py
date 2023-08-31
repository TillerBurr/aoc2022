from dataclasses import dataclass
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
EXPECTED = 140


data = (Path(__file__).parent / "input.txt").read_text()

List_ish: TypeAlias = int | list["List_ish"]


@dataclass
class ListIsh:
    item: List_ish

    def __lt__(self, other):
        return correct_order(self.item, other.item)


def parse_input(_input: str) -> List_ish:
    _input += "\n[[2]]\n[[6]]"
    all_packets = _input.replace("\n\n", "\n")
    packets = [ListIsh(eval(i)) for i in all_packets.splitlines()]
    return packets


def compute_soln(_input: str) -> Any:
    parsed = parse_input(_input)
    parsed.sort()
    return (parsed.index(ListIsh([[6]])) + 1) * (parsed.index(ListIsh([[2]])) + 1)
    return parsed


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
