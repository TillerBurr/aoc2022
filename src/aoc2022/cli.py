import re
import subprocess
from pathlib import Path
from time import perf_counter
from typing import Annotated

import sh
import typer
from httpx import request
from rich import print

app = typer.Typer()

env = Path(__file__).parent / ".env"
cookie = env.read_text().strip()

ALREADY_SOLVED = re.compile(
    "You don't seem to be solving the right level.  Did you already complete it?"
)
CORRECT = re.compile("That's the right answer!")

INCORRECT_TOO_HIGH = re.compile("That's not the right answer; your answer is too high.")
INCORRECT_TOO_LOW = re.compile("That's not the right answer; your answer is too low.")


def create_day_path(day: int) -> Path:
    return Path(__file__).parent / f"day{day:02}"


def input_request(year: int, day: int) -> str:
    input_url = f"https://adventofcode.com/{year}/day/{day}/input"
    r = request(
        "GET", input_url, headers={"Cookie": cookie, "User-Agent": "It'sa me, Mario"}
    )
    return r.content.decode()


@app.command(name="download-input")
def get_input(
    day: Annotated[int, typer.Option("-d")] = 1,
    year: Annotated[int, typer.Option("-y")] = None,
) -> int:
    year = year or int(Path(__file__).parent.name[-4:])
    print(year)
    content = input_request(year, day)
    day_path = create_day_path(day)
    if not day_path.exists():
        day_path.mkdir()
        temp = day_path.parent / "day00/part1.py"
        sh.cp(temp, day_path / "part1.py")
    input_path = day_path / "input.txt"
    input_path.write_text(content)
    lines = input_path.read_text().splitlines()
    print(lines[:20])
    print(f"Visit https://adventofcode.com/{year}/day/{day} for the puzzle")


def post_solution(year: int, day: int, part: int, answer: int) -> str:
    r = request(
        "POST",
        f"https://adventofcode.com/{year}/day/{day}/answer",
        data={"level": part, "answer": answer},
        headers={"Cookie": cookie, "User-Agent": "It'sa me, Mario"},
    )
    return r.content.decode()


@app.command()
def submit_answer(
    answer: Annotated[str, typer.Option("-a")],
    day: Annotated[int, typer.Option("-d")] = 1,
    part: Annotated[int, typer.Option("-p")] = 1,
    year: Annotated[int, typer.Option("-y")] = None,
):
    year = year or int(Path(__file__).parent.name[-4:])
    r = post_solution(year=year, day=day, part=part, answer=answer)
    if ALREADY_SOLVED.search(r):
        print("❌❌ Already solved ❌❌")
    elif INCORRECT_TOO_HIGH.search(r):
        print("❌❌ Too High ❌❌")
    elif INCORRECT_TOO_LOW.search(r):
        print("❌❌ Too Low ❌❌")
    elif CORRECT.search(r):
        print("✅✅ Correct! ✅✅")
        if part == 1:
            day_path = day_path = create_day_path(day)
            sh.cp(day_path / "part1.py", day_path / "part2.py")
    else:
        print(r)


@app.command()
def test(
    day: Annotated[int, typer.Option("-d")] = 1,
    part: Annotated[int, typer.Option("-p")] = 1,
) -> int:
    day_path = day_path = create_day_path(day)
    test_file = day_path / f"part{part}.py"
    subprocess.run(["pytest", test_file, "-s"])


@app.command("solve")
def calculate_answer(
    day: Annotated[int, typer.Option("-d")] = 1,
    part: Annotated[int, typer.Option("-p")] = 1,
) -> int:
    day_path = day_path = create_day_path(day)
    test_file = day_path / f"part{part}.py"
    t_1 = perf_counter()
    subprocess.run(["python", test_file])
    run_time = perf_counter() - t_1
    print(f"Process took {run_time:.02f} Seconds")


if __name__ == "__main__":
    app()
