from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from rich import print

from aoc2022.utils.point import Point

SAMPLE_INPUT = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
EXPECTED = 26

data = (Path(__file__).parent / "input.txt").read_text()


def parse_line(line: str) -> tuple[Point, Point]:
    sensor, beacon = line.split(": ")
    sensor_x, sensor_y = sensor.split(", ")
    sensor_x = sensor_x.split("=")[-1]
    sensor_y = sensor_y.split("=")[-1]
    beacon_x, beacon_y = beacon.split(", ")
    beacon_x = beacon_x.split("=")[-1]
    beacon_y = beacon_y.split("=")[-1]
    return Point(int(sensor_x), int(sensor_y)), Point(int(beacon_x), int(beacon_y))


@dataclass(frozen=True)
class SensorBeacon:
    sensor: Point
    beacon: Point

    @property
    def distance_to_beacon(self) -> int:
        # d = |x1-x2|+|y1-y2|
        return self.sensor.manhattan_distance(self.beacon)


def parse_input(_input: str) -> list[SensorBeacon]:
    lines = _input.splitlines()
    parsed_lines = [parse_line(line) for line in lines]
    sensors = [SensorBeacon(x[0], x[1]) for x in parsed_lines]
    return sensors


def compute_coverage(_input: str, y: int) -> set[Point]:
    sensors = set()
    beacons = set()
    covered = set()
    parsed = parse_input(_input)
    for sensor in parsed:
        sensors.add(sensor.sensor)
        beacons.add(sensor.beacon)
    for sensor in parsed:
        d = sensor.distance_to_beacon
        y_s = sensor.sensor.y
        x_s = sensor.sensor.x
        # d(Point(x_s,y_s),Point(x,y))=|x_s-x|+|y_s-y|
        x_dist = d - abs(y - y_s)  # |x-x_s|
        """
        x_s-x_dist=x_s-|x-x_s|=x if x<x_s, 2x_s-x if x>x_s
        x_s+x_dist=x_s+|x-x_s|=x if x>x_s, 2x_s-x if x<x_s
        """
        for i in range(-x_dist, x_dist + 1):
            test_pt = Point(x_s + i, y)
            covered.add(test_pt)

    return covered - beacons - sensors


def compute_soln(_input: str, y: int) -> Any:
    empty = compute_coverage(_input, y)
    row_emp = [x for x in empty if x.y == y]

    return len(row_emp)


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    soln = compute_soln(_input, 10)
    assert soln == expected


if __name__ == "__main__":
    soln = compute_soln(data, 2_000_000)
    print(soln)
