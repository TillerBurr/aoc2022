import math
import operator
from collections import Counter, deque
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from pathlib import Path

import pytest
from rich import print

SAMPLE_INPUT = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
EXPECTED = 2713310158


@dataclass
class Monkey:
    items: deque[int]
    func: Callable[[int], int]
    test: Callable[[int], bool]
    mod: int
    if_true: int
    if_false: int


data = (Path(__file__).parent / "input.txt").read_text()


def pow(x: int, y: int) -> int:
    return x**y


def is_mod_n(val: int, mod: int) -> bool:
    return (val % mod) == 0


def lcm_mod(monkeys: list[Monkey]) -> int:
    return math.lcm(*[x.mod for x in monkeys])


def parse_input(_input: str) -> tuple[list[Monkey], Counter]:
    monkeys = []
    c = Counter()
    c.update()
    monkey_list = [x.splitlines() for x in _input.split("\n\n")]
    for i, monkey in enumerate(monkey_list):
        starting_items = [int(x) for x in monkey[1].split(": ")[1].split(", ")]
        c.update({i: 0})
        d = deque(starting_items)
        operation = monkey[2].split(": ")[1]
        if "* old" in operation:
            func = partial(pow, y=2)

        elif "*" in operation:
            val = int(operation.split()[-1])
            func = partial(operator.mul, val)
        elif "+" in operation:
            val = int(operation.split()[-1])
            func = partial(operator.add, val)
        mod = int(monkey[3].split()[-1])
        test = partial(is_mod_n, mod=mod)
        if_true = int(monkey[4].split()[-1])
        if_false = int(monkey[5].split()[-1])
        monkeys.append(Monkey(d, func, test, mod, if_true, if_false))
    return (monkeys, c)


def process_turn(
    monkey_num: int, monkeys: list[Monkey], counter: Counter, mod: int
) -> tuple[list[Monkey], Counter]:
    monkey = monkeys[monkey_num]
    while monkey.items:
        item = monkey.items.popleft()
        item = monkey.func(item) % mod
        if monkey.test(item):
            monkeys[monkey.if_true].items.append(item)
        else:
            monkeys[monkey.if_false].items.append(item)
        counter.update({monkey_num: 1})
    return monkeys, counter


def process_round(
    monkeys: list[Monkey], counter: Counter, mod: int
) -> tuple[list[Monkey], Counter]:
    for i in range(len(monkeys)):
        monkeys, counter = process_turn(i, monkeys, counter, mod)
    return monkeys, counter


def process_mult_rounds(
    monkeys: list[Monkey], num_rounds: int, counter: Counter, mod: int
) -> tuple[list[Monkey], Counter]:
    for i in range(num_rounds):
        monkeys, counter = process_round(monkeys, counter, mod)

    return monkeys, counter


def calculate_monkey_inspections(
    monkeys: list[Monkey], counter: Counter, num_rounds: int, mod: int
) -> int:
    process_mult_rounds(monkeys, num_rounds, counter, mod)
    most_inspections = [x[1] for x in counter.most_common(2)]
    return most_inspections[0] * most_inspections[1]


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    monkeys, counter = parse_input(_input)
    mod = lcm_mod(monkeys)
    assert calculate_monkey_inspections(monkeys, counter, 10000, mod) == expected


if __name__ == "__main__":
    monkeys, counter = parse_input(data)
    mod = lcm_mod(monkeys)
    print(f"Input:{calculate_monkey_inspections(monkeys,counter,10000,mod)}")
