from pathlib import Path

import pytest
from rich import print
from collections import defaultdict

SAMPLE_INPUT = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k\
"""
EXPECTED = 95437

data = Path("./input.txt").read_text()

cwd = root = Path("/")
files = defaultdict(int)


def parse_input(_input: str) -> int:
    _input = _input.splitlines()
    input_lines = [x.split() for x in _input]
    for line in input_lines:
        match line:
            case ["$", "cd", "/"]:
                cwd = root
            case ["$", "cd", ".."]:
                cwd = cwd.parent
                print(cwd)
            case ["$", "cd", name]:
                cwd = cwd / name

            case [size, _] if size.isdigit():
                for d in [cwd, *cwd.parents]:
                    files[d] += int(size)
    result = sum([x for x in files.values() if x <= 100_000])
    return result


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert parse_input(_input) == expected


if __name__ == "__main__":
    print(f"Input:{parse_input(data)}")
