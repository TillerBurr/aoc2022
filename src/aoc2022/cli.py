from pathlib import Path
from typing import Annotated
import typer
from rich import print
from httpx import request

app = typer.Typer()

env = Path(__file__).parent / ".env"
cookie = env.read_text().strip()


def input_request(year: int, day: int) -> str:
    input_url = f"https://adventofcode.com/{year}/day/{day}/input"
    r = request("GET", input_url, headers={"Cookie": cookie, "User-Agent": "just me"})
    return r.content.decode()


@app.command(name="download-input")
def get_input(
    year: Annotated[int, typer.Option()] = 2022,
    day: Annotated[int, typer.Option()] = 1,
) -> int:
    content = input_request(year, day)
    day_str = str(day).zfill(2)
    day_path = Path(__file__).parent / f"day{day_str}"
    if not day_path.exists():
        day_path.mkdir()
    input_path = day_path / "input.txt"
    input_path.write_text(content)
    lines = input_path.read_text().splitlines()
    print(lines[:20])


@app.command()
def help_me():
    print("Help Me")


if __name__ == "__main__":
    app()
