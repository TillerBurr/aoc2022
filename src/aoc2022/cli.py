from pathlib import Path
from typing import Annotated
import typer
from rich import print
from httpx import request
import sh
import re


app = typer.Typer()

env = Path(__file__).parent / ".env"
cookie = env.read_text().strip()

ALREADY_SOLVED = re.compile(
    "You don't seem to be solving the right level.  Did you already complete it?"
)
CORRECT = re.compile(">That's the right answer!")


def input_request(year: int, day: int) -> str:
    input_url = f"https://adventofcode.com/{year}/day/{day}/input"
    r = request(
        "GET", input_url, headers={"Cookie": cookie, "User-Agent": "It'sa me, Mario"}
    )
    return r.content.decode()


@app.command(name="download-input")
def get_input(
    day: Annotated[int, typer.Option("-d")] = 1,
) -> int:
    year = int(Path(__file__).parent.name[-4:])
    content = input_request(year, day)
    day_str = str(day).zfill(2)
    day_path = Path(__file__).parent / f"day{day_str}"
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
    answer: Annotated[int, typer.Option("-a")],
    day: Annotated[int, typer.Option("-d")] = 1,
    part: Annotated[int, typer.Option("-p")] = 1,
):
    year = int(Path(__file__).parent.name[-4:])
    r = post_solution(year=year, day=day, part=part, answer=answer)
    if ALREADY_SOLVED.search(r):
        print("❌❌ Already solved ❌❌")
    elif CORRECT.search(r):
        print("✅✅Correct!✅✅")
        if part == 1:
            day_path = Path(__file__).parent / f"day{day:02}"
            sh.cp(day_path / "part1.py", day_path / "part2.py")
    else:
        print(r)


if __name__ == "__main__":
    app()
